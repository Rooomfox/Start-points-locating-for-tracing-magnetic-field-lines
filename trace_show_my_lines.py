import math
import cmath
import numpy as np
import matplotlib.pyplot as plt


# a point "index, point_index, r, t_a(radian), x, y, z, length, br, bz, bt, b"
def readFile(filename):
	with open(filename) as file_object:
		lines = file_object.readlines()

	Newlist = []
	for line in lines:
		Newlist.append(line.split())

	points = []
	for line in range(len(Newlist)):
		n = int(Newlist[line][0])
		p_i = int(Newlist[line][1])
		r = float(Newlist[line][2])
		t_a = float(Newlist[line][3])
		x = float(Newlist[line][4])
		y = float(Newlist[line][5])
		z = float(Newlist[line][6])
		c_l = float(Newlist[line][7])
		b_r = float(Newlist[line][8])
		b_z = float(Newlist[line][9])
		b_t = float(Newlist[line][10])
		b = float(Newlist[line][11])
		point = [x, y, z]
		points.append(point)
	return points


if __name__ == '__main__':
	lines = []
	for i in range(1, 72):
		if i%5 == 0:
			print(f'now processing on file {i}.')
		filename = f'C:/cygwin64/home/12164/code/data/FFHR-b2_a+0.00.{i}.trac'
		points = readFile(filename)
		points2 = list(zip(*points))
		lines.append(points2)
	
	fig = plt.figure()
	ax = fig.add_subplot(projection='3d')

	for i in range(len(lines)):
		ax.plot(lines[i][0], lines[i][1], lines[i][2], alpha=0.5)

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