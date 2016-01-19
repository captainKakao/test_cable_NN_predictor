#!/usr/bin/python3.4

''' **************************************************************** '''

import math
import matplotlib.pyplot as plt

''' **************************************************************** '''

el_count = 100 # количество элементов

cable_len = 100 # длина кабеля, метры

Ckt = 0.02 # коэффициент касательной составляющей

Ckn = 1.2 # коэффициент нормальной составляющей

Dk = 0.01 # диаметр кабеля

ro = 1025 # плотность воды

Vb = 1.5 # скорость течения (уточнить - скорость потока относительно кабеля это, а не течение) 

Gk = 0 # остаточная плавучесть




# массивы координат элементов

# прямой
x_k = list(range(0, el_count + 1))
y_k = list(range(0, el_count + 1))
z_k = list(range(0, el_count + 1))

# обратный
x_kn = list(range(0, el_count + 1))
y_kn = list(range(0, el_count + 1))
z_kn = list(range(0, el_count + 1))

''' **************************************************************** '''

def static():
	
	global el_count
	global cable_len
	global Ckt
	global Ckn
	global Dk
	global ro
	global Vb
	global Gk


	global x_k
	global y_k
	global z_k


	# длина одного элемента
	''' dbl_dLk  '''
	el_len = cable_len / el_count

	# суммарные силы по осям от аппарата (с учётом гидродинамики и плавучести)
	Fx = 100
	Fy = 500
	Fz = 0

	# начальные координаты
	x_k[0] = 0
	y_k[0] = 0
	z_k[0] = 0
	
	# номер текущего отрезка
	''' int_numLk '''
	cur_pos = 1

	while True:
	
		#print(cur_pos)
		
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
		
		# знак направления
		if Cos_Ax >= 0:
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
		''' if cur_pos == el_count + 2: '''
		if cur_pos == el_count + 1:
			break
		
		####
	
	mod_F = math.sqrt(Fx ** 2 + Fy ** 2 + Fz ** 2)

	####
	
''' **************************************************************** '''

def visual():
	
	'''
	http://nbviewer.ipython.org/github/whitehorn/Scientific_graphics_in_python/blob/master/P1%20Chapter%201%20Pyplot.ipynb
	'''
	
	global x_k
	global y_k
	global z_k
	
	
	
	fig = plt.figure()   # Создание объекта Figure
	
	#plt.scatter(1.0, 1.0)   # scatter - метод для нанесения маркера в точке (1.0, 1.0)  
	
	#print (fig.axes)  
	
	#plt.savefig('fig1')
	
	for i in range(0,len(x_k)):
		
		plt.scatter(x_k[i], y_k[i])
		
	plt.show()

''' **************************************************************** '''

# для запуска из консоли
if __name__ == '__main__':
	
	static()
	
	visual()
