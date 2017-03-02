# coding = utf-8
test = '''
4 4 1
1 2 3 4
5 6 7 8
9 0 1 2
3 4 5 6
'''
my_list = [int(num) for num in input().split()]
m = my_list[0]
n = my_list[1]
trans_driection = my_list[2]
temp_list = []
for i in range(m):
	temp_list.append(my_list[3+n*i:3+(i+1)*n])

def trans_matric(matric,trans=0):
	temp = [[0 for i in range(n)] for j in range(m)]
	if trans == 0:
		for i in range(m):
			for j in range(n):
				temp[i][j] = matric[i][-j-1]
	else:
		for i in range(m):
			for j in range(n):
				temp[i][j] = matric[-i-1][j]
	return temp
print(my_list)
print(temp_list)
print(trans_matric(temp_list,trans_driection))