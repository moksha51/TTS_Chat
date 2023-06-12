import socket
import time
import datetime
import tkinter as tk
import audio

SERVER_ADDRESS = 'localhost'
PORT = 5000

def connect_to_server():
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((SERVER_ADDRESS, PORT))
            print(f"[{get_timestamp()}] Client to Server Connection Established")
            break
        except socket.error as e:
            print(f"[{get_timestamp()}] Failed to connect from client to server. Retrying connection...")
            time.sleep(2)


def get_timestamp():
    return datetime.datetime.now().strftime("%H:%M:%S_%d-%b-%Y")

def push_to_talk_press():
    push_to_talk_button.config(bg='red')
    audio.record_audio()
    print("Audio Recording Started")


def push_to_talk_release():
    push_to_talk_button.config(bg='SystemButtonFace')
    audio.save_audio()
    print("Audio Recording Stopped")


def send_text_message():
    sent_text = text_entry.get()
    print('Base:' + sent_text)
    text_entry.delete(0, tk.END)


def play_siren_sound():
    play_canned_message("siren.wav")


def play_canned_message2():
    play_canned_message("canned2.wav")


def play_canned_message3():
    play_canned_message("canned3.wav")


def play_recent_audio_message():
    play_recent_audio()
    print("Replaying most recent audio transmission")



def start_gui_client():
    global push_to_talk_button
    global text_entry

    window = tk.Tk()
    window.title("Radio Comms (Client)")

    push_to_talk_button = tk.Button(window, text="Push to Talk1", command=push_to_talk_press)
    push_to_talk_button.pack()

    text_entry = tk.Entry(window)
    text_entry.pack()

    send_button = tk.Button(window, text="Send", command=send_text_message)
    send_button.pack()

    canned_button1 = tk.Button(window, text="Siren", command=play_canned_message1)
    canned_button1.pack()

    canned_button2 = tk.Button(window, text="SOS", command=play_canned_message2)
    canned_button2.pack()

    canned_button3 = tk.Button(window, text="Fisherman", command=play_canned_message3)
    canned_button3.pack()

    recent_audio_button = tk.Button(window, text="Replay Last Message", command=play_recent_audio_message)
    recent_audio_button.pack()

    window.mainloop()


start_gui_client()
