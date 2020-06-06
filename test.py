from get_nic import getnic

interfaces = getnic.interfaces()
ip = getnic.ipaddr(interfaces)

interface_list = []
ethernet_address = {}
ethernet_keys = []
ethernet_values = []
interface_count = 0

for i in ip.keys():
    interface_list.append(i)
    for x in ip[i].keys():
        if interface_list[interface_count] == 'lo':
            if x == 'inet4':
                ethernet_address.update(lo=ip[i][x])
        elif interface_list[interface_count] == 'eth0':
            if x == 'inet4':
                ethernet_address.update(eth0=ip[i][x])
        elif interface_list[interface_count] == 'wlan0':
            if x == 'inet4':
                ethernet_address.update(wlan0=ip[i][x])
    interface_count += 1

for k,v in ethernet_address.items():
    ethernet_keys.append(k)
    ethernet_values.append(v)
