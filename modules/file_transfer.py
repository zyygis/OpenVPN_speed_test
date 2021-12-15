from scp import SCPClient

def sendFiles(ssh, name_rut9):
    try:
        scp = SCPClient(ssh.get_transport())
        scp.put(r"/home/studentas/Documents/python/OpenVPN_speed_test/config/static.key", r"/etc/vuci-uploads/")
        scp.put(r"/home/studentas/Documents/python/OpenVPN_speed_test/config/openvpn", r"/etc/config/")
        scp.put(r"/home/studentas/Documents/python/OpenVPN_speed_test/config/firewall", r"/etc/config/")
        if name_rut9:
            scp.put(r"/home/studentas/Documents/python/OpenVPN_speed_test/packages/iperf3_3.10.1-1_mips_24kc.ipk", r"/tmp/")
        else:
            scp.put(r"/home/studentas/Documents/python/OpenVPN_speed_test/packages/iperf3_3.10.1-1_arm_cortex-a7_neon-vfpv4.ipk", r"/tmp/")
    except Exception as e:
        print(e)
        ssh.close()
        exit()
