

class Helper_curves:
    # Newton forward differences method to calculate curve points
    @staticmethod
    def fwd_diff(curve_points, step, x, delta_x1, delta_x2, delta_x3, 
                    y, delta_y1, delta_y2, delta_y3):
        i = step
        while i <= 1:
            i += step
            x = x + delta_x1
            delta_x1 = delta_x1 + delta_x2
            delta_x2 = delta_x2 + delta_x3
            y = y + delta_y1
            delta_y1 = delta_y1 + delta_y2
            delta_y2 = delta_y2 + delta_y3
            curve_points.append((x, y))
        return curve_points