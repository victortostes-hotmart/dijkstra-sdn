from time import sleep;
from mininet.util import quietRun;

def round_robin(l, n=2):
  lists = [[] for _ in range(n)];
  i = 0;
  for elem in l:
    lists[i].append(elem);
    i = (i + 1) % n;
  return lists;

def build_commands(servers, clients, protocol, timeInSecs, bw):
  clientCommands = [];
  serverCommands = [];
  
  for client, server in zip(clients, servers[::-1]):
    if protocol is 'UDP':
      serverCommands.append((server, 'iperf -s -u -i 1 > %s_%s.txt' % (protocol, client.name)))
      clientCommands.append((client, 'iperf -c %s -t %d -i 1 -u -b %sM' % (server.IP(), timeInSecs, bw)))
    elif protocol is 'TCP':
      serverCommands.append((server, 'iperf -s -i 1 > %s_%s.txt' % (protocol, client.name)))
      clientCommands.append((client, 'iperf -c %s -t %d -i 1 -b %sM' % (server.IP(), timeInSecs, bw)))

  return serverCommands, clientCommands;

def start_test(network, serverCommands, clientCommands, timeInSecs):
  print("Starting Servers");
  pids = [];
  for host, command in serverCommands:
    pid = host.popen(command, shell=True );
    pids.append(pid);

  print("Starting Clients");
  for host, command in clientCommands:
    host.popen(command, shell=True );
    pids.append(pid);

  print("Waiting...");

  sleep(timeInSecs);

  for pid in pids:
    pid.kill();

  print("Done..");


def pairs_test(network=None, protocol='TCP', timeInSecs=15, bw=1):
  quietRun('pkill -9 iperf');

  clients, servers = round_robin(network.hosts);

  serverCommands, clientCommands = build_commands(servers, clients[::-1], protocol, timeInSecs, bw);
  start_test(network, serverCommands, clientCommands, timeInSecs);
  


# def test(network):
#   quietRun('pkill -9 iperf');

#   clients, servers = round_robin(network.hosts);

#   print("Starting Servers");

#   for host in servers:
#     host.popen('iperf -s -u -i 1 > iperf_%s.txt' % (host.name), shell=True );

#   print("Starting Clients");

#   for client in clients:
#     for server in servers:
#       # cmd = 'iperf -c %s -t %d -i 1 -u -b %sM > iperf_%s_%s.txt' % (server.IP(), seconds, bw, client.name, server.name)
#       cmd = 'iperf -c %s -t %d -i 1 -u -b %sM' % (server.IP(), seconds, bw)
#       client.popen(cmd, shell=True );

#   print("Waiting...");

#   for host in network.hosts:
#     host.monitor();

#   print("Done..");
