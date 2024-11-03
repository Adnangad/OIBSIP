from customtkinter import *
import customtkinter as ctk
from PIL import Image
from bmi import bmi_class, bmi_category_text
from db import DB

class BMICalc:
    """A class that contains the code"""
    
    def __init__(self) -> None:
        """Initializes the attributes to be used"""
        self.root = CTk()
        self.db = DB()
        # Create page1 and page2 frames
        self.page1 = CTkFrame(self.root)
        self.page2 = CTkFrame(self.root)
        self.page3 = CTkFrame(self.root)
        
        self.warn_txt = None
        self.error_txt = None
        
        # Initializes variables
        self.name_var = ctk.StringVar()
        self.name = None
        self.age_var = ctk.StringVar()
        self.age =0
        self.height_var = ctk.StringVar()
        self.height = 0
        self.weight_var = ctk.StringVar()
        self.weight = 0
        self.a= 0
        self.w = 0
        self.h = 0
        self.w_t = None
        self.h_t = None
        self.gender = None
        self.bmi = None
        
        # Sets up window
        self.root.title("BMI Calculator")
        self.root.geometry("800x800")
        
        # Places both pages in the same location (0,0), only one will be visible at a time
        self.page1.place(x=0, y=0, relwidth=1, relheight=1)
        self.page2.place(x=0, y=0, relwidth=1, relheight=1)
        self.page3.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Initially raises page1
        self.page1.tkraise()
    
    def page_one(self):
        """Creates widgets for page 1"""
        # frame1 on page1
        frame1 = CTkFrame(self.page1, fg_color="white")
        frame1.pack(fill="x")
        
        # Loads the image      
        img = CTkImage(light_image=Image.open('images/bot.jpg'), size=(350, 350))
        img_label = CTkLabel(frame1, image=img, text=None)
        img_label.pack()
        
        # Greeting label
        greet = CTkLabel(frame1, text="Welcome!", font=("Avantgarde", 20, "bold"), text_color="black", bg_color="transparent")
        greet.pack()
        
        # frame2
        frame2 = CTkFrame(self.page1, fg_color="navyblue", corner_radius=20)
        frame2.pack(fill="both", expand=True)
        
        label1 = CTkLabel(frame2, text="What's your name?", font=("Avantgarde", 20, "bold"))
        label1.pack(pady=30)
        
        name_entry = CTkEntry(frame2, width=300, height=35, corner_radius=8, fg_color="lightblue", text_color="black", textvariable=self.name_var)
        name_entry.pack()
        
        subBut = CTkButton(frame2, width=140, height=26, corner_radius=9, text='Submit', command=self.get_name, font=("Avantgarde", 14, "bold"), text_color="white")
        subBut.pack(pady=20)
        
        self.warn_txt = CTkLabel(frame2, text="", font=("Avantgarde", 16, "bold"), text_color="red")
        self.warn_txt.pack(pady=10)
        
        nextBut = CTkButton(frame2, width=150, height=30, corner_radius=10, text='Next ->', font=("Avantgarde", 16, "bold"), command=self.next_pg)
        nextBut.pack(side="right", padx=25)
        
    
    def page_two(self):
        """Creates widgets for page 2"""
        top_frame = CTkFrame(self.page2, fg_color="navyblue", height=300)
        top_frame.pack(fill="x")
        
        self.labl = CTkLabel(top_frame, text=f"Hi {self.name}!", font=("Avantgarde", 20, "bold"))
        self.labl.pack(side="left", padx=30, pady=(40, 50))
    
        frame = CTkFrame(self.page2, fg_color="white", corner_radius=1)
        frame.pack(fill="x")
    
        img = CTkImage(light_image=Image.open('images/male2.jpg'), size=(150, 150))
        img_label = CTkLabel(frame, image=img, text=None)
        img_label.pack(side="left", padx=(235, 10), pady=(20, 0))
        img2 = CTkImage(light_image=Image.open('images/female.jpg'), size=(150, 150))
        img2_label = CTkLabel(frame, image=img2, text=None)
        img2_label.pack(side="left", padx=(20, 0), pady=(20, 0))
    
        frame2 = CTkFrame(self.page2, fg_color="white", corner_radius=1)
        frame2.pack(fill="x")        
        self.genderbut = CTkSegmentedButton(frame2, width=400, height=40, corner_radius=10, values=["Male ", "Female"], unselected_color="grey", dynamic_resizing=False, selected_color="skyblue", selected_hover_color="skyblue", command=self.select_gender)
        self.genderbut.pack(pady=20)
    
        frame3 = CTkFrame(self.page2, fg_color="white", corner_radius=1)
        frame3.pack(fill="both", expand=True)

        # age widget
        age_label = CTkLabel(frame3, text="Age", font=("Avantgarde", 20, "bold"), text_color="black")
        age_entry = CTkEntry(frame3, width=300, height=35, corner_radius=8, fg_color="Alice blue", text_color="black", textvariable=self.age_var)
        age_label.grid(row=0, column=2, padx=10, pady=10)
        age_entry.grid(row=0, column=3, padx=10, pady=10)
        
        #weight widget
        weight_label = CTkLabel(frame3, text="Weight", font=("Avantgarde", 20, "bold"), text_color="black")
        weight_entry = CTkEntry(frame3, width=300, height=35, corner_radius=8, fg_color="Alice blue", text_color="black", textvariable=self.weight_var)
        weight_opt = CTkOptionMenu(frame3, width=100, values=["kgs", "lbs"], fg_color="Alice blue", text_color="black", command=self.weight_option)
        weight_opt.set("metrics")
        weight_label.grid(row=1, column=2, padx=10, pady=10)
        weight_entry.grid(row=1, column=3, padx=10, pady=10)
        weight_opt.grid(row=1, column=4, padx=10, pady=10)
        
        #height widget
        height_label = CTkLabel(frame3, text="Height", font=("Avantgarde", 20, "bold"), text_color="black")
        height_entry = CTkEntry(frame3, width=300, height=35, corner_radius=8, fg_color="Alice blue", text_color="black", textvariable=self.height_var)
        height_opt = CTkOptionMenu(frame3, width=100, values=["metres", "cms", "feet"], fg_color="Alice blue", text_color="black", command=self.height_option)
        height_opt.set("metrics")
        height_label.grid(row=2, column=2, padx=10, pady=10)
        height_entry.grid(row=2, column=3, padx=10, pady=10)
        height_opt.grid(row=2, column=4, padx=10, pady=10)
        
        self.error_txt = CTkLabel(frame3, text="", font=("Avantgarde", 20, "bold"), text_color="red")
        self.error_txt.grid(row=4, column=0, columnspan=5, padx=10, pady=(10, 10), sticky="ew")
        
        calcbut = CTkButton(frame3, width=200, height=40, corner_radius=10, text="Calculate bmi", font=("Avantgarde", 16, "bold"), command=self.calculatebmi)        
        calcbut.grid(row=5, column=3, pady=(20, 15))
        
        # Replacing pack with grid for the button
        backBut = CTkButton(frame3, width=150, height=30, corner_radius=10, text='Back', font=("Avantgarde", 16, "bold"), command=lambda: self.page1.tkraise())
        backBut.grid(row=6, column=0, columnspan=2, pady=10, padx=20)
    
    def page_three(self):
        """Contains widgets for page 3"""
        top_frame = CTkFrame(self.page3, fg_color="navyblue", height=300)
        top_frame.pack(fill="x")
    
        labl = CTkLabel(top_frame, text=f"Your BMI result", font=("Avantgarde", 20, "bold"))
        labl.pack(side="left", padx=30, pady=(20, 20))
    
        frame = CTkFrame(self.page3, corner_radius=10, fg_color="white")
        frame.pack(fill="x")
        self.bmi_rev = CTkLabel(frame, text="", font=("Avantgarde", 25, "bold"))
        self.bmi_rev.pack(pady=(20, 5))
        self.bm_cat = CTkLabel(frame, text="", font=("Avantgarde", 20, "bold"), text_color="black")
        self.bm_cat.pack(pady=(10, 10))
        self.info_but = CTkSegmentedButton(
            frame, width=400,  height=50, corner_radius=10,
            values=[f"Age\n{self.age}", f"Weight\n{self.w_t}", f"Height\n{self.h_t}"],
            state=DISABLED, dynamic_resizing=False, fg_color="skyblue",
            unselected_color="skyblue", font=("Arial", 17, "bold"), text_color_disabled="black")
        self.info_but.pack(pady=(10, 20))
        colors = ['blue', 'lightblue', 'Alice blue', 'green', 'yellow', 'orange', '#E34234', 'red']
        category = ["Very Severely underweight", "Severely underweight", "Underweight",
                "Normal", "Overweight", "Obese class 1", "Obese class 2", "Obese class 3"]
        valuez = ["<16.0", "16.0-16.9", "17.0-18.4", "18.5-24.9", "25.0-29.9", "30.0-34.9", "35.0-39.9", ">39.9"]
        
        x = 1
        j = 0
        
        frame2 = CTkFrame(self.page3, corner_radius=10, fg_color="white")
        frame2.pack(fill="both", expand=True, pady=(5, 0))
        key_lab = CTkLabel(frame2, font=("Avantgarde", 30, "bold"), text_color="black", text="Key")
        key_lab.grid(row=0, column=0, pady=(15, 10), padx=(40, 10))
        for col in colors:
            round_widget = CTkLabel(frame2, text="bmi", width=70, height=30, fg_color=col)
            cat_lab = CTkLabel(frame2, text=category[j], font=("Avantgarde", 20, "bold"), text_color="black")
            valz = CTkLabel(frame2, text=valuez[j], font=("Avantgarde", 20, "bold"), text_color="black")
            
            round_widget.grid(row=x, column=1, pady=(5), padx=(50, 10))
            cat_lab.grid(row=x, column=2, pady=(5), padx=(10, 40))
            valz.grid(row=x, column=3, pady=(5), padx=(10, 30))
            x += 1
            j += 1
        backBut = CTkButton(frame2, width=150, height=30, corner_radius=10, text='Back', font=("Avantgarde", 16, "bold"), command=lambda: self.page2.tkraise())
        backBut.grid(row=9, column=0, columnspan=2, pady=10, padx=30)
    def select_gender(self, val):
        """Sets the gender based on the users option"""
        self.gender = val
        
    def next_pg(self):
        """Navigates to page 2"""
        self.get_name()
        if self.name:
            self.labl.configure(text=f"Hi {self.name}!")
            self.page2.tkraise()
        else:
            self.warn_txt.configure(text='PLease submit a proper name', text_color='red')
        
    def get_name(self):
        """Retrieves the user's name entry"""
        if len(self.name_var.get()) > 2:
            self.name = self.name_var.get()
            if self.db.check_data(self.name):
                user = self.db.get_data(self.name)
                self.age = user[1]
                if self.age != 0:
                    self.age_var.set(f"{self.age}")
                self.height = user[3]
                if self.height != 0:
                    self.height_var.set(f"{self.height}")
                self.weight = user[2]
                if self.weight != 0:
                    self.weight_var.set(f"{self.weight}")
                self.gender = user[4]
                if self.gender != 'no':
                    self.genderbut.set(f"{self.gender}")
                self.warn_txt.configure(text=f"Welcome back {self.name}, press next to proceed", text_color='lightgreen')
            else:
                self.db.insert_data(self.name)
                self.warn_txt.configure(text="You have been added to the database, press next to continue", text_color='lightgreen')
        else:
            self.warn_txt.configure(text='PLease submit a proper name', text_color='red')
    
    def height_option(self, val):
        """Retreives the height option selected by the user and adjusts th eight value accordingly"""
        self.h = val
    
    def weight_option(self, val):
        """retreives the weight option selected and adjusts the weight value accordingly"""
        self.w = val
    
    def calculatebmi(self):
        if self.gender is None or self.gender == 'no':
            self.error_txt.configure(text="Please select your gender")
        val = self.h
        if val == 0:
            self.error_txt.configure(text="Please select a metric option")
        if val == "metres":
            try:
                self.height = float(self.height_var.get())
                self.h_t = f"{self.height_var.get()} {val}"
            except Exception:   
                self.error_txt.configure(text="Invalid weight input, please enter valid data")
        elif val == "cms":
            try:
                self.height = float(self.height_var.get()) / 100
                self.h_t = f"{self.height_var.get()} {val}"
            except Exception:
                self.error_txt.configure(text="Invalid height input, please enter valid data")
        elif val == "feet":
            try:
                self.height = float(self.height_var.get()) * 0.3048
                self.h_t = f"{self.height_var.get()} {val}"
            except Exception:
                self.error_txt.configure(text="Invalid height input, please enter valid data")
                
        valz = self.w
        
        if valz == 0:
            self.error_txt.configure(text="Please select a metric option")
        if valz == "kgs":
            try:
                self.weight = float(self.weight_var.get())
                self.w_t = f"{self.weight_var.get()} {valz}"
            except Exception:
                self.error_txt.configure(text="Invalid weight input, please enter valid data")
        elif valz == "lbs":
            try:
                self.weight = float(self.weight_var.get()) / 2.20462
                self.w_t = f"{self.weight_var.get()} {valz}"
            except Exception:
                self.error_txt.configure(text="Invalid weight input, please enter valid data")
        print(f'height is {self.height}\nweight is {self.weight}')
        self.bmi = self.weight / (self.height * self.height)
        if self.bmi:
            self.db.update_data(self.name,int(self.age),
                                self.weight,
                                self.height,
                                self.gender)
            print(self.bmi)
            bmi_type = bmi_class(self.bmi)
            self.bmi_rev.configure(text=f"{self.bmi:.2f}")
            bmi_colors = {
            "Very Severely underweight": "blue",
            "Severely underweight": "lightblue",
            "Underweight": "AliceBlue",
            "Normal": "green",
            "Overweight": "yellow",
            "Obese class 1": "orange",
            "Obese class 2": "#E34234",
            "Obese class 3": "red"
            }
            self.bmi_rev.configure(text_color=bmi_colors.get(bmi_type, "black"))
            bmi_cat = bmi_category_text(self.bmi)
            self.bm_cat.configure(text=bmi_cat)
            self.age = self.age_var.get()
            self.info_but.configure(values=[f"Age\n{self.age}", f"Weight\n{self.w_t}", f"Height\n{self.h_t}"])
            self.error_txt.configure(text="")
            self.page3.tkraise()
        
    def create_widgets(self):
        """Creates the widgets to be used"""
        self.page_one()
        self.page_two()
        self.page_three()
        
    def main(self):
        """Contains the main code that runs the app"""
        self.create_widgets()
        self.root.mainloop()


if __name__ == '__main__':
    bmi = BMICalc()
    bmi.main()
