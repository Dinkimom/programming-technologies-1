import requests
from sqlalchemy import create_engine, Table, Column, String, Float, MetaData
from sqlalchemy.sql import select


class WeatherProvider:
    def __init__(self, key):
        self.key = key

    def get_data(self, location, num_of_days):
        url = 'https://api.openweathermap.org/data/2.5/forecast'
        params = {
            'q': location,
            'appid': self.key,
            'units': 'metric',
            'cnt': num_of_days
        }

        if num_of_days < 1 | num_of_days > 17:
            raise Exception('Invalid input. Number of days should be from 1 to 16')

        try:
            data = requests.get(url, params).json()

            # for row in data['list']:
            #     print(row['main'])

            return [{
                'main': row['weather'][0]['main'],
                'description': row['weather'][0]['description'],
                'temp': row['main']['temp'],
                'feels_like': row['main']['feels_like'],
                'temp_min': row['main']['temp_min'],
                'temp_max': row['main']['temp_max'],
                'pressure': row['main']['pressure'],
            } for row in data['list']]
        except Exception as e:
            return e


engine = create_engine('sqlite:///weather.sqlite3')
metadata = MetaData()
weather = Table(
    'weather',
    metadata,
    Column('date', String),
    Column('mint', Float),
    Column('maxt', Float),
    Column('location', String),
    Column('humidity', Float),
)
metadata.create_all(engine)

c = engine.connect()

provider = WeatherProvider('97fc4bb256b73c3617b684c1588bd57b')

result = provider.get_data('Volgograd,Russia', 1)

print(result)

# c.execute(weather.insert(), provider.get_data('Volgograd,Russia', '2020-09-20', '2020-09-29'))
#
# for row in c.execute(select([weather])):
#     print(row)
