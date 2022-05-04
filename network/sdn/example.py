#!/usr/bin/python
import time;                                                                            
                                                                                             
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost, Host, Node
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.node import OVSKernelSwitch 
from mininet.node import Controller, RemoteController, OVSController

class Topology( Topo ):
  " SDN."

  def __init__( self ):
    "My SDN topo."

    # Ini topo
    Topo.__init__( self )


    # host y switch
    h1 = self.addHost( 'h1' )
    h2 = self.addHost( 'h2' )
    h3 = self.addHost( 'h3' )
    h4 = self.addHost( 'h4' )
    h5 = self.addHost( 'h5' )
    s1 = self.addSwitch( 's1', cls=OVSKernelSwitch )
    s2 = self.addSwitch( 's2', cls=OVSKernelSwitch )
    s3 = self.addSwitch( 's3', cls=OVSKernelSwitch )
    s4 = self.addSwitch( 's4', cls=OVSKernelSwitch )
    s5 = self.addSwitch( 's5', cls=OVSKernelSwitch )

    # links
    self.addLink( h1, s1 )
    self.addLink( h2, s2 )
    self.addLink( h3, s3 )
    self.addLink( h4, s4 )
    self.addLink( h5, s5 )
    self.addLink( s1, s2 )
    self.addLink( s2, s3 )
    self.addLink( s2, s4 )
    self.addLink( s3, s4 )
    self.addLink( s4, s5 )
    

def create_network():
  "Creates SDN network."

  network = Mininet( 
    topo=Topology(),
    controller=RemoteController('c1', ip='172.16.238.12:6633' ),
  )

  # info('Dumping host connections')
	# dumpNodeConnections(network.hosts)
	# info('Dumping switch connections')
	# dumpNodeConnections(network.switches)

  network.start()
  # time.sleep(10)
  # network.pingAll();
  CLI(network);
  

  # network.iperf(
  #   hosts=(network.hosts[0], network.hosts[1] )
  # )

  # for i in range(10):
  #   for j in range(10):
  #       network.iperf(
  #         hosts=(network.hosts[i], network.hosts[j] )
  #       )
  
  # network.stop()

if __name__ == '__main__':
  setLogLevel( 'info' )  # for CLI output
  create_network()