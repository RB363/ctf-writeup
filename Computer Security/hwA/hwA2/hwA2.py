from pwn import *
from fractions import Fraction
from Crypto.Util.number import long_to_bytes
import time,sys

def progressbar(it, prefix="", size=60):
    count = len(it)
    def _show(_i):
        x = int(size*_i/count)
        sys.stdout.write("%s[%s%s] %i/%i\r\n" % (prefix, "#"*x, "."*(size-x), _i, count))
        sys.stdout.flush()

    _show(0)
    for i, item in enumerate(it):
        yield item
        _show(i+1)
    sys.stdout.write("\n")
    sys.stdout.flush()

r = remote("csie.ctf.tw",10140)

r.recvuntil("> ")
r.sendline("1")

c = int(r.recvline().split()[-1])
e = int(r.recvline().split()[-1])
n = int(r.recvline().split()[-1])

submap = {}
for i in range(0, 16):
    submap[-n * i % 16] = i

L = Fraction(0, 1)
R = Fraction(1, 1)

# for i in progressbar(range(1024//4 + 1), "Computing: ", 20):
for i in range(1024//4 ):
    r.recvuntil("> ")
    r.sendline("2")

    test = c*pow(16,(i+1)*e,n)
    r.sendline(str(test))
    t = int(r.recvline().split()[-1] )
    k = submap[t]
    # k = 0 if t == 0 else -t%16
    L, R = L + (R - L) * Fraction(k, 16), L + (R - L) * Fraction(k + 1, 16)


m = int(L * n) 
print("m = " + str(hex(m)))
print(long_to_bytes(m))
