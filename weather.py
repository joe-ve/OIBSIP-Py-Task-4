import requests
import tkinter as tk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime

def get_weather(api_key, location):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': location,
        'appid': api_key,
        'units': 'metric'
    }
    
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

def get_forecast(api_key, location):
    base_url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {
        'q': location,
        'appid': api_key,
        'units': 'metric'
    }
    
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

def display_weather():
    location = location_entry.get()
    data = get_weather(api_key, location)
    forecast_data = get_forecast(api_key, location)
    
    if data and forecast_data:
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        weather_description = data['weather'][0]['description']
        local_time = datetime.datetime.utcfromtimestamp(data['dt'] + data['timezone']).strftime('%Y-%m-%d %H:%M:%S')
        
        weather_info.set(f"Temperature: {temp}°C\nHumidity: {humidity}%\nWeather: {weather_description.capitalize()}\nLocal Time: {local_time}")

        fig.clear()
        ax1 = fig.add_subplot(121)
        categories = ['Temperature (°C)', 'Humidity (%)']
        values = [temp, humidity]
        ax1.bar(categories, values, color=['blue', 'green'])
        ax1.set_ylim(0, 100)
        ax1.set_title("Current Weather")
        
        ax2 = fig.add_subplot(122)
        forecast_temps = [item['main']['temp'] for item in forecast_data['list'][:5]]
        forecast_times = [datetime.datetime.utcfromtimestamp(item['dt']).strftime('%Y-%m-%d %H:%M:%S') for item in forecast_data['list'][:5]]
        ax2.plot(forecast_times, forecast_temps, marker='o')
        ax2.set_title("5-Day Forecast")
        ax2.set_xlabel("Time")
        ax2.set_ylabel("Temperature (°C)")
        ax2.tick_params(axis='x', rotation=45)
        
        fig.tight_layout()
        canvas.draw()
    else:
        messagebox.showerror("Error", "Failed to get weather data. Please check your input and try again.")

if __name__ == "__main__":
    api_key = "2fd248bff1e6adc49dfe68f5852831c0"

    root = tk.Tk()
    root.title("Weather App")
    
    tk.Label(root, text="Enter city name or zip code:").pack(pady=5)
    location_entry = tk.Entry(root, width=30)
    location_entry.pack(pady=5)
    
    weather_info = tk.StringVar()
    tk.Label(root, textvariable=weather_info).pack(pady=10)
    
    tk.Button(root, text="Get Weather", command=display_weather).pack(pady=5)
    
    fig = Figure(figsize=(10, 4), dpi=100)
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack(pady=10)
    
    root.mainloop()