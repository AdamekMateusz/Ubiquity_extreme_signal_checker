import socket,time,os
from ssh2.session import Session
import datetime




def start_function():
    #we get simple information for the users
    login=input("Please give login: ")
    passwd=input("Please give password: ")
    subnet=input("Please give subnet just like that 192.168.1.0: ")
    port_connection=input("Please give port which you use to connect with SSH: ")
    cut_of_signal=input("Please give value when signal will be accepted like critical: ")

    #we modify subnet like that nmap scan for all subnet
    subnet=subnet.split('.')
    search_sub=".".join(subnet[0:(len(subnet)-1)])
    print(search_sub)
    subnet[-1]='*'
    subnet=".".join(subnet)
    #awk '{print $6}' get all IP addres which nmap search with open ports
    column="awk '{print $6}'"
    filepath="/home/mateusz/Desktop/temp_file.txt"
    #all search Ip will be save to tempoaray file
    y=os.system(f"nmap -p {port_connection} --open {subnet} | grep {search_sub} | {column} > {filepath}")

    #we read from the file
    f=open(filepath,mode='r')
    #all ip is writing to the list
    ip_list=f.readlines()
    f.close()
    #the file is closing and will be removed
    os.system(f"rm -r {filepath}")

    #ip was writing in the list looks like (176.99.54.27), in this part the () will be removed

    new_one = []
    for ip in ip_list:
        ip=ip.replace('\n',"")
        ip=ip.replace("(","")
        ip = ip.replace(")", "")
        new_one.append(ip)

    print(new_one)
    print(new_one[-1])
    print(type(new_one[-1]))
    #here we return all date which we need to login
    return login, passwd,int(port_connection),new_one,cut_of_signal



def login_fun(user="admin",password="admin",port=22,host='192.168.1.1'):

    #we name aour output file using currency data and hour
    data_obj = datetime.datetime.now()
    data_obj = str(data_obj)
    data_obj = data_obj.replace("-", "_")
    data_obj = data_obj.replace(" ", "_")
    data_obj = data_obj.replace(":", "_")

    print(data_obj[0:16])
    nazwa = "output_all_1" + data_obj[0:16] + ".txt"
    os.system(f"touch {nazwa}")
    directory = os.getcwd()

    filepath=directory+"/"+nazwa

    #we create secound file which get singal above cut_of_signal which we load from keyboard
    nazwa_v2="extreme_signal"+ data_obj[0:16] + ".txt"
    filepath_v2 = directory + "/" + nazwa_v2


    f = open(filepath, "a")
    main_list=[]
    #iteration over all hosts
    for hostname in host:
        #print(type(hostname))
        #print(hostname)
        #print(port)
        #print(type(port))

        #I checked port if is open, if open return return 0, above I first search with nmap open ports
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if(sock.connect_ex((hostname,port))==0):
            print(f"Port {port} is open ")

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((hostname, port))

            #we are create our sesssion
            session = Session()  # initializing sesion
            session.handshake(sock)
            #try authorize by login and password which we read from keyboard
            try:
                session.userauth_password(user, password)
            except:
                print("Incorretc login or password")
                continue


            channel = session.open_session()
            # start the interactive shell in the channnel
            channel.shell()
            # channel.write("vcgencmd measure_temp\n")
            # channel.write("clear\n")

            #we search our signal in Ubiquity file
            channel.write("mca-status | grep signal\n")
            channel.write("mca-status | grep chain\n")
            time.sleep(1)


            size, data = channel.read()
            my_list = []
            my_list.append(hostname)
            parametr = data.decode()
            parametr = parametr.split('\r\n')
            parametr.pop(-1)
            my_list.extend(parametr)

            #write to file our output form Ubiquity
            #print(my_list)
            zapis = data.decode()
            f.write(str(my_list))
            f.write("\n")
            main_list.append(my_list)
            channel.close()
            print("Exit status: {0}".format(channel.get_exit_status()))
        else:
            print("Port is close")
            continue
    return main_list,filepath_v2
#write to file which caled extremal_signal singla which above cut_of signal
def critical_signal(all,filepath_v2,cutoff='80'):
    for ever in all:
        signal=ever[1].replace("signal=","")
        signal=int(signal)
        f = open(filepath_v2, "a")
        if signal <= int(cutoff):
            f.write(str(ever))
            f.write("\n")


login,passwd,port_connect,hostname,cutoff=start_function()
#print(login)
#print(passwd)
#print(port_connect)
#print(hostname)
all_output,filepath_v2=login_fun(user=login,password=passwd,port=port_connect,host=hostname)
critical_signal(all_output,filepath_v2,cutoff)