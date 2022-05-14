#!/usr/bin/python
import time;

from mininet.topo import Topo;
from mininet.net import Mininet;
from mininet.cli import CLI;
from mininet.log import setLogLevel;
from mininet.node import OVSKernelSwitch;
from mininet.node import RemoteController;
from mininet.link import TCLink;

class Topology( Topo ):
  " SDN."

  def __init__( self ):
    "My SDN topo."

    # Ini topo
    Topo.__init__( self )


    # Hosts
    h1 = self.addHost('h1');
    h2 = self.addHost('h2');
    h3 = self.addHost('h3');
    h4 = self.addHost('h4');

    # Switches
    s1 = self.addSwitch('s1', cls=OVSKernelSwitch);
    s2 = self.addSwitch('s2', cls=OVSKernelSwitch);
    s3 = self.addSwitch('s3', cls=OVSKernelSwitch);
    s4 = self.addSwitch('s4', cls=OVSKernelSwitch);

    # Links Host-Switch
    self.addLink(h1, s1, bw=10, delay='5ms');
    self.addLink(h2, s2, bw=10, delay='5ms');
    self.addLink(h3, s3, bw=10, delay='5ms');
    self.addLink(h4, s4, bw=10, delay='5ms');

    # Links Switch-Switch
    self.addLink(s1, s2, bw=10, delay='5ms');
    self.addLink(s2, s3, bw=10, delay='5ms');
    self.addLink(s3, s4, bw=10, delay='5ms');
    self.addLink(s4, s1, bw=10, delay='5ms');
    

def create_network():
  "Creates SDN network."

  network = Mininet( 
    topo=Topology(),
    link=TCLink,
    controller=RemoteController('c1', ip='172.16.238.12:6633' ),
  )

  network.start();
  time.sleep(30);
  # network.waitConnected();
  network.pingFull();
  network.pingFull();
  CLI(network);
  network.stop();
  

if __name__ == '__main__':
  setLogLevel( 'info' )  # for CLI output
  create_network()
