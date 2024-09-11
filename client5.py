# # client2.py
# from socket import *

# serverName = 'localhost'
# serverPort = 15000
# clientSocket = socket(AF_INET, SOCK_STREAM)

# try:
#     clientSocket.connect((serverName, serverPort))

#     print("Welcome to server's calculator")
#     while True:
#         print('Do you wish to calculate: 1.Yes 2.No')
#         choice = input()
#         if choice == '1':
#             sentence = input("Enter operation (e.g., '2 + 3'): ")
#             clientSocket.send(sentence.encode())
#             modifiedSentence = clientSocket.recv(1024)
#             print("From Server:", modifiedSentence.decode())
#         elif choice == '2':
#             print('Disconnected')
#             break
#         else:
#             print('Invalid input')
            
# except KeyboardInterrupt:
#     print("\nClient program terminated by user.")
# except ConnectionError as e:
#     print(f"Connection error: {e}")

# clientSocket.close()
from socket import *
import tkinter as tk
from tkinter import messagebox

def calculate():
    choice = choice_var.get()
    if choice == '1':
        operation = operation_entry.get()
        clientSocket.send(operation.encode())
        modifiedSentence = clientSocket.recv(1024).decode()
        result_label.config(text="Result: " + modifiedSentence)
    elif choice == '2':
        messagebox.showinfo("Disconnected", "Disconnected from server")
        clientSocket.close()
        root.destroy()
    else:
        messagebox.showerror("Error", "Invalid input")

serverName = 'localhost'
serverPort = 15000
clientSocket = socket(AF_INET, SOCK_STREAM)

try:
    clientSocket.connect((serverName, serverPort))

    root = tk.Tk()
    root.title("Calculator Client")

    choice_var = tk.StringVar()
    operation_label = tk.Label(root, text="Enter operation (e.g., '2 + 3'): ")
    operation_label.pack()
    operation_entry = tk.Entry(root)
    operation_entry.pack()

    choice_frame = tk.Frame(root)
    choice_frame.pack()
    choice_label = tk.Label(choice_frame, text="Do you wish to calculate:")
    choice_label.pack(side="left")
    choice_radio1 = tk.Radiobutton(choice_frame, text="Yes", variable=choice_var, value='1')
    choice_radio1.pack(side="left")
    choice_radio2 = tk.Radiobutton(choice_frame, text="No", variable=choice_var, value='2')
    choice_radio2.pack(side="left")

    calculate_button = tk.Button(root, text="Calculate", command=calculate)
    calculate_button.pack()

    result_label = tk.Label(root, text="")
    result_label.pack()

    root.mainloop()
    
except KeyboardInterrupt:
    print("\nClient program terminated by user.")
except ConnectionError as e:
    print(f"Connection error: {e}")

clientSocket.close()
