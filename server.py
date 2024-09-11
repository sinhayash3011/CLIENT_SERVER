#server.py
import socket
import threading
import ssl
from datetime import datetime, timedelta, timezone
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

def generate_self_signed_cert():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"IN"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Karnataka"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"Bangalore"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"My Calculator"),
        x509.NameAttribute(NameOID.COMMON_NAME, u"192.168.0.111"),
    ])

    cert = x509.CertificateBuilder().subject_name(
    subject
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.now(timezone.utc)
    ).not_valid_after(
        datetime.now(timezone.utc) + timedelta(days=365)
    ).sign(private_key, hashes.SHA256(), default_backend())

    private_key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

    cert_bytes = cert.public_bytes(serialization.Encoding.PEM)

    with open("server.key", "wb") as key_file:
        key_file.write(private_key_bytes)

    with open("server.crt", "wb") as cert_file:
        cert_file.write(cert_bytes)

# Generate self-signed certificate and private key
generate_self_signed_cert()

def calculator(A, B, op):
    if op.lower() in ('add', '+'):
        return A + B
    elif op.lower() in ('sub', '-'):
        return A - B
    elif op.lower() in ('mul', 'x', '*'):
        return A * B
    elif op.lower() in ('div', '/'):
        if B != 0:
            return A / B
        else:
            return "Error: Division by zero"
    elif op.lower() in ('exp', '^','**'):
        return A ** B
    elif op.lower() in ('mod', '%'):
        return A % B
    else:
        return "Error: Invalid operation"

def handle_client(connectionSocket, addr):
    print("Connection from", addr)
    try:
        while True:
            input_data = connectionSocket.recv(1024).decode()
            if not input_data:
                break
            data = input_data.split()
            result = calculator(int(data[0]), int(data[2]), data[1])
            connectionSocket.send(str(result).encode())
    finally:
        connectionSocket.shutdown(socket.SHUT_RDWR)
        connectionSocket.close()

serverPort = 15000
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(("", serverPort))
print('The server is ready to receive')

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="server.crt", keyfile="server.key")

serverSocket.listen(5)

while True:
    connectionSocket, addr = serverSocket.accept()
    ssl_connectionSocket = context.wrap_socket(connectionSocket, server_side=True) #wraps with ssl encryption
    client_thread = threading.Thread(target=handle_client, args=(ssl_connectionSocket, addr))
    client_thread.start()
