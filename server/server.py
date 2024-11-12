import socket
import threading
from datetime import datetime

# server configs
HOST = '127.0.0.1'
PORT = 65432

clients = {}
messages = []

def handle_client(conn, addr):
    conn.sendall(b"Enter a username: \n")
    username = conn.recv(1024).decode('utf-8').strip()
    if username in clients:
        conn.sendall(b"username already taken. disconnecting...")
        conn.close()
        return
    
    clients[username] = conn
    broadcast_all(f"{username} has joined the server.", "server")
    conn.sendall(b"here are the last two messages:\n")
    for msg in messages[-2:]:
        conn.sendall((msg + "\n").encode('utf-8'))

    
    # handle client messages
    while True:
        try:
            data = conn.recv(1024).decode('utf-8').strip()
            if data == "%leave":
                leave_group(username)
                break
            elif data.startswith("%post"):
                _, message = data.split(" ", 1)
                post_message(username, message)
            elif data == "%users":
                send_user_list(conn)
            elif data.startswith("%message"):
                _, message_id = data.split()
                send_message_content(conn, message_id)
            else:
                conn.sendall("unknown command \n")
        except:
            break
    conn.close()

def broadcast_all(message, sender):
    formatted_message = f"{datetime.now()} - {sender}: {message} \n"
    print(formatted_message)
    for username, client_conn in clients.items():
        try:
            client_conn.sendall(formatted_message.encode('utf-8'))
        except:
            continue

def post_message(username, body):
    message_id = len(messages) + 1
    post_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"Message {message_id} by {username} on {post_date} : {body}"
    messages.append(message)

    broadcast_all(message, username)

def send_user_list(conn):
    user_list = ', '.join(clients.keys())
    conn.sendall(f"users: {user_list}".encode('utf-8'))

def send_message_content(conn, message_id):
    try:
        index = int(message_id) - 1
        # print(f"message index: {index}")
        if 0 <= index < len(messages):
            conn.sendall(messages[index].encode('utf-8'))
        else:
            conn.sendall(f"message not found, should be in the range 1 - {messages.length}, inclusive.\n".encode('utf-8'))
    except:
        conn.sendall("invalid message id \n".encode('utf-8'))

def leave_group(username):
    del clients[username]
    broadcast_all(f"{username} has left the server.", "server")
    update_user_list()

def update_user_list():
    user_list = ', '.join(clients.keys())
    for client_conn in clients.values():
        client_conn.sendall(f"users: {user_list}".encode('utf-8'))

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"server started on host {HOST} and port {PORT}")

    while True:
        conn, addr = server.accept()
        print(f"client requested connection: {conn}, {addr}")
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    main()
