l=[]
a=set()
count = 0
try:
    N = int(input('Enter a positive integer: '))
except ValueError:
    print('You must enter a positive integer!')
    N = int(input('Enter a positive integer: '))
for i in range(N):
    l.append(i)
for n in l:
    def isPrime(n):
        if n == 1:
            return
        m = 2
        while m * m <= n:
            if n % m == 0:
                return
            m += 1
        return n
    a.add(isPrime(n))
a.discard(None)
print(f"The prime numbers smaller than {N} include: ")
for s in a:
    if count % 9 == 0:
        print('\n')
    else:
        print(s,end=' ')
    count += 1


