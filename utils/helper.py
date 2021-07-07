import re


class Helper:
	@staticmethod
	def get_coords_from_entry(string):
		return (
			list(
				map(
					lambda x: tuple(map(float, x.split(","))), 
					re.findall(
						r'\(([ ]*-?\d+\.?\d*[ ]*[,][ ]*-?\d+\.?\d*[ ]*)\)',
						string
					)
				)
			)
		)

	def validate_hex_color_entry(hex):
		r = re.search("^#([A-Fa-f0-9]{9}|[A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$", hex)
		if (r):
			return r.group()
		else:
			return None
		


