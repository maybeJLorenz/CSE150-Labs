# Lab5 Skeleton
#
#     Last Modified: november 4, 4:30pm
# 

from pox.core import core

import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class Routing (object):
    
  def __init__ (self, connection):
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.connection = connection

    # This binds our PacketIn event listener
    connection.addListeners(self)

  def do_routing (self, packet, packet_in, port_on_switch, switch_id):
    # port_on_swtich - the port on which this packet was received
    # switch_id - the switch which received this packet

    # Your code here
    ip_header = packet.find('ipv4')
    tcp_header = packet.find('tcp')
    udp_header = packet.find('udp')
    icmp_header = packet.find('icmp')

    ## Defining IPs
      # Univeristy Data Center
    exam_ip = "10.100.100.2/24"
    web_ip = "10.100.100.20"
    dns_ip = "10.100.100.56"

      # IT Department LAN
    itWS_ip = "10.40.3.30"
    itPC_ip = "10.40.3.254"

      # Faculty LAN
    facultyWS_ip = "10.0.1.2/24"
    printer_ip = "10.0.1.4/24"
    facultyPC_ip = "10.0.1.4/24"

      # Student Housing LAN
    student1_ip = "10.0.2.2/24"
    student2_ip = "10.0.2.40"
    lab_ip = "10.0.2.40"

      # Internet
    trusted_ip = "10.0.203.6/32"
    guest1_ip = "10.0.198.6/32"
    guest2_ip = "10.0.198.10/32"

    def accept():
      msg = of.ofp_flow_mod()
      msg.data = packet_in
      msg.match = of.ofp_match.from_packet(packet)
      msg.idle_timeout = 45
      msg.hard_timeout = 600
      msg.actions.append(of.ofp_action_output(port=of.OFPP_NORMAL))
      msg.buffer_id = packet_in.buffer_id
      self.connection.send(msg)
      print("Packet Accepted - Flow Table Installed on Switches")
    
    def drop():
      msg = of.ofp_flow_mod()
      msg.match = of.ofp_match.from_packet(packet)
      msg.idle_timeout = 45
      msg.hard_timeout = 600
      print("Packet Dropped - Flow Table Installed on Switches")

    # Rule #1: icmp between Student Housing, Faculty, and IT Dep. 
    #    NO: Univeristy or Internet

    # Rule #2: tcp between University, IT Dep, Faculty, Student Housing, and trustedPC
    #       - NO: Internet
    #       - Only Faculty LAN may access exam server


    # Rule #3: udp between University, IT Dep, Faculty, and Student Housing
    #       - NO: Internet


    # Rule #4: all other traffic is dropped
    drop()
      
    pass

  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """
    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    self.do_routing(packet, packet_in, event.port, event.dpid)

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Routing(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)