import tkinter as tk
from audio import record_audio, play_canned_message, play_recent_audio, save_audio
import sys
import socket
import errno
from main import SEAHAWK_IP_ADDRESS



def start_gui_server():
    global push_to_talk_button
    global text_entry

    window = tk.Tk()
    window.title("Radio Comms(Server)")

    push_to_talk_button = tk.Button(window, text="Push to Talk1", command=push_to_talk_press)
    push_to_talk_button.pack()

    text_entry = tk.Entry(window)
    text_entry.pack()

    send_button = tk.Button(window, text="Send Text Message", command=send_text_message)
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


start_gui_server()