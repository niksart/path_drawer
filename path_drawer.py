from math import floor


# given list_tuples as a parameter, this function skims double coordinates (putting them in a set) AND split them
# in two different coordinates
# list_tuples is a list of tuples like this: ((w-1, w), h).
# Semantically a tuple expresses two coordinates: (w-1, h) e (w, h)
def _get_set_coordinates(list_tuples):
	s = set()
	for ((x1, x2), y) in list_tuples:
		s.add((x1, y))
		s.add((x2, y))

	return s


# get y in order to complete ((x-1,x),y)
def _get_y(x):
	if floor(x) == int(x):  # if number is not a decimal number I return it
		return floor(x)
	else:                        # else return it rounded (excess)
		return floor(x) + 1


# auxiliary function (numpy inverts x with y)
def _set_x_y(matrix, coordinates, n):
	(x, y) = coordinates
	matrix[y][x] = n


# point a is a=(0,0) : implicit parameter
# point b is b=(x, y): the only parameter
def _get_diagonal_coordinates(b):
	(width, height) = b
	
	# list_tuples è una lista di tuple ((w-1, w), h). Semanticamente esprime due coordinate: (w-1, h) e (w, h)
	list_tuples = [((w - 1, w), _get_y(height / width * w)) for w in range(1, width+1)]

	# set_coordinates è l'insieme delle coordinate della diagonale
	set_coordinates = _get_set_coordinates(list_tuples)
	set_coordinates.add((0, 0))  # aggiungo la coordinata iniziale

	set_coordinates.add((width-1, height-1))

	return set_coordinates


# with segment I mean or horizontal or vertical segment
def _segment(p1, p2):
	(x1, y1) = p1
	(x2, y2) = p2

	coordinates_set = set()
	if x1 == x2 and y1 == y2:
		coordinates_set.add((x1, y1))
	elif x1 == x2:
		for y in range(y1, y2 + 1):
			coordinates_set.add((x1, y))
	elif y1 == y2:
		for x in range(x1, x2 + 1):
			coordinates_set.add((x, y1))

	return coordinates_set


def _symmetrize(coordinates_set, dimensions):
	(width, height) = dimensions
	new_coordinates_set = set()
	if width % 2 == 0:
		# axe of symmetry between width/2-1 and width/2
		asse = int(width/2)
		for (x, y) in coordinates_set:
			if x < asse:
				d = asse - x
				new_x = asse + d - 1
				new_coordinates_set.add((new_x, y))
			else:
				d = x - asse + 1
				new_x = asse - d
				new_coordinates_set.add((new_x, y))
	else:
		# axe of symmetry is floor(width/2)
		asse = floor(width/2)
		for (x, y) in coordinates_set:
			if x == asse:
				new_coordinates_set.add((x, y))
			elif x < asse:
				d = asse - x
				new_x = asse + d
				new_coordinates_set.add((new_x, y))
			else:
				d = x - asse
				new_x = asse - d
				new_coordinates_set.add((new_x, y))

	return new_coordinates_set


def _check_for_swap(p1, p2):
	(x1, y1) = p1
	(x2, y2) = p2
	# particular cases for swapping
	if (x1 > x2 and y1 > y2) or (x1 < x2 and y1 > y2) or (x1 > x2 and y1 == y2) or (x1 == x2 and y1 > y2):
		return (x2, y2), (x1, y1)
	else:
		return p1, p2


def _get_coordinates_set(p1, p2, offset):
	(x1, y1) = p1
	(x2, y2) = p2
	(offset_x, offset_y) = offset

	if x1 == x2 or y1 == y2:
		return _segment((x1 - offset_x, y1 - offset_y), (x2 - offset_x, y2 - offset_y))
	elif x1 > x2 and y1 < y2:  # the same case of below (else branch) but I have to _symmetrize the coordinates
		offset_x = x2
		offset_y = y1
		target = (x1 - offset_x, y2 - offset_y)
		width = x1 - offset_x + 1
		height = y2 - offset_y + 1
		return _symmetrize(_get_diagonal_coordinates(target), (width, height))  # axe of symmetry: x = width/2
	else:
		return _get_diagonal_coordinates((x2 - offset_x, y2 - offset_y))


# funzione che data la matrice e due punti da unire modifica la matrice unendo i punti p1 e p2
def draw_path(matrix, p1, p2):
	rotate = False  # shall I rotate 90 deg anticlockwise the coordinates?
	(x1, y1) = p1
	(x2, y2) = p2

	width = max(x1, x2) + 1
	height = max(y1, y2) + 1

	offset_x = min(x1, x2)
	offset_y = min(y1, y2)

	# swap between point in particular cases
	(x1, y1), (x2, y2) = _check_for_swap((x1, y1), (x2, y2))

	# compute the result rotating by 90 deg anticlockwise the coordinates
	if (height - offset_y)/(width - offset_x) > 1 and x1 != x2 and y1 != y2:
		rotate = True
		width, height = height, width
		offset_x, offset_y = offset_y, offset_x
		x1, y1 = y1, x1  # have to flip x with y because of the rotation of the matrix
		x2, y2 = y2, x2

		(x1, y1), (x2, y2) = _check_for_swap((x1, y1), (x2, y2))  # check again

	coordinates_set = _get_coordinates_set((x1, y1), (x2, y2), (offset_x, offset_y))  # set with coordinates to draw

	for (x, y) in coordinates_set:
		if rotate:  # flip x with y
			_set_x_y(matrix, (y + offset_y, x + offset_x), 1)
		else:
			_set_x_y(matrix, (x + offset_x, y + offset_y), 1)
