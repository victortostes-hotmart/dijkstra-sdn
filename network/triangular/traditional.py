#!/usr/bin/python
import sys;
import os;

from mininet.topo import Topo;
from mininet.net import Mininet;
from mininet.node import OVSBridge;
from mininet.cli import CLI;
from mininet.log import setLogLevel;
from mininet.link import TCLink;

sys.path.append(os.path.abspath("./network/commom/"));
import performance;

class Topology( Topo ):
  "Traditional."

  def __init__( self ):
    "Mytopo"

    # Ini topo
    Topo.__init__( self )

    # Hosts
    h1 = self.addHost('h1');
    h2 = self.addHost('h2');
    h3 = self.addHost('h3');

    # Switches
    s1 = self.addSwitch('s1', cls=OVSBridge, stp=1);
    s2 = self.addSwitch('s2', cls=OVSBridge, stp=1);
    s3 = self.addSwitch('s3', cls=OVSBridge, stp=1);

    # Links
    self.addLink(h1, s1, bw=10, delay='5ms');
    self.addLink(h2, s2, bw=10, delay='5ms');
    self.addLink(h3, s3, bw=10, delay='5ms');
    
    self.addLink(s1, s2, bw=10, delay='5ms');
    self.addLink(s2, s3, bw=10, delay='5ms');
    self.addLink(s3, s1, bw=10, delay='5ms');


def create_network():
  "Creates traditional network."

  network = Mininet( 
    topo=Topology(),
    switch=OVSBridge,
    link=TCLink
  )

  network.start();
  network.waitConnected();
  performance.full_test(network=network, protocol='TCP', timeInSecs=30, bw=5, folder='network/triangular/results/TRADITIONAL');
  performance.full_test(network=network, protocol='UDP', timeInSecs=30, bw=5, folder='network/triangular/results/TRADITIONAL')

  network.stop();

if __name__ == '__main__':
  setLogLevel('info')  # for CLI output
  create_network()