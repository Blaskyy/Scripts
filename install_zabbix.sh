#!/usr/bin/bash
# 
# ---------------------------------------------------
# 监控客户端安装说明
# 该脚本仅用于centos发行版使用
# bash# sh install_zabbix_agent.sh 
# 项目名参数位于脚本第12行
# ---------------------------------------------------
#
# elex-ops

Project_Name='zabbix' #project name

yum -y install sed iproute gawk libcurl libcurl-devel curl curl-devel

Zabbix_Server='127.0.0.1' #zabbix server ip
Kernel_Version=`uname -r | sed 's/[^e]*\(el[0-9]\).*/\1/'`
Interface=`route -n | awk '{if($1~"^0.0.0.0")print $NF}'`
Server_Active=`ip a | sed -nr '/inet /{s#\s+inet\s([^/]*)/.*#\1:10051#;H};${x;s/^\n//;s/1\n/1,/gp}'`
Public_Ip_Addr=`ip addr ls $Interface | awk -vFS='[ /]+' '/inet /{print $3}END{prongf "\n"}'`

if [ `yum search zabbix |grep zabbix-agent -c` -eq 0 ]; then
    if [ $Kernel_Version != "el5" ]; then
        rpm -Uvh http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
        rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-6
    else
        rpm -Uvh http://dl.fedoraproject.org/pub/epel/5/x86_64/epel-release-5-4.noarch.rpm
        rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-5
    fi
fi

Zabbix_Packet=`yum search zabbix | awk -F: '/agent/{print $1}' | tail -1`

if [ `rpm -qa |grep ${Zabbix_Packet} -c` -le 1 ]; then
    yum -y remove zabbix
    yum -y install ${Zabbix_Packet}
    Zabbix_Dir=/etc/zabbix/zabbix_agentd.conf
    sed -i "s/^\(Server=\).*/\1${Zabbix_Server}/" $Zabbix_Dir
    sed -i "s/\(CFG_FILE:-\).*/\1\/etc\/zabbix\/zabbix_agentd.conf}/" /etc/init.d/zabbix-agent
    sed -i "s/^\(ServerActive=\).*/\1${Zabbix_Server}/" $Zabbix_Dir
    sed -i "s/^\(Hostname=\).*/\1${Project_Name}_${Public_Ip_Addr}/" $Zabbix_Dir
    mkdir -p /etc/zabbix/bin/
    sed -i "/COMMIT/i \-A INPUT -m state --state NEW -m tcp -p tcp --dport 10050 -j ACCEPT" /etc/sysconfig/iptables
    sed -i "/COMMIT/i \-A INPUT -m state --state NEW -m tcp -p tcp --dport 10051 -j ACCEPT" /etc/sysconfig/iptables
    /etc/init.d/iptables restart
    /etc/init.d/zabbix-agent restart
fi

