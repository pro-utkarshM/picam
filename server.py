import socket
import subprocess

# This script does not require changes for RPi 5 compatibility.
# It receives a network stream and plays it using VLC.
# Ensure VLC is installed on the machine running this script.
# On Debian/Ubuntu/Raspberry Pi OS: sudo apt install vlc

# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(0)

# Accept a single connection and make a file-like object out of it
print("Server listening on port 8000. Waiting for a connection...")
connection = server_socket.accept()[0].makefile('rb')
print("Connection received. Starting player...")

try:
    # --- THIS LINE IS CHANGED ---
    # We add '--live-caching=100' to reduce the playback buffer to 100ms
    cmdline = ['vlc', '--demux', 'h264', '--avcodec-hw=none', '--live-caching=100', '-']
    player = subprocess.Popen(cmdline, stdin=subprocess.PIPE)
    while True:
        # Repeatedly read 1k of data from the connection and write it to
        # the media player's stdin
        data = connection.read(1024)
        if not data:
            break
        player.stdin.write(data)
finally:
    print("Connection closed.")
    connection.close()
    server_socket.close()
    if 'player' in locals():
        player.terminate()
