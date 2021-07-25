from abc import abstractclassmethod
from utils.clipper import Clipper
from utils.transformer import Transformer
import numpy as np

class GraphicObjectCreator:
	def __init__(self, canvas):
		self.canvas = canvas

	# create a graphic object based on the coordinates amount
	def create(self, name, coords, is_closed = False, fill = "#000000", is_filled=False):
		l = len(coords)
		if l == 1:
			return Dot(self.canvas, "[Dot]%s" % name, coords, fill = fill)
		elif l == 2:
			return Line(self.canvas, "[Line]%s" % name, coords, fill = fill)
		else:
			return Wireframe(
				self.canvas,
				"[Wireframe]%s" % name,
				coords,
				is_closed,
				fill = fill,
				is_filled = is_filled
			)

class GraphicObject:
	def __init__(
		self, 
		canvas, 
		name, 
		coords, 
		is_closed = False, 
		fill = "#000000", 
		is_filled=False
	):
		self.canvas = canvas
		self.name = name
		self.is_closed = is_closed
		self.coordinates = coords
		self.scn = []
		self.fill = fill
		self.is_filled = is_filled
	
	@abstractclassmethod
	def draw(self, matrix):
		pass

	@abstractclassmethod
	def get_center(self):
		pass
	
	# take real name of the object (what was specified in creation)
	def get_real_name(self):
		return self.name[self.name.index("]") + 1:]

	# transform object coordinates
	def transform(self, matrix):
		new_coords = []
		for coord in self.coordinates:
			coord_multi = np.dot(np.array([coord[0], coord[1], 1]), matrix)
			new_coords.append((coord_multi[0], coord_multi[1]))
		self.coordinates = new_coords
	
	# calculates object coordinates in normalized coordinate system
	def update_scn(self, matrix):
		new_coords = []
		for coord in self.coordinates:
			coord_multi = np.dot(np.array([coord[0], coord[1], 1]), matrix)
			new_coords.append((coord_multi[0], coord_multi[1]))
		self.scn = new_coords

class Dot(GraphicObject):
	def draw(self, matrix):
		# normalize coordinates
		self.update_scn(matrix)

		# dot is not inside window. We don't need to draw
		if (max(map(abs, self.scn[0])) > 1):
			return 

		# get viewport coordinates
		c = self.canvas.transform_viewport(self.scn)
		x, y = c[0]

		# draw a line
		self.canvas.create_line(x, y, x + 1, y, fill = self.fill)
	
	def get_center(self):
		center = self.coordinates[0]
		return (center[0], center[1])

class Line(GraphicObject):
	def draw(self, matrix):
		# normalize coordinates
		self.update_scn(matrix)

		# gets clipped line
		clipped = self.canvas.clipping_function(self.scn, 1)

		# line is not inside window. Ignore it
		if (not clipped):
			return

		# get viewport coordinates
		c = self.canvas.transform_viewport(clipped)

		x1, y1 = c[0]
		x2, y2 = c[1]

		# draw a line
		self.canvas.create_line(x1, y1, x2, y2, fill = self.fill)
	
	def get_center(self):
		orderedx = self.coordinates.copy()
		orderedy = self.coordinates.copy()
		orderedx.sort(key=lambda x: x[0])
		orderedy.sort(key=lambda x: x[1])
		x = (orderedx[0][0] + orderedx[-1][0])/2
		y = (orderedy[0][1] + orderedy[-1][1])/2
		return (x, y)

class Wireframe(GraphicObject):
	def draw(self, matrix):
		# normalize coordinates
		self.update_scn(matrix)

		# is a filled object?
		if (self.is_filled):
			self.__draw_filled()
		else:
			self.__draw_wire()
		
	def __draw_wire(self):
		for i in range(len(self.scn) - 1):
			# get clipped line
			clipped = self.canvas.clipping_function(self.scn[i:i+2], 1)

			# line is not inside window. Ignore it
			if (not clipped):
				continue

			# get viewport coordinates
			transformed = self.canvas.transform_viewport(clipped)
			x1, y1 = transformed[0]
			x2, y2 = transformed[1]

			# draw a line
			self.canvas.create_line(x1, y1, x2, y2, fill = self.fill)
		
		# is a closed shape? If so, connect first and last points
		if self.is_closed:
			clipped = self.canvas.clipping_function(
				[self.scn[0], self.scn[-1]],
				1
			)
			if (not clipped):
				return
			transformed = self.canvas.transform_viewport(clipped)
			x1, y1 = transformed[0]
			x2, y2 = transformed[1]
			self.canvas.create_line(x1, y1, x2, y2, fill = self.fill)

	def __draw_filled(self):
		# get clipped polygon
		polygon = Clipper.cohen_sutherland_polygon(self.scn, 1)

		# polygon is not inside window
		if (not polygon):
			return

		# get viewport coordinates
		transformed = self.canvas.transform_viewport(polygon)
		temp = []

		# turns [(x1, y1), (x2, y2)...] into [x1, y1, x2, y2, ...]
		for p in transformed:
			temp.extend(p)

		# draw a filled polygon
		self.canvas.create_polygon(temp, fill = self.fill)

	def get_center(self):
		orderedx = self.coordinates.copy()
		orderedy = self.coordinates.copy()
		orderedx.sort(key=lambda x: x[0])
		orderedy.sort(key=lambda x: x[1])
		x = (orderedx[0][0] + orderedx[-1][0])/2
		y = (orderedy[0][1] + orderedy[-1][1])/2
		return (x, y)

# note that this object is static, it's not part of the world. So we don't need
# to make any kind of transformation in it
class Subcanvas(GraphicObject):
	def draw(self):
		c = self.coordinates
		for i in range(len(c) - 1):
			x1, y1 = c[i]
			x2, y2 = c[i + 1]
			self.canvas.create_line(x1, y1, x2, y2, fill = self.fill)
		
		x1, y1 = c[-1]
		x2, y2 = c[0]
		self.canvas.create_line(x1, y1, x2, y2, fill = self.fill)

class Axis(Line):
	# make axis bigger or smaller to support window zoom in and zoom out
	def update_scale(self, coef):
		scale = Transformer.scale(
				Transformer.identity(),
				(coef, coef),
				self.get_center()
		)
		self.transform(scale)
	
	# move axis to support window movement
	def update_range(self, vector):
		translation = Transformer.translation(
			Transformer.identity(),
			vector
		)
		self.transform(translation)

# class used for objects that are not drawn. For example, the window
class LazyGraphicObject(GraphicObject):
	def __init__(self, coords):
		super().__init__(
			canvas = None,
			name = "lazy-object",
			coords = coords
		)

class LazyWireframe(LazyGraphicObject, Wireframe):
	# we only need parent functions
	def __dummy(self):
		pass

class LazyLine(LazyGraphicObject, Line):
	# we only need parent functions
	def __dummy(self):
		pass

class LazyDot(LazyGraphicObject, Dot):
	# we only need parent functions
	def __dummy(self):
		pass
