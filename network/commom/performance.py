from time import sleep;
from mininet.util import quietRun;

def round_robin(l, n=2):
  lists = [[] for _ in range(n)];
  i = 0;
  for elem in l:
    lists[i].append(elem);
    i = (i + 1) % n;
  return lists;

seconds = 15;
bw = 1;

def pairs_test(network):
  quietRun('pkill -9 iperf');

  clients, servers = round_robin(network.hosts);

  clientCommands = [];
  serverCommands = [];
  
  for client, server in zip(clients[:-1], servers[1:]):
    serverCommands.append((server, 'iperf -s -u -i 1 > iperf_%s.txt' % (client.name)))
    clientCommands.append((client, 'iperf -c %s -t %d -i 1 -u -b %sM' % (server.IP(), seconds, bw)))

  print("Starting Servers");
  for host, command in serverCommands:
    host.popen(command, shell=True );

  print("Starting Clients");
  for host, command in clientCommands:
    host.popen(command, shell=True );

  print("Waiting...");

  for host in network.hosts:
    host.monitor();

  print("Done..");

  

def test(network):
  quietRun('pkill -9 iperf');

  clients, servers = round_robin(network.hosts);

  print("Starting Servers");

  for host in servers:
    host.popen('iperf -s -u -i 1 > iperf_%s.txt' % (host.name), shell=True );

  print("Starting Clients");

  for client in clients:
    for server in servers:
      # cmd = 'iperf -c %s -t %d -i 1 -u -b %sM > iperf_%s_%s.txt' % (server.IP(), seconds, bw, client.name, server.name)
      cmd = 'iperf -c %s -t %d -i 1 -u -b %sM' % (server.IP(), seconds, bw)
      client.popen(cmd, shell=True );

  print("Waiting...");

  for host in network.hosts:
    host.monitor();

  print("Done..");
