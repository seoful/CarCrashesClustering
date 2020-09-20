from pymongo import MongoClient
import json
from datetime import datetime


class Db:

    def __init__(self):
        self.client = MongoClient(
            "mongodb+srv://seoful:prpzg6RO5sfTWhrH@crashes.kk22f.mongodb.net/crashes?retryWrites=true&w=majority")

    def get_crashes_for_year(self, year):
        db = self.client['crashes'][str(year)]
        crashes = db.find({})
        crashes = self.reduce_crashes(crashes)
        return json.dumps(crashes)

    def get_crashes_for_period(self, start: datetime, end: datetime) -> str:
        start_year = start.year
        end_year = end.year
        crashes_arr = []
        for year in (start_year, end_year + 1):
            db = self.client['crashes'][str(year)]
            crashes = db.find({'$and': [{'date': {"$gte": start}},
                                        {'date': {"$lte": end}}]})
            crashes = self.reduce_crashes(crashes)
            crashes_arr += list(crashes)
        return json.dumps(crashes_arr)

    def get_crash(self, year, id):
        db = self.client['crashes'][str(year)]
        crash = db.find_one({'ac_id': int(id)})
        del crash['_id']
        crash['date'] = str(crash['date'])
        return json.dumps(crash)

    def reduce_crashes(self, crashes):
        crashes_arr = []
        for crash in crashes:
            crash_obj = {
                'date': str(crash['date']),
                'id': crash['ac_id'],
                'type': str(crash['kind']),
                'lng': crash['lng'],
                'ltd': crash['ltd']
            }
            crashes_arr.append(crash_obj)
        return crashes_arr
