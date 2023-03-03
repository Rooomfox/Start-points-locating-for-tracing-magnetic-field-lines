import os
import shutil
import math
import cmath
import numpy as np
import matplotlib.pyplot as plt


def readFile(path, filename, f_dict, toroidal_angle=0):
	'''a line has: index, point_index, r, t_a(radian), x, y, z,
	   length, br, bz, bt, b.'''
	if os.path.exists(path):
		result_p = [[a] for a in f_dict]
		f_num = len(f_dict)
		t_a_radi = math.radians(toroidal_angle)
		for i in range(f_num):
			filename2 = filename + str(i+1) + '.trac'
			with open(filename2, 'rb') as file_object:
				first_line = file_object.readline()
				f_l = first_line.split()
				r = float(f_l[2])
				x = r * math.cos(t_a_radi)
				y = r * math.sin(t_a_radi)
				z = float(f_l[6])
				
				file_size = os.path.getsize(filename2)
				if file_size > 300:
					offset = -100
					while True:
						file_object.seek(offset, 2)
						lines = file_object.readlines()
						if len(lines) >= 2:
							last_line = lines[-1]
							break
						offset *= 2
				else:
					lines = file_object.readlines()
					if lines != []:
						last_line = lines[-1]
					else:
						last_line = first_line

				l_l = last_line.split()
				point_index = int(l_l[1])

				p = [x, y, z, point_index]
				result_p[i] += p

		print('location | x | y | z | length')
		for p in result_p:
			print(p)

		return result_p


def readFile2(filename2):
	'''a poincare plot has: index, point_index, r, t_a(radian),
	   x, y, z, length, br, bz, bt, b, m(circle).'''
	with open(filename2) as file_object:
		first_line = file_object.readline()
		f_l = first_line.split()
		magnetic_axis_r = float(f_l[2])
		magnetic_axis_z = float(f_l[6])

	return magnetic_axis_r, magnetic_axis_z


def lineIntersectCircle(p, lsp, esp):
    # p is the circle parameter, lsp and lep is the two end of the line
    x0, y0, r0 = p
    x1, y1 = lsp
    x2, y2 = esp
    if r0 == 0:
        return -1
    if x1 == x2:
        if abs(r0) >= abs(x1 - x0):
            p1 = x1, round(y0 - math.sqrt(r0 ** 2 - (x1 - x0) ** 2), 5)
            p2 = x1, round(y0 + math.sqrt(r0 ** 2 - (x1 - x0) ** 2), 5)
            inp = [p1, p2]
            # select the points lie on the line segment
            # inp = [p for p in inp if p[0] >= min(x1, x2) and p[0] <= max(x1, x2)]
        else:
            inp = []
    else:
        k = (y1 - y2) / (x1 - x2)
        b0 = y1 - k * x1
        a = k ** 2 + 1
        b = 2 * k * (b0 - y0) - 2 * x0
        c = (b0 - y0) ** 2 + x0 ** 2 - r0 ** 2
        delta = b ** 2 - 4 * a * c
        if delta >= 0:
            p1x = round((-b - math.sqrt(delta)) / (2 * a), 5)
            p2x = round((-b + math.sqrt(delta)) / (2 * a), 5)
            p1y = round(k * p1x + b0, 5)
            p2y = round(k * p2x + b0, 5)
            inp = [[p1x, p1y], [p2x, p2y]]
            # select the points lie on the line segment
            # inp = [p for p in inp if p[0] >= min(x1, x2) and p[0] <= max(x1, x2)]
        else:
            inp = []

    return inp if inp != [] else -1


def decideBorder(p_list, reactor_spec, toroidal_angle=0, circles=[]):
	'''reactor_spec is a list: [major_radius, minor_radius,
	   magnetic_axis_r, magnetic_axis_z].
	   toroidal_angle uses degrees.'''
	ps = []
	if p_list == []:
		major_r = reactor_spec[0]
		minor_r = reactor_spec[1]
		magnetic_axis = reactor_spec[2:4]
		t_a_radi = math.radians(toroidal_angle)
		p_a = t_a_radi / math.radians(36) * math.radians(180)
		mx = magnetic_axis[0] * math.cos(t_a_radi)
		my = magnetic_axis[0] * math.sin(t_a_radi)

		lsp = [magnetic_axis[0], magnetic_axis[1]]
		esp_x = magnetic_axis[0] + math.cos(-p_a)
		esp_y = magnetic_axis[1] + math.sin(-p_a)
		esp = [esp_x, esp_y]
		c = [major_r, 0, minor_r]

		res = lineIntersectCircle(c, lsp, esp)

		if res == -1:
			print('lineIntersectCircle function error.')
		else:
			for p in res:
				px = p[0] * math.cos(t_a_radi)
				py = p[0] * math.sin(t_a_radi)
				ps.append(['l_l', px, py, p[1]])
			ps[-1][0] = 'r_l'

			ps.insert(-1, ['l_l', mx, my, magnetic_axis[1]])
			ps.insert(-1, ['r_l', mx, my, magnetic_axis[1]])

		esp_x2 = magnetic_axis[0] + math.cos(-p_a - 0.5 * math.pi)
		esp_y2 = magnetic_axis[1] + math.sin(-p_a - 0.5 * math.pi)
		esp2 = [esp_x2, esp_y2]

		res2 = lineIntersectCircle(c, lsp, esp2)

		if res2 == -1:
			print('lineIntersectCircle function_2 error.')
		else:
			for p in res2:
				px = p[0] * math.cos(t_a_radi)
				py = p[0] * math.sin(t_a_radi)
				ps.append(['b_r', px, py, p[1]])
			ps[-1][0] = 't_r'

			ps.insert(-1, ['b_r', mx, my, magnetic_axis[1]])
			ps.insert(-1, ['t_r', mx, my, magnetic_axis[1]])
		return ps

	else:
		min_c = circles[0]
		max_c = circles[1]
		list1, list2, list3, list4 = [], [], [], []
		for p in p_list:
			if p[0] == 'l_l':
				list1.append(p)
			elif p[0] == 'r_l':
				list2.append(p)
			elif p[0] == 't_r':
				list3.append(p)
			elif p[0] == 'b_r':
				list4.append(p)
		list_direction1 = [list1, list4]
		list_direction2 = [list2, list3]

		for a_list in list_direction1:
			for index, p in enumerate(a_list):
				if p[4] >= min_c and a_list[index + 1][4] >= min_c:
					ps.append(a_list[index - 1])
					break
			a_list_revese = a_list[::-1]
			for index, p in enumerate(a_list_revese):
				if p[4] != max_c and a_list_revese[index + 1][4] != max_c:
					if index == 0:
						ps.append(a_list_revese[0])
					else:
						ps.append(a_list_revese[index - 1])
					break

		for a_list in list_direction2:
			a_list_revese = a_list[::-1]
			for index, p in enumerate(a_list_revese):
				if p[4] >= min_c and a_list_revese[index + 1][4] >= min_c:
					ps.append(a_list_revese[index - 1])
					break
			for index, p in enumerate(a_list):
				if p[4] != max_c and a_list[index + 1][4] != max_c:
					if index == 0:
						ps.append(a_list[0])
					else:
						ps.append(a_list[index - 1])
					break
			ps[-1], ps[-2] = ps[-2], ps[-1]
		return ps


def generatePoints(start_p, end_p, step):
	points = []
	start_p_array = np.array(start_p)
	end_p_array = np.array(end_p)
	length = np.linalg.norm(end_p_array - start_p_array)
	p_num = length // step + 1
	p_num = int(p_num)
	vector = [end_p[i]-start_p[i] for i in range(3)]

	for n in range(p_num):
		x = start_p[0] + vector[0] / p_num * n
		y = start_p[1] + vector[1] / p_num * n
		z = start_p[2] + vector[2] / p_num * n
		points.append([x, y, z])

	points.append(end_p)

	return points


def drawStartPoints(points):
	x, y, z = list(zip(*points))

	fig = plt.figure()
	ax = fig.add_subplot(projection='3d')

	ax.scatter(x, y, z, c='b')

	# add support lines
	line1 = [[0, 8], [0, 0], [0, 0]]
	cn2 = cmath.rect(8, math.radians(36))
	line2 = [[0, cn2.real], [0, cn2.imag], [0, 0]]
	ax.scatter(0, 0, 0, c='r')
	ax.plot(line1[0], line1[1], line1[2], c='r')
	ax.plot(line2[0], line2[1], line2[2], c='r')

	ax.set_xlabel('X')
	ax.set_ylabel('Y')
	ax.set_zlabel('Z')

	plt.show()


def generateFile(points, filename):
	p_num = len(points)
	str_ps = []
	for p in points:
		str_p = str(p[0])+'  '+str(p[1])+'  '+str(p[2])
		str_ps.append(str_p)

	fo = open(filename, 'w')
	fo.write(f'{p_num}\n')
	for str_p in str_ps:
		fo.write(str_p+'\n')
	fo.close()


def generateFile2(f_dict, filename2):
	fo = open(filename2, 'w')
	for f in f_dict:
		fo.write(f+'\n')
	fo.close()


def generateFile3(ps, filename3):
	fo = open(filename3, 'w')
	for p in ps:
		fo.write(f'{p[0]} {p[1]} {p[2]} {p[3]}\n')
	fo.close()


if __name__ == '__main__':
	toroidal_angle = 6
	major_r = 5.46
	minor_r = 1.9
	# if change maximum circles, change 'go_mgtrc_FFHR...' at the same time.
	circles = [2560, 128000]
	# step starts from 0.1
	step = 0.01
	main_route = 'C:/cygwin64/home/12164/code/'
	output_file = main_route + 'FFHR-b2_a+0.00.startpoints.dat'
	output_file2 = main_route + 'f_dict.txt'
	output_file3 = main_route + 'boundaries.txt'

	path = main_route + 'data'
	path2 = main_route + 'spac'

	if os.path.exists(path2):
		f_dict = []
		all_points = []
		filename = path2 + f'/FFHR-b2_a+0.00.{toroidal_angle + 1}.plot'
		filename2 = path + '/FFHR-b2_a+0.00.'
		magnetic_axis_r, magnetic_axis_z = readFile2(filename)
		reactor_spec = [major_r, minor_r, magnetic_axis_r, magnetic_axis_z]

		if not os.path.exists(path):
			os.makedirs(path)
			ps = decideBorder([], reactor_spec, toroidal_angle)
			# ps is in format: ['loaction', x, y, z, circle]
		else:
			with open(output_file2) as file_object:
				f_dict = file_object.readlines()
				f_dict = [f.strip() for f in f_dict]
			p_list = readFile(path, filename2, f_dict, toroidal_angle)
			ps = decideBorder(p_list, reactor_spec, toroidal_angle, circles)
			# ps is in format: ['loaction', x, y, z, circle]
			os.remove(output_file2)

		print(f'the precision now is {10 * step}.')
		print('the boundary is as follows:')
		print('location | x | y | z')
		for b in ps:
			print(f'{b[0]} {b[1]} {b[2]} {b[3]}')
		generateFile3(ps, output_file3)

		f_dict2 = []
		for i in range(int(len(ps) / 2)):
			start_p = ps[2 * i][1:4]
			end_p = ps[2 * i + 1][1:4]
			label = ps[2 * i][0]
			points = generatePoints(start_p, end_p, step)
			if len(points) > 20 and f_dict != []:
				points = points[:10] + points[-10:]
			f_dict2 += len(points) * [label]
			all_points += points
		drawStartPoints(all_points)
		generateFile(all_points, output_file)
		generateFile2(f_dict2, output_file2)

		new_step = round(0.1 * step, 5)
		print('file has been made. ' + 
			  f'change the step to {new_step}.')
		# if os.path.exists(path):
		# 	shutil.rmtree(path)
		# else:
		# 	raise Exception('file doesn\'t exist.')
	else:
		os.makedirs(path)
		generateFile([[1, 1, 1],], output_file)
		print('first tracing for finding magnetic axis.\n'+
			  'after running tracing program, '+
			  'please change folder \'data\' to \'spac\'.')