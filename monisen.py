import time
def prime(num):
	if num <= 1:
		return False
	for i in range(2, int(num**0.5) + 1):
		if num % i == 0:
			return False
	return True

def monisen(no):
	ms = []
	x = 2
	while len(ms) <= no:
		m = 2**x - 1
		if prime(m) and prime(x):
			ms.append(m)
		x += 1
	return ms[no-1]

def foo(num,base):
    if(num >= base):
        foo(num//base , base)
    print (num%base, end= ' ')

def f(x):
	p = 1
	for i in range(1,101):
		p += x**i/i
	return p

def printStar(num,c):
	n = -1
	a = -1
	left = 0
	while n < num:
		left = num - n
		a += 2
		n += 2*a
	a -= 2
	t = (a - 1)//2
	for i in range(a):
		for j in range(t-abs(i-t)):
			print(' ',end='')
		for k in range(abs(i-t)*2+1):
			print(c,end='')
		print()
	print(left)



if __name__ == '__main__':

	printStar(0,'*')