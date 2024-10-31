# Lab 5 controller skeleton 
#
# Based on of_tutorial by James McCauley
#
# last modified: october 30, 6:45

from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class Firewall (object):
  """
  A Firewall object is created for each switch that connects.
  A Connection object for that switch is passed to the __init__ function.
  """
  def __init__ (self, connection):
    
    self.connection = connection
    connection.addListeners(self)

  
  def do_firewall (self, packet, packet_in):

    ## implemented stuff to accept()
    def accept(self, packet, packet_in):
      msg = of.ofp_flow_mod()
      msg.data = packet_in
      msg.match = of.ofp_match.from_packet(packet)
      msg.idle_timeout = 45
      msg.hard_timeout = 600
      msg.actions.append(of.ofp_action_output(port=of.OFPP_NORMAL))
      msg.buffer_id = packet_in.buffer_id
      self.connection.send(msg)
      print("Packet Accepted - Flow Table Installed on Switches")

    ## added to drop()
    def drop(packet, packet_in):
      msg = of.ofp_flow_mod()
      msg.data = packet_in
      msg.match = of.ofp_match.from_packet(packet)
      msg.idle_timeout = 45
      msg.hard_timeout = 600
      msg.buffer_id = packet_in.buffer_id
      print("Packet Dropped - Flow Table Installed on Switches")

    # Write firewall code 
    ip_header = packet.find('ipv4')
    tcp_header = packet.find('tcp')
    udp_header = packet.find('udp')

    # Defining IPs
    laptop_ip = "10.1.1.2"
    server_ip = "10.1.1.1"
    lights_ip = "10.1.2.1"
    fridge_ip = "10.1.2.2"

    # if ip_header is None:
    #   return
    
    # Rule #1: allow ARP and ICMP for general connectivity
    if packet.find('arp') or packet.find('icmp'):
        self.accept(packet, packet_in)
    else:
        self.drop(packet, packet_in)  # Drop other non-IP packets
        return

    # Rule #2: Web Traffic - allow all TCP traffic between laptop and server
    if tcp_header:
        if (ip_header.srcip == laptop_ip and ip_header.dstip == server_ip) or \
            (ip_header.srcip == server_ip and ip_header.dstip == laptop_ip):
            self.accept(packet, packet_in)
            return

    # Rule #3a: IoT Access - allow all TCP traffic between laptop and lights
    if tcp_header and ip_header.srcip == laptop_ip and ip_header.dstip == lights_ip:
        self.accept(packet, packet_in)
        return

    # Rule #3b: IoT Acess - allow all UDP traffic between laptop and fridge
    if udp_header and ip_header.srcip == laptop_ip and ip_header.dstip == fridge_ip:
        self.accept(packet, packet_in)
        return

    # Rule #4: Laptop/Server General Management - allow all UDP traffic between laptop and server
    if udp_header:
        if (ip_header.srcip == laptop_ip and ip_header.dstip == server_ip) or \
            (ip_header.srcip == server_ip and ip_header.dstip == laptop_ip):
              self.accept(packet, packet_in)
              return

    # Default Deny: Drop all other traffic
    self.drop(packet)

  
  def _handle_PacketIn (self, event):
    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    self.do_firewall(packet, packet_in)

  def launch ():
    
    def start_switch (event):
      log.debug("Controlling %s" % (event.connection,))
      Firewall(event.connection)
    core.openflow.addListenerByName("ConnectionUp", start_switch)
