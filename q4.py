try:
    N = int(input('Enter a number:'))
except ValueError:
    print('Error')
a=1
while N <= 0:
    print('The integer should be positive!')
    N = int(input('Enter a number:'))
if N > 0:
    print('m', 'm+1', 'm**(m+1)')
    for i in range(N):
        a=i+1
        b=a+1
        c=a**(a+1)
        print(a,'','',b,'','','',c)


