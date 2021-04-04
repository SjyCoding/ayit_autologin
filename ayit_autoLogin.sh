#!/bin/bash

#--------------------------------------------------------------
#下面是需要修改的参数
#
#这里填学号
id=""

#这里填密码
password=""

#这里填运营商(移动: yidong  联通: unicom 电信: telecom)
isp=""

#--------------------------------------------------------------
#此参数在校园网无大规模改动时,无需修改
nasip="172.168.254.100"

#检测网络链接畅通
function network() {
	#超时时间
	local timeout=1

	#目标网站
	local target=www.baidu.com

	#获取响应状态码
	local ret_code=$(curl -I -s --connect-timeout ${timeout} ${target} -w %{http_code} | tail -n1)

	if [ "x$ret_code" = "x200" ]; then
		#网络畅通
		return 1
	else
		#网络不畅通
		return 0
	fi

	return 0
}

while [ $? -eq 0 ]; do
	ip=$(ifconfig ens33 | grep "inet addr" | awk '{print $2}')
	curl -d "DDDDD=%2C0%2C${id}%40${isp}&upass=${password}&R1=0&R2=0&R6=0&para=00&0MKKey=123456&buttonClicked=&redirect_url=&err_flag=&username=&password=&user=&cmd=&Login=" "http://172.168.254.6:801/eportal/?c=ACSetting&a=Login&protocol=http:&hostname=172.168.254.6&iTermType=2&wlanuserip=${ip}&wlanacip=${nasip}&mac=000000000000&ip=${ip}&enAdvert=0&loginMethod=1"
	sleep 5
done
echo "网络畅通，你可以上网冲浪！"
exit 0
