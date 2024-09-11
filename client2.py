# client2.py
import socket
import ssl

serverName = '192.168.103.170'
serverPort = 15000

# Create a TCP socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Create an SSL context
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    # Establish a connection with the server using SSL
    with context.wrap_socket(clientSocket, server_hostname=serverName) as ssl_clientSocket:
        ssl_clientSocket.connect((serverName, serverPort))

        print("Welcome to the server's calculator")
        while True:
            print('Do you wish to calculate: 1.Yes 2.No')
            choice = input()
            if choice == '1':
                sentence = input("Enter operation[EG:2+3 ; PLEASE SPACE BETWEEN EACH INPUT]: ")
                ssl_clientSocket.send(sentence.encode())
                modifiedSentence = ssl_clientSocket.recv(1024)
                print("From Server:", modifiedSentence.decode())
            elif choice == '2':
                print('Disconnected from server!!!!!')
                break
            else:
                print('Invalid input')

except KeyboardInterrupt:
    print("\nClient program terminated by user.")
except ConnectionError as e:
    print(f"Connection error: {e}")

# Close the SSL client socket
ssl_clientSocket.close()
