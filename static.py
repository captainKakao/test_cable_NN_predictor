#!/usr/bin/python3.4

''' **************************************************************** '''

import math
import matplotlib.pyplot as plt
import random



import keras
import numpy as np

''' **************************************************************** '''

class FLOW(object):
	def method(self, depth):
		print('depth', round(abs(depth)))
		my_flow = random.randrange(-10, 10, 2)
		# my_flow = random.randrange(0, 10, 2)
		# return my_flow / 10
		if my_flow > 0:
			print('depth', print(my_flow))
		# return my_flow - 5
		return 0.2

flow = FLOW()

el_count  =  10    # количество элементов
cable_len =  100    # длина кабеля, метры
Ckt       =    0.02 # коэффициент касательной составляющей
Ckn       =    1.2  # коэффициент нормальной составляющей
Dk        =    0.01 # диаметр кабеля
ro        = 1025    # плотность воды
Vb        =    1.5  # скорость течения (уточнить - скорость потока относительно кабеля это, а не течение)
Gk        =    0    # остаточная плавучесть

in_data = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]


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
	# сила на ходовом конце кабеля
	Fx =   50
	Fy = 100
	Fz =   0

	in_data[0][0] = el_count
	in_data[0][1] = cable_len
	in_data[0][2] = Ckt
	in_data[0][3] = Ckn
	in_data[0][4] = Dk
	in_data[0][5] = ro
	in_data[0][6] = Vb
	in_data[0][7] = Gk
	in_data[0][8] = Fx
	in_data[0][9] = Fy
	in_data[0][10] = Fz


	# начальные координаты
	x_k[0] = 0
	y_k[0] = 0
	z_k[0] = 0
	
	# номер текущего отрезка
	cur_pos = 1

	while True:
	
		# 1 
	
		# результирующая сила - модуль
		# ходовой конец кабеля
		mod_F = math.sqrt(Fx ** 2 + Fy ** 2 + Fz ** 2)
	
		# направляющие косинусы
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




		# Vb = flow.method(y_k[cur_pos])
		#print('x_k', x_k[cur_pos])



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
	
	
	
	# fig = plt.figure()   # Создание объекта Figure
	
	fig = plt.figure(1,(28,16))   # Создание объекта Figure
	a1 = plt.subplot(321)
	a1.set_title('calculated')

	#plt.scatter(1.0, 1.0)   # scatter - метод для нанесения маркера в точке (1.0, 1.0)
	plt.scatter(0, 0, color='red')
	a = len(x_k) - 1
	plt.scatter(x_k[a], y_k[a], color='red')

	print (fig.axes)
	
	#plt.savefig('fig1')
	
	for i in range(0,len(x_k)):
		
		#plt.scatter(1000*x_k[i], 1000*y_k[i],10)
		plt.scatter(x_k[i], y_k[i], 10, color='green')

	#plt.savefig("fig2")

	plt.plot(x_k, y_k, color='green')


	# plt.show()










	k = 1000


	# in_data = [[10, 100, 0.02, 1.2, 0.01, 1025, 1.5, 0, 50, 100, 0]]

	for i in range(0, len(in_data[0])):
		in_data[0][i] = in_data[0][i] / k

	model = keras.models.load_model('C:/Users/Professional/PycharmProjects/cable_NN/cable_NN.keras')
	print(in_data[:1])
	res = model.predict(in_data[:1])

	for i in range(0, len(res[0])):
		res[0][i] = res[0][i] * k

	list_res = res.tolist()

	r = int(len(list_res[0]) / 3)

	x = [0 for i in range(r)]
	y = [0 for i in range(r)]
	z = [0 for i in range(r)]

	for i in range(0, len(list_res[0])):
		if i < 11:
			x[i] = list_res[0][i]
		if i > 10 and i < 22:
			y[i - 11] = list_res[0][i]
		if i > 21 and i < 33:
			z[i - 22] = list_res[0][i]

	# print(x)
	# print(y)
	# print(z)

	# fig_1 = plt.figure()  # Создание объекта Figure
	a2 = plt.subplot(322)
	a2.set_title('predicted')

	fig_1 = plt.figure(1, (28, 16))  # Создание объекта Figure


	plt.scatter(0, 0, color='green')
	a = len(x) - 1
	plt.scatter(x[a], y[a], color='green')

	for i in range(0, len(x)):
		plt.scatter(x[i], y[i], 10, color='red')
	plt.plot(x, y, color='red')


	a3 = plt.subplot(323)
	a3.set_title('comparison')

	plt.plot(x_k, y_k, color='green')
	plt.plot(x, y, color='red')

	x_ = [0 for i in range(len(x))]
	for i in range(0, len(x_)):
		x_[i] = x[i] - x_k[i]

	y_ = [0 for i in range(len(y))]
	for i in range(0, len(y_)):
		y_[i] = y[i] - y_k[i]

	z_ = [0 for i in range(len(z))]
	for i in range(0, len(z_)):
		z_[i] = z[i] - z_k[i]

	t = np.arange(0, 11, 1)
	nul = [0,0,0,0,0,0,0,0,0,0,0]
	print(len(x_))
	X = plt.subplot(324)
	X.set_title('X error')


	plt.plot(t, nul, color='black')
	plt.plot(t, x_, color='orange')

	Y = plt.subplot(325)
	Y.set_title('Y error')

	plt.plot(t, nul, color='black')
	plt.plot(t, y_, color='blue')

	Z = plt.subplot(326)
	Z.set_title('Z error')

	plt.plot(t, nul, color='black')
	plt.plot(t, z_, color='purple')

	plt.show()

#
	# t = np.arange(0.0, 2.0, 0.01)
	# s1 = np.sin(2 * np.pi * t)
	# s2 = np.sin(4 * np.pi * t)
	#
	# plt.figure(1)
	# plt.subplot(211)
	# plt.scatter(x_k[a], y_k[a])
	# plt.subplot(212)
	# plt.scatter(x[a], y[a])

	# plt.show()

''' **************************************************************** '''

# для запуска из консоли
if __name__ == '__main__':
	
	static()
	
	visual()

