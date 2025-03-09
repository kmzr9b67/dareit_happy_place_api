import sqlite3

class Database():
    _instance = None

    def __new__(cls):
        if Database._instance == None:
            Database._instance = super(Database,cls).__new__(cls)
        return Database._instance


    def __init__(self):
        if not hasattr(self, 'db'):
            self.db = sqlite3.connect('districts-info.db', check_same_thread=False)
            self.cursor = self.db.cursor()
    

    def create_info_table(self, citi:str) -> None:
        # TODO 2: Dopisać wartości jakie mają być brane podwzględę cen nieruchmości 
        # TODO 3: Zmienić nazwy kolumn.
        self.cursor.execute(f'''CREATE TABLE {citi} 
                            (id INTEGER PRIMARY KEY, 
                            district_name varchar(250) NOT NULL UNIQUE,
                            area FLOAT NOT NULL,
                            nr_of_inhabitants FLOAT NOT NULL, 
                            nr_of_people_per_pharmacy FLOAT,
                            nr_of_people_per_clinic FLOAT, 
                            nr_of_med_consult_per_capita FLOAT,
                            nr_of_kindergartens INTEGER,
                            nr_of_children_in_edu_inst  FLOAT, 
                            areas_green FLOAT,
                            nr_of_unemployed FLOAT,
                            birthrate FLOAT)''')
    
    @staticmethod
    def to_dictionary(t: tuple) -> dict:
        return {'district_name': t[1],
                'area': t[2],
                'nr_of_inhabitants': t[3],
                'nr_of_people_per_pharmacy': t[4],
                'nr_of_people_per_clinic': t[5],
                'nr_of_med_consult_per_capita': t[6],
                'nr_of_kindergartens': t[7], 
                'nr_of_children_in_edu_inst': t[8],
                'areas_green': t[9],
                'nr_of_unemployed': t[10],
                'birthrate': t[11]
                }
        
    def insert_data_citi_table(self, citi:str, data:list) -> None:
        self.cursor.execute(f'''INSERT into {citi} VALUES{data}''')
        self.db.commit()

    def get_data_for_ditrict(self, column:str) -> dict:
        result = self.cursor.execute(f'''SELECT * 
                                   FROM warsaw
                                   WHERE district_name = "{column}";''')
        tuple_result = list(result)[0]
        return Database.to_dictionary(t=tuple_result)
    
    def get_data_for_districts(self, district:str, district_2: str):
        query = '''SELECT *
                    FROM warsaw
                    WHERE district_name IN (?,?);'''
        results = self.cursor.execute(query, (district, district_2))
        tuple_results = list(results)
        dict_results = {}
        counter = 0
        
        for i in tuple_results:
            dict_results[counter] = Database.to_dictionary(t = i)
            counter += 1
            
        return dict_results
    
