import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock, mainthread


import socket
import threading

kivy.require("1.9.0")

client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class MyRoot(BoxLayout):
    
    def __init__(self):
        super(MyRoot, self).__init__()

    def send_message(self):
        print("hi I am senidng a messagr")
        client.send(f"{self.nickname_text.text}: {self.message_text.text}".encode("utf-8"))
        self.update_chat_text(self.nickname_text.text + ": " + self.message_text.text)
        print("hi I have sent a messagr:", self.message_text.text)
        if "food" in self.message_text.text: 
            self.foodie_bot("activate")
        elif "food" in self.chat_text.text:
            if "yes" in self.message_text.text: 
                self.foodie_bot("yes")
            elif "no" in self.message_text.text:
                self.foodie_bot("no")
    
    def foodie_bot(self, msg): 
        if msg == "activate": 
            self.update_chat_text("Foodie Bot: Would you like a list of food recommendations?")
        if msg == "yes": 
            self.update_chat_text("Foodie Bot: Hamburger, French Fries, Sushi, BBQ, Ice Cream")
        if msg == "no": 
            self.update_chat_text("Foodie Bot: Ok bye")


    def connect_to_server(self):
        if self.nickname_text != "":
            print("ip text blah:", self.ip_text.text)
            client.connect((self.ip_text.text, 9999))
            message = client.recv(1024).decode('utf-8')
            if message == "NICK":
                client.send(self.nickname_text.text.encode('utf-8'))
                self.send_btn.disabled = False
                self.message_text.disabled = False
                self.connect_btn.disabled = True
                self.ip_text.disabled = True
                # self.chat_text.disabled=False
                # self.chat_text.readonly = False
                # print("resetting text earlier")
                # self.chat_text.text = "reset"
                print("yay")

                self.make_invisible(self.connection_grid)
                self.make_invisible(self.connect_btn)

                # updated_text = [False, ""]

                thread = threading.Thread(target=self.receive)
                thread.start()

                # while True:
                #     if updated_text[0] == True: 
                #         print("hiii")
                #         self.chat_text.text = updated_text[1]
                #         updated_text[0] = False
                #         print("self chat should have been updated: ", self.chat_text.text)

    def make_invisible(self, widget):
        widget.visible = False
        widget.size_hint_x = None
        widget.size_hint_y = None
        widget.height = 0
        widget.width = 0
        widget.text = ""
        widget.opacity = 0

    def receive(self):
        stop = False
        while not stop:
            try:
                message = client.recv(1024).decode('utf-8') 
                print("message debug yay:", message)
                print("chat text debug1:", self.chat_text.text)
                # print("updated_text debug:", updated_text)
                # self.chat_text.text = "boop"
                # self.chat_text.text += message 
                # updated_text[0] = True
                # updated_text[1] += message
                # print("chat text debug2:", chat_text.text)
                self.update_chat_text(message)
                print("againnnn")
            except:
                print("ERROR")
                client.close()
                stop = True

    @mainthread
    def update_chat_text(self, new_message): 
        print("update chat: ", self.chat_text.text)
        total = self.chat_text.text + new_message + "\n"
        print("total: ", total)
        self.chat_text.text = total
        print("hey is this okay")

        


class NeuralWebChat(App):

    def build(self):
        return MyRoot()

neuralWebChat = NeuralWebChat()
neuralWebChat.run()


