"""
TRAP over multiple transports
+++++++++++++++++++++++++++++

The following script sends two SNMP TRAP notification using the 
following options:

* with SNMPv1
* with community name 'public'
* over IPv4/UDP and IPv6/UDP
* send TRAP notification
* to a Manager at localhost:162 and [::1]
* with TRAP ID 'coldStart' specified as an OID
* include managed objects information:
* with default Uptime value
* with default Agent Address with '127.0.0.1'
* overriding Enterprise OID with 1.3.6.1.4.1.20408.4.1.1.2

The following Net-SNMP commands will produce similar SNMP notification:

| $ snmptrap -v1 -c public udp:localhost 1.3.6.1.4.1.20408.4.1.1.2 127.0.0.1 1 0 12345
| $ snmptrap -v1 -c public udp6:[::1] 1.3.6.1.4.1.20408.4.1.1.2 127.0.0.1 1 0 12345

"""  #
from pysnmp.carrier.asyncio.dispatch import asyncioDispatcher
from pysnmp.carrier.asyncio.dgram import udp, udp6, unix
from pyasn1.codec.ber import encoder
from pysnmp.proto import api

# Protocol version to use
pMod = api.protoModules[api.protoVersion1]
# pMod = api.protoModules[api.protoVersion2c]

# Build PDU
trapPDU = pMod.TrapPDU()
pMod.apiTrapPDU.setDefaults(trapPDU)

# Traps have quite different semantics across proto versions
if pMod == api.protoModules[api.protoVersion1]:
    pMod.apiTrapPDU.setEnterprise(trapPDU, (1, 3, 6, 1, 1, 2, 3, 4, 1))
    pMod.apiTrapPDU.setGenericTrap(trapPDU, "coldStart")

# Build message
trapMsg = pMod.Message()
pMod.apiMessage.setDefaults(trapMsg)
pMod.apiMessage.setCommunity(trapMsg, "public")
pMod.apiMessage.setPDU(trapMsg, trapPDU)

transportDispatcher = asyncioDispatcher()

# UDP/IPv4
transportDispatcher.registerTransport(
    udp.domainName, udp.UdpSocketTransport().openClientMode()
)
transportDispatcher.sendMessage(
    encoder.encode(trapMsg), udp.domainName, ("localhost", 162)
)

# UDP/IPv6
transportDispatcher.registerTransport(
    udp6.domainName, udp6.Udp6SocketTransport().openClientMode()
)
transportDispatcher.sendMessage(encoder.encode(trapMsg), udp6.domainName, ("::1", 162))

## Local domain socket
# transportDispatcher.registerTransport(
#    unix.domainName, unix.UnixSocketTransport().openClientMode()
# )
# transportDispatcher.sendMessage(
#    encoder.encode(trapMsg), unix.domainName, '/tmp/snmp-manager'
# )

# Dispatcher will finish as all scheduled messages are sent
transportDispatcher.runDispatcher()

transportDispatcher.closeDispatcher()
