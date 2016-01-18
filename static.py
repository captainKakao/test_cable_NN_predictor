#!/usr/bin/python3.4

''' **************************************************************** '''

import math

''' **************************************************************** '''

el_count = 1000 # количество элементов

cable_len = 100 # длина кабеля, метры

Ckt = 0.02 # коэффициент касательной составляющей

Ckn = 1.2 # коэффициент нормальной составляющей

Dk = 0.01 # диаметр кабеля

ro = 1025 # плотность воды

Vb = 1.5 # скорость течения (уточнить - скорость потока относительно кабеля это, а не течение) 

Gk = 0 # остаточная плавучесть? проверить!

''' **************************************************************** '''

def static():

	# массивы координат элементов

	# прямой
	x_k = list(range(0, el_count + 1))
	y_k = list(range(0, el_count + 1))
	z_k = list(range(0, el_count + 1))

	# обратный
	x_kn = list(range(0, el_count + 1))
	y_kn = list(range(0, el_count + 1))
	z_kn = list(range(0, el_count + 1))

	# длина одного элемента
	''' dbl_dLk  '''
	el_len = cable_len / el_count

	# суммарные силы по осям - должны получать от аппарата
	Fx = 100
	Fy = 0
	Fz = 0

	# начальные координаты
	''' в программе почему-то c единицы - base 1 в бейсике - проверить '''
	x_k[0] = 0
	y_k[0] = 0
	z_k[0] = 0

	# только для отладки
	a = 5

	# номер текущего отрезка
	''' int_numLk '''
	cur_pos = 1

	while True:
	
		# 1 
	
		# результирующая сила - модуль
		mod_F = math.sqrt(Fx ** 2 + Fy ** 2 + Fz ** 2)
	
		# направляющие косинусы
		''' dbl_ '''
		Cos_Ax = Fx / mod_F
		Cos_Ay = Fy / mod_F
		Cos_Az = Fz / mod_F
	
		# 2
	
		# координаты элемента
		x_k[cur_pos] = x_k[cur_pos - 1] - el_len * Cos_Ax
		y_k[cur_pos] = y_k[cur_pos - 1] - el_len * Cos_Ay
		z_k[cur_pos] = z_k[cur_pos - 1] - el_len * Cos_Az
	
		# 3
	
		if Cos_Ax >= 0:
			# знак направления
			''' int_modCax '''
			mod_cax = 1
		else:
			mod_cax = -1
	
		# касательная составляющая
		Fkt = Ckt * Ckn * el_len * Dk * math.pi * ro * mod_cax * ((Vb * Cos_Ax) ** 2) / 2
	
		# нормальная составляющая
		Fkn = Ckn * el_len * Dk * ro * ((Vb * math.sqrt(1 - Cos_Ax ** 2)) ** 2) / 2
	
		# 4
		''' dbl_CosAxg ''' ''' dbl_CosAy ''' ''' dbl_CosAz '''
		Cos_Axg = -math.sqrt((Cos_Ay) ** 2 + (Cos_Az) ** 2)
		
		if Cos_Axg == 0:
		
			Cos_Ayg = 0	#	''' dbl_CosAyg '''
			Cos_Azg = 0	#	''' dbl_CosAzg '''
		
		else:
			
			Cos_Ayg = -Cos_Ax * Cos_Ay / Cos_Axg
			Cos_Azg = -Cos_Ax * Cos_Az / Cos_Axg
		
		# 5
		# силы
	
		Fx = Fx - Fkt * Cos_Ax + Fkn * Cos_Axg
	
		# комментарий по поводу смены знака
	
		Fy = Fy + Gk * el_len - Fkt * Cos_Ay + Fkn * Cos_Ayg
		Fz = Fz - Fkt * Cos_Az + Fkn * Cos_Azg
	
		# 6
	
		cur_pos += 1	# счётчик
	
		# условие выхода из цикла
		if cur_pos == el_count + 2:
			break
		
		####
	
	mod_F = math.sqrt(Fx ** 2 + Fy ** 2 + Fz ** 2)

	####
	
''' **************************************************************** '''

# для запуска из скрипта
if __name__ == '__main__':
	
	static()
