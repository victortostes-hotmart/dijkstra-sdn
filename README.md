# Dijkstra - Shortest Path on SDN Network (POX Controller) :postbox:

An SDN forwarding packets strategy based on Dijkstra algorithm to find shortest path on network topology using [POX](https://github.com/noxrepo/pox) controller. 

---

<p align="center">
  <a href="#setup">Setup</a>&nbsp;&nbsp;
  <a href="#running">Running</a>&nbsp;&nbsp;
  <a href="#benchmarking">Benchmarking</a>&nbsp;&nbsp;
</p>

---

## Setup

After clone this repository, start [Docker](https://www.docker.com/) services with [Docker Compose](https://docs.docker.com/compose/):

```ssh
docker-compose up -d
```

Check out container logs with:

```ssh
docker-compose logs -f --tail=200 mininet sdn-controller
```

## Running

Create your [Mininet](http://mininet.org) topology file on [`/network`](https://github.com/victortostes-hotmart/dijkstra-sdn/tree/main/network) folder;

Controller service interface will be exposed on address `172.16.238.12:6633`, make sure your network points to the correct address.

Enter on [Mininet](http://mininet.org) container with:

```ssh
docker-compose exec mininet bash
```

Then, run your tests with:

```ssh
mn -c && python network/PATH_TO_YOUR_TOPOLOGY_FILE.py
```

Here is some examples:

```ssh
# Triangular topology (Without controller)
mn -c && python network/triangular/traditional.py

# Triangular topology
mn -c && python network/triangular/sdn.py

# Custom topology with loops (Without controller)
mn -c && python network/custom/traditional.py

# Custom topology with loops
mn -c && python network/custom/sdn.py
```

## Benchmarking

Comparing built controller with traditional Ethernet network packet forwarding strategy using STP protocol.

To be defined.

```ssh
# Custom topology with loops
./network/database_generator.sh network/custom/results/TRADITIONAL 10

./network/database_generator.sh network/custom/results/SDN 10
```

<sub>
Authored by Victor Tostes - UFMG
</sub>
