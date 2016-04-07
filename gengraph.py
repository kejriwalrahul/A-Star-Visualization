import sys

def point(i,j):
	return str(i)+","+str(j)

out = open(sys.argv[1],"w")

for i in range(int(sys.argv[2])):
	for j in range(int(sys.argv[2])):
		if i+1<int(sys.argv[2]):
			out.write(point(i,j) + " " + point(i+1,j)+" 2\n")
			# if j+1<int(sys.argv[2]):
			# 	out.write(point(i,j) + " " + point(i+1,j+1)+" 2\n")
		if j+1<int(sys.argv[2]):
			out.write(point(i,j) + " " + point(i,j+1)+" 2\n")
			# if i-1>=0:
			# 	out.write(point(i,j) + " " + point(i-1,j+1)+" 2\n")
