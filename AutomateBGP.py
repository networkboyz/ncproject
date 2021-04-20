from devices import R1,R2,R3,R4,R5,R6,R7,R8,R9,R10
from datetime import datetime
from netmiko import ConnectHandler
import time

def verify_config(net_connect, cmd='show run | inc router bg$
    #Check if BGP is configured on the router's
    output = net_connect.send_command_expect(cmd)
    return 'bgp' in output

def rm_config(net_connect, cmd='no router bgp', as_number=''$
    #Remove BGP Configuration
    bgp_cmd = ("{} {}".format(cmd, str(as_number)))
    cmd_list = [bgp_cmd]
    output = net_connect.send_config_set(cmd_list)
    if net_connect.device_type == 'R1,R2,R3,R4,R5,R6,R7,R8,R$
        output += net_connect.commit()
    print (output)

def bgp_config(net_connect, file_name=''):
    #Configure BGP on router.
    try:
        output = net_connect.send_config_from_file(config_fi$
        if net_connect.device_type == 'R1,R2,R3,R4,R5,R6,R7,$
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
        print ("{}: {}".format(net_connect.device_type, net_$
        if verify_config(net_connect):
            print ("BGP is configured on this router")
            rm_config(net_connect, as_number=as_number)
        else:
            print ("No BGP configured on this router.")

        # Check BGP is removed.
        if verify_config(net_connect):
            raise ValueError("BGP configuration is not remov$

        #Create file based on device type.
        device_type = net_connect.device_type
        host = net_connect.host
        file_name = 'config_' + host + '.txt'

        # Configure BGP
        output = bgp_config(net_connect, file_name)
        print (output)

        print

    # Wait for BGP Neighborship Establishment
    time.sleep(60)

    # Validate BGP Neighborship
    for a_device in device_list:
        net_connect = ConnectHandler(**a_device)
        net_connect.enable()
        print ("Validating BGP: ")
        print ("{}: {}".format(net_connect.device_type, net_$
        output = net_connect.send_command("sh ip bgp sum")
        print ('#' * 80)
        print (output)
        print ('#' * 80)
        print

    print ("Time elapsed: {}\n".format(datetime.now() - star$


if __name__ == "__main__":
    main()