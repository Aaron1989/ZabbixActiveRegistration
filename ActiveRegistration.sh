#!/bin/bash

download_zabbix(){
    #Download soft
    cd /opt/
    rpm -e zabbix-agent
    wget -O libtool-ltdl-2.4.2-20.el7.x86_64.rpm  http://ress.oss-cn-qingdao-internal.aliyuncs.com/zabbix%2Flibtool-ltdl-2.4.2-20.el7.x86_64.rpm
    wget -O unixODBC-2.3.1-11.el7.x86_64.rpm  http://ress.oss-cn-qingdao-internal.aliyuncs.com/zabbix%2FunixODBC-2.3.1-11.el7.x86_64.rpm
    wget -O zabbix-agent-3.0.1-1.el7.x86_64.rpm http://ress.oss-cn-qingdao-internal.aliyuncs.com/zabbix%2Fzabbix-agent-3.0.1-1.el7.x86_64.rpm
    rpm -ivh libtool-ltdl-2.4.2-20.el7.x86_64.rpm
    rpm -ivh unixODBC-2.3.1-11.el7.x86_64.rpm
    rpm -ivh zabbix-agent-3.0.1-1.el7.x86_64.rpm
}

do_config(){
    #get ipaddress
    ip=`ifconfig eth0 | grep "inet" | awk '{print $2}'`
    #config agent
    sed -i 's#Server=127.0.0.1#Server='"$zabbixIP"'#g' /etc/zabbix/zabbix_agentd.conf
    sed -i 's#ServerActive=127.0.0.1#ServerActive='"$zabbixIP"'#g' /etc/zabbix/zabbix_agentd.conf
    sed -i 's/\(Hostname=\).*/\1'"$ip"'/g' /etc/zabbix/zabbix_agentd.conf
    sed -i 's/# HostMetadata=/HostMetadata='"$env"-"$product"'/g' /etc/zabbix/zabbix_agentd.conf
    sed -i "s/# UnsafeUserParameters=0/UnsafeUserParameters=1/g" /etc/zabbix/zabbix_agentd.conf
    wget -N -P /etc/zabbix http://ress.oss-cn-qingdao-internal.aliyuncs.com/zabbix/tcp_status_ss.sh
	wget -N -P /etc/zabbix/zabbix_agentd.d http://ress.oss-cn-qingdao-internal.aliyuncs.com/zabbix/tcp_status_ss.conf
    wget -N -P /etc/zabbix http://ress.oss-cn-qingdao-internal.aliyuncs.com/zabbix/get_jvmlist.sh
	wget -N -P /etc/zabbix http://ress.oss-cn-qingdao-internal.aliyuncs.com/zabbix/get_jvmstatus.sh
	wget -N -P /etc/zabbix http://ress.oss-cn-qingdao-internal.aliyuncs.com/zabbix/jvm_list.sh
	wget -N -P /etc/zabbix http://ress.oss-cn-qingdao-internal.aliyuncs.com/zabbix/set_jvmstatus.sh
	wget -N -P /etc/zabbix/zabbix_agentd.d http://ress.oss-cn-qingdao-internal.aliyuncs.com/zabbix/userparameter_jvm.conf
	chmod +x /etc/zabbix/*.sh
	sed -i 's/# AllowRoot=0/AllowRoot=1/g' /etc/zabbix/zabbix_agentd.conf
	cat /var/spool/cron/root | grep '/etc/zabbix/jvm_list.sh'
	if [ $? -ne 0 ]
	then
    echo "24 * * * * /bin/bash /etc/zabbix/jvm_list.sh" >>/var/spool/cron/root
    echo "*/5 * * * * /bin/bash /etc/zabbix/get_jvmstatus.sh" >>/var/spool/cron/root
	fi
}

do_system_enable(){
    systemctl restart zabbix-agent.service
    systemctl enable zabbix-agent.service
}

do_attach(){
    echo 'env'
    echo $env
    echo 'product'
    echo $product
    echo 'zabbixIP'
    echo $zabbixIP
    echo 'download_zabbix'
    download_zabbix
    echo 'do_config'
    do_config
    echo 'do_system_enable'
    do_system_enable
    echo 'done'
    exit
    exit
}


while [[ $# > 1 ]]
do
    key=$1
    shift
    case "$key" in
        --env)
            env=$1
            shift
            ;;
        --product)
            product=$1
            shift
            ;;
        --zabbixIP)
            zabbixIP=$1
            shift
            ;;
        *)
            echo "usage: $0 <--env env> <--product product> <--zabbixIP zabbixIP>"
            exit 1
            ;;
    esac
done

do_attach