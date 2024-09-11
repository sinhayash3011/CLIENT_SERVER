#client3 GUI
import socket
import ssl
import tkinter as tk
from tkinter import messagebox

def calculate():
    operation = operation_entry.get()
    ssl_clientSocket.send(operation.encode())
    modifiedSentence = ssl_clientSocket.recv(1024).decode()
    result_label.config(text="Result: " + modifiedSentence)

def disconnect():
    messagebox.showinfo("Disconnected", "Disconnected from server")
    ssl_clientSocket.close()
    root.destroy()

serverName = 'localhost'
serverPort = 15000

# Create a TCP socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Create an SSL context
context = ssl.create_default_context()

try:
    # Load the server's certificate
    context.load_verify_locations('server.crt')

    # Establish a connection with the server using SSL
    ssl_clientSocket = context.wrap_socket(clientSocket, server_hostname=serverName)
    ssl_clientSocket.connect((serverName, serverPort))

    root = tk.Tk()
    root.title("SSL-TCP-CLIENT")
    root.geometry("400x200")  # Set window size
    root.configure(bg='#F9F5E1')  # Set background color

    operation_label = tk.Label(root, text="Enter operation(EG:- 2 + 3: please give space after each input): ", bg='#F9F5E1')
    operation_label.pack()
    operation_entry = tk.Entry(root, width=30)  # Make the entry field wider
    operation_entry.pack()

    calculate_button = tk.Button(root, text="Calculate", command=calculate, bg='#7D3C98', fg='white', width=20, height=2)  # Increase button size
    calculate_button.pack()

    exit_button = tk.Button(root, text="Exit", command=disconnect, bg='#633974', fg='white', width=20, height=2)  # Increase button size
    exit_button.pack()

    result_label = tk.Label(root, text="", bg='#F9F5E1')
    result_label.pack()

    root.mainloop()
    
except KeyboardInterrupt:
    print("\nClient program terminated by user.")
except ConnectionError as e:
    messagebox.showerror("Connection Error", f"Connection error: {e}")
    ssl_clientSocket.close()
    root.destroy()
