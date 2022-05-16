#!/usr/bin/python
import sys;
import os;
import time;

from mininet.topo import Topo;
from mininet.net import Mininet;
from mininet.cli import CLI;
from mininet.log import setLogLevel;
from mininet.node import OVSKernelSwitch;
from mininet.node import RemoteController;
from mininet.link import TCLink;

sys.path.append(os.path.abspath("./network/commom/"));
import performance;

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

    # Switches
    s1 = self.addSwitch('s1', cls=OVSKernelSwitch);
    s2 = self.addSwitch('s2', cls=OVSKernelSwitch);
    s3 = self.addSwitch('s3', cls=OVSKernelSwitch);

    # links
    self.addLink( h1, s1, bw=10, delay='5ms' )
    self.addLink( h2, s2, bw=10, delay='5ms' )
    self.addLink( h3, s3, bw=10, delay='5ms' )
    self.addLink( s1, s2, bw=10, delay='5ms' )
    self.addLink( s2, s3, bw=10, delay='5ms' )
    self.addLink( s3, s1, bw=10, delay='5ms' )
    

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
  # network.pingFull();
  network.pingFull();
  # performance.full_test(network=network, protocol='TCP', timeInSecs=30, bw=1, folder='network/triangular/results/SDN');
  performance.full_test(network=network, protocol='UDP', timeInSecs=30, bw=0.1, folder='network/triangular/results/SDN');

  network.stop();
  

if __name__ == '__main__':
  setLogLevel( 'info' )  # for CLI output
  create_network()
