INSIDE = 0
LEFT = 1
RIGHT = 2
BOTTOM = 4
TOP = 8
class Clipper:
	@staticmethod
	def region_code(x, y, coef):
		x_min, x_max, y_min, y_max = -coef, coef, -coef, coef
		code = INSIDE
		if x < x_min:
			code |= LEFT
		if x > x_max:
			code |= RIGHT
		if y < y_min:
			code |= BOTTOM
		if y > y_max:
			code |= TOP
	
		return code
	
	@staticmethod
	def cohen_sutherland(line, coef):
		x_min, x_max, y_min, y_max = -coef, coef, -coef, coef
		x1, y1 = line[0]
		x2, y2 = line[1]

		code1 = Clipper.region_code(x1, y1, coef)
		code2 = Clipper.region_code(x2, y2, coef)
		valid = False
	
		while True:
			if code1 == 0 and code2 == 0:
				valid = True
				break

			elif (code1 & code2) != 0:
				break
	
			else:
				code_out = code1 if code1 != INSIDE else code2
	
				if code_out & TOP:
					x = x1 + ((x2 - x1)/(y2 - y1))*(y_max - y1)
					y = y_max
	
				elif code_out & BOTTOM:
					x = x1 + ((x2 - x1)/(y2 - y1))*(y_min - y1)
					y = y_min
	
				elif code_out & RIGHT:
					y = y1 + ((y2 - y1)/(x2 - x1))*(x_max - x1)
					x = x_max
	
				elif code_out & LEFT:
					y = y1 + ((y2 - y1)/(x2 - x1))*(x_min - x1)
					x = x_min
	
				if code_out == code1:
					x1, y1 = x, y
					code1 = Clipper.region_code(x1, y1, coef)
	
				else:
					x2, y2 = x, y
					code2 = Clipper.region_code(x2, y2, coef)
	
		if valid:
			return [(x1, y1), (x2, y2)]
		return []

	@staticmethod
	def liang_barsky(line, coef):
		d1 = line[0]
		d2 = line[1]

		xmax, xmin, ymax, ymin = coef, -coef, coef, -coef

		dx = d2[0] - d1[0]
		dy = d2[1] - d1[1]
		p = [-dx, dx, -dy, dy]
		q = [d1[0] - xmin, xmax - d1[0], d1[1] - ymin, ymax - d1[1]]

		pos = [1]
		neg = [0]
		for i in range(4):
			if p[i] < 0:
				neg.append(q[i]/p[i])
			elif p[i] > 0:
				pos.append(q[i]/p[i])
			elif (q[i] < 0):
					return []
		
		u1 = max(neg)
		u2 = min(pos)

		# outside window
		if (u1 > u2):
			return []

		clipped = [
			(d1[0]+dx*u1, d1[1]+dy*u1),
			(d1[0]+dx*u2, d1[1]+dy*u2)
		]

		return clipped
