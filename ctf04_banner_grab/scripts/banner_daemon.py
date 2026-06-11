#!/usr/bin/env python3

import socket
import threading
import datetime

HOST="0.0.0.0"

DAEMONS = {
  110: ("FLAG{id1YnQWd}\n"),
  9001: ("FLAG{FkdENVQm}\n"),
  55389: ("FLAG{TvKxYN9Q}\n"),
}

def handle_client(conn, addr, banner):
  with conn:
    conn.sendall(banner.encode())

def listen_on_port(port, banner):
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, port))
    s.listen(5)
    print(f"listening on port {port}")
    while True:
      conn, addr = s.accept()
      print(f"connection from {addr[0] on port {port}")
      threading.Thread(
        target=handle_client,
        args=(conn, addr, banner),
        daemon=True
      ).start()

def main():
  for port, banner in DAEMONS.items():
    t = threading.Thread(
      target=listen_on_port,
      args=(port, banner),
      daemon=True
    )
    t.start()
  #keep main thread alive
  while True:
    pass

if __name__ == "__main__":
  main()
