from time import sleep, time
from functools import wraps

# some functions
def a_func():
	sleep(.5)
	
def b_func():
	sleep(.5)

def some(func):
	t = time()
	func()
	print(func.__name__, 'run:', time() - t)

'''

>>> some(a_func)

a_func run: 0.5

>>> some(b_func)

b_func run: 0.5

'''

# try to avoid code repeating and calculations
def c_func(sleep_time=0.3):
	sleep(sleep_time)

def some(func, *args, **kwargs):
	t = time()
	func(*args, **kwargs)
	print(func.__name__, 'run:', time() - t)

'''

>>> some(c_func, sleep_time=0.2)

c_func run: 0.20000004768371582

>>> some(c_func, 0.1)

c_func run: 0.10000014305114746

'''

# decoration point
def d_func(sleep_time=0.1):
	sleep(sleep_time)

def some(func):
	def wrapper(*args, **kwargs):
		t = time()
		func(*args, **kwargs)
		print(func.__name__, 'run:', time() - t)
	return wrapper

d_func = some(d_func)

'''

>>> d_func(0.5)

d_func run: 0.5000500679016113

>>> d_func(sleep_time=0.3)

d_func run: 0.300029993057251

>>> print(d_func.__name__)

wrapper

'''

# original function name and docstring protection with functools @wraps
def some(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		t = time()
		func(*args, **kwargs)
		print(func.__name__, 'run:', time() - t)
	return wrapper
    
@some
def e_func(sleep_time=0.5):
	""" It is e_func """
	sleep(sleep_time)

'''

>>> e_func(sleep_time=0.1)

e_func run: 0.10000991821289062

>>> print(e_func.__name__, ':', e_func.__doc__)

e_func :  It is e_func

'''

# two decorators
def some(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		t = time()
		result = func(*args, **kwargs)
		print(func.__name__, 'run:', time() - t)
		return result
	return wrapper

def some_result(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		result = func(*args, **kwargs)
		if result > 50:
			print('Incorrect result ( >50 ): {0}'.format(result))
		return result
	return wrapper

@some
@some_result
def calc(x):
	return x ** 2

'''

>>> calc(5)

calc run: 0.0

25

>>> calc(8)

Incorrect result ( >50 ): 64

calc run: 0.044004201889038086

64

'''

# decorator that takes arguments
def some_result(limit):
	def dec(func):
		@wraps(func)
		def wrapper(*args, **kwargs):
			result = func(*args, **kwargs)
			if result > limit:
				print('Incorrect result ( > {0} ): {1}'.format(limit, result))
			return result
		return wrapper
	return dec

@some_result(75)
def a_calc(x):
	return x ** 3

@some_result(60)
def b_calc(x):
	return x ** 3

'''

>>> a_calc(4)

64

>>> a_calc(6)

Incorrect result ( > 75 ): 216

216

>>> b_calc(4)

Incorrect result ( > 60 ): 64

64

>>> b_calc(3)

27

'''
