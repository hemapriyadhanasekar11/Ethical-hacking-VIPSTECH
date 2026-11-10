from scapy all import sniff,IP
def track(packet):
    if IP in packet:
        print("Source",packet[IP].src)
        print("Destination",packet[Ip].dst)
        print("Size",len(packet),"Bytes")
        print("______________________________")
        sniff(prn=track,count=2)
