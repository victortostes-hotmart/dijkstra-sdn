# #!/bin/bash

# # cp ../app/custom/* ./ext

# ./pox.py dijkstra openflow.discovery openflow.spanning_tree
./pox.py dijkstra openflow.discovery --eat-early-packets openflow.spanning_tree --no-flood --hold-down