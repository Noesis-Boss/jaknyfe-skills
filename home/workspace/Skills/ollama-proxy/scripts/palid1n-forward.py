import socket
import socks
import threading
import sys

SOCKS5_HOST = "localhost"
SOCKS5_PORT = 1080
LISTEN_HOST = "127.0.0.1"
LISTEN_PORT = 8020
TARGET_HOST = "100.66.26.103"
TARGET_PORT = 8020

def handle_client(client_sock):
    try:
        proxy_sock = socks.create_connection(
            (TARGET_HOST, TARGET_PORT),
            proxy_type=socks.PROXY_TYPE_SOCKS5,
            proxy_addr=(SOCKS5_HOST, SOCKS5_PORT),
        )
    except Exception as e:
        client_sock.close()
        return

    def relay(src, dst):
        try:
            while True:
                data = src.recv(4096)
                if not data:
                    break
                dst.sendall(data)
        except Exception:
            pass
        finally:
            src.close()
            dst.close()

    t1 = threading.Thread(target=relay, args=(client_sock, proxy_sock), daemon=True)
    t2 = threading.Thread(target=relay, args=(proxy_sock, client_sock), daemon=True)
    t1.start()
    t2.start()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((LISTEN_HOST, LISTEN_PORT))
    server.listen(5)
    print(f"Listening on {LISTEN_HOST}:{LISTEN_PORT}, forwarding via SOCKS5 to {TARGET_HOST}:{TARGET_PORT}", flush=True)
    while True:
        client_sock, addr = server.accept()
        t = threading.Thread(target=handle_client, args=(client_sock,), daemon=True)
        t.start()

if __name__ == "__main__":
    main()