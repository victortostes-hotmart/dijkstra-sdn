#!/usr/bin/python
import time;
import sys;
import os;                                                                       
                                                                                             
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
    s1 = self.addSwitch('s1', cls=OVSKernelSwitch);
    s2 = self.addSwitch('s2', cls=OVSKernelSwitch);
    s3 = self.addSwitch('s3', cls=OVSKernelSwitch);
    s4 = self.addSwitch('s4', cls=OVSKernelSwitch);
    s5 = self.addSwitch('s5', cls=OVSKernelSwitch);
    s6 = self.addSwitch('s6', cls=OVSKernelSwitch);
    s7 = self.addSwitch('s7', cls=OVSKernelSwitch);
    s8 = self.addSwitch('s8', cls=OVSKernelSwitch);
    s9 = self.addSwitch('s9', cls=OVSKernelSwitch);
    s10 = self.addSwitch('s10', cls=OVSKernelSwitch);

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
    self.addLink(s1, s2, bw=10, delay='15ms', loss=1);
    self.addLink(s1, s8, bw=10, delay='15ms', loss=1);
    self.addLink(s1, s10, bw=10, delay='15ms', loss=1);
    self.addLink(s2, s3, bw=10, delay='15ms', loss=1);
    self.addLink(s2, s6, bw=10, delay='15ms', loss=1);
    self.addLink(s2, s7, bw=10, delay='15ms', loss=1);
    self.addLink(s2, s8, bw=10, delay='15ms', loss=1);
    self.addLink(s3, s4, bw=10, delay='15ms', loss=1);
    self.addLink(s3, s6, bw=10, delay='15ms', loss=1);
    self.addLink(s4, s5, bw=10, delay='15ms', loss=1);
    self.addLink(s5, s6, bw=10, delay='15ms', loss=1);
    self.addLink(s6, s7, bw=10, delay='15ms', loss=1);
    self.addLink(s7, s8, bw=10, delay='15ms', loss=1);
    self.addLink(s8, s9, bw=10, delay='15ms', loss=1);
    self.addLink(s9, s10, bw=10, delay='15ms', loss=1);


def create_network():
  "Creates SDN network."

  network = Mininet( 
    topo=Topology(),
    link=TCLink,
    controller=RemoteController('c1', ip='172.16.238.12:6633' )
  )

  network.start();
  time.sleep(30);
  network.pingFull();
  
  performance.full_test(network=network, protocol='TCP', timeInSecs=200, bw=0.3, folder='network/custom/results/SDN3');
  performance.full_test(network=network, protocol='UDP', timeInSecs=200, bw=0.3, folder='network/custom/results/SDN3');
  network.stop();

if __name__ == '__main__':
  setLogLevel( 'info' )  # for CLI output
  create_network()
