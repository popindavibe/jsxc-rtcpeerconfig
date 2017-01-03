## RTCPeerConfig with ephemeral auth via Turn server's API

### Forewords
This project was made to be able to enable video-chat between two end nodes running JSXC within a SOGo v3 Web interface (via WebRTC), covering the case of the dreaded **symmetrical NAT**. 

WebRTC (Web Real-Time Communication) is a collection of communications protocols and application programming interfaces that enable real-time communication over peer-to-peer connections. -- **Wikipedia**

Being peer-to-peer and only browser-dependant (meaning no other software required) makes it incredibly attractive, and after bumping my head for a while and calling for help, I realized that the peer-to-peer communication is **not always possible** if you are within a LAN using **symmetrical NAT** (as it does not say : a router with symmetrical NAT maintains its NAT table in such a way that ports used to connect outside are not the one the client asked for, making it impossible for the other node to enable a direct peer connection).

Thankfully, **ICE protocol** and coturn's TURN/STUN server came to the rescue. A **TURN** server is what it says : Traversal Using Relays around NAT. It is the only way to manage WebRTC connection through the NAT. The TURN server is in charge of relaying each and every packets between the two nodes (goodbye peer-to-peer and hello overhead on TURN server).
So, it's not perfect, but can be the only way (if any) depending of you local network.

### Why this project
Being a happy user of SOGo, I early on activated Turn configuration with long-term credentials. Problem is: the secret password of my turn user was visible and downloadable from the js script. Not optimal. I learnt that ephemeral credentials was the way to go to solve that issue.
[https://github.com/jsxc/jsxc](JSXC)'s github community helped me understand how to set it up and test it. There is already a PHP script included with jsxc (might not be up-to-date on sjsxc) which enables dynamic creation of ephemeral credentials (timestamp is part of the equation, so it has to be on-demand), **if you have PHP on your server**.
SOGo being objective-C, the server I got it running on has no PHP installed on it. 

This was the perfect opportunity to write a little python script and install uwsgi to be able to call that script through nginx. 
Some extra info :
 * integration of jsxc in SOGo (sjsxc) documentation can be found on jsxc's github Wiki under [https://github.com/jsxc/jsxc/wiki/Install-sjsxc-%28SOGo%29](Install sjsxc (SOGo))
 * a coturn server's configuration example can also be found on jsxc's github Wiki [https://github.com/jsxc/jsxc/wiki/WebRTC-how-to](WebRTC How To)

### How it works
The cgi-bin directory contains all python-related files. Actual python files as well as the config files for uswgi and TURN authentication. Once everything is set up, anything reaching `/cgi-bin/*` will invariably result in a call to the python script wsgi.py, which itself is a callable for `getturncredentials.py`.

In the meantime, might be good to protect your config files from outsiders by adding in your nginx SOGo's configuration file :
```
# Turn credentials / config files
   location ~ "(.*\.inc|.*\.json)$" { deny all; }
```

Now, install uwsgi, clone repository and start uwsgi daemon with provided config file:
```
apt-get install uwsgi uwsgi-core uwsgi-plugin-python

cd /usr/lib/GNUstep/SOGo/WebServerResources/sjsxc/ajax

git clone https://gitlab.nomagic.fr/popi/jsxc-rtcpeerconfig.git .

uwsgi --plugin python --json cgi-bin/sjsxc.json
```
Now you just have to tell Nginx to send everything addressed to `/cgi-bin` to the uwsgi daemon.

At the end of SOGo's vhost, add:
```
   location ~ /cgi-bin 
   { 
      uwsgi_pass unix:/tmp/uwsgi.sock;
      include            uwsgi_params;

      proxy_redirect     off;
      proxy_set_header   Host $host;
      proxy_set_header   X-Real-IP $remote_addr;
      proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header   X-Forwarded-Host $server_name;
   }
```
Here we use a unix socket to connect to **uwsgi**.

Reload nginx:
```
service nginx configtest
service nginx reload
```

Test via curl or browser:
```
curl https://example.com/SOGo/WebServerResources/sjsxc/ajax/cgi-bin/wsgi

{"iceServers": [{"urls": ["stun:stun.example.com", "stun:stun.example2.com"]}, {"username": "1483455638:userWebrtc", "credential": "wOk4VXXXXXXXXXO90=", "urls": ["turn:turn.example.com", "turn:turn.example2.com"]}], "ttl": 86400}
```
note : here the credential is a _hash_, not the **real** shared secret. The hash is generated from the secret and the username, which itself is a gathering of timestamp and username.

Finally, in you sjsxc/js folder on SOGo's server, modify **sjsxc.js** RTCPeedConfig url's setting. 
Go to directory and make a copy:
```
cd /usr/lib/GNUstep/SOGo/WebServerResources/sjsxc/js
cp -p sjsxc.js sjsxc.js.bak
```

Create the patch file sjsxc.patch containing:
```
--- sjsxc.js
+++ sjsxc.js
@@ -174 +174 @@
-            url: '/SOGo.woa/WebServerResources/sjsxc/ajax/getturncredentials.php'
+            url: '/SOGo.woa/WebServerResources/sjsxc/ajax/cgi-bin/wsgi'
```

Apply patch:
```
patch -u < sjsxc.patch
```

### The extra mile
You should now have a symmetrical NAT-proofed visio solution. Here below is the added settings to get our uswgi daemon to start up at boot time.


