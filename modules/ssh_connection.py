import paramiko
import time

def createSSHClient(hostname, username, password):
    port = "22"
    try:
        total_attempts = 3
        for attempt in range(total_attempts):
            ssh = paramiko.SSHClient()
            ssh.load_system_host_keys()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname, port, username, password)
            shell = ssh.invoke_shell()
        return ssh, shell
    except Exception as e:
        print(e)
        exit()

def waitForResponse(shell):
    attempts=0 
    while not shell.recv_ready():
        time.sleep(1)
        attempts += 1
        # print(attempts)
        if attempts > 30:
            print("Device not responding")
            exit()

def sendCommand(shell, command):
    try:
        shell.send(command + "\n")
        # time.sleep(2)
    except Exception as e:
        print("Error sending command", e)
        exit()

def getResponse(shell):
    try:
        waitForResponse(shell)
        terminal_data = shell.recv(9999).decode()
        return terminal_data
    except Exception as e:
        print(e)
        exit()
















# class Connection:

    # __sshCon = None

    # def connect(self):
    #     host = "192.168.3.1"
    #     user = "root"
    #     passw = "Admin123"

    #     ssh = paramiko.SSHClient()
    #     ssh.load_system_host_keys()
    #     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    #     try:
    #         total_attempts = 3
    #         for attempt in range(total_attempts):
    #             print(attempt)
    #             ssh.connect(hostname = host, username = user, password = passw)
    #             self.__sshCon = ssh
    #             self.__transport = ssh.get_transport()
    #             self.__session = self.__transport.open_session()
    #             self.__session.setblocking(0)
    #             self.__session.get_pty()
    #             self.__session.invoke_shell()
    #             self.waitForTerminal()
    #             print(self.__session.recv(9999))
    #             print("conn")
    #             return
    #     except Exception as e:
    #         print("Connection error (ssh): ", e)
    #         exit()
    #     print("connected")

    # def waitForTerminal(self):
    #     attempts=0 
    #     while not self.__session.recv_ready():
    #         time.sleep(1)
    #         attempts += 1
    #         if attempts > 185:
    #             break

    # def __del__(self):
    #     if self.__sshCon:
    #         print("ssh connection closed")
    #         self.__sshCon.close()
    #     if self.__transport:
    #         print("transport closed")
    #         self.__transport.close()