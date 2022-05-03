from pox.core import core;
import pox.openflow.libopenflow_01 as of;
from pox.openflow.discovery import Discovery;
from pox.lib.revent import *;

from graph import Graph;

# Flow timeouts
FLOW_IDLE_TIMEOUT = 0;
FLOW_HARD_TIMEOUT = 0;

class Switch(EventMixin):
    def __init__(self, manager):
        self.connection = None;
        self.ports = None;
        self.dpid = None;
        self._listeners = None;

    def disconnect(self):
        if self.connection is not None:
            self.connection.removeListeners(self._listeners);
            self.connection = None;
            self._listeners = None;

    def connect(self, connection):
        if self.dpid is None:
            self.dpid = connection.dpid;
        assert self.dpid == connection.dpid;
        if self.ports is None:
            self.ports = connection.features.ports;
            for port in self.ports:
                if port.port_no == of.OFPP_CONTROLLER or port.port_no == of.OFPP_LOCAL:
                    continue;
        self.disconnect();

        self.connection = connection;
        self._listeners = self.listenTo(connection);


class Dijkstra(EventMixin):
    def __init__(self):
        def startup():
            core.openflow.addListeners(self, priority = 0);
            core.openflow_discovery.addListeners(self);
        
        self.TopologyGraph = Graph();
        self.switches = {};
        self.mac_map = {};
        core.call_when_ready(startup, ('openflow','openflow_discovery'))
        print "Controller running..."

    def flood_packet(self, packet_in_event):
        """ Floods the packet """
        msg = of.ofp_packet_out(data = packet_in_event.ofp);
        msg.in_port = packet_in_event.port;
        msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD));
        packet_in_event.connection.send(msg);
    
    def flush_flow_tables(self):
        """ Flushes switches flow tables """
        msg = of.ofp_flow_mod(command=of.OFPFC_DELETE);
        for connection in core.openflow.connections:
            connection.send(msg);

    def _install(self, switch, in_port, out_port, dstEth, data = None):
        msg = of.ofp_flow_mod();
        msg.match.dl_dst = dstEth;
        msg.match.in_port = in_port;
        msg.idle_timeout = FLOW_IDLE_TIMEOUT;
        msg.hard_timeout = FLOW_HARD_TIMEOUT;
        msg.actions.append(of.ofp_action_output(port = out_port));
        if data is not None:
            msg.data = data;
        self.switches[switch].connection.send(msg);

    def _install_path(self, path, dstEth, event = None):
        for sw,in_port,out_port in path[::-1]:
            print("INSTALLING FLOW (dst: %s) ON %s FOR %i -> %i" % (dstEth, sw, in_port, out_port));
            if event is not None and sw == event.dpid:
                self._install(sw, in_port, out_port, dstEth, event.ofp);
            else:
                self._install(sw, in_port, out_port, dstEth);

    def install_path(self, path, event):
        packet = event.parsed
        # Install flow on path;
        self._install_path(path, packet.dst, event);

        # Reverse path and install it backwards;
        pathReverse = [(sw,out_port,in_port) for sw,in_port,out_port in path];
        self._install_path(pathReverse, packet.src);
        
    def _handle_PacketIn(self, event):
        packet = event.parsed;

        if packet.type != packet.IP_TYPE:
            self.flood_packet(event);
            return;

        src = self.mac_map.get(packet.src);
        if src is None:
            src = (event.dpid, event.port);
            self.mac_map[packet.src] = src;
        
        if packet.dst not in self.mac_map:
            self.flood_packet(event);
        else:
            dst = self.mac_map[packet.dst];
            path = self.TopologyGraph.find_shortest_path(src, dst);
            self.install_path(path, event);
        
    def _handle_ConnectionUp(self, event):
        switch = self.switches.get(event.dpid)
        if switch is None:
            # Adds new switch to switches map;
            switch = Switch(self);
            switch.dpid = event.dpid;
            self.switches[event.dpid] = switch;
            switch.connect(event.connection)

            # Adds new switch to graph topology;
            self.TopologyGraph.add_node(event.dpid);

            # Flushes switches flow tables; 
            self.flush_flow_tables();

    def _handle_ConnectionDown (self, event):
        switch = self.switches.get(event.dpid);
        if switch is not None:
            # Removes switch from switches map;
            del self.switches[event.dpid];

            # Flushes switches flow tables; 
            self.flush_flow_tables();
 
    def _handle_LinkEvent(self, event):
        l = event.link;
        sw1 = l.dpid1;
        sw2 = l.dpid2;
        pt1 = l.port1;
        pt2 = l.port2;

        if event.added:
            self.TopologyGraph.add_edge(sw1, sw2, pt1, pt2);
        if event.removed:
            self.TopologyGraph.remove_edge(sw1,sw2);

def launch():  
    core.registerNew(Dijkstra);
