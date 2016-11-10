## Samuel Rohrer (rohrer) and Ian Lin
#  October 30, 2016
#  read in LIDAR data and convert to nice struct
import os
from collections import namedtuple
import math

# kinda like a c++ struct, just a simple tuple
Scan = namedtuple("Scan", "x y r z")
Segment = namedtuple("Segment", "startIdx endIdx")

# constants
lidarDir = './ISRtest_frames'
frameDir = './ISRtest_LIDARlog'


class Scans():

    def __init__(self):
        # array of 4 arrays of Scan objects
        self.laser = [[], [], [], []]
        # array of 4 arrays of Segment objects
        self.segments = [[], [], [], []]

    def readLidarData(self, filename):
        for filename in os.listdir(lidarDir):
            with open(filename) as f:
    			None

# example: the z value for the 10th scan from laser 2 is
scans = Scans()
# index from 0
#scans.laser[1][9].z
# example: create a segment representing the first 6
# points of laser 4 and add into class
seg = Segment(0, 5)
scans.segments[3].append(seg)


def findCos3dPoint(x, xp1):
	mag_x = sqrt(x.x**2 + x.y**2 + x.z**2)
	mag_xp1 = sqrt(xp1.x**2 + xp1.y**2 + xp1.z**2)
	dot = x.x * xp1.x + x.y * xp1.y + x.z * xp1.z
	return dot / (mag_x * mag_xp1)


# start making segmentation data
# iterate over the laser
for i in range(0, 4):
	# iterate over length of laser scan
	last_new_seg_idx = 0
	for j in range(1, len(scans.laser[i])):
		cos_alpha = findCos3dPoint(scans.laser[i][j], scans.laser[i][j + 1])
		r = scans.laser[i][j].r
		rp1 = scans.laser[i][j + 1].r
		dist = sqrt(r**2 + rp1**2 - 2 * r * rp * cos_alpha)
		c0 = 0
		c1 = sqrt(2 * (1 - cos_alpha))
		dist_thd = c0 + c1 * min(r, rp1)
		# check if its a new segment
		if (dist > dist_thd):
			seg = Segment(last_new_seg_idx, j)
			scans.segments[i].append(seg)
			last_new_seg_idx = j

# write each segment to a new file
# iterate over each laser
for l in range(0, 4):
	for i in range(0, len(scans.segments[l])):
		# TODO: figure out how to write to many different files
		file = open('segmentData/laser#%i_segment#%i.txt' % (l, i), 'w')
		# go through segments and print coordinates
		lenSegment = scans.segments[l][i].endIdx - scans.segments[l][i].startIdx
		# print x
		for x in range(0, lenSegment):
			val = scans.laser[l][x].x
			file.write(str(val) + " ")
		file.write("\n")
		# print y
		for y in range(0, lenSegment):
			val = scans.laser[l][y].y
			file.write(str(val) + " ")
		file.write("\n")
		# print z
		for z in range(0, lenSegment):
			val = scans.laser[l][z].z
			file.write(str(val) + " ")
		file.write("\n")
		file.close()
