try:
	import appdirs
except ModuleNotFoundError:
	raise RuntimeError('One of the required modules known as "appdirs" isn\'t installed.')

import os
from sys import exit
import sys

try:
	from tkinter.filedialog import askdirectory
	from tkinter.font import Font
	from tkinter.ttk import Progressbar
	from tkinter import *
	from tkinter import messagebox
	from tkinter.ttk import *
except ModuleNotFoundError:
	raise RuntimeError('tkinter is not installed on your Python interpreter, '
		'see https://stackoverflow.com/a/25905642/16378482 if you\'re using UNIX-based OS')

from zipfile import ZipFile

class InstallerInitError(Exception):
	def __init__(self):
		super().__init__('Installer has not yet fully initialized.')

root: Tk = None
path: StringVar = None
extracting: bool = False

def resources_path() -> str:
	# This function is necessary when it is built into an executable
	if not hasattr(sys, '_MEIPASS'): return ''
	return f"{sys._MEIPASS}/"

def init():
	global root
	if not root: root = Tk()
	root.protocol('WM_DELETE_WINDOW', abort)
	root.iconbitmap(f"{resources_path()}installer.ico")
	root.title('Disrichie')
	root.resizable(False, False)
	center()

def ask_dir(path: str) -> str:
	new_path = askdirectory(initialdir=path if not path else None, mustexist=True)
	if not new_path: return path
	return new_path

def center():
	global root
	if not root: raise InstallerInitError()

	window_height = 500
	window_width = 500
	screen_width = root.winfo_screenwidth()
	screen_height = root.winfo_screenheight()
	x_cordinate = int((screen_width / 2) - (window_width / 2))
	y_cordinate = int((screen_height / 2) - (window_height / 2))

	root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

def abort(loop_if_no: bool = False):
	global extracting
	if extracting: return
	response = messagebox.askyesno('Cancel', 'Do you want to exit installation?')

	if response: exit()
	elif not response:
		if loop_if_no: loop()
		else: pass

def fail(reason: str):
	global extracting
	if extracting: extracting = False
	messagebox.showerror('Installation error', reason)
	switch(4)

def clear():
	global root
	if not root: raise InstallerInitError()

	for widget in root.winfo_children():
		widget.destroy()

def draw_separators():
	global root
	if not root: raise InstallerInitError()
	header_sep = Separator(root, orient=HORIZONTAL)
	navigation_sep = Separator(root, orient=HORIZONTAL)
	header_sep.place(relx=0, rely=0.15, relwidth=1, relheight=1)
	navigation_sep.place(relx=0, rely=0.92, relwidth=1, relheight=1)

def switch(index: int = 0):
	global root, path, extracting
	if not root and not path: raise InstallerInitError()
	if len(root.winfo_children()) > 0: clear()
	if index < 5: draw_separators()

	if index == 0: # Welcome screen
		# Create header
		header = Label(root, text='Welcome')
		font = Font(font=header['font'])
		header.config(font=(font.actual(), 18))
		header.pack(side=TOP, anchor=NW, padx=8, pady=8)

		# Create text
		text = Label(root, text='To begin installation of Disrichie, click "Install" to proceed.')
		text.pack(side=TOP, anchor=NW, padx=8)

		# Create navigation buttons
		btn_frame = Frame(root)
		btn_frame.pack(side=BOTTOM, anchor=E, padx=8, pady=8)
		btn = Button(btn_frame, text='Install', command=lambda: switch(1))
		btn.pack(in_=btn_frame, side=RIGHT)
		btn2 = Button(btn_frame, text='Exit', command=lambda: abort())
		btn2.pack(in_=btn_frame, side=RIGHT)
	elif index == 1: # Destination screen
		# Initialize path if not
		if not path: path = StringVar(value=f"{appdirs.user_data_dir()}/disrichie")

		# Create header
		header = Label(root, text='Destination Location')
		font = Font(font=header['font'])
		header.config(font=(font.actual(), 18))
		header.pack(side=TOP, anchor=NW, padx=8, pady=8)

		# Create text
		text = Label(root, text='Where do you want to install Disrichie?')
		text.pack(side=TOP, anchor=NW, padx=8)

		# Create destination entry and change button
		dest_frame = Frame(root)
		dest_frame.pack(side=TOP, anchor=NW, padx=8, pady=16)
		btn_change = Button(root, text='Change...', command=lambda: path.set(ask_dir(path.get())))
		btn_change.pack(in_=dest_frame, side=RIGHT, padx=8)
		entry = Entry(dest_frame, width=50, textvariable=path)
		entry.pack(in_=dest_frame, side=RIGHT)

		# Create navigation buttons
		btn_frame = Frame(root)
		btn_frame.pack(side=BOTTOM, anchor=E, padx=8, pady=8)
		btn = Button(btn_frame, text='Next', command=lambda: switch(2))
		btn.pack(in_=btn_frame, side=RIGHT)
		btn2 = Button(btn_frame, text='Go back', command=lambda: switch(0))
		btn2.pack(in_=btn_frame, side=RIGHT)
	elif index == 2: # Installing page
		# Lock the exit button
		extracting = True

		# Create header
		header = Label(root, text='Installing')
		font = Font(font=header['font'])
		header.config(font=(font.actual(), 18))
		header.pack(side=TOP, anchor=NW, padx=8, pady=8)

		# Create text
		text = Label(root, text='Copying installation files, please wait...')
		text.pack(side=TOP, anchor=NW, padx=8)

		# Create extraction status text
		status_text_str = StringVar(value='Initializing')
		status_text = Label(root, textvariable=status_text_str)
		status_text.pack(side=TOP, anchor=NW, padx=8, pady=16)

		# Create extraction progress bar
		bar = Progressbar(orient=HORIZONTAL, length=500, mode='determinate', maximum=100, value=0)
		bar.pack(side=TOP, anchor=NW, padx=8)

		# Extract required files
		os.makedirs(path.get(), exist_ok=True)

		if not os.path.isfile(f"{resources_path()}files.zip"):
			status_text_str.set('Error')
			fail('Missing installation files! Contact the author.')
			return

		zipfile = ZipFile(f"{resources_path()}files.zip")
		uncompressed_size = sum(file.file_size for file in zipfile.infolist())
		extract_size = 0

		for file in zipfile.infolist():
			extract_size += file.file_size
			status_text_str.set('Unpacking...')
			bar['value'] = extract_size * 100 / uncompressed_size
			zipfile.extract(file, path.get())
		
		# Close zipfile to save memory, then unlock the exit button, then switch to 4th screen
		zipfile.close()
		extracting = False
		switch(3)
	elif index == 3: # Installation success screen
		# Create header
		header = Label(root, text='Install success')
		font = Font(font=header['font'])
		header.config(font=(font.actual(), 18))
		header.pack(side=TOP, anchor=NW, padx=8, pady=8)

		# Create text
		text = Label(root, text='You may now exit this installation.')
		text.pack(side=TOP, anchor=NW, padx=8)

		# Create exit button
		btn = Button(root, text='Close', command=lambda: exit())
		btn.pack(side=BOTTOM, anchor=E, padx=8, pady=8)
	elif index == 4: # Failed to install screen
		# Create header
		header = Label(root, text='Failed to install')
		font = Font(font=header['font'])
		header.config(font=(font.actual(), 18))
		header.pack(side=TOP, anchor=NW, padx=8, pady=8)

		# Create text
		text = Label(root, text='An error occurred while setting up, you may now exit this installation.')
		text.pack(side=TOP, anchor=NW, padx=8)

		# Create exit button
		btn = Button(root, text='Close', command=lambda: exit(1))
		btn.pack(side=BOTTOM, anchor=E, padx=8, pady=8)

def loop():
	global root
	if not root: raise InstallerInitError()

	try:
		root.mainloop()
	except KeyboardInterrupt:
		abort(True)

try:
	init()
except TclError as error:
	if error.args[0] == 'no display name and no $DISPLAY environment variable':
		print('GUI in your environment is not supported.')
		exit(1)
	else: pass

switch()
loop()