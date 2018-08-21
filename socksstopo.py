
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.topo import Topo
from mininet.link import TCLink


class SOCKSTopo( Topo ):

	def __init__( self ):
		Topo.__init__( self )

		# Add hosts and switches
		clientHost = self.addHost('h1', ip = '10.0.12.1/24')
		proxyHost  = self.addHost('h2', ip = '10.0.12.2/24')
		serverHost = self.addHost('h3', ip = '10.0.23.3/24')

		cpSwitch = self.addSwitch('s1')
		psSwitch = self.addSwitch('s2')

		self.addLink(clientHost, cpSwitch, delay = '100ms')
		self.addLink(proxyHost,  cpSwitch)
		self.addLink(proxyHost,  psSwitch, params1 = { 'ip': '10.0.23.2/24' })
		self.addLink(serverHost, psSwitch, delay = '50ms')
		
	


topos = { 'sockstopo': (lambda: SOCKSTopo()) }
 
if __name__ == '__main__':
	setLogLevel( 'info' )
	net = Mininet(topo=SOCKSTopo(), link=TCLink, controller=None)
	net.start()
	
	client = net.get('h1')
	proxy  = net.get('h2')
	server = net.get('h3')
	
	proxy.cmdPrint('ifconfig h2-eth1 10.0.23.2/24')
	
	client.cmdPrint('ip r a default via 10.0.12.2')
	server.cmdPrint('ip r a default via 10.0.23.2')
	proxy.cmdPrint('sysctl net.ipv4.ip_forward net.ipv4.ip_forward=1')
	
	client.cmdPrint('/home/vlad/sigcomm18demo/proxyme.sh')
	client.cmdPrint('/home/vlad/sixtysocks/sixtysocks -m proxify -l 12345 -U user -P passwd -s 10.0.12.2 -p 1080 -D -V /home/vlad/sigcomm18demo/socks.crt &> /dev/null &')
	
	proxy.cmdPrint('/home/vlad/sixtysocks/sixtysocks -m proxy -t 1080 -U user -P passwd -K /home/vlad/sigcomm18demo/socks.key -C /home/vlad/sigcomm18demo/socks.crt &> /dev/null &')
	
	server.cmdPrint('/usr/sbin/start_apache2')
	
	client.cmdPrint('ovs-ofctl add-flow s1 actions=flood')
	client.cmdPrint('ovs-ofctl add-flow s2 actions=flood')
	
	
	CLI(net)
	
	server.cmdPrint('killall httpd-prefork')
	server.cmdPrint('killall sixtysocks')
	
	net.stop()
