#!/usr/bin/env python
import os
import argparse
import time
import subprocess
import paramiko
import socket

is_run_flink=True
is_run_ts=True
is_run_oai = True
epc_cmd=""
enb_cmd=""
kafka_cmd=""
cmd = "ls"
oai_password="password"

oai_ip ="192.168.200.3"
flink_ip ="192.168.200.1"
tensorflow_ip ="192.168.200.2"

ssh_flink = ""#"user@" + flink_ip
ssh_ts = ""#"user@"+ tensorflow_ip
ssh_oai = ""#"user@"+ oai_ip


args=""
kafka_conf=""
is_kill_all_oai = False
is_run_all_oai = True

def exe_cmd(cmd):
    try:
        print("shell: ", cmd)    
        subprocess.call(cmd, shell=True)
        
    except:    
        print("errno_num")
"""
def run_kafka(args):
    cmd_zk = "xterm -hold -e "
    cmd_zk += args.kafkaDir + "/bin/zookeeper-server-start.sh "
    cmd_zk += args.kafkaDir + "/config/zookeeper.properties &"    
    
    cmd_brokers="xterm -hold -e "
    cmd_brokers += kafka_conf + "/bin/kafka-server-start.sh "
    cmd_brokers += kafka_conf + "/config/server.properties &"

    cmd_consumer = "xterm -hold -e "
    cmd_consumer += kafka_conf + "/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic oai &"

    cmd_producer ="xterm -hold -e "
    cmd_producer += kafka_conf + "/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic oai &"
    
    exe_cmd(cmd_zk)
    time.sleep(2)
    exe_cmd(cmd_brokers)
    time.sleep(3)
    exe_cmd(cmd_consumer)
    time.sleep(2)
    exe_cmd(cmd_producer)
"""
def send_tcp_req(req):
    SERVER_IP=oai_ip
    SERVER_PORT = 60000
    BUFFER_SIZE = 1024
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((SERVER_IP, SERVER_PORT))
        s.send(req)
        print ("senr req to ", SERVER_IP, ": ", req)
        data = s.recv(BUFFER_SIZE)
        s.close()
        print ("Server feedback: ", data)
    except Exception as e:
        print(e)
    
    

def run_mme():
    cmd = 'xterm  -T "mme" -e ssh ' + ssh_oai + ' "/home/user/openair-cn/scripts/run_mme" &'
    exe_cmd(cmd)

def run_hss():
    cmd = 'xterm  -T "hss" -e ssh ' + ssh_oai + ' "/home/user/openair-cn/scripts/run_hss" &'
    exe_cmd(cmd)



def run_spgw():
    cmd = 'xterm  -T "spgw" -e ssh ' + ssh_oai + ' "/home/user/openair-cn/scripts/run_spgw" &'
    exe_cmd(cmd)


def run_epc():
    cmd = "ssh "+ssh_oai+" 'source /home/user/openair-cn/oaienv'"
    exe_cmd(cmd)
    time.sleep(1)
    
    run_hss()
    time.sleep(2)
    run_mme()
    time.sleep(2)
    run_spgw()
    time.sleep(2)

def run_enb():
    cmd ='xterm -T "enb" -e ssh '+ ssh_oai +' " source /home/user/openairinterface5g/oaienv; sudo -E ~/openairinterface5g/cmake_targets/lte_build_oai/build/lte-softmodem -O ~/openairinterface5g/conf/enb.band7.tm1.25PRB.usrpb210.conf" &' 
    exe_cmd(cmd)


def run_zookeeper():
    kfk_dir = '~/app/kafka_2.11-2.1.0'
    cmd = 'xterm  -T \"zookeeper\" -e ssh ' + ssh_oai +' "'
    cmd += kfk_dir + '/bin/zookeeper-server-start.sh '
    cmd += kfk_dir + '/config/zookeeper.properties" &'
    exe_cmd(cmd)

def run_brokers():
    kfk_dir = '~/app/kafka_2.11-2.1.0'
    cmd = 'xterm  -T \"broker\" -e ssh ' + ssh_oai +' "'
    cmd += kfk_dir + '/bin/kafka-server-start.sh '
    cmd += kfk_dir + '/config/server.properties" &'
    exe_cmd(cmd)

def run_producer():
    kfk_dir = '~/app/kafka_2.11-2.1.0'
    cmd = 'xterm -T \"producer\" -e ssh ' +  ssh_oai +' "'
    cmd += kfk_dir + '/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic '+ "oai" +'&'
    exe_cmd(cmd)

def run_consumer():
    kfk_dir = '~/app/kafka_2.11-2.1.0'
    cmd = 'xterm  -T \"consumer\"  -e '
    cmd += kfk_dir + '/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic '+ "oai" +'&'
    exe_cmd(cmd)

def run_flink_app():
    cmd = 'xterm  -T \"flink\" -e ssh ' + ssh_flink +' "cd workspace/spaas;java -Dlog4j.configurationFile="./conf/log4j2.xml" -jar target/FlinkAverager.jar --input-topic oai --output-topic oai-ts --bootstrap.servers '+oai_ip+':9092 --zookeeper.connect '+oai_ip+':2181 --group.id oai --thread.nums 2" &'
    exe_cmd(cmd)

def run_tensorflow():
    cmd = 'xterm  -T \"tensorflow\" -e ssh ' + ssh_ts +' "cd workspace/spaas/ts;python linreg.py" &'
    exe_cmd(cmd)    

def run_ws():
    pass

def run_nc():
    #cmd = 'xterm -T \"nc\" -hold -e ssh ' +  ssh_oai +' "nc -t localhost 60000" &'
    """
    print('copy this command: {"req":"CONFIG_PROTO","name":"kafka", "active":"true","period":1}')
    cmd = "nc -t 192.168.200.3 60000"
    exe_cmd(cmd)
    """
    req = '{"req":"CONFIG_PROTO","name":"kafka", "active":"true","period":1}'
    send_tcp_req(req)
    """
    SERVER_IP=oai_ip
    SERVER_PORT = 60000
    BUFFER_SIZE = 1024
    req = '{"req":"CONFIG_PROTO","name":"kafka", "active":"true","period":1}'
    
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SERVER_IP, SERVER_PORT))
    s.send(req)
    data = s.recv(BUFFER_SIZE)
    s.close()
    print ("Server: ", data)
    """

def run_oai():
    run_epc()
    run_enb()

def run_all():
    run_oai()
    run_zookeeper()
    time.sleep(5)

    run_brokers()
    time.sleep(3)

    run_flink_app()
    time.sleep(3)

    run_tensorflow()
    time.sleep(2)

    run_nc()


def kill_pid(pid):
    cmd ='ssh '+  ssh_oai +' sudo kill '+pid
    exe_cmd(cmd)

def get_pids(grep_item, service_ip):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) #handle no known_hosts error
    ssh.connect(service_ip, username='user', password=oai_password)
    stdin, stdout, stderr = ssh.exec_command("ps aux | grep "+grep_item+" | grep -v grep | awk '{print $2}'")
    #stdin.write('mme pids:\n')
    stdin.flush()
    stdout=stdout.readlines()
    ssh.close()
    pids=[]
    for p in stdout:
        pids.append(p[:-1]) #remove last char, which is \n

    return pids

def kill_zookeeper():
    print("killing zookeeper..")
    for pid in get_pids("zookeeper.properties", oai_ip):
        cmd = 'ssh ' + ssh_oai + ' "sudo kill ' + pid + '"'
        exe_cmd(cmd)    

def kill_brokers():
    print("killing brokers..")
    for pid in get_pids("server.properties", oai_ip):
        cmd = 'ssh ' + ssh_oai + ' "sudo kill -9 ' + pid + '"'
        exe_cmd(cmd)

def kill_mme():
    print("killing mme..")
    for pid in get_pids("mme", oai_ip):
        cmd = 'ssh ' + ssh_oai + ' "sudo kill ' + pid + '"'
        exe_cmd(cmd)

def kill_spgw():
    print("killing spgw..")
    for pid in get_pids("spgw", oai_ip):
        cmd = 'ssh ' + ssh_oai + ' "sudo kill ' + pid + '"'
        exe_cmd(cmd)

def kill_hss():
    print("killing hss..")
    for pid in get_pids("hss", oai_ip):
        cmd = 'ssh ' + ssh_oai + ' "sudo kill ' + pid + '"'
        exe_cmd(cmd)

def kill_epc():
    kill_mme()
    kill_spgw()
    kill_hss()

def kill_enb():
    print("killing enb..")
    for pid in get_pids("lte-softmodem", oai_ip):
        cmd = 'ssh ' + ssh_oai + ' "sudo kill ' + pid + '"'
        exe_cmd(cmd)

def kill_flink():
    print("killing flink..")
    for pid in get_pids("java", flink_ip):
        cmd = 'ssh ' + ssh_flink + ' "echo password | sudo -S kill ' + pid + '"'
        exe_cmd(cmd)

def kill_tensorflow():
    print("killing tensorflow..")
    for pid in get_pids("python", tensorflow_ip):
        cmd = 'ssh ' + ssh_ts + ' "echo password | sudo -S kill ' + pid + '"'
        exe_cmd(cmd)

def kill_oai():
    kill_epc()
    kill_enb()

def kill_nc():
    req='{"req":"CONFIG_PROTO","name":"kafka", "active":"false"}'
    send_tcp_req(req)
    

def kill_all():
    kill_tensorflow()
    time.sleep(1)
    kill_flink()
    time.sleep(2)

    kill_oai()
    time.sleep(2)

    kill_brokers()
    time.sleep(5)
    kill_zookeeper()
    time.sleep(1)


def main(args):
    
    if args.run_all:
        run_all()

    if args.run_all_oai:
        run_oai()

    if args.run_epc:
        run_epc()
    
    if args.run_enb:
        run_enb()

    if  args.run_zookeeper :  #"false" or args.run_zookeeper == "f") or (args.kill_zookeeper == "true" or args.kill_zookeeper == "t") or args.kill_all =="true" or args.kill_all =="t":
        run_zookeeper()
        time.sleep(2)

    if args.run_kafka_brokers:
        """
        brokers depend on zookeeper
        """
        run_zookeeper()
        time.sleep(2)
        run_brokers()
        time.sleep(2)

    if args.run_flink_app:
        run_flink_app()
        time.sleep(3) 

    if args.run_tensorflow:
        run_tensorflow()
        time.sleep(2)

    if args.run_nc:
        run_nc()

    if args.kill_nc:
        kill_nc()


    """
    Kill services
    """
    if args.kill_all:
        kill_all()


    if args.kill_all_oai:
        kill_oai()

    if args.kill_epc:
        kill_epc()

    if args.kill_enb:
        kill_enb()

    if args.kill_zookeeper :
        kill_brokers()
        time.sleep(3)
        kill_zookeeper()

    if args.kill_kafka_brokers :
        kill_brokers()
        time.sleep(3)

    if args.kill_tensorflow:
        kill_tensorflow()

    if args.kill_flink_app:
        kill_flink()


if __name__ =="__main__":
    
    parser = argparse.ArgumentParser()

    parser.add_argument("--run_all","-rall", action='store_true', help="run all")
  
    parser.add_argument("--run_all_oai","-rao", action='store_true', help="run all aoi: epc and enb")
    parser.add_argument("--run_epc","-repc", action='store_true', help="run epc")
    parser.add_argument("--run_enb","-renb", action='store_true', help="run enb")
    
    parser.add_argument("--run_zookeeper","-rz", action='store_true', help="run zookeeper -rk true/t")
    parser.add_argument("--run_kafka_brokers","-rkb", action='store_true', help="run kafka -rk t/true")
    
    parser.add_argument("--run_nc","-rnc", action='store_true',help="run netcate -nc t/true")
    
    parser.add_argument("--run_flink_app","-rfa", action='store_true',help="run flink app -rfa t/true")
    
    parser.add_argument("--run_tensorflow","-rts", action='store_true',help="run tensorflow -rts t/true")
    
    parser.add_argument("--kill_all","-kall", action='store_true',help="kill all services: -kall true/t ")

    parser.add_argument("--kill_all_oai","-kao",action='store_true',help="kill all aoi: epc and enb: -kao t or -kao true")
    parser.add_argument("--kill_zookeeper","-kz",action='store_true',help="kill zookeeper: -kz t or -kz true")
    parser.add_argument("--kill_kafka_brokers","-kfb",action='store_true',help="kill brokers: -kb t or -kb true")

    parser.add_argument("--kill_epc","-kepc", action='store_true', help="kill epc")
    parser.add_argument("--kill_enb","-kenb", action='store_true', help="kill enb")

    parser.add_argument("--kill_flink_app","-kfa",action='store_true',help="kill flink app: -kf")
    parser.add_argument("--kill_tensorflow","-kts",action='store_true',help="kill tensorflow: -kts")

    parser.add_argument("--kill_nc","-knc",action='store_true',help="stop aoi kafak via tcp")


    parser.add_argument("--kafkaDir","-dir",help="root directory of Kafka")
    parser.add_argument("--runZookeeper","-zookeeper", action='store_true',help="run zookeeper")
    parser.add_argument("--runBrokers","-brokers", action='store_true', help="run brokers")
    parser.add_argument("--runProduer","-produer", action='store_true',help="run producer")
    parser.add_argument("--runConsumer","-consumer", action='store_true',help="run consumer")
    parser.add_argument("--kafkaTopic","-topic", action='store_true',help="Kafka topic")
    
    parser.add_argument("--spgwNic","-nic",help="network interface for spgw")
    parser.add_argument("--enb","-e",help="enb autorun")

    parser.add_argument("--oai_ip","-oip",help="OAI ip")
    parser.add_argument("--flink_ip","-fip",help="flink ip")
    parser.add_argument("--tensorflow_ip","-tsip",help="tensorflow ip")

    
    args = parser.parse_args()
    
    if not args.oai_ip ==None:
        oai_ip = args.oai_ip

    if not args.flink_ip==None:
        flink_ip= args.flink_ip

    if not args.tensorflow_ip == None:
        tensorflow_ip= args.tensorflow_ip

    if args.kafkaDir==None:
        args.kafkaDir = "~/app/kafka_2.11-2.1.0"
    
    if args.kafkaTopic==None:
        args.kafkaTopic = "oai"

    if args.spgwNic == None:
        args.spgwNic = "wlp2s0"

    ssh_flink = "user@" + flink_ip
    ssh_ts = "user@"+ tensorflow_ip
    ssh_oai = "user@"+ oai_ip
    
    
    main(args)
