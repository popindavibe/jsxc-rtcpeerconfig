## RTCPeerConfig via python and jsxc on SOGo with ephemeral auth via Turn server's API

### Forewords
This project was made to be able to enable video-chat between two end nodes running JSXC within a SOGo v3 Web interface (via WebRTC), covering the case of the dreaded **symmetrical NAT**. 

WebRTC (Web Real-Time Communication) is a collection of communications protocols and application programming interfaces that enable real-time communication over peer-to-peer connections. -- **Wikipedia**

Being peer-to-peer and only browser-dependant (meaning no other software required) makes it incredibly attractive, and after bumping my head for a while and calling for help, I realized that the peer-to-peer communication is **not always possible** if you are within a LAN using **symmetrical NAT** (as it does not say : a router with symmetrical NAT maintains its NAT table in such a way that ports used to connect outside are not the one the client asked for, making it impossible for the other node to enable a direct peer connection).

Thankfully, **ICE protocol** and coturn's TURN/STUN server came to the rescue. A **TURN** server is what it says : Traversal Using Relays around NAT. It is the only way to manage WebRTC connection through the NAT. The TURN server is in charge of relaying each and every packets between the two nodes (goodbye peer-to-peer and hello overhead on TURN server).
So, it's not perfect, but can be the only way (if any) depending of you local network.

See the [Wiki](https://gitlab.nomagic.fr/popi/jsxc-rtcpeerconfig/wikis/home]) section for howto install and deploy the scripts and requirements associated on your SOGo server.
