## RTCPeerConfig via python and jsxc on SOGo with ephemeral auth via Turn server's API

### Forewords
This project was made to be able to enable video-chat between two end nodes running [JSXC](https://www.jsxc.org/) within a [SOGo v3](https://sogo.nu/) Web interface (using WebRTC). 

WebRTC (Web Real-Time Communication) is a collection of communications protocols and application programming interfaces that enable real-time communication over peer-to-peer connections. -- **Wikipedia**

Being peer-to-peer and only browser-dependant (meaning no other software required) makes it incredibly attractive.
The **ICE protocol** was create as a way to enable listing several methods to successfully try to establish connectivity between two end nodes.

In most of the situation a STUN server will be used first for nodes behind NAT to be able to gather enough info before starting peer-to-peer connection.

The peer-to-peer communication is **not always possible** if you are within a LAN using **symmetrical NAT**. A router with symmetrical NAT activated maintains its NAT table in such a way that ports used to connect outside are not the same number the client node opened asked for, the router randomly opens a different port and keep the mapping in its NAT table, making it impossible for the remote node to enable a direct peer-to-peer connection).

This is where [coturn's TURN/STUN server](https://github.com/coturn/coturn) comes to the rescue.
A **TURN** server is what it says : Traversal Using Relays around NAT. It is the only way to manage WebRTC connection through the NAT. The TURN server is in charge of relaying each and every packets between the two nodes (goodbye peer-to-peer and hello overhead on TURN server).
So, it's not perfect, but can be the only way (if any) depending of you local network.

This little development was made for WebRTC end-nodes to be able to connect from a **symmetrical NAT** activated LAN router.

See the [Wiki](https://gitlab.nomagic.fr/popi/jsxc-rtcpeerconfig/wikis/home) section for howto install and deploy the scripts and requirements associated on your SOGo server.
