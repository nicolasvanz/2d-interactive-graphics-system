import tkinter as tk
import window
from shapes import *
from tk_adaptations import *

class NewObjectWindowInterface(tk.Toplevel):
	def __init__(self, mainwindow):
		self.mainwindow = mainwindow

	@abstractclassmethod
	def submit(self):
		pass

	def show(self):
		# create second window
		super().__init__()
		self.title("New Object")
		
		# we shouldn't place elements directly in root
		self.mainframe = Frame(self)
		self.mainframe.grid(row = 0, column = 0)

		# build user interface
		self.__init_ui()

	def hide(self):
		# destroy the window
		super().destroy()

	def __init_ui(self):
		# build top frame
		self.__build_fr_top()
		# build bottom frame
		self.__build_fr_bottom()

	def __build_fr_top(self):
		# create elements
		self.fr_top   = Frame(self.mainframe)
		self.lb_name  = Label(self.fr_top, text = "Name")
		self.lb_coord = Label(self.fr_top, text = "Coordinates")
		self.lb_isClosed = Label(self.fr_top, text = "Is a closed object")
		self.ent_name  = tk.Entry(self.fr_top)
		self.ent_coord = tk.Entry(self.fr_top)
		self.chkValue = tk.BooleanVar() 
		self.checkB_isClosed = tk.Checkbutton(self.fr_top, variable = self.chkValue)

	
		# positioning elements
		self.fr_top.grid(         row = 0, column = 0)
		self.lb_name.grid(        row = 0, column = 0)
		self.ent_name.grid(       row = 1, column = 0)
		self.lb_coord.grid(       row = 2, column = 0)
		self.ent_coord.grid(      row = 3, column = 0)
		self.lb_isClosed.grid(    row = 4, column = 0)
		self.checkB_isClosed.grid(row = 5, column = 0)
	
	def __build_fr_bottom(self):
		# create bottom frame
		self.fr_bottom = Frame(self.mainframe)

		# create buttons
		self.btn_ok = Button(
			self.fr_bottom,
			text = "Ok",
			command = self.submit
		)
		self.btn_cancel = Button(
			self.fr_bottom,
			text = "Cancel",
			command = self.hide
		)

		# positioning elements
		self.fr_bottom.grid( row = 2, column = 0)
		self.btn_ok.grid(    row = 0, column = 0)
		self.btn_cancel.grid(row = 0, column = 1)

class MainWindowInterface(tk.Tk):
	def __init__(self):
		# create window
		super().__init__()

		# we shouldn't place elements directly in root
		self.mainframe = Frame(self)
		
		self.new_object_window = window.NewObjectWindow(mainwindow = self)
		self.canvas = window.Viewport(self.mainframe, mainwindow = self)

		self.__init_ui()
		
		self.mainframe.grid(row = 0, column = 0)
		self.canvas.grid(row = 0, column = 1)
	
	@abstractclassmethod
	def __zoom_in(self):
		pass

	@abstractclassmethod
	def __zoom_out(self):
		pass

	@abstractclassmethod
	def __move_up(self):
		pass

	@abstractclassmethod
	def __move_down(self):
		pass

	@abstractclassmethod
	def __move_left(self):
		pass

	@abstractclassmethod
	def __move_right(self):
		pass

	def __init_ui(self):
		self.frame_left = Frame(self.mainframe)
		self.frame_commands = Frame(self.frame_left)
		self.frame_zoom = Frame(self.frame_commands)
		self.frame_arrows = Frame(self.frame_commands)
		self.fr_list_box = Frame(self.frame_left)
		
		self.lb_objNames = Label(self.fr_list_box, text = "Object Names")
		self.lst_objNames = tk.Listbox(self.fr_list_box)

		self.button_newobject = Button(
			self.frame_commands,
			text = "New Object",
			command = self.__new_object
		)

		self.button_in = Button(
			self.frame_zoom,
			text = "In",
			command = self.__zoom_in
		)

		self.button_out = Button(
			self.frame_zoom,
			text = "Out",
			command = self.__zoom_out
		)

		self.button_up = tk.Button(
			self.frame_arrows,
			text = "^",
			command = self.__move_up
		)

		self.button_down = tk.Button(
			self.frame_arrows,
			text = "v",
			command = self.__move_down
		)
		self.button_left = tk.Button(
			self.frame_arrows,
			text = "<",
			command = self.__move_left
		)
		self.button_right = tk.Button(
			self.frame_arrows,
			text = ">",
			command = self.__move_right
		)		

		# positioning elements
		self.frame_left.grid(      row = 0, column = 0)
		self.frame_commands.grid(  row = 1, column = 0)
		self.button_newobject.grid(row = 0, column = 0)
		self.frame_zoom.grid(      row = 1, column = 0)
		self.button_in.grid(       row = 0, column = 0)
		self.button_out.grid(      row = 0, column = 1)
		self.frame_arrows.grid(    row = 2, column = 0)
		self.fr_list_box.grid(     row = 0, column = 0)
		self.lb_objNames.grid(     row = 0, column = 0)
		self.lst_objNames.grid(    row = 1, column = 0)
		self.button_up.grid(       row = 0, column = 0, columnspan = 2)
		self.button_left.grid(     row = 1, column = 0)
		self.button_right.grid(    row = 1, column = 1)
		self.button_down.grid(     row = 2, column = 0, columnspan = 2)

	def __new_object(self):
		self.new_object_window.show()