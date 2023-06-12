import socket
import pyaudio
import threading
import wave
import datetime
import os
import time
import tkinter as tk

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
SERVER_ADDRESS = 'localhost'
PORT = 5000
RECORDINGS_FOLDER = "ReceivedAudioRecordings"
CANNED_MESSAGES_FOLDER = "CannedAudioRecordings"

def audio_sender(sock):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    while True:
        try:
            data = stream.read(CHUNK)
            sock.sendall(data)
        except socket.error as e:
            print(f"Socket error: {e}")
            break

    stream.stop_stream()
    stream.close()
    audio.terminate()
    sock.close()

def record_audio(frames):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    while True:
        data = stream.read(CHUNK)
        frames.append(data)

def save_audio(frames, folder):
    if frames:
        timestamp = datetime.datetime.now().strftime("%H%M%S_%d%m%Y")
        filename = f"{timestamp}_recording.wav"
        directory = os.path.join(os.getcwd(), folder)

        if not os.path.exists(directory):
            os.makedirs(directory)

        file_path = os.path.join(directory, filename)

        wf = wave.open(file_path, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(pyaudio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        if folder == RECORDINGS_FOLDER:
            print("Audio Recording Archived on Client Side")
        elif folder == os.path.join(os.getcwd(), RECORDINGS_FOLDER):
            print("Audio Recording Received on Server Side")

def play_canned_message(message_file):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        output=True)

    file_path = os.path.join(os.getcwd(), CANNED_MESSAGES_FOLDER, message_file)

    if not os.path.exists(file_path):
        print("Canned message file does not exist")
        return

    wf = wave.open(file_path, 'rb')

    while True:
        data = wf.readframes(CHUNK)
        if not data:
            break
        stream.write(data)

    wf.close()
    stream.stop_stream()
    stream.close()
    audio.terminate()

    print("Prerecorded Audio File Sent")

def play_recent_audio():
    directory = os.path.join(os.getcwd(), RECORDINGS_FOLDER)
    files = os.listdir(directory)
    files.sort(key=lambda x: os.path.getctime(os.path.join(directory, x)), reverse=True)

    if not files:
        print("No recent audio recordings found")
        return

    recent_file = files[0]
    file_path = os.path.join(directory, recent_file)

    if not os.path.exists(file_path):
        print("Recent audio file does not exist")
        return

    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        output=True)

    wf = wave.open(file_path, 'rb')

    while True:
        data = wf.readframes(CHUNK)
        if not data:
            break
        stream.write(data)

    wf.close()
    stream.stop_stream()
    stream.close()
    audio.terminate()

    print("Replaying most recent audio transmission")

def connect_to_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (SERVER_ADDRESS, PORT)

    while True:
        try:
            sock.connect(server_address)
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S_%d-%b-%Y')}] Client to Server Connection Established")
            return sock
        except socket.error as e:
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S_%d-%b-%Y')}] Fail to connect from client to server, retrying connection")
            time.sleep(2)

def start_audio():
    sock = connect_to_server()
    frames = []

    send_thread = threading.Thread(target=audio_sender, args=(sock,))
    send_thread.start()

    recording_thread = threading.Thread(target=record_audio, args=(frames,))
    recording_thread.start()

    while True:
        if not send_thread.is_alive() or not recording_thread.is_alive():
            break

    save_audio(frames, RECORDINGS_FOLDER)
    save_audio(frames, os.path.join(os.getcwd(), RECORDINGS_FOLDER))