# Weather App - محسّن
import tkinter as tk
from tkinter import messagebox
import requests

# ----- دالة جلب الطقس وإظهار النتائج -----
def getWeather():
    city = textareaentry.get().strip()
    if not city:
        messagebox.showwarning("Input required", "Please enter a city name.")
        return

    api_key = "f956d3bc4701b44c02fe62aaaceb3e3c"  # ملاحظة: لا ترفع المفتاح في GitHub
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url, timeout=8)
    except requests.exceptions.RequestException as e:
        # مشاكل الشبكة أو المهلة
        messagebox.showerror("Network error", f"Failed to connect to the weather service.\n{e}")
        return

    # تأكد من حالة الرد
    if response.status_code != 200:
        # حاول نقرأ رسالة الخطأ من الرد لو موجودة
        try:
            data = response.json()
            err = data.get("message", "Unknown error")
        except ValueError:
            err = "Unknown error"
        # عرض رسالة للمستخدم
        messagebox.showinfo("No data", f"Could not find weather for '{city}'.\n{err}")
        # ضع قيم N/A في الواجهة
        temperatureValuelabel.config(text="N/A")
        humidityValuelabel.config(text="N/A")
        windspeedValuelabel.config(text="N/A")
        PressureValuelabel.config(text="N/A")
        precipitationValuelabel.config(text="N/A")
        window.title("Almdrasa Weather App")
        return

    # لو الرد ناجح: فرز البيانات وتحديث الواجهه
    try:
        data = response.json()
        # استخراج القيم بأمان باستخدام .get
        city_name = data.get("name", city)
        temperature = data.get("main", {}).get("temp")
        humidity = data.get("main", {}).get("humidity")
        wind_speed_ms = data.get("wind", {}).get("speed")  # m/s
        pressure = data.get("main", {}).get("pressure")
        description = None
        weather_list = data.get("weather")
        if weather_list and isinstance(weather_list, list):
            description = weather_list[0].get("description")

        # تحضير السلاسل للعرض (مع تقريبات)
        if temperature is not None:
            temp_text = f"{round(temperature, 1)} °C"
        else:
            temp_text = "N/A"

        if humidity is not None:
            humidity_text = f"{humidity} %"
        else:
            humidity_text = "N/A"

        if wind_speed_ms is not None:
            # تحويل m/s إلى km/h
            wind_kmh = wind_speed_ms * 3.6
            wind_text = f"{round(wind_kmh,1)} km/h"
        else:
            wind_text = "N/A"

        if pressure is not None:
            pressure_text = f"{pressure} hPa"
        else:
            pressure_text = "N/A"

        if description:
            precip_text = description.capitalize()  # وصف نصي، مش كمية أمطار
        else:
            precip_text = "N/A"

        # تحديث الـ Labels في الواجهة
        temperatureValuelabel.config(text=temp_text)
        humidityValuelabel.config(text=humidity_text)
        windspeedValuelabel.config(text=wind_text)
        PressureValuelabel.config(text=pressure_text)
        precipitationValuelabel.config(text=precip_text)

        # تحديث عنوان النافذة باسم المدينة
        window.title(f"Almdrasa Weather App - {city_name}")

    except Exception as e:
        messagebox.showerror("Parsing error", f"Failed to read weather data.\n{e}")
        return

# ----- واجهة المستخدم -----
window = tk.Tk()
window.title("Almdrasa Weather App")
window.rowconfigure(0, weight=0)
window.rowconfigure(1, weight=1)
window.columnconfigure(0, weight=0)
window.columnconfigure(1, weight=1)
window.columnconfigure(2, weight=0)

# صف الادخال
textarealabel = tk.Label(window, text="Location:")
textarealabel.grid(column=0, row=0, sticky="e", padx=10, pady=10)

textareaentry = tk.Entry(window)
textareaentry.grid(column=1, row=0, padx=10, pady=10, sticky="we")

searchbtt = tk.Button(window, text="Search", command=getWeather)
searchbtt.grid(column=2, row=0, padx=10, pady=10, sticky="nsew")

# تسهيل الاستخدام: اضغط Enter لتنفيذ البحث
def on_enter_key(event):
    getWeather()

textareaentry.bind("<Return>", on_enter_key)

# تسميات المعلومات
temperaturelabel = tk.Label(window, text="Temperature:")
temperaturelabel.grid(column=0, row=1, sticky="e", padx=10, pady=6)

humiditylabel = tk.Label(window, text="Humidity:")
humiditylabel.grid(column=0, row=2, sticky="e", padx=10, pady=6)

windspeedlabel = tk.Label(window, text="Wind Speed:")
windspeedlabel.grid(column=0, row=3, sticky="e", padx=10, pady=6)

Pressurelabel = tk.Label(window, text="Pressure:")
Pressurelabel.grid(column=0, row=4, sticky="e", padx=10, pady=6)

precipitationlabel = tk.Label(window, text="Condition:")
precipitationlabel.grid(column=0, row=5, sticky="e", padx=10, pady=6)

# قيم النتائج (تُحدث بالدالة)
temperatureValuelabel = tk.Label(window, text="-- °C")
temperatureValuelabel.grid(column=1, row=1, sticky="w")

humidityValuelabel = tk.Label(window, text="-- %")
humidityValuelabel.grid(column=1, row=2, sticky="w")

windspeedValuelabel = tk.Label(window, text="-- km/h")
windspeedValuelabel.grid(column=1, row=3, sticky="w")

PressureValuelabel = tk.Label(window, text="-- hPa")
PressureValuelabel.grid(column=1, row=4, sticky="w")

precipitationValuelabel = tk.Label(window, text="--")
precipitationValuelabel.grid(column=1, row=5, sticky="w")

window.mainloop()
