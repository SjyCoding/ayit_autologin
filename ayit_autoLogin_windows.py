"""
校园网自动登录 v0.0.1
    原始代码来自于 https://sunlanchang.github.io/2017/10/31/%E6%A0%A1%E5%9B%AD%E7%BD%91%E8%87%AA%E5%8A%A8%E7%99%BB%E5%BD%95%E8%84%9A%E6%9C%AC/
校园网登陆网址
    http://172.168.254.6/a70.htm?wlanuserip=172.19.219.87&wlanacname=&wlanacip=172.168.254.100&mac=000000000000

"""
import datetime
import os
import socket
from glob import glob
import time
import subprocess as sp
import requests

# 连接方式  以太网/WALN
link_fs = "以太网"
# 这个是固定的, cmd输入ipconfig查看上面所选的两届方式对应的IPv4地址
local_ip = "172.19.192.251"
# 运营商
移动 = 'yidong'
联通 = 'unicom'
电信 = 'telecom'
# 选择运营商
yunyingshang = 移动

# 学号姓名
username = '18031210211'
password = '888888'

powershell_cmd = "curl " \
                 "-URi 'http://172.168.254.6:801/eportal/?c=ACSetting&a=Login&protocol=http:&hostname=172.168.254.6" \
                 "&iTermType=2&wlanuserip=" + local_ip + \
                 "&wlanacip=172.168.254.100&mac=000000000000&ip=" + local_ip + \
                 "&enAdvert=0&loginMethod=1' -Body 'DDDDD=%2C0%2C" + username + "%40" + yunyingshang + "&upass=" + password + \
                 "&R1=0&R2=0&R6=0&para=00&0MKKey=123456&buttonClicked=&redirect_url=&err_flag=&username=&password=&user=&cmd=&Login=' " \
                 "-Method Post"

# 校园网ip
edu_ip = '172.168.254.6'
edu_url = 'http://172.168.254.6/'


# 是否连上网, 请求指定url, 判断是否响应成功
def is_connect_web(url):
    status_code = requests.get(url).status_code
    if status_code == 200:
        return True
    else:
        return False


# ping指定ip, 返回是否成功
def check_ping(ip, count=1, timeout=500):
    cmd = 'ping -n %d -w %d %s > NUL' % (count, timeout, ip)
    res = os.system(cmd)
    return True if res == 0 else False


# 获取当前时间
def get_time():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


# 获取当前日期 用于生成日志文件名称
def get_day():
    return datetime.datetime.now().strftime('%Y-%m-%d')


# 日志收集
def log(msg, is_output=True):
    log_str = get_time() + ' - ' + msg
    # 打开文件 如果文件不存在则创建 将光标放在文件末尾
    log_file = open("./log/" + get_day() + ".log", mode='a', encoding='utf8')
    log_file.write(log_str + "\n")  # 写入一行数据
    log_file.close()  # 关闭文件

    if is_output:  # 是否打印到控制台
        print(log_str)


def run(self, cmd, timeout=15):
    b_cmd = cmd.encode(encoding=self.coding)
    try:
        b_outs, errs = self.popen.communicate(b_cmd, timeout=timeout)
    except sp.TimeoutExpired:
        self.popen.kill()
        b_outs, errs = self.popen.communicate()
    outs = b_outs.decode(encoding=self.coding)
    return outs, errs


# PowerShell类, 包含和PowerShell相关的一些方法
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


# 主运行逻辑
def main():
    log("安阳工学院校园网自动登录脚本开始执行")
    while True:
        if is_connect_web("http://www.baidu.com"):
            log("连接成功, 可以正常联网")
            break

        with PowerShell('GBK') as ps:
            # 在连接校园网的情况下, 获取本机ip
            # out, err = ps.run('ipconfig')
            # if link_fs == "以太网":
            #     local_ip = out.split(link_fs)[3].split(':')[9].split('\r\n')[0].strip()
            cmd = "curl " \
                  "-URi 'http://172.168.254.6:801/eportal/?c=ACSetting&a=Login&protocol=http:&hostname=172.168.254.6" \
                  "&iTermType=2&wlanuserip=" + local_ip + \
                  "&wlanacip=172.168.254.100&mac=000000000000&ip=" + local_ip + \
                  "&enAdvert=0&loginMethod=1' -Body 'DDDDD=%2C0%2C" + username + "%40" + yunyingshang + "&upass=" + password + \
                  "&R1=0&R2=0&R6=0&para=00&0MKKey=123456&buttonClicked=&redirect_url=&err_flag=&username=&password=&user=&cmd=&Login=' " \
                  "-Method Post"
            outs, errs = ps.run(cmd)

    os.system('pause')


# TODO 自动获取ip待完成
def test():
    import os, re
    addresses = os.popen(
        'IPCONFIG | FINDSTR /R "Ethernet adapter Local Area Connection .* Address.*[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*"')
    first_eth_address = re.search(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', addresses.read()).group()
    print(first_eth_address)
    hostname = socket.gethostname()
    print(socket.gethostbyname(hostname))
    pass


if __name__ == '__main__':
    main()
