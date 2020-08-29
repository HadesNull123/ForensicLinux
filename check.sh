#!/usr/bin/env bash
Disk="/root/log/$(date +%d-%m-%Y)"
mkdir -p $Disk
chmod 777 $Disk
echo "******** Check log Linux ********"
echo "******** Check all process ********"
users=$(awk -F":" '$7 == "/bin/bash" {print $1}' /etc/passwd)
for i in $users ; do
    ps -elf -u $i > $Disk/ps_$i.txt
    top -b -n 5 -U $i > $Disk/top_$i.txt

done

echo "******** Check port ********"

netstat -ntlpu > $Disk/netstat_ntlpu.txt
netstat -nap > $Disk/netstat_nap.txt

echo "******** Check Crontab ********"
ls -l -R /etc/cron* > $Disk/cron.txt
echo "******** Crontab info ********" >> $Disk/cron.txt
user_cron=$(awk -F":" '$7 == "/bin/bash" {print $1}' /etc/passwd)
for i in $user_cron ; do
    crontab -u $i -l > $Disk/crontab_"$i"
done

echo "******** Check start up ********"

ls -latr /home/*/.bash_profile >> $Disk/1.txt
ls -latr /home/*/.bash_history  >> $Disk/1.txt
ls -latr /home/*/.bash_logout >> $Disk/1.txt
ls -latr /home/*/.bashrc >> $Disk/1.txt
is=$(cat $Disk/1.txt | awk '{print $9}' )
for i in $is ; do
      ik=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 10 | head -n 1)
    cp $i $Disk/$ik.txt
done


echo "******** Check auto start, enviroment, path ********"

service --status-all > $Disk/auto_start.txt
find / -perm -4000 -o -perm -2000 >&/dev/null > $Disk/permission.txt
user_path=$(awk -F":" '$7 == "/bin/bash" {print $1}' /etc/passwd)
for i in $user_path ; do
    sudo -Hiu $i env | grep PATH > $Disk/path.txt
done

echo "******** Check config ********"
cp -r /etc/profile.d $Disk/profile.d


echo "******** Check sudoers ********"

user_sudoers=$(awk -F":" '{print $1}' /etc/passwd)
for i in $user_sudoers ; do
    sudo -l -U $i | grep not || echo "User $i sudo" >> $Disk/User_sudoer.txt
done

echo "******** Check ssh log ********"

cat /var/log/secure* | grep Accepted > $Disk/secure_log.txt

echo "******** Check IPtables ********"
iptables -L -vn -t nat > $Disk/iptables.txt 

echo "******** Find url from source code ********"
chmod +x find_url.py
python find_url.py
cp log_url_ip.txt $Disk

echo "******** Scan Shell ********"
chmod +x VShellScanner
./VShellScanner
cp -R output $Disk

zip -r /root/log_server.zip $Disk

