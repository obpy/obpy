#!/usr/bin/env python
"""
This file is part of The OpenBlox Game Engine.

    The OpenBlox Game Engine is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    The OpenBlox Game Engine is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with The OpenBlox Game Engine.  If not, see <http://www.gnu.org/licenses/>.

"""
__author__="openblocks"
__date__ ="$Nov 12, 2010 5:03:56 PM$"

import os
import subprocess
import shlex

import wizard
import Tkinter
import ttk

from PIL import Image, ImageTk

pipe = None

def set_pipe(new_pipe):

    global pipe
    
    pipe = new_pipe

def get_pipe():

    global pipe

    return pipe

def run_install():

    if wiz.current == 3:

        if get_pipe() == None:

            if os.name == 'posix':

                p = subprocess.Popen(shlex.split('python setup.py install'), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

                set_pipe(p)

            elif os.name == 'nt':

                p = subprocess.Popen(shlex.split('python.exe setup.py install'), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                set_pipe(p)

            root.after(100, run_install)

        else:

            string = get_pipe().stdout.readline()
            get_pipe().poll()

            if string != '':

                install_progress.insert(Tkinter.END, string)
                install_progress.see(Tkinter.END)
                root.after(100, run_install)

            else:

                frame = ttk.Frame(wiz.page_container(4))
                retval = get_pipe().returncode
                endstr = None

                if retval == 0:
                    
                    endstr='''
                    The installation completed sucessfully!
                    We hope you will enjoy using The OpenBlox Game Engine!
                    '''

                else:

                    endstr='''
                    There was a problem with the installation.
                    Contact the OpenBlox developers at:
                    http://openblox.sourceforge.net/?q=forum for more information.
                    '''

                endlabel = ttk.Label(frame, text=endstr)
                endlabel.pack()

                wiz.add_page_body(frame)
                wiz.next_page()

    
    else:
        root.after(100, run_install)

root = Tkinter.Tk()

style = ttk.Style()
style.theme_use('clam')

wiz = wizard.Wizard(npages=5)

wiz.master.minsize(400, 350)

frame0 = ttk.Frame(wiz.page_container(0))

logo = Image.open(os.path.join('data', 'oblogo-small.png'))
logo = ImageTk.PhotoImage(logo)

logo_widget = ttk.Label(frame0, image=logo)
logo_widget.pack(side=Tkinter.LEFT)

welcome_text = ttk.Label(frame0, text='Welcome to the OpenBlox Game Engine installer!\nThis installer will guide you through the process of installing The OpenBlox Game Engine.')
welcome_text.pack(side=Tkinter.LEFT)

frame1 = ttk.Frame(wiz.page_container(1))

l_scrollbar = ttk.Scrollbar(frame1)
l_scrollbar.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)

license_header = ttk.Label(frame1, text='License')
license_header.pack(side=Tkinter.TOP)

license = Tkinter.Text(frame1)
license.insert(Tkinter.END, open('LICENSE.txt').read())
license.configure(state=Tkinter.DISABLED, yscrollcommand=l_scrollbar.set)
l_scrollbar.configure(command=license.yview)
license.pack()

reminder = ttk.Label(frame1, text='If you agree with the license, you may continue.')
reminder.pack(side=Tkinter.BOTTOM)

frame2 = ttk.Frame(wiz.page_container(2))

confirm = ttk.Label(frame2, text='You may now begin the installation.\nYou will probably need an Internet connection to continue.')
confirm.pack()

frame3 = ttk.Frame(wiz.page_container(3))

ip_scrollbar = ttk.Scrollbar(frame3)
ip_scrollbar.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)

install_progress = Tkinter.Text(frame3)
install_progress.pack()

install_progress.configure(yscrollcommand=ip_scrollbar.set)
ip_scrollbar.configure(command=install_progress.yview)

wiz.add_page_body(frame0)
wiz.add_page_body(frame1)
wiz.add_page_body(frame2)
wiz.add_page_body(frame3)

wiz.pack(fill='both', expand=True)

root.title('OpenBlox Game Engine Installer')

root.after(100, run_install)

root.mainloop()