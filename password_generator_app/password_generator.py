"""Password generator app"""
import customtkinter as ctk
import random
from tkinter import messagebox
import re

class PasswordGen:
    """Class that contains code for the app"""
    au = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    al = 'abcdefghijklmnopqrstuvwxyz'
    lower_case = list(al)
    upper_case = list(au)
    symbols = ['!', '@', '.', '#', '%', '$', '^', '(', ')', '-', '_', '+', '=',
           '/', '>', '<', ',', '{', '}', '[', ']', '|', '\\']
    numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    def __init__(self) -> None:
        """Initializes attributes"""
        self.root = ctk.CTk()
        self.root.title('Password Generator')
        self.root.geometry("700x700")
        
        self.scale_value = ctk.IntVar(value=0)
        
        self.switch_var = ctk.StringVar(value="no")
        self.switch_var_2 = ctk.StringVar(value="no2")
        self.switch_var_3 = ctk.StringVar(value="no3")
        self.switch_var_4 = ctk.StringVar(value="no4")
        
        self.password_length = 0
        self.password = ''
        self.text = 'The generated password will appear here'
        self.choices = []
        
        
        self.label2 = None
        self.label3 = None

    def generate_password(self):
        """Generates a password"""
        password = ''
        if len(self.choices) < 1:
            self.label2.configure(text=f'Invalid, please select at least one security option for the password', text_color='red')
        elif self.password_length > 4:
            for _ in range(self.password_length):
                if 1 in self.choices:
                    password += random.choice(PasswordGen.lower_case)
                    if len(password) >= self.password_length:
                        break
                if 2 in self.choices:
                    password += random.choice(PasswordGen.upper_case)
                    if len(password) >= self.password_length:
                        break
                if 3 in self.choices:
                    password += random.choice(PasswordGen.symbols)
                    if len(password) >= self.password_length:
                        break
                if 4 in self.choices:
                    password += str(random.choice(PasswordGen.numbers))
                    if len(password) >= self.password_length:
                        break
            
            # Shuffles the generated password and sets it
            password_ls = list(password)
            random.shuffle(password_ls)
            self.password = "".join(password_ls)
            
            # Updates the label with the generated password
            self.label2.configure(text=f'Generated password is: {self.password}', text_color='green')
            print(self.password)
            pwd_str = self.check_pwd_strength(self.password)
            if pwd_str == "Strong":
                self.label3.configure(text=f'Password Strength: {pwd_str}', text_color='green')
            elif pwd_str == "Medium":
                self.label3.configure(text=f'Password Strength: {pwd_str}', text_color='orange')
            else:
                self.label3.configure(text=f'Password Strength: {pwd_str}', text_color='red')    
            
        else:
            self.label2.configure(text=f'Invalid, the password length must be greater than 0', text_color='red')
    
    def check_pwd_strength(self, passwrd):
        """Checks the strength of the password"""
        length = len(passwrd)
        lower = re.search(r'[a-z]', passwrd) is not None
        upper = re.search(r'[A-Z]', passwrd) is not None
        digit = re.search(r'[0-9]', passwrd) is not None
        special = re.search(r'[@$!%*?&#^-_+;:,"/{}|]', passwrd) is not None
        
        if length > 8 and upper and lower and digit and special:
            return "Strong"
        elif length > 8 and (upper or lower) and digit:
            return "Medium"
        else:
            return "Weak"

    def update_label(self, value):
        """Update the label with the current scale value"""
        value = int(float(value))
        self.password_length = value
        self.label_var.set(f"Password Length: {value}")

    def toggle_switch(self):
        """Checks the values for the toggle_buttons"""
        val_1 = self.switch_var.get()
        val_2 = self.switch_var_2.get()
        val_3 = self.switch_var_3.get()
        val_4 = self.switch_var_4.get()
        
        # Update choices based on the switch states
        self.choices.clear()
        if val_1 == "yes":
            self.choices.append(1)
        if val_2 == "yes2":
            self.choices.append(2)
        if val_3 == "yes3":
            self.choices.append(3)
        if val_4 == "yes4":
            self.choices.append(4)

    def create_widgets(self):
        """Creates widgets"""
        # frame1
        frame = ctk.CTkFrame(self.root, corner_radius=20, width=700, height=100)
        frame.pack(fill="x", pady=10)
        
        self.label_var = ctk.StringVar(value="Password Length: 0")
        label = ctk.CTkLabel(frame, textvariable=self.label_var, font=("Arial", 16, "bold"))
        label.pack(side="left", pady=10, padx=20)
        
        slider = ctk.CTkSlider(frame, from_=0, to=50, orientation="horizontal", command=self.update_label)
        slider.pack(side="left", pady=10, padx=5)
        slider.set(self.scale_value.get())
        
        # frame2
        frame2 = ctk.CTkFrame(self.root, corner_radius=20, width=700, height=100)
        frame2.pack(fill="x", pady=20)
        
        label = ctk.CTkLabel(frame2, text="Security options", font=("Arial", 20, "bold"))
        label.pack(pady=10)
        
        toggle_1 = ctk.CTkSwitch(frame2, text="Include Lower case letters      (a-z)", font=("Arial", 16, "bold"), variable=self.switch_var, onvalue="yes", offvalue="no", command=self.toggle_switch)
        toggle_1.pack(pady=20)
        toggle_2 = ctk.CTkSwitch(frame2, text="Include Upper case letters      (A-Z)", variable=self.switch_var_2, onvalue="yes2", offvalue="no2", command=self.toggle_switch, font=("Arial", 16, "bold"))
        toggle_2.pack(pady=20)
        toggle_3 = ctk.CTkSwitch(frame2, text="Include Special characters  (!^* etc)", variable=self.switch_var_3, onvalue="yes3", offvalue="no3", command=self.toggle_switch, font=("Arial", 16, "bold"))
        toggle_3.pack(pady=20)
        toggle_4 = ctk.CTkSwitch(frame2, text="Include Numbers (0-9)           ", variable=self.switch_var_4, onvalue="yes4", offvalue="no4", command=self.toggle_switch, font=("Arial", 16, "bold"))
        toggle_4.pack(pady=20)
        
        # frame3
        frame3 = ctk.CTkFrame(self.root, corner_radius=20, width=700, height=100)
        frame3.pack(fill="x", pady=20)
        
        genbut = ctk.CTkButton(frame3, text='Generate Password', font=("Arial", 12, "bold"), command=self.generate_password)
        genbut.pack(pady=10)
        
        # frame4
        frame4 = ctk.CTkFrame(self.root, corner_radius=20, width=700, height=600)
        frame4.pack(fill="x", pady=20)
        
        self.label2 = ctk.CTkLabel(frame4, text=self.text, font=("Arial", 16, "bold"))
        self.label2.pack(pady=20, padx=25, anchor="w")
        
        self.label3 = ctk.CTkLabel(frame4, text="Password Strength: No password generated ", font=("Arial", 16, "bold"))
        self.label3.pack(pady=10, padx=25, anchor="w")
        
        copy_but = ctk.CTkButton(frame4, text='copy to clipboard', font=("Arial", 12, "bold"), command=self.copy_to_clip)
        copy_but.pack(pady=10, padx=25)
        
    
    def copy_to_clip(self):
        """Copys the generated password to the clipboard"""
        self.root.clipboard_clear()
        self.root.clipboard_append(self.password)
        self.show_notification()
        self.root.update()
    
    def show_notification(self):
        """Indicates that the password has been copied to clipboard"""
        messagebox.showinfo("Copied")
    
    def main(self):
        """main code that runs the app"""
        print(self.choices)
        self.create_widgets()
        self.root.mainloop()


if __name__ == '__main__':
    pg = PasswordGen()
    pg.main()
