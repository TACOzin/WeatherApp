import kivy
kivy.require('2.1.0')  # Kivy version

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.clock import Clock
import requests
from datetime import datetime
from kivy.core.window import Window

Window.size = (1280,720)

class WeatherApp(App):
    def build(self):
        # ウィジェットの配置
        self.layout = BoxLayout(orientation='vertical')

        # 時刻表示用のLabel
        self.time_label = Label(text='Time: N/A', size_hint_y=None, size_hint_x=.15, height=30)
        self.layout.add_widget(self.time_label)

        # 天気情報表示用のLabel
        self.weather_label = Label(text='Weather: N/A', size_hint_y=None, size_hint_x=.15, height=30)
        self.layout.add_widget(self.weather_label)

        # 温度表示用のLabel
        self.temperature_label = Label(text='Temperature: N/A', size_hint_y=None, size_hint_x=.15, height=30)
        self.layout.add_widget(self.temperature_label)

        # 湿度表示用のLabel
        self.humidity_label = Label(text='Humidity: N/A', size_hint_y=None, size_hint_x=.15, height=30)
        self.layout.add_widget(self.humidity_label)

        #降水確率表示用のLabel
        self.pop_label = Label(text='Precipitation: N/A', size_hint_y=None, size_hint_x=.15, height=30)
        self.layout.add_widget(self.pop_label)

        # 画像表示用のImage
        self.image = Image(source='../../images/start.gif')  # デフォルトの画像
        self.image.anim_delay = 0.05  # GIFの再生速度を設定
        self.layout.add_widget(self.image)

        # 毎分データを更新
        Clock.schedule_interval(self.update_weather, 60)
        Clock.schedule_interval(self.update_time, 1)

        return self.layout
    
    def update_time(self, dt):
        # 現在時刻を更新
        current_time = datetime.now().strftime('%H:%M:%S')
        self.time_label.text = f'Time: {current_time}'

    def update_weather(self, dt):
        # OpenWeatherMapのAPIキーと都市名を指定
        api_key = 'YourAppkey'
        city_name = 'Tokyo'
        units = 'metric'

        # OpenWeatherMapのAPIエンドポイント
        api_url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&units={units}&appid={api_key}'

        # APIから天気情報を取得
        try:
            response = requests.get(api_url)
            data = response.json()

            # 天気情報を更新
            weather_description = data['weather'][0]['description']
            temperature = data['main']['temp']
            humidity = data['main']['humidity']
            pop = data.get('pop',0) * 100

            self.weather_label.text = f'Weather: {weather_description}'
            self.temperature_label.text = f'Temperature: {temperature:.2f}°C'
            self.humidity_label.text = f'Humidity: {humidity}%'
            self.pop_label.text = f'Precipitation: {pop:.2f}%'

            # 天気コードに応じてGIFを更新
            gif_path = self.get_gif_path(data['weather'][0]['id'])
            self.image.source = gif_path

        except Exception as e:
            print(f"Error fetching weather data: {e}")

    def get_gif_path(self, weather_code):
        # 天気コードに応じてGIFのパスを返す
        if 200 <= weather_code < 300: # Thunderstorm (雷雨)
            return 'Thunderstorm.gif'
        elif 300 <= weather_code < 400: # Drizzle (霧雨)
            return 'Drizzle.gif'
        elif 500 <= weather_code < 600: # Rain (雨)
            return 'rain.gif'
        elif 600 <= weather_code < 700: # Snow (雪)
            return 'snow.gif'
        elif 700 <= weather_code < 800: # Atmosphere (大気)
            return 'Atmo.gif'
        elif weather_code == 800: # Clear (晴れ)
            return 'Clear.gif'
        elif 801 <= weather_code < 900: # Clouds (曇り)
            return 'clouds.gif'
        else:
            return 'other.gif'

if __name__ == '__main__':
    WeatherApp().run()
