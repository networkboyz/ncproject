from datetime import datetime
from netmiko import ConnectHandler
from devices import R1,R2,R3,R4,R5,R6,R7,R8,R9,R10


def check_bgp(net_connect, cmd='show run | inc router bgp'):
    #Check if BGP is configured on the router's
    output = net_connect.send_command_expect(cmd)
    return 'bgp' in output

def remove_bgp_config(net_connect, cmd='no router bgp', as_number=''):
    #Remove BGP Configuration
    bgp_cmd = ("{} {}".format(cmd, str(as_number)))
    cmd_list = [bgp_cmd]
    output = net_connect.send_config_set(cmd_list)
    if net_connect.device_type == 'R1,R2,R3,R4,R5,R6,R7,R8,R9,R10':
        output += net_connect.commit()
    print (output)

def configure_bgp(net_connect, file_name=''):
    #Configure BGP on router.
    try:
        output = net_connect.send_config_from_file(config_file=file_name)
        if net_connect.device_type == 'R1,R2,R3,R4,R5,R6,R7,R8,R9,R10':
            output += net_connect.commit()
        return output
    except IOError:
        print ("Error reading file: {}".format(file_name))

def main():
    device_list = [R1,R2,R3,R4,R5,R6,R7,R8,R9,R10]
    start_time = datetime.now()
    print

    for a_device in device_list:
        as_number = a_device.pop('as_number') 
        net_connect = ConnectHandler(**a_device)
        net_connect.enable()
        print ("{}: {}".format(net_connect.device_type, net_connect.find_prompt()))
        if check_bgp(net_connect):
            print ("BGP is configured on this router")
            remove_bgp_config(net_connect, as_number=as_number)
        else:
            print ("No BGP configured on this router.")

        # Check BGP is removed.
        if check_bgp(net_connect):
            raise ValueError("BGP configuration is not removed.")

        #Create file based on device type.
        device_type = net_connect.device_type
        host = net_connect.host
        file_name = 'config_' + host + '.txt'

        # Configure BGP
        output = configure_bgp(net_connect, file_name)
        print (output)

        print

    print ("Time elapsed: {}\n".format(datetime.now() - start_time))


if __name__ == "__main__":