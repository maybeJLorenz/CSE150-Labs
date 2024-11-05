#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import RemoteController
#
#
#     Last Modified: november 5, 11:40am
#

class MyTopology(Topo):
  def __init__(self):
    Topo.__init__(self)

    ## Adding Hosts
      ## Workstations
    facultyWS = self.addHost('facultyWS', ip='10.0.1.2/24', mac="00:00:02:00:01", defaultRoute="s2-eth2")
    labWS = self.addHost('labWS', ip='10.0.2.3/24', mac="00:00:03:00:01", defaultRoute="s3-eth3")
    itWS = self.addHost('itWS', ip='10.40.3.30', mac="00:00:04:00:01", defaultRoute="s4-eth4")
    
      ## Laptops
    facultyPC = self.addHost('facultyPC', ip='10.0.1.4/24', mac="00:00:02:00:02", defaultRoute="s2-eth2")
    studentPC1 = self.addHost('studentPC1', ip='10.0.2.2/24', mac="00:00:03:00:02", defaultRoute="s3-eth3")
    studentPC2 = self.addHost('studentPC2', ip='10.0.2.40', mac="00:00:03:00:03", defaultRoute="s3-eth3")
    itPC = self.addHost('itPC', ip='10.40.3.254', mac="00:00:04:00:02", defaultRoute="s4-eth4")
    trustedPC = self.addHost('trustedPC', ip='10.0.203.6/32', mac="00:00:01:00:01", defaultRoute="s1-eth1")
    guest1 = self.addHost('guest1', ip='10.0.198.6/32', mac="00:00:01:00:02", defaultRoute="s1-eth1")
    guest2 = self.addHost('guest2', ip='10.0.198.10/32', mac="00:00:01:00:03", defaultRoute="s1-eth1")
    
      ## Servers
    examServer = self.addHost('examServer', ip='10.100.100.2/24', mac="00:00:05:00:01", defaultRoute="s5-eth5")
    webServer = self.addHost('webServer', ip='10.100.100.20', mac="00:00:05:00:02", defaultRoute="s5-eth5")
    dnsServer = self.addHost('dnsServer', ip='10.100.100.56', mac="00:00:05:00:03", defaultRoute="s5-eth5")
    
      ## Other
    printer = self.addHost('printer', ip='10.0.1.3/24', mac="00:00:02:00:03", defaultRoute="s2-eth2")

    ## Adding Switches
    s1 = self.addSwitch('s1') ## core switch
    s2 = self.addSwitch('s2') ## faculty switch
    s3 = self.addSwitch('s3') ## student housing switch
    s4 = self.addSwitch('s4') ## IT department switch
    s5 = self.addSwitch('s5') ## university data switch

    ## Adding Links
      ## University Data Center
    self.addLink(examServer, s5)
    self.addLink(webServer, s5)
    self.addLink(dnsServer, s5)
    self.addLink(s5, s1)

      ## IT Department LAN
    self.addLink(itWS, s4)
    self.addLink(itPC, s4)
    self.addLink(s4, s1)

      ## Student Housing LAN
    self.addLink(studentPC1, s3)
    self.addLink(studentPC2, s3)
    self.addLink(labWS, s3)
    self.addLink(s3, s1)

      ## Faculty LAN
    self.addLink(facultyWS, s2)
    self.addLink(printer, s2)
    self.addLink(facultyPC, s2)
    self.addLink(s2, s1)

      ## Internet
    self.addLink(trustedPC, s1)
    self.addLink(guest1, s1)
    self.addLink(guest2, s1)
   
    # laptop1 = self.addHost('Laptop1', ip='200.20.2.8/24',defaultRoute="Laptop1-eth1")

    # switch1 = self.addSwitch('s1')

    # self.addLink(laptop1, switch1, port1=1, port2=2)
    
    

if __name__ == '__main__':
  #This part of the script is run when the script is executed
  topo = MyTopology() #Creates a topology
  c0 = RemoteController(name='c0', controller=RemoteController, ip='127.0.0.1', port=6633) #Creates a remote controller
  net = Mininet(topo=topo, controller=c0) #Loads the topology
  net.start() #Starts mininet
  CLI(net) #Opens a command line to run commands on the simulated topology
  net.stop() #Stops mininet
