import subprocess
import os
import time

current_dir = os.path.dirname(os.path.abspath(__file__))

# 建立兩個子進程分別運行 server.py 和 client.py
p1 = subprocess.Popen(['python', os.path.join(current_dir, 'server.py')], shell=True)
time.sleep(1)
p2 = subprocess.Popen(['python', os.path.join(current_dir, 'client.py')], shell=True)

# 等待兩個進程結束
p1.wait()
p2.wait()
