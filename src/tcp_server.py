import socket
import threading

def start_socket_server():
    host = '127.0.0.1'
    port = 4544

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"[SOCKET] TCP-сервер запущено на {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"[SOCKET] Нове підключення: {addr}")
        client_socket.sendall(f"Привіт з TCP сервера!\n")
        client_socket.close()