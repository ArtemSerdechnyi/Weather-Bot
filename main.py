import requests
import config
import json
from aiogram import Bot, executor, Dispatcher, types
from thefuzz import fuzz, process

bot = Bot(token=config.token)
dp = Dispatcher(bot=bot)


@dp.message_handler(commands=['start'])
async def start(msg: types.Message) -> None:
    await msg.answer('Enter your city:')
    await msg.delete()


@dp.message_handler(content_types=['text'])
async def all_msg(msg: types.Message) -> types.Message:
    capitalize_text_msg = msg.text.title().strip()
    print(capitalize_text_msg.split())

    if capitalize_text_msg in city:
        lat = data.get(capitalize_text_msg)['latitude']
        lon = data.get(capitalize_text_msg)['longitude']
        url_weather = config.WEATHER_URL.format(lat=lat, lon=lon, API_key=config.WEATHER_TOKEN)
        response_weather: dict = json.loads(requests.get(url_weather).text)
        cloudiness = response_weather.get('weather')[0]['main']
        temp = round(int(response_weather.get('main')['temp']) - 273.15)
        feels_like = round(int(response_weather.get('main')['feels_like']) - 273.15)
        wind_speed = response_weather.get('wind')['speed']
        return await msg.answer(f"""
        {capitalize_text_msg} city:
    Cloudiness: {cloudiness} 
    Temperature: {temp} ℃
    Feels like: {feels_like} ℃
    Wind speed: {wind_speed} m/s
""", parse_mode='HTML')

    for i in capitalize_text_msg.split():
        if not i.isalpha():
            break
    else:
        fuzz_word = process.extract(capitalize_text_msg, city, limit=6, scorer=fuzz.ratio)
        walid_fuzz_word = ', '.join([i[0] for i in fuzz_word if i[1] >= 70])
        if walid_fuzz_word:
            return await msg.answer(f'Maybe you meant: <b>{walid_fuzz_word}</b>?', parse_mode='HTML')
    await msg.answer('City not found.')


with open('city_coordinates', 'r', encoding='utf8') as file:
    data = json.load(file)
    city = data.keys()

if __name__ == '__main__':
    executor.start_polling(dp)
