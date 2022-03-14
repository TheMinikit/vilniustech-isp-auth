import hashlib
from kivy.app import App
from kivy.properties import (StringProperty, ObjectProperty)
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.bubble import Button


class AuthBox(GridLayout):

    def __init__(self, **kwargs):
        super(AuthBox, self).__init__(**kwargs)

        self.result = StringProperty()
        self.popup_window = ObjectProperty()

        self.cols = 2

        self.add_widget(Label())
        self.add_widget(Label())

        self.add_widget(Label(text="Username", size_hint=(1, 0.6), font_size=25))
        self.name = TextInput(multiline=False, size_hint=(1, 0.6), font_size=25)
        self.add_widget(self.name)

        self.add_widget(Label(text="Password", size_hint=(1, 0.6), font_size=25))
        self.password = TextInput(multiline=False, password=True, size_hint=(1, 0.6), font_size=25)
        self.add_widget(self.password)

        self.add_widget(Label(size_hint=(1, 0.5)))
        self.add_widget(Label(size_hint=(1, 0.5)))

        self.login_button = Button(text="Login")
        self.login_button.bind(on_press=lambda x: self.check_username())
        self.add_widget(self.login_button)

        self.login_button = Button(text="Register")
        self.login_button.bind(on_press=lambda x: self.register_user())
        self.add_widget(self.login_button)

    def check_username(self):
        if len(self.name.text) > 0:
            users = {}
            users_db = open("users_db.txt", "r")
            for line in users_db:
                users[line.split()[0]] = line.split()[1]
            users_db.close()
            if self.name.text in users.keys():
                self.check_password()
            else:
                self.popup_window = Popup(title="Login Status", content=Label(text="Invalid Username"),
                                          size_hint=(0.4, 0.2))
                self.popup_window.open()

    def check_password(self):
        if len(self.password.text) > 0:
            self.users = {}
            self.users_db = open("users_db.txt", "r")
            for line in self.users_db:
                self.users[line.split()[0]] = line.split()[1]
            self.users_db.close()
            self.result = hashlib.md5(str(self.password.text).encode('utf-8'))
            self.password.text = ''
            if self.users[self.name.text] == self.result.hexdigest():
                self.popup_window = Popup(title="Login Status", content=Label(text="You have logged in successfully"), size_hint=(0.4, 0.2))
                self.popup_window.open()
                print("Input hash:    " + str(self.result.hexdigest()))
                print("Database hash: " + str(self.users[self.name.text]))
            else:
                self.popup_window = Popup(title="Login Status", content=Label(text="Invalid password"),
                                          size_hint=(0.4, 0.2))
                self.popup_window.open()

    def register_user(self):
        self.users = {}
        self.users_db = open("users_db.txt", "r")
        for line in self.users_db:
            self.users[line.split()[0]] = line.split()[1]
        self.users_db.close()
        if self.name.text in self.users.keys():
            self.popup_window = Popup(title="Error", content=Label(text="This username is taken"),
                                      size_hint=(0.4, 0.2))
            self.popup_window.open()
        else:
            self.users_db = open("users_db.txt", "a")
            self.result = hashlib.md5(str(self.password.text).encode('utf-8'))
            self.password.text = ''
            self.users_db.write(str(self.name.text) + " " + str(self.result.hexdigest() + "\n"))
            self.users_db.close()
            self.popup_window = Popup(title="Register status", content=Label(text="User successfully registered"),
                                      size_hint=(0.4, 0.2))
            self.popup_window.open()


class AuthApp(App):
    def build(self):
        return AuthBox()


if __name__ == '__main__':
    AuthApp().run()
