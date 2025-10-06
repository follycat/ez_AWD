import pythonping
from concurrent.futures import ThreadPoolExecutor

def get_ip(ip):
    res = pythonping.ping(ip)
    if "Reply" in str(res):
        print(ip)
        return ip  # 返回存活的IP
    print("false")
    return None

ip = []
for num in range(1,244):       #更改循环位置
     ip.append("192-168-1-" + str(num) + ".pvp6189.bugku.cn")  #需要更改循环位置以及ip地址
     # ip.append("192.168.1." + str(num))
with ThreadPoolExecutor(max_workers=100) as executor:
    results = executor.map(get_ip, ip)

# 收集存活的IP地址
alive_ips = [ip for ip in results if ip is not None]

# 将存活IP写入ip.txt文件
with open(r"ip.txt", "w") as f:
    for ip in alive_ips:
        f.write(f"{ip}\n")
