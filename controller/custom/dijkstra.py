from collections import defaultdict

from pox.core import core;
import pox.openflow.libopenflow_01 as of;
from pox.openflow.discovery import Discovery;
from pox.lib.revent import *;
from pox.lib.util import dpid_to_str;
from graph import Graph;

# Flow timeouts
FLOW_IDLE_TIMEOUT = 0;
FLOW_HARD_TIMEOUT = 0;

def build_path(switches_path, adjacency, event, switch_dst, final_port):
    path = [];
    in_port = event.port;
    
    for s1,s2 in zip(switches_path[:-1],switches_path[1:]):
        out_port = adjacency[s1][s2];
        path.append((s1,in_port,out_port));
        in_port = adjacency[s2][s1];
    
    path.append((switch_dst,in_port,final_port));

    return path;
        

class Switch(EventMixin):
    def __init__(self, manager):
        self.connection = None;
        self.ports = None;
        self.dpid = None;
        self._listeners = None;

    def disconnect(self):
        if self.connection is not None:
            self.connection.removeListeners(self._listeners)
            self.connection = None;
            self._listeners = None;

    def connect(self, connection):
        if self.dpid is None:
            self.dpid = connection.dpid
        assert self.dpid == connection.dpid
        if self.ports is None:
            self.ports = connection.features.ports
            for port in self.ports:
                if port.port_no ==  of.OFPP_CONTROLLER or port.port_no == of.OFPP_LOCAL:
                    continue
        self.disconnect()                   

        self.connection = connection
        self._listeners = self.listenTo(connection)


class Dijkstra(EventMixin):  
    
    def __init__(self):
        def startup():
            core.openflow.addListeners(self, priority = 0);
            core.openflow_discovery.addListeners(self);
        
        self.G = Graph();
        self.switches = {};
        self.adjacency = defaultdict(lambda : defaultdict(lambda : None));
        self.mac_map = {};
        core.call_when_ready(startup, ('openflow','openflow_discovery'))
        print "Controller running..."

    def flood_packet(self, packet_in_event):
        """ Floods the packet """
        msg = of.ofp_packet_out();
        msg.data = packet_in_event.ofp;
        msg.in_port = packet_in_event.port;
        msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD));
        packet_in_event.connection.send(msg);

    def flush_flow_tables(self):
        msg = of.ofp_flow_mod(command=of.OFPFC_DELETE);
        for connection in core.openflow.connections:
            connection.send(msg);

    def _install (self, switch, in_port, out_port, dstEth, data = None):
        msg = of.ofp_flow_mod();
        msg.match.dl_dst = dstEth;
        msg.match.in_port = in_port;
        msg.idle_timeout = FLOW_IDLE_TIMEOUT;
        msg.hard_timeout = FLOW_HARD_TIMEOUT;
        msg.actions.append(of.ofp_action_output(port = out_port));
        if data is not None:
            msg.data = data;
        print('INSTALL', switch, in_port, out_port, dstEth);
        self.switches[switch].connection.send(msg);

    def _install_path (self, path, dstEth, event = None):
        for sw,in_port,out_port in path[::-1]:
            if event is not None and sw == event.connection.dpid:
                self._install(sw, in_port, out_port, dstEth, event.ofp);
            else:
                self._install(sw, in_port, out_port, dstEth);

    def install_path (self, path, event):
        packet = event.parsed
        # We have a path -- install it
        self._install_path(path, packet.dst, event);

        # Now reverse it and install it backwards
        pathReverse = [(sw,out_port,in_port) for sw,in_port,out_port in path];
        self._install_path(pathReverse, packet.src);
        
    def _handle_PacketIn(self, event):
        packet = event.parsed;

        if packet.type != packet.IP_TYPE:
            self.flood_packet(event);
            return;

        print("PACKET", event.connection.dpid, packet.src, packet.dst)

        packetInSwitch = self.switches[event.connection.dpid];
        loc = (packetInSwitch, event.port);

        knownLoc = self.mac_map.get(packet.src);
        if knownLoc is None:
            print("Learned", packet.src, loc[0], loc[1]);
            self.mac_map[packet.src] = loc;
        
        if packet.dst.is_multicast:
            print("Flood multicast from %s", packet.src)
            self.flood_packet(event);
        else:
            if packet.dst not in self.mac_map:
                print("%s unknown -- flooding" % (packet.dst,))
                self.flood_packet(event);
            else:
                dst = self.mac_map[packet.dst];
                routes = self.G.dijkstra(loc[0].dpid);
                path = build_path(routes[dst[0].dpid], self.adjacency, event, dst[0].dpid, dst[1]);
                print('PATH', path);
                self.install_path(path, event);


    def _handle_ConnectionUp(self, event):
        switch = self.switches.get(event.dpid)
        if switch is None:
            # Adds new switch to switches map;
            switch = Switch(self);
            switch.dpid = event.dpid;
            print("ADDING SWITCH", event.dpid, switch)
            self.switches[event.dpid] = switch;
            switch.connect(event.connection)

            # Adds new switch to graph topology;
            self.G.add_node(event.dpid);

            # Flushes all switches flow tables; 
            self.flush_flow_tables();


    def _handle_ConnectionDown (self, event):
        switch = self.switches.get(event.dpid);
        if switch is not None:
            # Removes switch from switches map;
            del self.switches[event.dpid];

            # Flushes all switches flow tables; 
            self.flush_flow_tables();
 
    def _handle_LinkEvent(self, event):
        l = event.link;
        sw1 = l.dpid1;
        sw2 = l.dpid2;
        pt1 = l.port1;
        pt2 = l.port2;

        if event.added:
            if self.adjacency[sw1][sw2] is None:
                self.adjacency[sw1][sw2] = pt1;
                self.adjacency[sw2][sw1] = pt2;
            self.G.add_edge(sw1, sw2);
        if event.removed:
            if sw2 in self.adjacency[sw1]:
                del self.adjacency[sw1][sw2];
            if sw1 in self.adjacency[sw2]:
                del self.adjacency[sw2][sw1];
            self.G.remove_edge(sw1,sw2);

def launch():  
    core.registerNew(Dijkstra);