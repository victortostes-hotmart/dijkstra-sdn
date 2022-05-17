#!/usr/bin/python
import sys;
import os;

from mininet.topo import Topo;
from mininet.net import Mininet;
from mininet.cli import CLI;
from mininet.log import setLogLevel;
from mininet.node import OVSBridge;
from mininet.link import TCLink;

sys.path.append(os.path.abspath("./network/commom/"));
import performance;

class Topology( Topo ):
  "Traditional."

  def __init__( self ):
    "My Traditional Topo"

    # Ini topo
    Topo.__init__( self );

    # Hosts
    h1 = self.addHost('h1');
    h2 = self.addHost('h2');
    h3 = self.addHost('h3');
    h4 = self.addHost('h4');
    h5 = self.addHost('h5');
    h6 = self.addHost('h6');
    h7 = self.addHost('h7');
    h8 = self.addHost('h8');
    h9 = self.addHost('h9');
    h10 = self.addHost('h10');

    # Switches
    s1 = self.addSwitch('s1', cls=OVSBridge, stp=1);
    s2 = self.addSwitch('s2', cls=OVSBridge, stp=1);
    s3 = self.addSwitch('s3', cls=OVSBridge, stp=1);
    s4 = self.addSwitch('s4', cls=OVSBridge, stp=1);
    s5 = self.addSwitch('s5', cls=OVSBridge, stp=1);
    s6 = self.addSwitch('s6', cls=OVSBridge, stp=1);
    s7 = self.addSwitch('s7', cls=OVSBridge, stp=1);
    s8 = self.addSwitch('s8', cls=OVSBridge, stp=1);
    s9 = self.addSwitch('s9', cls=OVSBridge, stp=1);
    s10 = self.addSwitch('s10', cls=OVSBridge, stp=1);

    # Links Host-Switch
    self.addLink(h1, s1, bw=10, delay='5ms', loss=1);
    self.addLink(h2, s2, bw=10, delay='5ms', loss=1);
    self.addLink(h3, s3, bw=10, delay='5ms', loss=1);
    self.addLink(h4, s4, bw=10, delay='5ms', loss=1);
    self.addLink(h5, s5, bw=10, delay='5ms', loss=1);
    self.addLink(h6, s6, bw=10, delay='5ms', loss=1);
    self.addLink(h7, s7, bw=10, delay='5ms', loss=1);
    self.addLink(h8, s8, bw=10, delay='5ms', loss=1);
    self.addLink(h9, s9, bw=10, delay='5ms', loss=1);
    self.addLink(h10, s10, bw=10, delay='5ms', loss=1);
    
    # Links Switch-Switch
    self.addLink(s1, s2, bw=10, delay='5ms', loss=1);
    self.addLink(s1, s8, bw=10, delay='5ms', loss=1);
    self.addLink(s1, s10, bw=10, delay='5ms', loss=1);
    self.addLink(s2, s3, bw=10, delay='5ms', loss=1);
    self.addLink(s2, s6, bw=10, delay='5ms', loss=1);
    self.addLink(s2, s7, bw=10, delay='5ms', loss=1);
    self.addLink(s2, s8, bw=10, delay='5ms', loss=1);
    self.addLink(s3, s4, bw=10, delay='5ms', loss=1);
    self.addLink(s3, s6, bw=10, delay='5ms', loss=1);
    self.addLink(s4, s5, bw=10, delay='5ms', loss=1);
    self.addLink(s5, s6, bw=10, delay='5ms', loss=1);
    self.addLink(s6, s7, bw=10, delay='5ms', loss=1);
    self.addLink(s7, s8, bw=10, delay='5ms', loss=1);
    self.addLink(s8, s9, bw=10, delay='5ms', loss=1);
    self.addLink(s9, s10, bw=10, delay='5ms', loss=1);


def create_network():
  "Creates traditional network."

  network = Mininet( 
    topo=Topology(),
    switch=OVSBridge,
    link=TCLink
  )

  network.start();
  network.waitConnected();
  network.pingFull();
  performance.full_test(network=network, protocol='TCP', timeInSecs=30, bw=1, folder='network/custom/results/TRADITIONAL');
  performance.full_test(network=network, protocol='UDP', timeInSecs=30, bw=1, folder='network/custom/results/TRADITIONAL');
  network.stop();
  
if __name__ == '__main__':
  setLogLevel('info')  # for CLI output
  create_network()