from flask import Flask, request
from db import Db

app = Flask(__name__)

db = Db()


@app.route('/accidents')
def get_accident_by_id():
    return db.get_crashes_for_year(request.args.get('year'))


@app.route('/accidents/exact')
def get_exact_accident():
    return db.get_crash(request.args.get('year'), request   .args.get('id'))


if __name__ == '__main__':
    app.run()
