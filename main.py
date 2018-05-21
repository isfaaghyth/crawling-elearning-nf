from requests import session
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import json

app = Flask(__name__)

url = 'https://elen.nurulfikri.ac.id'
loginurl = url + '/login/index.php'
taskurl = url + '/my/index.php?mynumber=-2'

@app.route('/cek', methods=['POST'])
def get():
    payload = {
        'action': 'login',
        'username': request.form.get('username'),
        'password': request.form.get('password')
    }

    req = session()
    req.post(loginurl, data=payload)

    content = req.get(taskurl)
    content = BeautifulSoup(content.text, "html.parser")
    course_name = content.find_all('div', class_='box coursebox')

    courses_item = []

    for i in course_name:
        name = i.find(class_='course_title').find(class_='title').find('a').text
        assignment = i.find_all(class_='assign overview')
        courses = []
        if len(assignment) != 0:
            for j in assignment:
                assignment_name = j.find(class_='name').find('a').text
                assignment_due = j.find(class_='info').text
                res_assignment = {
                    'title': assignment_name,
                    'due': assignment_due
                }
                courses.append(res_assignment)

        temp_item = {
            'course_name': name,
            'tasks': courses
        }
        courses_item.append(temp_item)

    return jsonify(courses_item)

if __name__ == '__main__':
     app.run(port='5002')
