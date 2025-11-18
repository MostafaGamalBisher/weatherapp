import tkinter as tk
from tkinter import ttk
import requests
import geonamescache

# Initialize geonamescache and get cities
gc = geonamescache.GeonamesCache()
cities_dict = gc.get_cities()
CITIES = [city['name'] for city in cities_dict.values() if city.get('population', 0) > 100000]
print(f"Loaded {len(CITIES)} cities")

def getWeather():
    api_key = "f956d3bc4701b44c02fe62aaaceb3e3c"
    city = textareaentry.get()
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    response = requests.get(url)
    data = response.json()

    if data.get("cod") != 200:
        temperatureValuelabel.config(text="N/A")
        humidityValuelabel.config(text="N/A")
        windspeedValuelabel.config(text="N/A")
        PressureValuelabel.config(text="N/A")
        precipitationValuelabel.config(text="N/A")
    else:
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        pressure = data["main"]["pressure"]
        precipitation = data["weather"][0]["description"]

        temperatureValuelabel.config(text=f"{temperature} °C")
        humidityValuelabel.config(text=f"{humidity} %")
        windspeedValuelabel.config(text=f"{wind_speed} km/h")
        PressureValuelabel.config(text=f"{pressure} hPa")
        precipitationValuelabel.config(text=f"{precipitation}")

def on_key_release(event):
    value = textareaentry.get()
    
    if value == '':
        # إخفاء الاقتراحات إذا كان الحقل فارغ
        suggestion_listbox.delete(0, tk.END)
        suggestion_frame.place_forget()
    else:
        # فلترة المدن بناء على الإدخال
        filtered_cities = [city for city in CITIES if value.lower() in city.lower()]
        
        # تحديث قائمة الاقتراحات
        suggestion_listbox.delete(0, tk.END)
        for city in filtered_cities[:8]:  # عرض أول 8 اقتراحات فقط
            suggestion_listbox.insert(tk.END, city)
        
        # إظهار إطار الاقتراحات تحت حقل الإدخال
        if filtered_cities:
            x = textareaentry.winfo_x()
            y = textareaentry.winfo_y() + textareaentry.winfo_height()
            width = textareaentry.winfo_width()
            
            suggestion_frame.place(x=x, y=y, width=width)
            suggestion_listbox.config(height=min(8, len(filtered_cities)))
        else:
            suggestion_frame.place_forget()

def on_suggestion_select(event):
    # عند اختيار اقتراح من القائمة
    selection = suggestion_listbox.curselection()
    if selection:
        selected_city = suggestion_listbox.get(selection[0])
        textareaentry.delete(0, tk.END)
        textareaentry.insert(0, selected_city)
        suggestion_frame.place_forget()
        # إخفاء لوحة المفاتيح على Android إذا كان ذلك مناسباً
        textareaentry.focus_set()

def on_focus_out(event):
    # إخفاء الاقتراحات عند فقدان التركيز (بعد فترة قصيرة)
    window.after(150, hide_suggestions)

def hide_suggestions():
    suggestion_frame.place_forget()

# Creating the main window
window = tk.Tk()
window.title("Almdrasa Weather App")
window.geometry("400x500")

# Configure grid
for i in range(6):
    window.rowconfigure(i, weight=1)
for i in range(3):
    window.columnconfigure(i, weight=1)

# Location label and entry
textarealabel = tk.Label(window, text="Location:")
textarealabel.grid(column=0, row=0, sticky="e", padx=10, pady=10)

# استخدام Entry عادي بدلاً من Combobox
textareaentry = tk.Entry(window, font=("Arial", 12))
textareaentry.grid(column=1, row=0, padx=10, pady=10, sticky="ew")
textareaentry.bind('<KeyRelease>', on_key_release)
textareaentry.bind('<FocusOut>', on_focus_out)

# إنشاء إطار للاقتراحات
suggestion_frame = tk.Frame(window, bg="white", relief="solid", borderwidth=1)
suggestion_listbox = tk.Listbox(suggestion_frame, font=("Arial", 10), bg="white", selectmode="single")
suggestion_listbox.pack(fill="both", expand=True)
suggestion_listbox.bind('<Double-Button-1>', on_suggestion_select)
suggestion_listbox.bind('<Return>', on_suggestion_select)

searchbtt = tk.Button(window, text="Search", command=getWeather, bg="#4CAF50", fg="white", font=("Arial", 10))
searchbtt.grid(column=2, row=0, padx=10, pady=10, sticky="nsew")

# Weather info labels
temperaturelabel = tk.Label(window, text="Temperature:", font=("Arial", 11))
temperaturelabel.grid(column=0, row=1, sticky="e", padx=10, pady=10)

humiditylabel = tk.Label(window, text="Humidity:", font=("Arial", 11))
humiditylabel.grid(column=0, row=2, sticky="e", padx=10, pady=10)

windspeedlabel = tk.Label(window, text="Wind Speed:", font=("Arial", 11))
windspeedlabel.grid(column=0, row=3, sticky="e", padx=10, pady=10)

Pressurelabel = tk.Label(window, text="Pressure:", font=("Arial", 11))
Pressurelabel.grid(column=0, row=4, sticky="e", padx=10, pady=10)

precipitationlabel = tk.Label(window, text="Description:", font=("Arial", 11))
precipitationlabel.grid(column=0, row=5, sticky="e", padx=10, pady=10)

# Value labels
temperatureValuelabel = tk.Label(window, text="-- °C", font=("Arial", 11))
temperatureValuelabel.grid(column=1, row=1, sticky="W")

humidityValuelabel = tk.Label(window, text="-- %", font=("Arial", 11))
humidityValuelabel.grid(column=1, row=2, sticky="W")

windspeedValuelabel = tk.Label(window, text="-- km/h", font=("Arial", 11))
windspeedValuelabel.grid(column=1, row=3, sticky="W")

PressureValuelabel = tk.Label(window, text="-- hPa", font=("Arial", 11))
PressureValuelabel.grid(column=1, row=4, sticky="W")

precipitationValuelabel = tk.Label(window, text="--", font=("Arial", 11))
precipitationValuelabel.grid(column=1, row=5, sticky="w")

window.mainloop()