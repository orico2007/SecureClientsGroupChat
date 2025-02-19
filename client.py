import socket
import ssl
import threading
import tkinter as tk
from tkinter import simpledialog, scrolledtext
import protocol

class Client:
    def __init__(self, master):
        self.master = master
        self.master.title("Client Chat")
        self.master.geometry("400x500")
        self.night_mode = True
        self.username = self.askUsername()
        self.ADDR = ("192.168.1.246", 8080)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        self.context.load_verify_locations(cafile="server.crt")
        self.s = self.context.wrap_socket(self.s, server_hostname="192.168.1.246")
        self.s.connect(self.ADDR)
        protocol.sendWithSize(self.username, self.s)
        self.chat_display = scrolledtext.ScrolledText(self.master, width=45, height=15, wrap=tk.WORD, font=("Arial", 12))
        self.chat_display.pack(padx=10, pady=10)
        self.chat_display.config(state=tk.DISABLED)
        self.message_entry = tk.Entry(self.master, width=40, font=("Arial", 12), relief=tk.SOLID, bd=1)
        self.message_entry.pack(padx=10, pady=10)
        self.send_button = tk.Button(self.master, text="Send", command=self.sendMessage, font=("Arial", 12, "bold"), relief=tk.RAISED)
        self.send_button.pack(padx=10, pady=10)
        self.night_mode_button = tk.Button(self.master, text="Toggle Night Mode", command=self.toggleNightMode, font=("Arial", 10), relief=tk.RAISED)
        self.night_mode_button.pack(padx=10, pady=5)
        self.master.bind('<Return>', self.onEnterPressed)
        self.setColors()
        threading.Thread(target=self.recvMessage, daemon=True).start()

    def setColors(self):
        if self.night_mode:
            self.bg_color = "#2e2e2e"
            self.fg_color = "#ffffff"
            self.button_bg = "#4CAF50"
            self.button_fg = "#ffffff"
            self.entry_bg = "#555555"
            self.entry_fg = "#ffffff"
        else:
            self.bg_color = "#f0f0f0"
            self.fg_color = "#000000"
            self.button_bg = "#4CAF50"
            self.button_fg = "#ffffff"
            self.entry_bg = "#ffffff"
            self.entry_fg = "#000000"

        self.master.config(bg=self.bg_color)
        self.chat_display.config(bg=self.bg_color, fg=self.fg_color)
        self.message_entry.config(bg=self.entry_bg, fg=self.entry_fg)
        self.send_button.config(bg=self.button_bg, fg=self.button_fg)
        self.night_mode_button.config(bg=self.button_bg, fg=self.button_fg)

    def toggleNightMode(self):
        self.night_mode = not self.night_mode
        self.setColors()  # Apply the new mode

    def askUsername(self):
        self.username_window = tk.Toplevel(self.master)
        self.username_window.title("Enter Your Username")
        self.username_window.geometry("300x150")

        label = tk.Label(self.username_window, text="Please enter a username:", font=("Arial", 12), pady=10)
        label.pack()

        self.username_entry = tk.Entry(self.username_window, font=("Arial", 12), width=25)
        self.username_entry.pack(pady=10)

        submit_button = tk.Button(self.username_window, text="Submit", command=self.submitUsername, font=("Arial", 12))
        submit_button.pack()

        self.master.wait_window(self.username_window)

        return self.username

    def submitUsername(self):
        username = self.username_entry.get().strip()
        if username:
            self.username = username
            self.username_window.destroy()
        else:
            self.username_entry.delete(0, tk.END)
            self.username_entry.insert(0, "Please enter a valid username")

    def sendMessage(self):
        message = self.message_entry.get()
        if message:
            protocol.sendWithSize(message, self.s)
            self.displayMessage(f"You: {message}", "blue")
            self.message_entry.delete(0, tk.END)

    def onEnterPressed(self, event=None):
        self.sendMessage()

    def recvMessage(self):
        while True:
            try:
                message = protocol.recvWithSize(self.s)
                if message:
                    self.displayMessage(message, "gray")
            except:
                self.displayMessage("Disconnected from server.", "red")
                break

    def displayMessage(self, message, color):
        if message and message != "Enter your username":
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.insert(tk.END, message + '\n')
            self.chat_display.config(state=tk.DISABLED)
            self.chat_display.tag_add(color, "1.0", "end")
            self.chat_display.tag_config(color, foreground=color)
            self.chat_display.yview(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    client = Client(root)
    root.deiconify()
    root.mainloop()
