import os;
from time import sleep;
from mininet.util import quietRun;

def round_robin(l, n=2):
  lists = [[] for _ in range(n)];
  i = 0;
  for elem in l:
    lists[i].append(elem);
    i = (i + 1) % n;
  return lists;

def prepare_test(folder):
  if not os.path.exists(folder):
    os.makedirs(folder)
  
  quietRun('pkill -9 iperf');

def build_server_command(server, protocol, folder):
  if protocol is 'UDP':
    return 'iperf -s -e -u -i 1 > %s/%s_%s.txt' % (folder, protocol, server.name);
  
  elif protocol is 'TCP':
    return 'iperf -s -i 1 > %s/%s_%s.txt' % (folder, protocol, server.name);

def build_client_command(server, protocol, bw, timeInSecs, folder):
  if protocol is 'UDP':
    return 'iperf -c %s -t %d -i 1 -e -u -b %sM' % (server.IP(), timeInSecs, bw);
  
  elif protocol is 'TCP':
    return 'iperf -c %s -t %d -i 1 -b %sM' % (server.IP(), timeInSecs, bw);
  

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

  sleep(timeInSecs + 5);

  for pid in pids:
    pid.kill();

  quietRun('pkill -9 iperf');
  print("Done..");


def pairs_test(network=None, protocol='TCP', timeInSecs=15, bw=1, folder=None):
  prepare_test(folder);
  
  clients, servers = round_robin(network.hosts);

  clientCommands = [];
  serverCommands = [];
  for client, server in zip(clients[::-1], servers):
    clientCommands.append((client, build_client_command(server, protocol, bw, timeInSecs, folder)));
    serverCommands.append((server, build_server_command(server, protocol, folder)));
  
  start_test(network, serverCommands, clientCommands, timeInSecs);


def full_test(network=None, protocol='TCP', timeInSecs=15, bw=1, folder=None):
  prepare_test(folder);

  clientCommands = [];
  serverCommands = [];
  for server in network.hosts:
    serverCommands.append((server, build_server_command(server, protocol, folder)));
    for client in network.hosts:
      if client != server:
        clientCommands.append((client, build_client_command(server, protocol, bw, timeInSecs, folder)));
  
  start_test(network, serverCommands, clientCommands, timeInSecs);
