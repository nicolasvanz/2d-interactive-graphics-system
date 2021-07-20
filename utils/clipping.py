class Clipping:

	@staticmethod
	def region_code(ponto, xw_esq, extremidades_window):
		x = ponto[0]
		y = ponto[1]
		region_code = [0, 0, 0, 0]
		yw_topo, yw_fundo, xw_dir, xw_esq = extremidades_window

		if y > yw_topo:
			region_code[0] = 1
		if y < yw_fundo:
			region_code[1] = 1
		if x > xw_dir:
			region_code[2] = 1
		if x < xw_esq:
			region_code[3] = 1
		return region_code
	
	@staticmethod
	def intersection(region_code, ponto, coef_ang, extremidades_window):
		yw_topo, yw_fundo, xw_dir, xw_esq = extremidades_window

		if region_code[0] == 1:
			x = ponto[0] + (1/(coef_ang*(yw_topo - ponto[1])))
			if x >= xw_esq and x <= xw_dir:
				return (True, (x, yw_topo))
		if region_code[1] == 1:
			x = ponto[0] + (1/(coef_ang*(yw_fundo - ponto[1])))
			if x >= xw_esq and x <= xw_dir:
				return (True, (x, yw_fundo))
		if region_code[2] == 1:
			y = coef_ang*(xw_dir - ponto[0]) + ponto[1]
			if y >= yw_fundo and y <= yw_topo:
				return (True, (xw_dir, y))
		if region_code[3] == 1:
			y = coef_ang*(xw_esq - ponto[0]) + ponto[1]
			if y >= yw_fundo and y <= yw_topo:
				return (True, (xw_esq, y))
		return (False, None)


	@staticmethod
	def cohen_suther(pontos_da_reta, extremidades_window):
		ponto1 = pontos_da_reta[1]
		ponto2 = pontos_da_reta[2]
		tudo_zero = [0, 0, 0, 0]
		pontos_clipados = [(0, 0), (0, 0)]
		region_code1 = Clipping.region_code(ponto1, extremidades_window)
		region_code2 = Clipping.region_code(ponto2, extremidades_window)

		if region_code1 == tudo_zero and region_code2 == tudo_zero:
			return (True,pontos_da_reta)
		
		for i in range(4):
			if region_code1[i] == region_code2[i]:
				return(False, None)
		coef_ang = (ponto2[1] - ponto1[1])/(ponto2[0] - ponto1[0])
		if region_code1 == tudo_zero:
			pontos_clipados[0] = pontos_da_reta[0]
			retorno = Clipping.intersection(region_code2, ponto2, coef_ang, extremidades_window)
			pontos_clipados[1] = retorno[1]
			return pontos_clipados

		if region_code2 == tudo_zero:
			pontos_clipados[1] = pontos_da_reta[1]
			retorno = Clipping.intersection(region_code1, ponto1, coef_ang, extremidades_window)
			pontos_clipados[0] = retorno[1]
			return pontos_clipados
		
		retorno1 = Clipping.intersection(region_code1, ponto1, coef_ang, extremidades_window)
		if not(retorno1[0]):
			return(False, None)
		retorno2 = Clipping.intersection(region_code2, ponto2, coef_ang, extremidades_window)
		pontos_clipados[0] = retorno1[1]
		pontos_clipados[1] = retorno2[1]
		return pontos_clipados
