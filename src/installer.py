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
    """
    Sets the pipe for the underlying installer(setup.py).
    """

    global pipe
    
    pipe = new_pipe

def get_pipe():
    """
    Returns the underlying pipe.
    """

    global pipe

    return pipe

def run_install():
    """
    Actually starts the installation process.
    """

    """
    Now, here's a bit of tricky asyncronous programming, so I'll explain:

    This method is called every once in a while.

    If it's the first time, it creates and saves a pipe the underlying installer(setup.py)
    Otherwise, it reads the pipe, and if the pipe has not closed, appends the data to a textbox.
    If the pipe HAS closed, then it checks the return value of the installer,
    and if the installation finished sucessfully, advances the wizard page, and tells the user
    that all is well.

    Otherwise, the user gets presented with an error message.
    """
    # We're on the installation page
    if wiz.current == 3:

        # Has the pipe been set(i.e, the user just selected the installation page)?
        if get_pipe() == None:

            # We have to call python.exe on Windows, python otherwise, so check here
            if os.name == 'posix':

                # Create the pipe
                p = subprocess.Popen(shlex.split('python setup.py install'), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

                # Set it
                set_pipe(p)

            elif os.name == 'nt':

                # Again, create and set
                p = subprocess.Popen(shlex.split('C:\Python26\python.exe setup.py install', posix = False), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

                set_pipe(p)

            # Set us up to be called again
            root.after(100, run_install)

        # We've already been called once, so we can read the pipe
        else:

            # Read a line of data
            string = get_pipe().stdout.readline()

            # Check for the return value
            get_pipe().poll()

            # Is there still data in the pipe?
            if string != '':

                # Insert the text, scroll to the end, and set us up to be called again
                install_progress.insert(Tkinter.END, string.replace('\n', os.linesep))
                install_progress.see(Tkinter.END)
                root.after(100, run_install)

            else:

                # The underlying installer's finshed. How'd it go?
                frame = ttk.Frame(wiz.page_container(4))
                retval = get_pipe().returncode
                endstr = None

                # Everything fine?
                if retval == 0:
                    
                    endstr='''
                    The installation completed sucessfully!
                    We hope you will enjoy using The OpenBlox Game Engine!
                    '''

                # Houston, we've got a problem...
                else:

                    endstr='''
                    There was a problem with the installation.
                    Contact the OpenBlox developers at:
                    http://openblox.sourceforge.net/?q=forum for more information.
                    '''

                # Create a label with the status text
                endlabel = ttk.Label(frame, text=endstr)
                endlabel.pack()

                # Advance the page
                wiz.add_page_body(frame)
                wiz.next_page()

    # Ah well. The user hasn't wanted to start installing yet, so wait a little more...
    else:
        root.after(100, run_install)

# Create the main window
root = Tkinter.Tk()

# Use the nice clam theme
style = ttk.Style()
style.theme_use('clam')

wiz = wizard.Wizard(npages=5)

wiz.master.minsize(400, 350)

# Welcome page

frame0 = ttk.Frame(wiz.page_container(0))

logo = Image.open(os.path.join('data', 'oblogo-small.png'))
logo = ImageTk.PhotoImage(logo)

logo_widget = ttk.Label(frame0, image=logo)
logo_widget.pack(side=Tkinter.LEFT)

welcome_text = ttk.Label(frame0, text='Welcome to the OpenBlox Game Engine installer!\nThis installer will guide you through the process of installing The OpenBlox Game Engine.')
welcome_text.pack(side=Tkinter.LEFT)

#######################################

# License page...brrrrr....

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

#######################################

# Confirmation page

frame2 = ttk.Frame(wiz.page_container(2))

confirm = ttk.Label(frame2, text='You may now begin the installation.\nYou will probably need an Internet connection to continue.')
confirm.pack()

#######################################

# Install frame. We actually install here

frame3 = ttk.Frame(wiz.page_container(3))

ip_scrollbar = ttk.Scrollbar(frame3)
ip_scrollbar.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)

install_progress = Tkinter.Text(frame3)
install_progress.pack()

install_progress.configure(yscrollcommand=ip_scrollbar.set)
ip_scrollbar.configure(command=install_progress.yview)

#########################################

# Add the frames

wiz.add_page_body(frame0)
wiz.add_page_body(frame1)
wiz.add_page_body(frame2)
wiz.add_page_body(frame3)

# Add the wizard
wiz.pack(fill='both', expand=True)

# Set the title
root.title('OpenBlox Game Engine Installer')

# Start the check to run the method that actually installs
root.after(10, run_install)

# Start the main loop
root.mainloop()