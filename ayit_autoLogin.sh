#!/bin/bash
lastip=""
while true; do
  newip=$(ifconfig eth2.2 | grep "inet addr" | awk '{print $2}' | cut -c 6-)
  curl -d "DDDDD=%2C0%2C学号%40运营商&upass=密码&R1=0&R2=0&R6=0&para=00&0MKKey=123456&buttonClicked=&redirect_url=&err_flag=&username=&password=&user=&cmd=&Login=" "http://172.168.254.6:801/eportal/?c=ACSetting&a=Login&protocol=http:&hostname=172.168.254.6&iTermType=2&wlanuserip=${newip}&wlanacip=172.168.254.100&mac=000000000000&ip=${newip}&enAdvert=0&loginMethod=1"
  lastip=$newip
  sleep 5
done
