import os
from dotenv import load_dotenv
from paramiko import SSHClient, AutoAddPolicy
from datetime import datetime
import json


load_dotenv()

nas_user = os.getenv("NAS_U")
nas_passw = os.getenv("NAS_P")
nas_ip = os.getenv("NAS_IP")

eweb_base = r'"\Program Files (x86)\Delta Controls\enteliWEB\website\support\eweb_backup"'
eweb_path = r"\Program Files (x86)\Delta Controls\enteliWEB\website\support\eweb_backup"
nas_base = r"Z:\Server Backups"


backup_array = []
with open(".\\server.json") as file:
    servers = json.load(file)

    for server in servers:
        server_client = SSHClient()
        server_client.set_missing_host_key_policy(AutoAddPolicy)

        server_client.connect(server["ip"],username=server["user"],password=server["passw"], look_for_keys=False)

        stdin, stdout, stderr = server_client.exec_command(r"dir "+eweb_base)

        backup_files = stdout.read().decode()

        err = stderr.read().decode()

        lines = backup_files.split("     ")

        final_file_name = None
        date_string = datetime.now().strftime("%Y%m%d")

        with server_client.open_sftp() as sftp:
            for index, line in enumerate(lines):
                if "Backup" in line:
                    fileline_arr = line.split("\r\n")

                    file_date = datetime.strptime(fileline_arr[-1].split(" ")[0], "%m/%d/%Y")

                    today = datetime.now()

                    delta = today - file_date

                    filename_arr = fileline_arr[0].split(" ")

                    if file_date.date() == today.date():
                        if len(filename_arr) > 2:
                            final_file_name= filename_arr[1]+" "+filename_arr[2]+" "+filename_arr[3]
                        else:
                            final_file_name= filename_arr[1]

                    sftp.get(eweb_path+"\\"+final_file_name,nas_base+"\\"+server["name"]+"\\"+final_file_name)

            
            sftp.close()
        
        server_client.close()
        



