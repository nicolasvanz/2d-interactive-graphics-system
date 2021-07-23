import tkinter as tk
import windows.interfaces as wi
from utils.tk_adaptations import *
from graphic_objects.shapes import *
from utils.transformer import *
from utils.helper import *
from utils.clipper import Clipper
from tkinter import filedialog
from functools import reduce


class MainWindow(wi.MainWindowInterface):
	def __init__(self):
		super().__init__()
		self.canvas.draw()

	def _new_object(self):
		# display new object window
		self.new_object_window.show()

	def _transform_object(self):
		# display transform object window
		self.transform_window.show()

	def get_selected_object(self):
		# get selected element in the object list
		index = self.lst_objNames.curselection()
		# must be one and only one object
		if (len(index) != 1): return -1

		return index[0]

	def _remove_object(self):
		index = self.get_selected_object()

		if (index == -1):
			print("No selected object to remove")
			return

		# remove object from object list
		self.canvas.remove_object(index)

		# remove object name from list box
		assert(index < self.lst_objNames.size())
		self.lst_objNames.delete(index)

	def _zoom_in(self):
		self.canvas.zoom(1/self.canvas.delta_zoom)

	def _zoom_out(self):
		self.canvas.zoom(self.canvas.delta_zoom)

	def _move_up(self):
		self.canvas.movewin(0, self.canvas.delta_move)

	def _move_down(self):
		self.canvas.movewin(0, -self.canvas.delta_move)

	def _move_left(self):
		self.canvas.movewin(90, self.canvas.delta_move)

	def _move_right(self):
		self.canvas.movewin(-90, self.canvas.delta_move)

	def _rotate_left(self):
		self.canvas.rotate(self.canvas.delta_angle)

	def _rotate_right(self):
		self.canvas.rotate(-self.canvas.delta_angle)

	def _import_objfile(self):
		filename = filedialog.askopenfilename(
			title="select a file"
		)
		self.obj_helper.import_obj(filename)

	def _export_objfile(self):
		filename = filedialog.asksaveasfilename(defaultextension='.obj')
		if filename is None:
			return

		self.obj_helper.export_obj(filename, self.canvas.graphicObjects)

class Viewport(tk.Canvas):
	def __init__(self, master, mainwindow):
		# root
		self.mainwindow = mainwindow

		# window properties
		self.win_angle = 0

		# viewport size
		self.width = 500
		self.height = 500

		# edge coefficient with which objects are cut 
		# (in normalized coordinates)
		self.clipping_pad = 0.9

		# note the subcanvas is static, so we don't need it to be 
		# a GraphicObject object
		coef = self.clipping_pad
		self.subcanvas = Subcanvas(
			self,
			"subcanvas",
			[
				(-coef, -coef),
				(coef, -coef),
				(coef, coef),
				(-coef, coef),
			],
			fill="DarkGoldenrod3"
		)
		self.clipping_function = Clipper.cohen_sutherland

		# navigation coefitients
		self.delta_move = 1/10
		self.delta_zoom = 1.1
		self.delta_angle = 10

		# scene scale
		self.imgscale = 1

		# window coordinates
		self.edges = LazyWireframe(
			[
				(-self.width/2, -self.width/2),
				(self.height/2, -self.width/2),
				(self.height/2, self.height/2),
				(-self.width/2, self.height/2)
			]
		)

		self.graphic_object_creator = GraphicObjectCreator(self)
		self.graphicObjects = []
		self.axis_list = []

		super().__init__(
			master = master,
			bg = "white",
			width = self.width,
			height = self.height,
		)

		self.__create_axis()

	def size(self):
		w1, w2, w3, w4 = self.edges.coordinates
		x = ((w2[0]-w1[0])**2+(w2[1]-w1[1])**2)**0.5
		y = ((w4[0]-w1[0])**2+(w4[1]-w1[1])**2)**0.5
		return (x, y)

	def get_center(self):
		return self.edges.get_center()
	
	def get_vup(self, as_line=False):
		edges = self.edges.coordinates
		x = edges[-1][0] - edges[0][0]
		y = edges[-1][1] - edges[0][1]
		# return as point or line
		if (as_line):
			return LazyLine([(0, 0), (x, y)])
		return LazyDot([(x, y)])

	def get_scn_matrix(self):
		# world transformation matrix to get coordinates in normalized
		# coordinate system
		size = self.size()
		matrix = Transformer.identity()
		matrix = Transformer.translation(matrix, tuple(map(lambda x: -x, self.get_center())))
		matrix = Transformer.scale(matrix, (1/(size[0]/2),1/(size[1]/2)), (0,0))
		matrix = Transformer.rotation(matrix,-self.win_angle, (0,0))
		return matrix

	def __create_axis(self):
		# note that the axis are 2 times bigger than the size of screen. 
		# We need it to be at least as larger as the window diagonal 
		# for rotation support.
		self.axisx = Axis(
			canvas = self,
			name = "axis-x",
			coords = [
				(-self.width, 0),
				(self.width, 0)
			],
			fill = "red"
		)
		self.axisy = Axis(
			canvas = self,
			name = "axis-y",
			coords = [
				(0, -self.height),
				(0, self.height)
			],
			fill = "green"
		)

		# add axis to the axis_list
		self.axis_list.append(self.axisx)
		self.axis_list.append(self.axisy)
		
		# draw scene
		self.draw()
	
	def transform_viewport(self, coords):
		# transform from window coordinates to viewport coordinates
		transformed = []
		kx = self.width
		ky = self.height
		for c in coords:
			x, y = c

			transformed.append(
				(
					(     (x + 1) / 2)  * kx,
					(1 - ((y + 1) / 2)) * ky
				)
			)

		return transformed
	
	def transform_object(self, index, matrix):
		# translate, scale or rotate an object
		obj = self.graphicObjects[index]
		obj.transform(matrix)
		self.draw()

	def create_object(self, name, coords, is_closed = False, fill = "black", is_filled = False):
		# create new graphic object
		newGraphicObject = self.graphic_object_creator.create(
			name,
			coords,
			is_closed,
			fill,
			is_filled,
		)

		# add new object to the list
		self.graphicObjects.append(newGraphicObject)

		# update object names list box
		self.mainwindow.lst_objNames.insert("end", newGraphicObject.name)

		# draw the scene
		self.draw()

		return newGraphicObject

	def remove_object(self, index):
		assert(index < len(self.graphicObjects))

		self.graphicObjects.pop(index)

		self.draw()

	def draw(self):
		self.delete("all")
		matrix = self.get_scn_matrix()
		for i in self.axis_list:
			i.draw(matrix)
		for i in self.graphicObjects:
			i.draw(matrix)
		self.subcanvas.draw()

	def movewin(self, angle, delta):
		# get translation vector
		vup = self.get_vup()
		matrix = Transformer.rotation(Transformer.identity(), angle, (0, 0))
		vup.transform(matrix)
		vup = tuple(map(lambda x: x*delta, vup.coordinates[0]))
		matrix = Transformer.translation(Transformer.identity(), vup)

		# apply translation
		self.edges.transform(matrix)

		# update axis range. They should follow window position
		x, y = vup
		self.axisx.update_range((x, 0))
		self.axisy.update_range((0, y))

		# redraw scene
		self.draw()
	
	def rotate(self, angle):
		# get rotation matrix
		matrix = Transformer.rotation(
			Transformer.identity(),
			angle,
			self.get_center()
		)
		# apply rotation
		self.edges.transform(matrix)

		# update angle
		self.win_angle += angle
		self.draw()

	def zoom(self, delta):
		# get scaling matrix
		matrix = Transformer.scale(
			Transformer.identity(),
			(delta,delta),
			self.get_center()	
		)

		# apply scaling
		self.edges.transform(matrix)

		# axis should follow screen zoom
		self.axisx.update_scale(self.imgscale*delta/self.imgscale)
		self.axisy.update_scale(self.imgscale*delta/self.imgscale)
		
		# update image scale
		self.imgscale *= delta

		# redraw scene
		self.draw()

class NewObjectWindow(wi.NewObjectWindowInterface):
	def submit(self):
		# get object name
		name = self.ent_name.get()

		# get object color
		color = self.ent_color.get() 
		
		if (not name):
			print("No name specified")
			return
		
		if (not color):
			color = "#000000"
		else:
			color = Helper.validate_hex_color_entry(color)
			if (not color):
				print("invalid color code")
				return		

		# get Check Button value
		is_closed = self.chkclosed.get()
		is_filled = self.chkfilled.get()
		
		# get coordinates list
		coord = Helper.get_coords_from_entry(self.ent_coord.get())

		if (not coord):
			print("No coordinates specified")
			return

		self.mainwindow.canvas.create_object(
			name,
			coord,
			is_closed,
			color,
			is_filled,
		)

class TransformWindow(wi.TransformWindowInterface):
	def add(self):
		index = self.transformation_index
		if (index == None):
			index = self.mainwindow.get_selected_object()
			if (index == -1):
				print("No object selected to transform")
				return
			self.transformation_index = index

		# get selected object itself
		obj = self.mainwindow.canvas.graphicObjects[index]

		# get checkbox values
		translate = self.translate.get()
		rotate = self.rotate.get()
		scale = self.scale.get()
	
		matrix = Transformer.identity()

		# scale?
		if scale:
			scale_factor = Helper.get_coords_from_entry(self.scal_ent.get())
			if (len(scale_factor) != 1):
				print("invalid scale factor specified")
				return
			scale_factor = scale_factor[0]
			center = obj.get_center()
			matrix = Transformer.scale(matrix, scale_factor, center)

		# rotate?
		if rotate:
			try:
				angle = float(self.rot_ent_angle.get())
			except ValueError:
				print("invalid angle specified")
				return
			rtype = self.rotation_type.get()
			if (rtype == self.rot_combbx_options[0]):
				point = obj.get_center()
			elif (rtype == self.rot_combbx_options[1]):
				point = (0, 0) # world center
			else:
				point = Helper.get_coords_from_entry(self.rot_ent_point.get())
				if (len(point) != 1):
					print("invalid rotation point specified")
					return
				point = point[0]
			matrix = Transformer.rotation(matrix, angle, point)

		# translate?
		if translate:
			vector = Helper.get_coords_from_entry(self.trans_ent.get())
			if (len(vector) != 1):
				print("invalid translation vector specified")
				return

			# translation should follow window rotation			
			vector_as_dot = LazyDot(vector)

			rotation = Transformer.rotation(
				Transformer.identity(),
				self.mainwindow.canvas.win_angle,
				(0, 0)
			)
			vector_as_dot.transform(rotation)

			matrix = Transformer.translation(matrix, vector_as_dot.coordinates[0])
		
		self._add_matrix(matrix)
		
	def submit(self):
		index = self.transformation_index

		if (not self.transformations):
			return

		matrix = reduce(np.dot, self.transformations)

		self.mainwindow.canvas.transform_object(index, matrix)
		
		self._reset_transformations()
