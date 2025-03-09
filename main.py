from fastapi import FastAPI
from pandas import read_csv
from sqlite3 import OperationalError

from database import Database


api = FastAPI()

@api.get('/')
def root() -> dict:
    return {'response': 'Chose the distric name afetr slash sign.'}

@api.get('/{district}')
def get_district(district: str) -> dict:
    db = Database()
    try: 
        result = db.get_data_for_ditrict(column = district.lower().strip())
    except OperationalError:
        db.create_info_table('warsaw')
        data_frame = read_csv('dane.csv')
        data_frame.to_sql('warsaw', db.db, if_exists='replace', index=False)
        result = db.get_data_for_ditrict(column = district.lower().strip())
    return result

@api.get('/{dict_1}/{dict_2}')
def get_districts(dict_1: str, dict_2: str) -> dict:
    db = Database()
    try: 
        result = db.get_data_for_districts(dict_1,  dict_2)
    except OperationalError:
        db.create_info_table('warsaw')
        data_frame = read_csv('dane.csv')
        data_frame.to_sql('warsaw', db.db, if_exists='replace', index=False)
        result = db.get_data_for_districts(dict_1,  dict_2)
    # Wyciąganie danych dla dwóch dystryktów
    return result