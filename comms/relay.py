#!/home/erick/.local/share/uv/python/cpython-3.13.2-linux-x86_64-gnu/bin/python3.13
"""TCP relay for CommunicationMod.

CommunicationMod launches this script as its external process. It:
1. Sends "ready\n" on stdout to signal CommunicationMod
2. Opens a TCP server on localhost:38281
3. Forwards CommunicationMod stdin (game state JSON) -> TCP client
4. Forwards TCP client messages -> stdout (commands to CommunicationMod)
5. Handles client disconnect/reconnect without crashing

Configure CommunicationMod external command to:
    python /data/code/sts_bot_2/comms/relay.py
"""

import sys
import socket
import threading
import select
import time

HOST = "localhost"
PORT = 38281


def stdin_to_client(client_lock, client_holder):
    """Read lines from stdin (CommunicationMod) and forward to TCP client."""
    while True:
        line = ""
        while True:
            ch = sys.stdin.read(1)
            if ch == "" or ch == "\n":
                break
            line += ch
        if not line:
            continue
        with client_lock:
            conn = client_holder.get("conn")
            if conn is not None:
                try:
                    conn.sendall((line + "\n").encode("utf-8"))
                except (BrokenPipeError, ConnectionResetError, OSError):
                    client_holder["conn"] = None


def client_to_stdout(client_lock, client_holder):
    """Read lines from TCP client and forward to stdout (CommunicationMod)."""
    buf = ""
    while True:
        with client_lock:
            conn = client_holder.get("conn")
        if conn is None:
            time.sleep(0.05)
            continue
        try:
            ready, _, _ = select.select([conn], [], [], 0.1)
            if not ready:
                continue
            data = conn.recv(4096)
            if not data:
                with client_lock:
                    client_holder["conn"] = None
                buf = ""
                continue
            buf += data.decode("utf-8")
            while "\n" in buf:
                line, buf = buf.split("\n", 1)
                if line:
                    print(line, end="\n", flush=True)
        except (ConnectionResetError, BrokenPipeError, OSError):
            with client_lock:
                client_holder["conn"] = None
            buf = ""


def accept_clients(server, client_lock, client_holder):
    """Accept new TCP client connections, replacing any existing one."""
    while True:
        conn, addr = server.accept()
        with client_lock:
            old = client_holder.get("conn")
            if old is not None:
                try:
                    old.close()
                except OSError:
                    pass
            client_holder["conn"] = conn


def main():
    # Signal CommunicationMod that we're ready
    print("ready", end="\n", flush=True)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(1)

    client_lock = threading.Lock()
    client_holder = {"conn": None}

    t_accept = threading.Thread(target=accept_clients, args=(server, client_lock, client_holder), daemon=True)
    t_stdin = threading.Thread(target=stdin_to_client, args=(client_lock, client_holder), daemon=True)
    t_stdout = threading.Thread(target=client_to_stdout, args=(client_lock, client_holder), daemon=True)

    t_accept.start()
    t_stdin.start()
    t_stdout.start()

    # Keep main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        server.close()


if __name__ == "__main__":
    main()
