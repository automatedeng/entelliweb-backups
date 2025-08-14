import os
from dotenv import load_dotenv
from paramiko import SSHClient, AutoAddPolicy
from datetime import datetime
import json


load_dotenv()

nas_user = os.getenv("NAS_U")
nas_passw = os.getenv("NAS_P")
nas_ip = os.getenv("NAS_IP")

eweb_path = r"\Program Files (x86)\Delta Controls\enteliWEB\website\support\eweb_backup"
eweb_base = r'"\Program Files (x86)\Delta Controls\enteliWEB\website\support\eweb_backup"'
desktop_base = r"C:\Users\awilliamson\Desktop"

nas_client = SSHClient()
nas_client.set_missing_host_key_policy(AutoAddPolicy)
nas_client.connect(nas_ip,username=nas_user, password=nas_passw)



with open(".\\server.json") as file:
    servers = json.load(file)

    for server in servers:
        print(server)


        server_client = SSHClient()
        server_client.set_missing_host_key_policy(AutoAddPolicy)

        server_client.connect(server["ip"],username=server["user"],password=server["passw"], look_for_keys=False)

        stdin, stdout, stderr = server_client.exec_command(r"dir "+eweb_base)

        backup_files = stdout.read().decode()

        err = stderr.read().decode()

        lines = backup_files.split("     ")

        final_file_name = None
        # date_string = datetime.now().strftime("%Y%m%d")

        with server_client.open_sftp() as sftp:
            for index, line in enumerate(lines):
                if "Backup" in line:
                    filename_arr = line.split("\r")[0].split(" ")

                    if len(filename_arr) > 2:
                        final_file_name= filename_arr[1]+" "+filename_arr[2]+" "+filename_arr[3]
                    else:
                        final_file_name= filename_arr[1]
                    
                    sftp.get(eweb_path+"\\"+final_file_name,desktop_base+"\\"+final_file_name)

            
            sftp.close()
        
        server_client.close()


nas_client.connect()
        



