import requests
from sqlalchemy import create_engine, Table, Column, String, Float, MetaData
from sqlalchemy.sql import select


class WeatherProvider:
    def __init__(self, key):
        self.key = key

    def fetch_data(self, location, num_of_days):
        url = 'https://api.openweathermap.org/data/2.5/forecast'
        params = {
            'q': location,
            'appid': self.key,
            'units': 'metric',
            'cnt': num_of_days
        }

        if num_of_days < 1 or num_of_days > 16:
            raise Exception('Invalid input. Number of days should be from 1 to 16')

        try:
            data = requests.get(url, params).json()

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


class DataBaseProvider:
    def __init__(self, connection_string):
        self.metadata = MetaData()
        self.table = Table(
            'weather',
            self.metadata,
            Column('main', String),
            Column('description', String),
            Column('temp', Float),
            Column('feels_like', Float),
            Column('temp_min', Float),
            Column('temp_max', Float),
            Column('pressure', Float),
        )
        self.engine = create_engine(connection_string)
        self.metadata.create_all(self.engine)

    def insert_data(self, data):
        print(data)
        try:
            client = self.engine.connect()
            client.execute(self.table.insert(), data)
        except Exception as e:
            return e

    def select_data(self):
        try:
            client = self.engine.connect()
            return client.execute(select([self.table]))
        except Exception as e:
            return e


provider = WeatherProvider('97fc4bb256b73c3617b684c1588bd57b')
db_client = DataBaseProvider('sqlite:///weather.sqlite3')

db_client.insert_data(provider.fetch_data('Volgograd,Russia', 16))

for row in db_client.select_data():
    print(row)
