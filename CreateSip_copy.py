serial = input("serial address for device")
from ldap3 import Server, Connection, ALL, SAFE_SYNC
import xml.etree.ElementTree as ET
from xml.dom import minidom
import time
#change based on your server
server = Server('ldap://192.168.12.189:389')
#change based upon your server
conn = Connection(server, 'CN=LDAP, CN=Users,DC=knight,DC=corp', 'BOCES10!', client_strategy=SAFE_SYNC, auto_bind=True)
status, result, response, _ = conn.search('OU=knightdir,DC=knight,DC=corp', '(objectclass=organizationalPerson)', attributes='*')
root = ET.Element("polycomConfig")
overrides = ET.SubElement(root, "reg")
list_of_dicts = [dict(obj) for obj in response]
infodicts = []
scraped = []
for i,dics in enumerate(list_of_dicts):
    #print(dics['raw_attributes'],'\n')
    infodicts.append(dics['raw_attributes'])

for i in infodicts:
    las = i['sn']
    las=str(las)
    last = las[3:-2]
    firs=i['givenName']
    firs=str(firs)
    first = firs[3:-2]
    phon=i['telephoneNumber']
    phon=str(phon)
    phone=phon[3:-2]
    now = {'first':first,'last':last,'phone':phone}
    scraped.append(now)
scraped.sort(key=lambda x: x['last'])
# Define the attributes and values
attributes_values = {
    "bg.color.selection": "2,1",
    "callLists.logConsultationCalls": "0",
    "softkey.feature.directories": "0",
    "voice.qualityMonitoring.collector.period": "20",
    "voIpProt.SIP.outboundProxy.address": "192.168.12.154",
    "voIpProt.SIP.outboundProxy.port": "5060",
    "voIpProt.SIP.outboundProxy.transport": "UDPOnly",
    "bg.color.bm.1.em.name": "Firetarget.jpg",
    "bg.color.bm.1.name": "Firetarget.jpg",
    "reg.1.auth.domain": "192.168.12.154",
    "reg.1.displayName": "6001",
    "reg.1.outboundProxy.address": "192.168.12.154",
    "reg.1.outboundProxy.port": "5060",
    "reg.1.outboundProxy.transport": "UDPOnly",
    "voIpProt.server.1.address": "192.168.12.154",
    "voIpProt.server.1.port": "5060",
    "voIpProt.server.1.transport": "UDPOnly",
    "reg.1.server.1.address": "192.168.12.154",
    "reg.1.server.1.port": "5060",
    "reg.1.server.1.transport": "UDPOnly",
    "reg.1.address": "101",
    "reg.1.auth.password": "DarkSideOfTheMoon-101",
    "reg.1.auth.userId": "101",
    "reg.1.extension": "101",
    "reg.1.label": "101",
    "reg.1.lineAddress": "101",
    "reg.1.lineKeys": "8",
    "reg.1.callsPerLineKey": "1",
}

current_address=12



for key, value in attributes_values.items():
    ET.SubElement(overrides, key).text = value
for i in scraped:
    current_address=str(current_address)
    name=(f"{i['last']}, {i['first']}")
    ET.SubElement(root,f'attendant.resourceList.{current_address}.address').text = i['phone']
    ET.SubElement(root,f'attendant.resourceList.{current_address}.label').text = str(name) 
    ET.SubElement(root,f'attendant.resourceList.{current_address}.type').text = "automata" 
    current_address=int(current_address)
    current_address+=1

    
with open(serial+"-sip.cfg", "w") as file:
    tree = ET.ElementTree(root)
    time.sleep(1)
    xml_str = ET.tostring(root, encoding='utf-8').decode() 
    xml_str = minidom.parseString(xml_str).toprettyxml(indent="    ")
    xml_str = f'{xml_str}'
    file.write(xml_str)


