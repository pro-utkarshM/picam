import socket
import time
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput # <--- CHANGE 1: This import is needed

# Connect a client socket to my_server:8000 (change my_server to the
# hostname or IP address of your server)
client_socket = socket.socket()
# !!! IMPORTANT !!!
# Replace 'my_server' with the IP address of the computer running the server script.
client_socket.connect(('192.168.68.111', 8000))

# Make a file-like object out of the connection
connection = client_socket.makefile('wb')

try:
    # Initialize the Picamera2 library
    picam2 = Picamera2()

    # Configure the camera for video recording
    video_config = picam2.create_video_configuration(main={"size": (640, 480)})
    picam2.configure(video_config)

    # Use the H.264 encoder
    encoder = H264Encoder(bitrate=1000000)
    
    # CHANGE 2: Wrap the connection in the FileOutput object
    output = FileOutput(connection)

    print("Camera initialized. Starting stream...")
    # CHANGE 3: Use the new 'output' object here
    picam2.start_recording(encoder, output)

    # Stream for 60 seconds
    time.sleep(60)

    # Stop recording
    picam2.stop_recording()
    print("Stream finished.")

finally:
    connection.close()
    client_socket.close()
    if 'picam2' in locals():
        picam2.close()
