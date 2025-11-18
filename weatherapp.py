#WeatherApp
#A simple weather application GUI using Tkinter

#importing the tkinter module + requests module

import tkinter as tk
import requests

#creating the API key and base URL for weather data

def getWeather ():

    api_key = "f956d3bc4701b44c02fe62aaaceb3e3c"

    city = textareaentry.get()    #getting the city name from the entry area

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    response = requests.get(url) #making the API request

    data = response.json() 

    if data.get("cod") != 200: #checking if the response is valid

        temperatureValuelabel.config(text="N/A")
        humidityValuelabel.config(text="N/A")
        windspeedValuelabel.config(text="N/A")
        PressureValuelabel.config(text="N/A")
        precipitationValuelabel.config(text="N/A")

    else:   #if the response is valid, extract the weather data and update the labels
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        pressure = data["main"]["pressure"]
        precipitation = data["weather"][0]["description"]

        temperatureValuelabel.config(text=f"{temperature} °C")
        humidityValuelabel.config(text=f"{humidity} %")
        windspeedValuelabel.config(text=f"{wind_speed} km/h")
        PressureValuelabel.config(text=f"{pressure} hPa")
        precipitationValuelabel.config(text=f"{precipitation} mm")
   
#Creating the main window

window = tk.Tk()
window.title("Almdrasa Weather App")
window.rowconfigure(0, weight=1)
window.rowconfigure(1, weight=1)
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
window.columnconfigure(2, weight=1)

#making the search button, the entry area & Location label

textarealabel = tk.Label(window, text="Location:")
textarealabel.grid( column=0 , row=0 , sticky="e" , padx=10 , pady=10)

textareaentry= tk.Entry(window)
textareaentry.grid(column=1, row=0, padx=10 , pady=10 , sticky="e")

searchbtt = tk.Button(window , text= "search" , command= getWeather) #linking the search button to the getWeather function
searchbtt.grid(column=2,row=0 , padx=10, pady=10 , sticky="nsew" )  

#making the weather info labels 

temperaturelabel = tk.Label(window, text="Temperature:")
temperaturelabel.grid( column=0 , row=1 , sticky="e" , padx=10 , pady=10)

humiditylabel = tk.Label(window, text="Humidity:")
humiditylabel.grid( column=0 , row=2 , sticky="e" , padx=10 , pady=10)

windspeedlabel = tk.Label(window, text="Wind Speed:")
windspeedlabel.grid( column=0 , row=3 , sticky="e" , padx=10 , pady=10)

Pressurelabel = tk.Label(window, text="Pressure:")
Pressurelabel.grid( column=0 , row=4 , sticky="e" , padx=10 , pady=10)

precipitationlabel = tk.Label(window, text="Precipitation:")
precipitationlabel.grid( column=0 , row=5 , sticky="e" , padx=10 , pady=10)

#completing the weather info labels

temperatureValuelabel = tk.Label(window, text="-- °C")
temperatureValuelabel.grid( column=1 , row=1 , sticky="W" )

humidityValuelabel = tk.Label(window, text="-- %")
humidityValuelabel.grid( column=1 , row=2 , sticky="W" )

windspeedValuelabel = tk.Label(window, text="-- km/h")
windspeedValuelabel.grid( column=1 , row=3 , sticky="W" )

PressureValuelabel = tk.Label(window, text="-- hPa")
PressureValuelabel.grid( column=1 , row=4 , sticky="W" )

precipitationValuelabel = tk.Label(window, text="-- %")
precipitationValuelabel.grid( column=1 , row=5 , sticky="w" )


window.mainloop()