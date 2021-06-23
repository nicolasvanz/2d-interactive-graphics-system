import tkinter as tk
import windows_interfaces
import re
import math
from tk_adaptations import *
from shapes import *


class MainWindow(windows_interfaces.MainWindowInterface):
	def __init__(self):
		super().__init__()

		# overwrite button functions 
		# (it takes initialy from MainWindowInterface functions)
		self.button_in.configure(   command = self.__zoom_in)
		self.button_out.configure(  command = self.__zoom_out)		
		self.button_up.configure(   command = self.__move_up)		
		self.button_down.configure( command = self.__move_down)
		self.button_left.configure( command = self.__move_left)
		self.button_right.configure(command = self.__move_right)

		self.canvas.draw()

	def __zoom_in(self):
		self.canvas.zoom(self.canvas.delta_zoom)
		
	def __zoom_out(self):
		self.canvas.zoom(1 / self.canvas.delta_zoom)

	def __move_up(self):
		self.canvas.movewin(0, self.canvas.delta_move)
		
	def __move_down(self):
		self.canvas.movewin(0, -self.canvas.delta_move)

	def __move_left(self):
		self.canvas.movewin(-self.canvas.delta_move, 0)

	def __move_right(self):
		self.canvas.movewin(self.canvas.delta_move, 0)

class Viewport(tk.Canvas):
	def __init__(self, master, mainwindow):
		self.mainwindow = mainwindow

		# viewport size
		self.width = 500
		self.height = 500

		# navigation coefitients
		self.delta_move = 30
		self.delta_zoom = 1.4

		# scene scale
		self.imgscale = 1

		# window coordinates
		self.minx = -self.width/2
		self.miny = -self.height/2
		self.maxx = self.width/2
		self.maxy = self.height/2

		self.graphicObjects = []

		self.graphic_object_creator = GraphicObjectCreator(
			self
		)

		super().__init__(
			master = master,
			bg = "white",
			width = self.width,
			height = self.height,
		)

		self.__create_axis()

	def transform(self, coords):
		transformed = []
		kx = self.width
		ky = self.height
		tx = (self.maxx-self.minx)
		ty = (self.maxy-self.miny)
		for c in coords:
			x, y = c

			transformed.append(
				(
					(     (x - self.minx) / tx)  * kx,
					(1 - ((y - self.miny) / ty)) * ky
				)
			)

		return transformed
	
	def __create_axis(self):
		axisx = AxisX(
			canvas = self,
			name = "axis-x",
			coords = [
				(-math.inf, 0),
				(math.inf, 0)
			],
			fill = "red"
		)
		axisy = AxisY(
			canvas = self,
			name = "axis-y",
			coords = [
				(0, -math.inf),
				(0, math.inf)
			],
			fill = "green"
		)

		# add axis to the objects list to display them
		self.graphicObjects.append(axisx)
		self.graphicObjects.append(axisy)
		
		self.draw()
	
	def create_object(self, name, coords, is_closed = False, fill = "black"):
		# create new graphic object
		newGraphicObject = self.graphic_object_creator.create(
			name,
			coords,
			is_closed,
			fill
		)

		# add new object to the list
		self.graphicObjects.append(newGraphicObject)

		# draw new object
		newGraphicObject.draw()

		return newGraphicObject

	def draw(self):
		self.delete("all")
		for i in self.graphicObjects:
			i.draw()
	
	def movewin(self, deltax, deltay):
		self.maxx += deltax
		self.minx += deltax
		self.maxy += deltay
		self.miny += deltay
		self.draw()
	
	def zoom(self, delta):
		rangex = (self.maxx - self.minx) / 2
		rangey = (self.maxy - self.miny) / 2
	
		# get center coordinates
		midlex = (self.maxx + self.minx) / 2
		midley = (self.maxy + self.miny) / 2

		# rearange window position
		self.minx = midlex - (rangex * 1 / delta)
		self.miny = midley - (rangey * 1 / delta)
		self.maxx = midlex + (rangex * 1 / delta)
		self.maxy = midley + (rangey * 1 / delta)

		# update image scale
		self.imgscale *= delta
		# redraw scene
		self.draw()


class NewObjectWindow(windows_interfaces.NewObjectWindowInterface):
	def submit(self):
		# get object name
		name = self.ent_name.get()
		
		if (not name):
			print("No name specified")
			return
		
		# ger Check Button value
		is_closed = self.chkValue.get()
		# get coordinates list
		coord = list(
			map(
				lambda x: tuple(map(int, x.split(","))), 
				re.findall(
					r'\(([ ]*-?\d+[ ]*[,][ ]*-?\d+[ ]*)\)',
					self.ent_coord.get()
				)
			)
		)

		if (not coord):
			print("No coordinates specified")
			return

		obj = self.mainwindow.canvas.create_object(
			name,
			coord,
			is_closed,
		)

		# update object names list box
		self.mainwindow.lst_objNames.insert("end", obj.name)
