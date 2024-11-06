"""Contains code that runs the app"""
from customtkinter import *
import customtkinter as ctk
from PIL import Image
from bmi import bmi_class, bmi_category_text
from db import DB
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.transforms import Bbox

class BMICalc:
    """A class that contains the code"""
    
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
    
    def __init__(self) -> None:
        """Initializes the attributes to be used"""
        self.root = CTk()
        self.db = DB()
        self.db.create_table()
        # Create page1 and page2 frames
        self.page1 = CTkFrame(self.root)
        self.page2 = CTkFrame(self.root)
        self.page3 = CTkFrame(self.root)
        self.page4 = CTkFrame(self.root)
        self.warn_txt = None
        self.error_txt = None
        
        # Initializes variables
        self.name_var = ctk.StringVar()
        self.name = None
        self.age_var = ctk.StringVar()
        self.age = None
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
        self.page4.place(x=0, y=0, relwidth=1, relheight=1)
        
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
        self.error_page3 = CTkLabel(frame, text="", font=("Avantgarde", 25, "bold"), text_color="red")
        self.error_page3.pack(pady=(5, 5))
        colors = ['blue', 'lightblue', '#f0f8ff', 'green', 'yellow', 'orange', '#E34234', 'red']
        bmi_cat = ["Very Severely underweight", "Severely underweight", "Underweight",
                "Normal", "Overweight", "Obese class 1", "Obese class 2", "Obese class 3"]
        valuez = [16, 16.9, 18.4, 24.9, 29.9, 34.9, 39.9, 40]        
        
        frame2 = CTkFrame(self.page3, corner_radius=10, fg_color="white")
        frame2.pack(fill="both", expand=True, pady=(5, 0))
        key_lab = CTkLabel(frame2, font=("Avantgarde", 30, "bold"), text_color="black", text="Chart")
        key_lab.pack(pady=(7, 6), padx=(40, 10), anchor="w")
        
        fig = Figure(figsize=(8, 3))
        ax = fig.add_subplot(111)
        ax.pie(valuez, radius=0.75, labels=bmi_cat, shadow=True, colors=colors, startangle=90, autopct='%1.1f%%')
        fig.subplots_adjust(top=0.9, bottom=0.1)
        chart = FigureCanvasTkAgg(fig, frame2)
        chart.get_tk_widget().pack()        
        
        backBut = CTkButton(frame2, width=150, height=30, corner_radius=10, text='calculate new', font=("Avantgarde", 16, "bold"), command=lambda: self.page2.tkraise())
        backBut.pack(pady=(10, 0), padx=(30, 5), anchor="w")
        
        histbut = CTkButton(
        frame2, width=150, height=30, corner_radius=10,
        text='History', font=("Avantgarde", 16, "bold"),
        command=lambda: self.page4.tkraise())
        histbut.pack(pady=(0, 10), padx=(10, 30), anchor="e")
        
    
    def page_four(self):
        """Contains the bmi history"""
        top_frame = CTkFrame(self.page4, fg_color="navyblue", height=300)
        top_frame.pack(fill="x")
    
        labl = CTkLabel(top_frame, text=f"BMI History", font=("Avantgarde", 35, "bold"))
        labl.pack(side="left", padx=30, pady=(20, 20))
        frame2 = CTkFrame(self.page4, corner_radius=10, fg_color="white")
        frame2.pack(fill="x", pady=(5, 5))
        backBut = CTkButton(frame2, width=150, height=30, corner_radius=10, text='Details', font=("Avantgarde", 16, "bold"), command=self.navigate_to_details)
        backBut.pack(pady=(40, 10), padx=(30, 5), anchor="w")
        frame = CTkFrame(self.page4, corner_radius=10, fg_color="white")
        frame.pack(fill="both", expand=True)
        
        labl = CTkLabel(frame, text="DATE", font=("Avantgarde", 30, "bold"), text_color="black")
        labl.grid(row=0, column=3, padx=(30, 10), pady=(20, 10))
        labl2 = CTkLabel(frame, text="BMI", font=("Avantgarde", 30, "bold"), text_color="black")
        labl2.grid(row=0, column=4, padx=(0, 10), pady=(20, 10))
        
        self.bmi_hist = CTkLabel(frame, text="", font=("Avantgarde", 25, "bold"), text_color="black")
        self.bmi_hist.grid(row=1, column=3, padx=(50, 10), pady=(5, 5))
        
        self.errorfetch = CTkLabel(frame, text="", font=("Avantgarde", 25, "bold"), text_color="red")
        self.errorfetch.grid(row=1, column= 2, pady=(10, 5), padx=(30, 10))
        
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
        self.name = self.name_var.get().strip()
        if not self.name:
            self.warn_txt.configure(text='PLease submit a proper name', text_color='red')
        self.check_if_present()
    
    def check_if_present(self):
        """Checks if the user is already in the db"""
        if self.db.check_data(self.name):
            user_data = self.db.get_data(self.name)
            self.user_id = self.db.get_user_id(self.name)
            self.warn_txt.configure(text=f"Welcome back {self.name}, press next to continue", text_color='green')
            self.age_var.set(str(user_data[1]))
            self.age = user_data[1]
            
            self.weight_var.set(str(user_data[2]))
            self.w_t = self.weight_var.get()
            self.weight = user_data[2]
            
            self.height_var.set(str(user_data[3]))
            self.h_t = self.height_var.get()
            self.height = user_data[3]
            
            self.gender = user_data[4]
            self.genderbut.set(user_data[4])
            self.info_but.configure(values=[f"Age\n{self.age}", f"Weight\n{self.w_t}", f"Height\n{self.h_t}"])
            bmi_vals = []
            try:
                data = self.db.get_bmi_date(self.user_id)
                text = ""
                for i in data:
                    text += f"{i[1]}         {i[0]}\n"
                    bmi_vals.append(i[0])
                self.bmi_hist.configure(text=text)
                self.errorfetch.configure(text="")
                self.page4.tkraise()
                
            except Exception:
                self.errorfetch.configure(text="Unable to fetch data from database, try again later.")
        else:
            self.warn_txt.configure(text=f"Press next to continue", text_color='green')
    
    def navigate_to_details(self):
        """Navigates to the details page"""
        if self.db.check_data(self.name):
            self.user_id = self.db.get_user_id(self.name)
            try:
                data = self.db.get_bmi_date(self.user_id)
                bmi_vals = []
                for i in data:
                    x = float(i[0])
                    bmi_vals.append(x)
                self.bmi_rev.configure(text=f"{bmi_vals[-1]}")
                bmi_type = bmi_class(bmi_vals[-1])
                self.bmi_rev.configure(text_color=BMICalc.bmi_colors.get(bmi_type, "black"))
                print("yess")
                bmi_cat = bmi_category_text(bmi_vals[-1])
                self.bm_cat.configure(text=bmi_cat)
                self.error_page3.configure(text="")
                self.page3.tkraise()
                                
            except Exception:
                self.errorfetch.configure(text="Unable to switch.")
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
        if self.age_var.get() == 0 or self.age_var.get() is None or self.age == 0:
              self.error_txt.configure(text="Invalid age input, please enter valid data")
        else:
            self.age = int(self.age_var.get())
            
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
        print(self.age)
        self.bmi = self.weight / (self.height * self.height)
        if self.bmi:
            if self.db.check_data(self.name):
                self.db.update_data(self.name, self.age, self.weight, round(self.height, 2), self.gender)
            else:
                self.db.insert_data(self.name,
                                    self.age,
                                    self.weight,
                                    round(self.height, 2),
                                    self.gender)
            self.user_id = self.db.get_user_id(self.name)
            bmi_type = bmi_class(self.bmi)
            self.bmi_rev.configure(text=f"{self.bmi:.2f}")
            self.db.insert_bmi_date(self.user_id, round(self.bmi, 2), datetime.now().date())
            
            self.bmi_rev.configure(text_color=BMICalc.bmi_colors.get(bmi_type, "black"))
            bmi_cat = bmi_category_text(self.bmi)
            self.bm_cat.configure(text=bmi_cat)
            self.age = self.age_var.get()
            self.info_but.configure(values=[f"Age\n{self.age}", f"Weight\n{self.w_t}", f"Height\n{self.h_t}"])
            self.error_txt.configure(text="")
            try:
                data = self.db.get_bmi_date(self.user_id)
                text = ""
                for i in data:
                    text += f"{i[1]}    {i[0]}\n"
                self.bmi_hist.configure(text=text)
            except Exception:
                self.errorfetch.configure(text="Unable to fetch data from database, try again later.")
            self.page3.tkraise()
        
    def create_widgets(self):
        """Creates the widgets to be used"""
        self.page_one()
        self.page_two()
        self.page_three()
        self.page_four()
        
    def main(self):
        """Contains the main code that runs the app"""
        self.create_widgets()
        self.root.mainloop()


if __name__ == '__main__':
    bmi = BMICalc()
    bmi.main()
