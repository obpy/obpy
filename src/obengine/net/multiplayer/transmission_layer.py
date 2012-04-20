#
# <module description>
# See <TODO: No Sphinx docs yet - add some> for the primary source of documentation
# for this module.
#
# Copyright (C) 2012 The OpenBlox Project
#
# This file is part of The OpenBlox Game Engine.
#
#     The OpenBlox Game Engine is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     The OpenBlox Game Engine is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with The OpenBlox Game Engine.  If not, see <http://www.gnu.org/licenses/>.
#


__author__ = "openblocks"
__date__ = "Apr 5, 2012 9:48:35 AM"


import asyncore
import socket
import struct
import time
import collections

import obengine.event
import obengine.async
import obengine.datatypes


class TransmissionLayer(asyncore.dispatcher):

    CLIENT_HANDSHAKE = 1
    SERVER_HANDSHAKE = 2
    CONNECTION_TERMINATION = 3
    INVALID_PACKET = 4
    DELIVERY_CONFIRMATION = 5
    PLUGIN_DOWNLOAD_REQUEST = 6
    PLUGIN_INSTALL_PACKET = 7
    PACKET_TYPE_ID_REQUEST = 8
    CLIENT_READY = 9
    HEARTBEAT = 10

    PACKET_HEADER_LENGTH = 10
    PACKET_TYPE_ID_LENGTH = 5
    TOTAL_PACKET_HEADER_LENGTH = PACKET_HEADER_LENGTH + PACKET_TYPE_ID_LENGTH

    PACKET_TIMEOUT = 1
    CONNECTION_TIMEOUT = 5

    def __init__(self, port, scheduler):

        self._socket = socket.socket(socket.AF_INET,
                                     socket.SOCK_DGRAM)
        self._port = port

        self._local_sequence = {}
        self._remote_sequence = {}
        self._last_ack = {}
        self._ack_bitfield = {}
        self._packet_history = {}
        self._lost_packets = set()

        self._is_writable = False
        self._queued_packet = {}
        self._expected_packet = {}
        self._connection_timeout_table = {}
        self._packet_timeout_table = {}
        self._timeout_task = obengine.async.Task(self._timeout_task_action)
        self._on_connection_timeout = obengine.event.Event()

        asyncore.dispatcher.__init__(self, self._socket)
        self._socket.bind(('127.0.0.1', self._port))

        self._scheduler = scheduler

        self._on_packet_recieved = obengine.event.Event()
        self._on_packet_lost = obengine.event.Event()

        self._confirmed_packets = {}
        self._on_packet_confirmed = obengine.event.Event()

    def start(self):

        self._scheduler.add(obengine.async.Task(self._poll))
        self._scheduler.add(obengine.async.Task(self._timeout_task))

    def _expect_packet(self, packet_type_id, address):
        self._expected_packet[address] = packet_type_id

    def handle_read(self):

        packet, address = self.socket.recvfrom(4096)

        try:
            packet_type_id = int(packet[TransmissionLayer.PACKET_HEADER_LENGTH:TransmissionLayer.TOTAL_PACKET_HEADER_LENGTH])

        except ValueError:

            self._queue_packet(address, TransmissionLayer.INVALID_PACKET)
            return

        remote_sequence, remote_ack, remote_ack_bitfield = struct.unpack('!Hii',
                                                                         packet[:TransmissionLayer.PACKET_HEADER_LENGTH])
        remote_ack_bitfield = obengine.datatypes.bitfield(remote_ack_bitfield)

        if remote_sequence > self._remote_sequence.setdefault(remote_sequence, 0):
            self._remote_sequence[address] = remote_sequence

        if remote_ack != self._local_sequence.setdefault(address, 0) - 1:
            if remote_ack not in self._lost_packets:

                self._lost_packets.add(remote_ack)
                self._on_packet_lost(address, remote_ack)

        if address not in self._ack_bitfield:
            self._ack_bitfield[address] = collections.deque(maxlen = 32)

        for bit in range(0, 31):
            self._ack_bitfield[address].appendleft(remote_ack_bitfield[bit])

        if address not in self._confirmed_packets:
            self._confirmed_packets[address] = collections.deque(maxlen = 33)

        self._confirm_packet(address, remote_ack)

        packet_history = list(self._ack_bitfield[address])
        for packet_num, _ in enumerate(packet_history):

            packet_num = remote_ack - packet_num
            if packet_num < 0:
                continue

            self._confirm_packet(address, packet_num)

        expected_packet_type_id = self._expected_packet.get(address)

        if expected_packet_type_id is not None:
            if packet_type_id != expected_packet_type_id:

                self._send_packet(address, TransmissionLayer.INVALID_PACKET)
                return

        packet_data = packet[TransmissionLayer.TOTAL_PACKET_HEADER_LENGTH:]

        self._reset_connection_timeout(address)
        self._reset_packet_timeout(address, remote_ack)
        self._on_packet_recieved(address, packet_type_id, packet_data)

    def handle_write(self):

        for address, (packet, sequence_number) in self._queued_packets.items():

            self._socket.sendto(packet, address)
            self._packet_timeout_table.setdefault(address, {})[sequence_number] = time.time()

            if address not in self._connection_timeout_table:
                self._reset_connection_timeout(address)

    def writable(self):
        return sum(map(len, self._queued_packet.iteritems())) >= 0

    def _send_packet(self, address, packet_type_id, optional_data = ''):

        packet_header = struct.pack('!Hii',
                                    self._local_sequence.setdefault(address, 0),
                                    self._last_ack.setdefault(address, 0),
                                    self._ack_bitfield)

        packed_packet_type_id = str(packet_type_id).zfill(TransmissionLayer.PACKET_TYPE_ID_LENGTH)
        packed_packet = (packet_header + packed_packet_type_id + optional_data, address)

        self._queued_packet[address] = (packed_packet, self._local_sequence[address])
        self._local_sequence[address] += 1

        return self._local_sequence[address] - 1

    def _confirm_packet(self, address, sequence_num):

        if sequence_num not in self._confirmed_packets[address]:
            if sequence_num >= self._last_ack[address] - 32:

                self._confirmed_packets[address].append(sequence_num)
                self._on_packet_confirmed(address, sequence_num)

    def _timeout_task_action(self, task):

        for address, timeout in self._connection_timeout_table.items():

            if time.time() - timeout >= TransmissionLayer.CONNECTION_TIMEOUT:

                del self._connection_timeout_table[address]
                self._on_connection_timeout(address)

        for address, suspect_packets in self._packet_timeout_table.items():

            for sequence_number, timeout in suspect_packets.items():

                if time.time() - timeout >= TransmissionLayer.PACKET_TIMEOUT:
                    if sequence_number not in self._lost_packets:

                        self._lost_packets.add(sequence_number)
                        self._on_packet_lost(address, sequence_number)
                        del self._packet_timeout_table[address][sequence_number]

    def _reset_connection_timeout(self, address):
        self._connection_timeout_table[address] = time.time()

    def _reset_packet_timeout(self, address, sequence_number):
        if self._packet_timeout_table[address].has_key(sequence_number):
            del self._packet_timeout_table[address][sequence_number]

    def _poll(self, task):

        asyncore.poll()
        return task.AGAIN


class ClientTransmissionLayer(TransmissionLayer):

    def __init__(self, server_address, port, scheduler):

        TransmissionLayer.__init__(self, port, scheduler)

        self._server_address = server_address
        self._connected = False

        self.on_connected = obengine.event.Event()
        self.on_packet_recieved = obengine.event.Event()
        self._on_packet_recieved += lambda a, p, d: self.on_packet_recieved(p, d)
        self.on_packet_lost = obengine.event.Event()
        self._on_packet_lost += lambda a, s: self.on_packet_lost(s)
        self.on_disconnected = obengine.event.Event()

    def send(self, packet_type_id, optional_data = ''):

        assert self._connected is True
        return self._send_packet(self._server_address, packet_type_id, optional_data)

    def connect(self, max_retries = 5):

        self._max_retries = max_retries
        self._retries = 0

        self._attempt_connection()

        self._on_packet_recieved += self._handle_server_handshake
        self._on_connection_timeout += self._retry_connection

    def _retry_connection(self, _):

        self._retries += 1

        if self._retries == self._max_retries:

            self._on_connection_timeout -= self._retry_connection
            self.on_disconnected()

        self._attempt_connection()

    def _attempt_connection(self):

        self._send_packet(self._server_address, ClientTransmissionLayer.CLIENT_HANDSHAKE)
        self.expect_packet(ClientTransmissionLayer.SERVER_HANDSHAKE)

    def _handle_server_handshake(self, _, __, ___):

        self._connected = True
        self._on_packet_recieved -= self._handle_server_handshake
        self.expect_packet(None)
        self._on_connection_timeout -= self._retry_connection
        self._on_connection_timeout += lambda a: self.on_disconnected()

        self.on_connected(self._server_address)


class ServerTransmissionLayer(TransmissionLayer):
    pass
