from abc import abstractclassmethod
from utils.transformer import Transformer
import numpy as np

class GraphicObjectCreator:
	def __init__(self, canvas):
		self.canvas = canvas

	def create(self, name, coords, is_closed = False, fill = "#000000"):
		l = len(coords)
		if l == 1:
			return Dot(self.canvas, "[Dot]%s" % name, coords, fill = fill)
		elif l == 2:
			return Line(self.canvas, "[Line]%s" % name, coords, fill = fill)
		else:
			return Wireframe(self.canvas, "[Wireframe]%s" % name, coords, is_closed, fill = fill)

class GraphicObject:
	def __init__(self, canvas, name, coords, is_closed = False, fill = "#000000"):
		self.canvas = canvas
		self.name = name
		self.is_closed = is_closed
		self.coordinates = coords
		self.scn = []
		self.fill = fill
	
	@abstractclassmethod
	def draw(self, matrix):
		pass

	@abstractclassmethod
	def get_center(self):
		pass
	
	def get_real_name(self):
		return self.name[self.name.index("]") + 1:]

	def transform(self, matrix):
		new_coords = []
		for coord in self.coordinates:
			coord_multi = np.dot(np.array([coord[0], coord[1], 1]), matrix)
			new_coords.append((coord_multi[0], coord_multi[1]))
		self.coordinates = new_coords
	
	def update_scn(self, matrix):
		new_coords = []
		for coord in self.coordinates:
			coord_multi = np.dot(np.array([coord[0], coord[1], 1]), matrix)
			new_coords.append((coord_multi[0], coord_multi[1]))
		self.scn = new_coords

class Dot(GraphicObject):
	def draw(self, matrix):
		self.update_scn(matrix)
		c = self.canvas.transform_viewport(self.scn)
		x, y = c[0]

		self.canvas.create_line(x, y, x + 1, y, fill = self.fill)
	
	def get_center(self):
		center = self.coordinates[0]
		return (center[0], center[1])

class Line(GraphicObject):
	def draw(self, matrix):
		self.update_scn(matrix)
		c = self.canvas.transform_viewport(self.scn)

		x1, y1 = c[0]
		x2, y2 = c[1]

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
		self.update_scn(matrix)
		c = self.canvas.transform_viewport(self.scn)
		for i in range(len(c) - 1):
			x1, y1 = c[i]
			x2, y2 = c[i + 1]
			self.canvas.create_line(x1, y1, x2, y2, fill = self.fill)
		
		# is a closed shape?
		if self.is_closed:
			x1, y1 = c[-1]
			x2, y2 = c[0]
			self.canvas.create_line(x1, y1, x2, y2, fill = self.fill)

	def get_center(self):
		orderedx = self.coordinates.copy()
		orderedy = self.coordinates.copy()
		orderedx.sort(key=lambda x: x[0])
		orderedy.sort(key=lambda x: x[1])
		x = (orderedx[0][0] + orderedx[-1][0])/2
		y = (orderedy[0][1] + orderedy[-1][1])/2
		return (x, y)

class Axis(Line):
	def update_scale(self, coef):
		scale = Transformer.scale(
				Transformer.identity(),
				(coef, coef),
				self.get_center()
		)
		self.transform(scale)

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
