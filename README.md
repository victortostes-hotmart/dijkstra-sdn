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

After clone this repository, start services with [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/):


```ssh
docker-compose up -d
```

Check out logs container logs with:

```ssh
docker-compose logs -f --tail=200 mininet sdn-controller
```

## Running

The controller interface will be exposed on address `172.16.238.12:6633`, make sure your [Mininet](https://mininet.org) network points to the correct address.

Enter on [Mininet](https://mininet.org) container with:

```ssh
docker-compose exec mininet bash
```

Once you're inside, run your tests with:

```ssh
mn -c && python network/YOUR_TOPOLOGY_FILE.py
```

Here is some examples:

```ssh
# Triangular topology (Without controller)
mn -c && python network/traditional/triangular.py

# Custom topology with loops (Without controller)
mn -c && python network/traditional/custom.py

# Triangular topology
mn -c && python network/sdn/triangular.py

# Custom topology with loops
mn -c && python network/sdn/custom.py
```

## Benchmarking

Comparing built controller with traditional Ethernet network packet forwarding strategy using STP protocol.

To be defined.


<sub>
Authored by Victor Tostes - UFMG
</sub>
