# We use a finite field Z[N] with a suitable root of unity to carry out the FFT

# forward fft using cooley tukey algorithm
def fft(sequence, root, modulo):
    if (len(sequence) == 1):
        return
    even = sequence[::2]
    odd = sequence[1::2]
    r = root * root
    r %= modulo
    fft(even, r, modulo)
    fft(odd, r, modulo)
    r = 1
    m = len(sequence)
    for i in range(m):
        j = i % (m//2)
        sequence[i] = even[j] + odd[j] * r
        r *= root
        sequence[i] %= modulo
        r %= modulo

# inverse fft
def ifft(sequence, root, inverse, modulo):
    m = len(sequence)
    for i in range(1, (m+1)//2):
        sequence[m-i], sequence[i] = sequence[i], sequence[m-i]
    fft(sequence, root, modulo)
    for i in range(m):
        sequence[i] = (sequence[i] * inverse) % modulo

# returns N, r where r has order 2^k modulo N
# N is likely to be prime, but not neccessary.
def find_ring(k):
    # We are looking for N = 2^k * t + 1 and r such that
    # r has order 2^k modulo N, i.e. r^2^(k-1) = -1
    t = 1
    while True:
        N = (t<<k) + 1
        for r in range(2, t+2):
            s = r
            for i in range(k-1):
                s *= s
                s %= N
            if N-s == 1:
                return N, r
        t += 1

# max is the maximum signal
def convolve(x, y, max = 1):
    n = len(x)
    k = len(bin(n))-3
    w = len(bin(max * max))-2
    # find a root or order 2^(k+w)
    modulo, root = find_ring(k+w)
    # root^2^w has order 2^k, which is what we need
    for i in range(w):
        root *= root
        root %= modulo
    inverse = modulo - int((modulo-1)//n)
    fft(x, root, modulo)
    fft(y, root, modulo)
    z = [x[i] * y[i] for i in range(len(x))]
    ifft(z, root, inverse, modulo)
    return z

# x, y are digit arrays (low to high order) in base b
# X = x[0] + x[1]b + x[1]b^2 + ...
def multiply_digits(x, y, b):
    # round up digits to power of 2 with the later half all zeros
    n = 1 << (len(bin(max(len(x),len(y))-1))-1)
    x = x + [0] * (n - len(x))
    y = y + [0] * (n - len(y))
    z = convolve(x, y, b-1)
    # just carry forward to make sure no digit is more than b
    carry = 0
    non_zero = 0
    for i in range(len(z)):
        carry += z[i]
        z[i] = carry % b
        if z[i] != 0:
            non_zero = i
        carry = carry // b
    # carry should be zero here
    # shave off trailing zeros
    return z[:non_zero+1]

def multiply(x, y):
    X = [int(digit) for digit in bin(x)[:1:-1]]
    Y = [int(digit) for digit in bin(y)[:1:-1]]
    Z = multiply_digits(X, Y, 2)
    out = 0
    for bit in reversed(Z):
        out = (out << 1) | bit
    return out
