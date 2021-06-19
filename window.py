from abc import abstractclassmethod
import tkinter as tk
import re

class GraphicObject:
	def __init__(self, name, is_closed = False, *args):
		self.name = name
		self.is_closed = is_closed
		self.coordinates = args
	
	@abstractclassmethod
	def draw(self):
		pass

class Frame(tk.Frame):
	def __init__(self, master, padx = 10, pady = 10, *args, **kwargs):
		super().__init__(master = master, padx = padx, pady = pady, *args, **kwargs)

class Label(tk.Label):
	def __init__(self, master, padx = 10, pady = 10, *args, **kwargs):
		super().__init__(master = master, padx = padx, pady = pady, *args, **kwargs)

class Button(tk.Button):
	def __init__(self, master, padx = 10, pady = 10, *args, **kwargs):
		super().__init__(master = master, padx = padx, pady = pady, *args, **kwargs)

class NewObjectWindow(tk.Toplevel):
	def __init__(self, mainwindow):
		self.main_window = mainwindow

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

	def __create_object(self):
		# get object name
		name = self.ent_name.get()
		# get coordinates list
		coord = list(
			map(
				lambda x: tuple(map(int, x.split(","))), 
				re.findall(
					r'\(([ ]*\d+[ ]*[,][ ]*\d+[ ]*)\)',
					self.ent_coord.get()
				)
			)
		)
		c = coord[0]
		x = c[0]
		y = c[1]
		canvas = self.main_window.canvas
		xvp = ((x - canvas.minx)/(canvas.maxx-canvas.minx)) * (canvas.maxx - canvas.minx)
		yvp = (1 - (y - canvas.miny)/(canvas.maxy-canvas.miny)) * (canvas.maxy - canvas.miny)

		self.main_window.canvas.create_line(xvp, yvp, xvp + 1, yvp)

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
		self.ent_name  = tk.Entry(self.fr_top)
		self.ent_coord = tk.Entry(self.fr_top)
	
		# positioning elements
		self.fr_top.grid(    row = 0, column = 0)
		self.lb_name.grid(   row = 0, column = 0)
		self.ent_name.grid(  row = 1, column = 0)
		self.lb_coord.grid(  row = 2, column = 0)
		self.ent_coord.grid( row = 3, column = 0)
	
	def __build_fr_bottom(self):
		# create bottom frame
		self.fr_bottom = Frame(self.mainframe)

		# create buttons
		self.btn_ok = Button(
			self.fr_bottom,
			text = "Ok",
			command = self.__create_object
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

class MainWindow(tk.Tk):
	def __init__(self):
		# create window
		super().__init__()

		# we shouldn't place elements directly in root
		self.mainframe = Frame(self)
		self.mainframe.grid(row = 0, column = 0)

		self.__build_interface()

		self.new_object_window = NewObjectWindow(self)

		self.canvas = Viewport(self.mainframe)
		self.canvas.grid(row = 0, column = 1)

	def __move(self, xam, yam):
		canvas = self.canvas
		for obj in canvas.find_all():
			canvas.move(obj, xam, yam)

	def __move_up(self):
		self.__move(0, -self.canvas.delta_move)
		self.canvas.miny -= self.canvas.delta_move
		self.canvas.maxy -= self.canvas.delta_move

	def __move_down(self):	
		self.__move(0, self.canvas.delta_move)
		self.canvas.miny += self.canvas.delta_move
		self.canvas.maxy += self.canvas.delta_move

	def __move_left(self):
		self.__move(-self.canvas.delta_move, 0)
		self.canvas.minx += self.canvas.delta_move
		self.canvas.maxx += self.canvas.delta_move

	def __move_right(self):
		self.__move(self.canvas.delta_move, 0)
		self.canvas.minx -= self.canvas.delta_move
		self.canvas.maxx -= self.canvas.delta_move

	def __build_interface(self):
		self.frame_commands = Frame(self.mainframe, padx = 10)
		self.frame_commands.grid(row = 0, column = 0)

		self.button_newobject = Button(
			self.frame_commands,
			text = "New Object",
			command = self.new_object
		)
		self.button_newobject.grid(row = 0, column = 0)

		self.frame_arrows = Frame(self.frame_commands)
		self.frame_arrows.grid(row = 1, column = 0)

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

		self.button_up.grid(row=0, column = 0, columnspan = 2)
		self.button_left.grid(row=1, column = 0)
		self.button_right.grid(row = 1, column = 1)
		self.button_down.grid(row=2, column = 0, columnspan = 2)

	def new_object(self):
		self.new_object_window.show()

class Viewport(tk.Canvas):
	def __init__(
		self,
		master, 
		width = 500, 
		height = 500, 
		delta_move = 10, 
		delta_zoom = 1.3
		):

		self.width = width
		self.height = height
		self.delta_move = delta_move
		self.delta_zoom = delta_zoom
		self.minx = -self.width/2
		self.miny = -self.height/2
		self.maxx = self.width/2
		self.maxy = self.height/2

		super().__init__(
			master = master,
			bg = "white",
			width = self.width,
			height = self.height,
		)

def test():
	root = MainWindow()
	root.mainloop()

if __name__ == "__main__":
	test()