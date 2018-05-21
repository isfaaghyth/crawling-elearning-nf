from requests import session
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import json

url = 'https://elen.nurulfikri.ac.id'
loginurl = url + '/login/index.php'
taskurl = url + '/my/index.php?mynumber=-2'

def login():
    payload = {'action': 'login', 'username': '###','password': '###'}
    with session() as ses:
        r = ses.post(loginurl, data=payload)
        return ses


session = login()
content = session.get(taskurl)
content = BeautifulSoup(content.text, "html.parser")
course_name = content.find_all('div', class_='box coursebox')

courses = []

for i in course_name:
    name = i.find(class_='course_title').find(class_='title').find('a').text
    print("nama matkul => ", name)

    assignment = i.find_all(class_='assign overview')
    if len(assignment) != 0:
        for j in assignment:
            assignment_name = j.find(class_='name').find('a').text
            assignment_due = j.find(class_='info').text
            print("-> ", assignment_name)
            print("-> ", assignment_due)
    else:
        print("-> tidak ada")
