from math import sin
from math import cos
from math import tan
a = int(input('Enter the left interval end point:'))
b = int(input('Enter the right interval end point:'))
if b > a:
    n = int(input('Enter the number of sub-intervals:'))
    while n <= 0:
        print('Error, number should be an integer!')
        n = int(input('Enter the number of sub-intervals:'))
    f = input('Choose the function type from cos, sin, and tan:')
    sub_inter = (b - a) / n
    num_int = 0
    for i in range(n):
        if f == 'cos':
            num_int += sub_inter * cos(a + sub_inter * (i - 1 / 2))
        elif f == 'sin':
            num_int += sub_inter * sin(a + sub_inter * (i - 1 / 2))
        elif f == 'tan':
            num_int += sub_inter * tan(a + sub_inter * (i - 1 / 2))
        else:
            print("Error! Choose from sin,cos,tan!")
    print(num_int)
else:
    print('Error, right end must bigger than left!')
    
