"""
Contains the code that runs the app
"""
from customtkinter import *
from datetime import datetime
from PIL import Image, ImageTk
import geopy
import timezonefinder as tz
from helper_functions import *
import pandas as pd
from urllib.request import urlopen
from io import BytesIO
import requests
import os
from dotenv import load_dotenv

load_dotenv()

class WeatherApp:
    """A class that contains the code"""

    api_key = os.getenv("API_KEY")

    def __init__(self):
        """Initializes variables to be used"""
        self.root = CTk()
        self.canvas = None
        self.city = None
        self.path = ''
        self.city_var = StringVar()  # Initialize as StringVar for text entry
        self.page = CTkFrame(self.root)
        self.error_message = None
        self.root.title('Weather App')
        self.fc_widgets = {}

        # Frame widget that contains all other widgets
        self.page.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.loading_label = CTkLabel(self.page, text="Loading...", font=("Helvetica", 20), text_color="white")
        self.loading_label.place_forget()
        
        # Initializes the app with full screen
        self.root.geometry("900x800")
    
    def show_loading(self):
        """Displays the loading animation"""
        self.loading_label.place(relx=0.5, rely=0.5, anchor="center")
        self.root.update_idletasks()

    def hide_loading(self):
        """Hides the loading animation"""
        self.loading_label.place_forget()
        self.root.update_idletasks()
    
    def get_data(self):
        """Retreives all the necessary data from the weather api"""
        self.show_loading()
        try:
            if self.city:
                x = get_coordinates_from_city(self.city)
                self.lattitude = x[0]
                self.longitude = x[1]
                self.date_time = get_date_time(self.longitude, self.lattitude)
                self.coordinates = None
            else:
                self.coordinates = find_coordinates()
            if self.coordinates:
                self.lattitude, self.longitude = self.coordinates
                self.city = get_city(self.longitude, self.lattitude)
                self.date_time = get_date_time(self.longitude, self.lattitude)
            base_url = f"https://api.weatherbit.io/v2.0/current?city={self.city}&key={WeatherApp.api_key}"
            data_today = requests.get(base_url)
            data_today = data_today.json()
            self.weather = data_today['data'][0]['weather']['description']
            self.temp = data_today['data'][0]['temp']
            self.icn = data_today['data'][0]['weather']['icon']
            self.wind = data_today['data'][0]['wind_spd']
            self.pressure = data_today['data'][0]['pres']
            self.image_url = f"https://www.weatherbit.io/static/img/icons/{self.icn}.png"
        except Exception:
            print("Error")
        finally:
            self.hide_loading()
        
    def get_forecast(self):
        """Gets the forecast of seven days"""
        self.fc_data = None
        if self.city:
            base_url = f'https://api.weatherbit.io/v2.0/forecast/daily?city={self.city}&key={WeatherApp.api_key}'
            self.fc_data = requests.get(base_url).json()
        else:
            self.coordinates = find_coordinates()
            if self.coordinates:
                self.lattitude, self.longitude = self.coordinates
                self.city = get_city(self.longitude, self.lattitude)
                base_url = f'https://api.weatherbit.io/v2.0/forecast/daily?city={self.city}&key={WeatherApp.api_key}'
                self.fc_data = requests.get(base_url).json()
        
            
    def create_frames(self):
        """Creates a canvas widget and places other widgets inside"""
        # Retrieves weather icon
        u = urlopen(self.image_url)
        rawdata = u.read()
        u.close()
        pil_image = Image.open(BytesIO(rawdata))

        self.ctk_image = CTkImage(light_image=pil_image, dark_image=pil_image, size=(100, 75))

        # Frame to hold today's weather details
        frame1 = CTkFrame(self.page, height=900)
        frame1.pack(fill="x")

        frame1.grid_columnconfigure(0, weight=0)
        frame1.grid_columnconfigure(1, weight=1)
        # Search and submit button for city search
        search_ent = CTkEntry(frame1, placeholder_text="Search for cities", width=500, height=35,
                                  corner_radius=15, bg_color="transparent", textvariable=self.city_var)
        search_ent.grid(row=0, column=0, columnspan=2, padx=(10, 10), pady=(10, 10))
        
        sub_but = CTkButton(frame1, text="Search", width=200, height=35, corner_radius=10, command=self.get_city)
        sub_but.grid(row=0, column=3, padx=(10, 10), pady=(10, 10))
        
        
        self.error_message = CTkLabel(frame1, text='', text_color='red', font=('Avantgarde', 30, 'bold'))
        self.error_message.grid(row=1, column=0, padx=(10, 10), pady=(10,0))

        # Weather information display
        self.img_label = CTkLabel(frame1, text=None, image=self.ctk_image)
        self.img_label.grid(row=2, column=0, padx=(25, 10), pady=(10, 10), sticky="w")
        self.city_label = CTkLabel(frame1, text=f"{self.city}", font=('Avantgarde', 30, 'bold'), text_color="white")
        self.city_label.grid(row=2, column=3, pady=(10, 5), padx=(10, 20))
        
        self.day_label= CTkLabel(frame1, text=f"{self.date_time['day']}, {self.date_time['month']}", text_color='white', font=('Avantgarde', 30, 'bold'))
        self.day_label.grid(row=2, column=5, pady=(10, 10), padx=(10, 20), sticky="e")
        self.time_label = CTkLabel(frame1, text=f"{self.date_time['time']} hrs", text_color='white', font=('Avantgarde', 30, 'bold'))
        self.time_label.grid(row=3, column=5, pady=(5, 10), padx=(10, 20), sticky="e")

        self.weather_label = CTkLabel(frame1, text=f"{self.weather}", font=('Avantgarde', 23, 'bold'), text_color="white")
        self.weather_label.grid(row=3, column=0, columnspan=2, pady=(0, 10), sticky="w", padx=(25, 10))
        self.temp_label = CTkLabel(frame1, text=f"{self.temp}\u2103", font=('Avantgarde', 23, 'bold'), text_color="white")
        self.temp_label.grid(row=3, column=3, pady=(20, 10), padx=(20, 5))

        # Additional weather details frame
        more_info = CTkFrame(self.page, height=300, corner_radius=15)
        more_info.pack(fill="x", pady=(10, 0))
        self.pressure_label = CTkLabel(more_info, text=f"Pressure: {self.pressure} mb", font=('Avantgarde', 23, 'bold'),
                                      text_color="white")
        self.pressure_label.grid(row=0, column=1, pady=(25, 10), padx=(25, 5), sticky="w")
        self.wind_label = CTkLabel(more_info, text=f"Wind speed: {self.wind} mph", font=('Avantgarde', 23, 'bold'),
                                  text_color="white")
        self.wind_label.grid(row=1, column=1, pady=(10, 20), padx=(25, 5), sticky="w")
        
        #forecast frame
        forecast_frame = CTkFrame(self.page, height=400, corner_radius=15)
        forecast_frame.pack(fill='both', expand=True, pady=(5, 0))
        column = 0
        fc_tit = CTkLabel(forecast_frame, text="7 day forecast", font=('Avantgarde', 23, 'bold'), text_color="white")
        fc_tit.grid(row=0, column=0, padx=(30, 5), pady=(10, 5), sticky="w")
        
        for fc in self.fc_data['data']:
            day = pd.Timestamp(fc['datetime']).day_name()
            day_now = self.date_time['day']
            
            #skip todays forecast
            if day == day_now:
                continue
            temp_fc = fc['temp']
            weather_fc = fc['weather']['description']
            icn = fc['weather']['icon']
            image_url_fc = f'https://www.weatherbit.io/static/img/icons/{icn}.png'
            u = urlopen(image_url_fc)
            read_data = u.read()
            u.close()
            
            self.fc_day = CTkLabel(forecast_frame, text=day, font=('Avantgarde', 23, 'bold'), text_color="white")
            self.fc_day.grid(row=1, column=column, pady=(20, 5), padx=(20 ,5))
            self.fc_widgets[f'{day}_day_label'] = self.fc_day
            
            image_fc = Image.open(BytesIO(read_data))
            self.image_fc = CTkImage(light_image=image_fc, dark_image=image_fc, size=(65, 65))            
            self.image_label = CTkLabel(forecast_frame, image=self.image_fc, text=None)
            self.image_label.grid(row=2, column=column, pady=(10, 5), padx=(20 ,5))
            self.fc_widgets[f'{day}_image_label'] = self.image_label
            
            self.fc_temp = CTkLabel(forecast_frame, text=f"{temp_fc}\u2103", font=('Avantgarde', 23, 'bold'), text_color="white")
            self.fc_temp.grid(row=3, column=column, pady=(10, 5), padx=(10 ,5))
            self.fc_widgets[f'{day}_temp_label'] = self.fc_temp
            
            self.fc_weather = CTkLabel(forecast_frame, text=weather_fc, font=('Avantgarde', 23, 'bold'), text_color="white")
            self.fc_weather.grid(row=4, column=column, pady=(10, 5), padx=(10 ,5))
            self.fc_widgets[f'{day}_weather_label'] = self.fc_weather
            
            column += 1
        unit_label = CTkLabel(forecast_frame, text=f"Metrics:", font=('Avantgarde', 23, 'bold'),
                                      text_color="white")
        unit_label.grid(row=0, column=4, pady=(10, 10))
        unit_opt = CTkOptionMenu(forecast_frame, width=100, values=["Celsius", "Fahrenheit"], fg_color="Alice blue", text_color="black", command=self.change_unit)
        unit_opt.set("")
        unit_opt.grid(row=0, column=5, padx=(0, 10), pady=(10, 10))
        
          
    def update_weather(self):
        self.error_message.configure(text="")
        self.weather_label.configure(text=self.weather)
        self.city_label.configure(text=self.city)
        self.temp_label.configure(text=f"{self.temp}\u2103")
        self.pressure_label.configure(text=f"Pressure: {self.pressure} mb")
        self.wind_label.configure(text=f"Wind speed: {self.wind} mph")
        self.time_label.configure(text=f"{self.date_time['time']} hrs")
        self.day_label.configure(text=f"{self.date_time['day']}")
        
        u = urlopen(self.image_url)
        rawdata = u.read()
        u.close()
        pil_image = Image.open(BytesIO(rawdata))
        self.ctk_image = CTkImage(light_image=pil_image, dark_image=pil_image, size=(75, 75))
        self.img_label.configure(image=self.ctk_image)
        
        for fc in self.fc_data['data']:
            day = pd.Timestamp(fc['datetime']).day_name()
            day_now = self.date_time['day']
            
            #skip todays forecast
            if day == day_now:
                continue
            temp_fc = fc['temp']
            weather_fc = fc['weather']['description']
            icn = fc['weather']['icon']
            image_url_fc = f'https://www.weatherbit.io/static/img/icons/{icn}.png'
            u = urlopen(image_url_fc)
            read_data = u.read()
            u.close()
            image_fc = Image.open(BytesIO(read_data))
            image_tk = CTkImage(light_image=image_fc, dark_image=image_fc, size=(70, 70))
            for key, val in self.fc_widgets.items():
                if key == f'{day}_image_label':
                    val.configure(image=image_tk)
                if key == f'{day}_weather_label':
                    val.configure(text=weather_fc)
                if key == f'{day}_temp_label':
                    val.configure(text=f"{temp_fc}\u2103")
            

    def create_widgets(self):
        """Creates the widgets"""
        self.create_frames()
    

    def get_city(self):
        """Retrieves the user's entry for the city"""
        if len(self.city_var.get()) > 0:
            exists = self.city_exists(self.city_var.get())
            if exists:
                self.city = self.city_var.get()
                self.error_message.configure(text="Loading....", text_color="green")
                self.get_data()
                self.get_forecast()
                self.update_weather()
            else:
                self.error_message.configure(text="City does not exist")
        else:
            self.error_message.configure(text="Please enter a city")

    def city_exists(self, name):
        """Checks whether a city exists"""
        geolocator = geopy.Nominatim(user_agent="city_locator")
        location = geolocator.geocode(name, timeout=20)
        return location is not None
    
    def change_unit(self, val):
        """Toggles the temperature unit"""
        if val == "Celsius":
            self.degrees()
        else:
            self.fahrenheit()
    
    def degrees(self):
        """converts the temp to celcius"""
        print("yessss")
        self.temp_label.configure(text=f"{self.temp}\u00B0C")
        for fc in self.fc_data['data']:
            day = pd.Timestamp(fc['datetime']).day_name()
            day_now = self.date_time['day']
            
            #skip todays forecast
            if day == day_now:
                continue
            temp_fc = fc['temp']
            for key, val in self.fc_widgets.items():
                if key == f'{day}_temp_label':
                    val.configure(text=f"{temp_fc}\u00B0C")
                    
    def fahrenheit(self):
        """Converts the temp to Fahrenheit"""
        x = str(temp_converter(self.temp))
        self.temp_label.configure(text=f"{x}\u00B0F")
        
        for fc in self.fc_data['data']:
            day = pd.Timestamp(fc['datetime']).day_name()
            day_now = self.date_time['day']
            
            #skip todays forecast
            if day == day_now:
                continue
            temp_fc = fc['temp']
            y = str(temp_converter(temp_fc))
            for key, val in self.fc_widgets.items():
                if key == f'{day}_temp_label':
                    val.configure(text=f"{y}\u00B0F")
    def main(self):
        """Main function that runs all the main functions"""
        self.get_data()
        self.get_forecast()
        self.create_widgets()
        self.root.mainloop()


if __name__ == '__main__':
    wa = WeatherApp()
    wa.main()