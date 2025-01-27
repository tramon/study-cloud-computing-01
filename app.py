from flask import Flask, json, jsonify
from flask import request, redirect
from flask import render_template
import datetime

from calc.calculations import tricky_divide, sum_calculation
from db.Dao import Dao

app = Flask(__name__)

dao = Dao()


@app.route("/", methods=['GET'])
def home():
    dataset = dao.read_top_100()
    return render_template('index.html', objects=dataset)


@app.route("/add", methods=['POST'])
def add():
    task_to_add = request.form['add']
    if task_to_add is not "":
        dao.insert_without_id(task_to_add)
    return redirect(request.referrer)


@app.route("/delete", methods=['POST'])
def delete():
    id_to_delete = request.form['delete']
    if id_to_delete.isdigit():
        dao.delete_by_id(id_to_delete)
    return redirect(request.referrer)


@app.route("/calendar", methods=['GET'])
def get_calendar():
    date_time_now = datetime.datetime.now()
    return render_template('calendar.html', date_time=date_time_now)


@app.route("/calc", methods=['GET'])
def get_calc():
    sum_of_two = 0
    divide_result = 0
    return render_template('calc.html', sum_of_two=sum_of_two, divide_result=divide_result)


@app.route("/sum", methods=['POST'])
def calc_sum():
    calc_add_first = request.form['add_one']
    calc_add_second = request.form['add_two']
    sum_of_two = sum_calculation(calc_add_first, calc_add_second)
    return render_template('calc.html', sum_of_two=sum_of_two)


# This will produce failures on purpose to help with test failures
@app.route("/divide", methods=['POST'])
def calc_divide():
    divide_first = request.form['divide_one']
    divide_second = request.form['divide_two']
    divide_result = tricky_divide(divide_first, divide_second)
    return render_template('calc.html', divide_result=divide_result)


@app.route("/api/get", methods=['GET'])
def get_all():
    json_dataset = dao.read_top_100()
    tasks_list = [task.to_dict() for task in json_dataset]
    return jsonify(tasks_list)


@app.route("/api/put", methods=['PUT'])
def put():
    task_to_add = request.form['put']
    if task_to_add is not "":
        dao.insert_without_id(task_to_add)
        return return_success(201)


@app.route("/api/delete", methods=['DELETE'])
def delete_via_api():
    id_to_delete = request.form['delete']
    if id_to_delete.isdigit():
        dao.delete_by_id(id_to_delete)
        return return_success()


def return_success(status_code=200):
    return json.dumps({'success': True}), status_code, {'ContentType': 'application/json'}


if __name__ == "__main__":
    app.run()
