#!/usr/bin/python                                                                            
                                                                                             
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost, Host, Node
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.nodelib import LinuxBridge

class Topology( Topo ):
  "Traditional."

  def __init__( self ):
    "Mytopo"

    # Ini topo
    Topo.__init__( self )

    # Hosts
    h1 = self.addHost( 'h1', ip = "127.0.0.2" )
    h2 = self.addHost( 'h2', ip = "127.0.0.3" )
    h3 = self.addHost( 'h3', ip = "127.0.0.4" )
    h4 = self.addHost( 'h4', ip = "127.0.0.5" )
    h5 = self.addHost( 'h5', ip = "127.0.0.6" )
    h6 = self.addHost( 'h6', ip = "127.0.0.7" )
    h7 = self.addHost( 'h7', ip = "127.0.0.8" )
    h8 = self.addHost( 'h8', ip = "127.0.0.9" )
    h9 = self.addHost( 'h9', ip = "127.0.0.10" )
    h10 = self.addHost( 'h10', ip = "127.0.0.11" )

    # Switches
    s1 = self.addSwitch( 's1', stp=True, cls = LinuxBridge )
    s2 = self.addSwitch( 's2', stp=True, cls = LinuxBridge )
    s3 = self.addSwitch( 's3', stp=True, cls = LinuxBridge )
    s4 = self.addSwitch( 's4', stp=True, cls = LinuxBridge )
    s5 = self.addSwitch( 's5', stp=True, cls = LinuxBridge )
    s6 = self.addSwitch( 's6', stp=True, cls = LinuxBridge )
    s7 = self.addSwitch( 's7', stp=True, cls = LinuxBridge )
    s8 = self.addSwitch( 's8', stp=True, cls = LinuxBridge )
    s9 = self.addSwitch( 's9', stp=True, cls = LinuxBridge )
    s10 = self.addSwitch( 's10', stp=True, cls = LinuxBridge )

    # Links Host-Switch
    self.addLink( h1, s1 )
    self.addLink( h2, s2 )
    self.addLink( h3, s3 )
    self.addLink( h4, s4 )
    self.addLink( h5, s5 )
    self.addLink( h6, s6 )
    self.addLink( h7, s7 )
    self.addLink( h8, s8 )
    self.addLink( h9, s9 )
    self.addLink( h10, s10 )
    
    # Links Switch-Switch
    self.addLink( s1, s2 )
    self.addLink( s1, s8 )
    self.addLink( s1, s10 )
    self.addLink( s2, s3 )
    self.addLink( s2, s6 )
    self.addLink( s2, s7 )
    self.addLink( s2, s8 )
    self.addLink( s3, s4 )
    self.addLink( s3, s6 )
    self.addLink( s4, s5 )
    self.addLink( s5, s6 )
    self.addLink( s6, s7 )
    self.addLink( s7, s8 )
    self.addLink( s8, s9 )
    self.addLink( s9, s10 )

def create_network():
  "Creates traditional network."

  network = Mininet( 
    topo=Topology(),
  )

  network.start()
  network.pingAll()
  
  network.stop()

if __name__ == '__main__':
  setLogLevel('info')  # for CLI output
  create_network()