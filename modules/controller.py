import modules.ssh_connection as connModule
import modules.config as configModule
import modules.gen_key as keyModule
import modules.file_transfer as filesModule
import modules.write_to_file as writemodule
import time
from tqdm import tqdm
# --Encryption types
# DES-CBC
# DES-EDE-CBC
# DES-EDE3-CBC
# DESX-CBC
# BF-CBC
# CAST5-CBC
# AES-128-CBC
# AES-192-CBC

# rutx09 84.15.129.227
# rutx11 84.15.161.186
class Control:

    client_ssh = None
    server_ssh = None

    def main(self,test_cycles, file_name):
        self.__configFile = configModule.Config()
        keyModule.makeKey()
        self.client_info, self.server_info = self.__configFile.get_info()
        self.server_setup()
        self.client_setup()
        self.speed_test(self.client_shell, self.client_info, self.server_info, test_cycles, file_name)
        self.server_ssh.close()
        self.client_ssh.close()

    def server_setup(self):
        print("Preparing server")
        self.__configFile.create_config("server")
        self.server_ssh, self.server_shell = connModule.createSSHClient(self.server_info["Server_LAN_ip"], self.server_info["Server_User"], self.server_info["Server_Password"])
        self.exec_commands(self.server_ssh, self.server_shell)
        connModule.sendCommand(self.server_shell, "iperf3 -s")

    def client_setup(self):
        print("Preparing client")
        self.__configFile.create_config("client")
        self.client_ssh, self.client_shell = connModule.createSSHClient(self.client_info["Client_WAN_ip"], self.client_info["Client_User"], self.client_info["Client_Password"])
        self.exec_commands(self.client_ssh, self.client_shell)
        # connModule.sendCommand(self.client_shell, "iperf3 -c " + self.server_info["Server_LAN_ip"])

    def speed_test(self, shell, client_info, server_info, test_cycles, file_name):
        output = connModule.getResponse(shell)
        test_cycles = int(test_cycles)
        upload = []
        download = []
        upload_sum = 0
        download_sum = 0
        print("...")
        for i in tqdm(range(test_cycles)):
            connModule.sendCommand(shell, "iperf3 -c " + server_info["Server_LAN_ip"])
            time.sleep(2)
            # print("Test cycle ", i)
            while True:
                output = connModule.getResponse(shell)
                if "- -" in output:
                    result = output.split("\n",3)[3].split()
                    upload.append(result[6])
                    download.append(result[16])

                    upload_sum += float(result[6])
                    download_sum += float(result[16])
                if "root" in output:
                    break
        
        upload_average = upload_sum / test_cycles
        download_average = download_sum / test_cycles

        file = writemodule.Write()
        if "tcp" in client_info["Protocol"]:
            client_info["Protocol"] = "tcp"
        test_data = self.do_list(client_info["Encryption"], client_info["LZO"], client_info["Protocol"], client_info["Authentication"], upload, download, format(upload_average, '.2f'), format(download_average, '.2f'))
        file.write_file(test_data, file_name)

    def do_list(self,encrypt, lzo, protocol, authent, upload, download,upaverage, downaverage):
        test_data = [['Encryption', 'LZO', ' '],[encrypt, lzo, ' '],[],['Authentication', 'Protocol', ' '],[authent, protocol, ' '],[],['Upload Mbits/sec', 'Download Mbits/sec', ' ']]
        for (line, dline) in zip(upload, download):
            test_data.append([line, dline, ' '])
        # test_data.append([])
        test_data.append(['Upload average', 'Download average', ' '])
        test_data.append([upaverage, downaverage, ' '])
        return test_data

    def exec_commands(self, ssh, shell):

        filesModule.sendFiles(ssh)
        time.sleep(2)
        connModule.sendCommand(shell, "/etc/init.d/openvpn restart")
        time.sleep(2)
        connModule.sendCommand(shell, "/etc/init.d/firewall restart")
        time.sleep(2)
        connModule.sendCommand(shell, "opkg install /tmp/iperf3_3.10.1-1_arm_cortex-a7_neon-vfpv4.ipk")
        time.sleep(2)

    def __del__(self):
        if self.server_ssh:
            self.server_ssh.close()
        if self.client_ssh:
            self.client_ssh.close()
