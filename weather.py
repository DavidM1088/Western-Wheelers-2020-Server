import configparser
import requests
import sys


def get_api_key():
    #config = configparser.ConfigParser()
    #config.read('config.ini')
    #return config['openweathermap']['api']
    return "d254d5637cae65353c98ac0aa641e7cd"


def get_weather(api_key, location):
    #url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}".format(location, api_key)
    #(282K − 273.15) × 9 / 5 + 32 = 47.93°F
    url = "https://api.openweathermap.org/data/2.5/weather?zip=94024,us&appid=d254d5637cae65353c98ac0aa641e7cd"
    # palo alto 7 days
    url = "https://api.openweathermap.org/data/2.5/onecall?lat=37.46&lon=-122.14&units=imperial&appid=d254d5637cae65353c98ac0aa641e7cd"
    r = requests.get(url)
    return r.json()


def main():
    print(sys.argv)
    if len(sys.argv) != 2:
        exit("Usage: {} LOCATION".format(sys.argv[0]))
    location = sys.argv[1]

    api_key = get_api_key()
    weather = get_weather(api_key, location)

    #print(weather['main']['temp'])
    print(weather)


if __name__ == '__main__':
    main()