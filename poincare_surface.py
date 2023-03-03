import matplotlib.pyplot as plt


# poincare plot: index, point_index, r, t_a(radian), x, y, z, length, br, bz, bt, b, m(circle)
def readFile(filename):
	with open(filename) as file_object:
		lines = file_object.readlines()

	Newlist = [] 
	for line in lines:
		Newlist.append(line.split())

	points = []
	for line in range(len(Newlist)):
		x = float(Newlist[line][2])
		# y = float(Newlist[line][3])
		y = float(Newlist[line][6])
		point = (x, y)
		points.append(point)
	return points


def readFile2(filename2):
	with open(filename2) as file_object:
		lines = file_object.readlines()
	
	newlist = []
	for line in lines:
		line = line.split()
		x = float(line[1])
		y = float(line[2])
		z = float(line[3])

		r = (x**2 + y**2)**0.5
		newlist.append([r, z])

	return newlist


# def poincare_plot_stochastic_area():
# 	filename = 'data/FFHR-d1_R15.6m_B4.7T_R3.50_g1.20_20181105_leg_poincare-72.dat'
# 	allPoints = readFile(filename)
# 	allPoints = [[row[i] for row in allPoints] for i in range(2)]
# 	return allPoints


def findpoints(points):
	points = list(zip(*points))
	top = max(points[1])
	bottom = min(points[1])
	index_top = points[1].index(top)
	index_bottom = points[1].index(bottom)
	top_p = [top, points[0][index_top]]
	bottom_p =[bottom, points[0][index_bottom]]
	return top_p, bottom_p


if __name__ == '__main__':
	i = 6
	# the exist data
	filename = f'data7200/FFHR-b2_a+0.00.{i+1}.plot'
	# filename = 'LCFS1/FFHR-d1_R15.6m_B4.7T_R3.50_g1.20_20181105_LCFS_poincare-00.dat'
	# my tracing data
	# filename = f'C:/cygwin64/home/12164/code/data/FFHR-b2_a+0.00.{i+1}.plot'
	filename2 = 'C:/cygwin64/home/12164/code/boundaries.txt'
	allPoints = readFile(filename)
	newlist = readFile2(filename2)

	# top_p, bottom_p = findpoints(allPoints)
	# print(top_p, bottom_p)

	allPoints = [[row[i] for row in allPoints] for i in range(2)]

	plt.scatter(allPoints[0], allPoints[1], alpha = 0.1, color = 'b', s = 2)
	plt.plot([newlist[0][0], newlist[5][0]],
			 [newlist[0][1], newlist[5][1]],
			 c = 'purple',
			 marker='.',
			 markersize=8)
	plt.plot([newlist[1][0], newlist[4][0]],
			 [newlist[1][1], newlist[4][1]],
			 c = 'blue',
			 marker='.',
			 markersize=8)
	plt.plot([newlist[2][0], newlist[7][0]],
			 [newlist[2][1], newlist[7][1]],
			 c='yellow',
			 marker='.',
			 markersize=8)
	plt.plot([newlist[3][0], newlist[6][0]],
			 [newlist[3][1], newlist[6][1]],
			 c='green',
			 marker='.',
			 markersize=8)

	plt.xlabel('x axis')
	plt.ylabel('y axis')
	plt.title(f'poincare surface at {i} degrees')
	plt.show()