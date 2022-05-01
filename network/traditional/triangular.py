#!/usr/bin/python
import time;                                                                           
                                                                                             
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

    # host and switch
    h1 = self.addHost( 'h1', ip = "127.0.0.2" )
    h2 = self.addHost( 'h2', ip = "127.0.0.3" )
    h3 = self.addHost( 'h3', ip = "127.0.0.4" )
    s1 = self.addSwitch( 's1', stp=True, cls = LinuxBridge )
    s2 = self.addSwitch( 's2', stp=True, cls = LinuxBridge )
    s3 = self.addSwitch( 's3', stp=True, cls = LinuxBridge )

    # Links
    self.addLink( h1, s1 )
    self.addLink( h2, s2 )
    self.addLink( h3, s3 )
    self.addLink( s1, s2 )
    self.addLink( s2, s3 )
    self.addLink( s3, s1 )

# def performance_test(network):
#   hostsNumber = len(network.hosts)
#   for i in range(1, hostsNumber+1):
#     hi = network['h' + str(i)]
#     hi.cmd('/usr/sbin/sshd')


def create_network():
  "Creates traditional network."

  network = Mininet( 
    topo=Topology(),
  )

  # info('Dumping host connections')
	# dumpNodeConnections(network.hosts)
	# info('Dumping switch connections')
	# dumpNodeConnections(network.switches)

  network.start()
  time.sleep(10)
  network.pingFull()
  network.pingFull()

  # performance_test(network)
  # network['h1'].cmd('ping h2')
  # network.monitor()
  # network.iperf(
  #   hosts=(network.hosts[0], network.hosts[1]),
  #   seconds=5
  # )

  # for i in range(3):
  #   for j in range(3):
  #       network.iperf(
  #         hosts=(network.hosts[i -1], network.hosts[j-1] )
  #       )
  
  network.stop()

if __name__ == '__main__':
  setLogLevel('info')  # for CLI output
  create_network()