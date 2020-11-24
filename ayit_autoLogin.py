"""
校园网自动登录 v0.0.1
    原始代码来自于 https://sunlanchang.github.io/2017/10/31/%E6%A0%A1%E5%9B%AD%E7%BD%91%E8%87%AA%E5%8A%A8%E7%99%BB%E5%BD%95%E8%84%9A%E6%9C%AC/
校园网登陆网址
    http://172.168.254.6/a70.htm?wlanuserip=172.19.219.87&wlanacname=&wlanacip=172.168.254.100&mac=000000000000

"""
import os
from glob import glob
import time
import subprocess as sp
import requests

# 校园网ip
EduIP = '172.168.254.6'

# 连接方式  以太网/WALN
link_fs = "以太网"

# 运营商
移动 = 'yidong'
联通 = 'unicom'
电信 = 'telecom'
# 选择运营商
yunyingshang = 移动

# 学号姓名
username = 18031210211
password = 888888

local_ip = ""

powershell_cmd = "curl " \
                 "-URi 'http://172.168.254.6:801/eportal/?c=ACSetting&a=Login&protocol=http:&hostname=172.168.254.6" \
                 "&iTermType=2&wlanuserip=" + local_ip + "&wlanacip=172.168.254.100&mac=000000000000&ip=" + local_ip + \
                 "&enAdvert=0&loginMethod=1' " \
                 "-Body 'DDDDD=%2C0%2C18031210211%40yidong&upass=888888&R1=0&R2=0&R6=0&para=00&0MKKey=123456" \
                 "&buttonClicked=&redirect_url=&err_flag=&username=&password=&user=&cmd=&Login=' " \
                 "-Method Post"

url = 'http://172.168.254.6/'


def run(self, cmd, timeout=15):
    b_cmd = cmd.encode(encoding=self.coding)
    try:
        b_outs, errs = self.popen.communicate(b_cmd, timeout=timeout)
    except sp.TimeoutExpired:
        self.popen.kill()
        b_outs, errs = self.popen.communicate()
    outs = b_outs.decode(encoding=self.coding)
    return outs, errs


# 查看连接的是否是校园网
def is_connect_edu():
    status_code = requests.get(url).status_code
    if status_code == 200:
        return True
    else:
        return False


# 是否连上网
def is_connect_web():
    r = requests.get("http://www.baidu.com").text
    print(type(r))
    if r.find('210.31.32.126') != -1:
        return False
    else:
        return True


def check_ping(ip, count=1, timeout=500):
    cmd = 'ping -n %d -w %d %s > NUL' % (count, timeout, ip)
    res = os.system(cmd)
    return 'ok' if res == 0 else 'failed'


# 直到校园网连接上为止
# while True:
#     if is_connect_edu():  # 是否连接上校园网
#         if not is_connect_web():  # 是否连接上外网
#             login()
#             if requests.get('http://www.baidu.com').status_code == 200:
#                 print('Already connected Internet')
#             else:
#                 print('Not connected Internet')
#         break

# print("ping Baidu - " + check_ping("baidu.com"))
# print("ping edu - " + check_ping(EduIP))
#
# if check_ping(EduIP) == 'ok':  # 能ping通校园网
#     while True:
#         print("login...")
#         if check_ping("baidu.com") == 'failed':  # ping不通百度 登陆校园网
#             # requests.post(url, data=data)
#             time.sleep(1)  # 休眠
#         else:
#             print("已连上网络")
#             break
#         time.sleep(1)  # 休眠
# else:
#     print("未连接校园网...")

class PowerShell:
    # from scapy
    def __init__(self, coding, ):
        cmd = [self._where('PowerShell.exe'),
               "-NoLogo", "-NonInteractive",  # Do not print headers
               "-Command", "-"]  # Listen commands from stdin
        startupinfo = sp.STARTUPINFO()
        startupinfo.dwFlags |= sp.STARTF_USESHOWWINDOW
        self.popen = sp.Popen(cmd, stdout=sp.PIPE, stdin=sp.PIPE, stderr=sp.STDOUT, startupinfo=startupinfo)
        self.coding = coding

    def __enter__(self):
        return self

    def __exit__(self, a, b, c):
        self.popen.kill()

    def run(self, cmd, timeout=15):
        b_cmd = cmd.encode(encoding=self.coding)
        try:
            b_outs, errs = self.popen.communicate(b_cmd, timeout=timeout)
        except sp.TimeoutExpired:
            self.popen.kill()
            b_outs, errs = self.popen.communicate()
        outs = b_outs.decode(encoding=self.coding)
        return outs, errs

    @staticmethod
    def _where(filename, dirs=None, env="PATH"):
        """Find file in current dir, in deep_lookup cache or in system path"""
        if dirs is None:
            dirs = []
        if not isinstance(dirs, list):
            dirs = [dirs]
        if glob(filename):
            return filename
        paths = [os.curdir] + os.environ[env].split(os.path.pathsep) + dirs
        try:
            return next(os.path.normpath(match)
                        for path in paths
                        for match in glob(os.path.join(path, filename))
                        if match)
        except (StopIteration, RuntimeError):
            raise IOError("File not found: %s" % filename)


def main():
    while True:
        with PowerShell('GBK') as ps:
            # 在连接校园网的情况下, 获取本机ip
            out, err = ps.run('ipconfig')
            if link_fs == "以太网":
                local_ip = out.split(link_fs)[3].split(':')[9].split('\r\n')[0].strip()

            cmd = "curl " \
                  "-URi 'http://172.168.254.6:801/eportal/?c=ACSetting&a=Login&protocol=http:&hostname=172.168.254.6" \
                  "&iTermType=2&wlanuserip=" + local_ip + "&wlanacip=172.168.254.100&mac=000000000000&ip=" + local_ip + \
                  "&enAdvert=0&loginMethod=1' " \
                  "-Body 'DDDDD=%2C0%2C18031210211%40yidong&upass=888888&R1=0&R2=0&R6=0&para=00&0MKKey=123456" \
                  "&buttonClicked=&redirect_url=&err_flag=&username=&password=&user=&cmd=&Login=' " \
                  "-Method Post"
            outs, errs = ps.run(cmd)
        if is_connect_web():
            print("联网成功")
            break


if __name__ == '__main__':
    main()
