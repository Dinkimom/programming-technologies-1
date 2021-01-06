import requests
from sqlalchemy import create_engine, Table, Column, String, Float, MetaData
from sqlalchemy.sql import select


class WeatherProvider:
    def __init__(self, key):
        self.key = key

    def get_data(self, location, start_date, end_date):
        url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/history'
        params = {
            'aggregateHours': 24,
            'startDateTime': f'{start_date}T00:0:00',
            'endDateTime': f'{end_date}T23:59:59',
            'unitGroup': 'metric',
            'location': location,
            'key': self.key,
            'contentType': 'json',
        }
        data = requests.get(url, params).json()
        return [
            {
                'date': row['datetimeStr'][:10],
                'mint': row['mint'],
                'maxt': row['maxt'],
                'location': 'Volgograd,Russia',
                'humidity': row['humidity'],
            }
            for row in data['locations'][location]['values']
        ]


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

provider = WeatherProvider('I3D60I88UB6KPSDAVGK38HNP5')
c.execute(weather.insert(), provider.get_data('Volgograd,Russia', '2020-09-20', '2020-09-29'))

for row in c.execute(select([weather])):
    print(row)
