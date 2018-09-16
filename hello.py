print("hello world!")

def test(a):
	a = a*3

def test1(b):
	b['b'] = b['b']*3

a = 3
test(a)
print(a)

b = {'b': 3}
test1(b)
print(b['b'])