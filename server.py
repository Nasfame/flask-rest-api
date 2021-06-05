import csv
import json
import os

from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def home():
    try:
        os.mkdir('data')
    finally:
        try:
            os.chdir('data')
            __ = os.popen('echo id,name,email,mobile,age > user.csv', 'w')
            os.chdir('.')
        finally:
            try:
                os.rename('user.csv', 'admin.csv')
            finally:
                return json.dumps("All went well")


@app.route('/users')
def listing():
    with open('data/user.csv', 'r') as f1:
        f1 = csv.DictReader(f1)
        li = list(f1)

    return json.dumps(li)


@app.route('/users/create', methods=['POST'])
def create():
    with open('data/user.csv', 'a') as f1:
        f1 = csv.writer(f1)
        cnt = json.loads(listing())
        values = list(request.json.values())
        values.insert(0, str(len(cnt) + 1))
        f1.writerow(values)
    return "Success"


@app.route('/users/show/<id>')
def show(id):
    cnt = json.loads(listing())
    return json.dumps(cnt[int(id) - 1])


@app.route('/users/edit/<id>', methods=['PATCH'])
def edit(id):
    id = int(id)
    cnt = json.loads(listing())
    cnt[id - 1] = request.json
    cnt[id - 1]['id'] = id
    with open('data/user.csv', 'w') as f1:
        f1 = csv.DictWriter(f1, fieldnames=['id', 'name', 'email', 'mobile', 'age'])
        f1.writeheader()
        f1.writerows(cnt)

    return "Edited"


@app.route('/users/delete/<int:id>', methods=['DELETE'])
def delete(id):
    cnt = json.loads(listing())
    cnt.pop(id - 1)
    for i in range(len(cnt)):
        cnt[i]['id'] = str(i + 1)
    with open('data/user.csv', 'w') as f1:
        f1 = csv.DictWriter(f1, fieldnames=['id', 'name', 'email', 'mobile', 'age'])
        f1.writeheader()
        f1.writerows(cnt)

    return "Deleted"


if __name__ == '__main__':
    app.run(debug=True)
