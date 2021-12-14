from json.decoder import JSONDecodeError
import json
from string import Template

class Config:

    __config = None
    __configName = "info.json"

    def __open_config(self):
        try:
            configFile = open(self.__configName, "r")
            self.__config = configFile
        except:
            print("Could not open ", self.__configName ,"file")
            exit(1)

    def get_info(self):
        self.__open_config()
        try:
            config = json.loads(self.__config.read())
        except JSONDecodeError:
            print("Error loading json file")
            exit()
        server_config = config["server_config"]
        client_config = config["client_config"]
        return server_config, client_config

    def __fill_in_template(self, role):
        server_config, client_config = self.get_info()

        server_config["Client_LAN_ip"] = server_config["Client_LAN_ip"][:-1] + "0"
        client_config["Server_LAN_ip"] = client_config["Server_LAN_ip"][:-1] + "0"

        if role == "server":
            type_tmpl = "server.tmpl"
            role_info = server_config
        elif role == "client":
            type_tmpl = "client.tmpl"
            role_info = client_config
        else:
            print("Wrong type")
            exit()
        try:
            with open('/home/studentas/Documents/python/OpenVPN_speed_test/templates/'+ type_tmpl, 'r') as f:
                template = Template(f.read())
                tmpl = template.substitute(role_info)
            return tmpl
        except Exception as e:
            print(e)
            exit()
    
    def create_config(self, role):
        tmpl = self.__fill_in_template(role)
        try:
            with open('/home/studentas/Documents/python/OpenVPN_speed_test/config/openvpn', 'a') as f:
                f.seek(0)
                f.truncate()
                f.write(tmpl)
        except Exception as e:
            print(e)
            exit()