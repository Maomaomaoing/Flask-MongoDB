# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 09:22:11 2018

@author: user
"""
import os
os.chdir('C:\\Users\\user\\Desktop\\hw1')
from pymongo import MongoClient
from flask import Flask, jsonify, abort, request, render_template, flash, redirect, session
from config import DevConfig
from urllib.parse import quote_plus
import json
from flask_wtf import Form
from wtforms import StringField, BooleanField, SelectField 
from wtforms.validators import DataRequired



""" 連接MongoDB """
uri = "mongodb://%s:%s@%s" % (quote_plus('Mao'), quote_plus('7711'), quote_plus('127.0.0.1'))
client = MongoClient(uri)
cllct = client.admin.homicide

""" 分析圖表, 搜尋 """
import make_plot
import attribute_value
plot_result = make_plot.make_plot()
print('plot_result OK')
value_dict = attribute_value.attribute_value()
print('value_dict OK')

class QueryForm(Form):  
    def get_choice(value_list):
        choices = [('---', '---')]
        for value in value_list:
            choices.append(tuple([value])*2)
        return choices
    
    AgencyType = SelectField('Agency Type', choices=get_choice(value_dict['Agency Type']))
    CrimeSolved = SelectField('Crime Solved', choices=get_choice(value_dict['Crime Solved']))
    CrimeType = SelectField('Crime Type', choices=get_choice(value_dict['Crime Type']))
    Month = SelectField('Month', choices=get_choice(value_dict['Month']))
    PerpetratorCount = SelectField('Perpetrator Count', choices=get_choice(value_dict['Perpetrator Count']))
    PerpetratorEthnicity = SelectField('Perpetrator Ethnicity', choices=get_choice(value_dict['Perpetrator Ethnicity']))
    PerpetratorRace = SelectField('Perpetrator Race', choices=get_choice(value_dict['Perpetrator Race']))
    PerpetratorSex = SelectField('Perpetrator Sex', choices=get_choice(value_dict['Perpetrator Sex']))
    Relationship = SelectField('Relationship', choices=get_choice(value_dict['Relationship']))
    State = SelectField('State', choices=get_choice(value_dict['State']))
    VictimCount = SelectField('Victim Count', choices=get_choice(value_dict['Victim Count']))
    VictimEthnicity = SelectField('Victim Ethnicity', choices=get_choice(value_dict['Victim Ethnicity']))
    VictimRace = SelectField('Victim Race', choices=get_choice(value_dict['Victim Race']))
    VictimSex = SelectField('Victim Sex', choices=get_choice(value_dict['Victim Sex']))
    Weapon = SelectField('Weapon', choices=get_choice(value_dict['Weapon']))
    Year = SelectField('Year', choices=get_choice(value_dict['Year']))

#class LoginForm(Form):
#    openid = StringField('openid', validators=[DataRequired()])
#    remember_me = BooleanField('remember_me', default=False)
#    
os.chdir('C:\\Users\\user\\Desktop\\hw1')
""" 初始化 Flask 類別成為 instance """
app = Flask(__name__)
app.config.from_object(DevConfig)

""" 路由和處理函式配對 """

@app.route('/')
def home():
    return render_template("home.html", title = 'Home')

@app.route('/analysis_result')
def analysis_result():
#    import make_plot
#    plot_result = make_plot.make_plot()
    return render_template("analysis_result.html", title = 'Analysis Result', plot_result = plot_result)

@app.route('/querying', methods = ['GET', 'POST'])
def querying():
    form = QueryForm()
#    import attribute_value
#    value_dict = attribute_value.attribute_value()
    
    if form.is_submitted():
        condition = {'Agency Type': form.AgencyType.data,
                     'Crime Solved': form.CrimeSolved.data,
                     'Crime Type': form.CrimeType.data,
                     'Month': form.Month.data,
                     'Perpetrator Count': form.PerpetratorCount.data,
                     'Perpetrator Ethnicity': form.PerpetratorEthnicity.data,
                     'Perpetrator Race': form.PerpetratorRace.data,
                     'Perpetrator Sex': form.PerpetratorSex.data,
                     'Relationship': form.Relationship.data,
                     'State': form.State.data,
                     'Victim Count': form.VictimCount.data,
                     'Victim Ethnicity': form.VictimEthnicity.data,
                     'Victim Race': form.VictimRace.data,
                     'Victim Sex': form.VictimSex.data,
                     'Weapon': form.Weapon.data,
                     'Year': form.Year.data}
        current_key = list(condition.keys())
        for key in current_key:
            if condition[key] == '---':
                condition.pop(key, None)
        result = cllct.find(condition)

        query_result = []
        for data in result:
            for r in ['City', 'Agency Name', '_id', 'Agency Code', 
                    'Incident', 'Record ID', 'Victim Age', 
                    'Perpetrator Age', 'Record Source']:
                data.pop(r, None)
            data.pop('_id', None)
            if len(query_result) < 1:
                query_result.append(list(data.keys()))
            query_result.append(list(data.values()))
        session['query_result'] = query_result
        return render_template("querying.html", title = 'Querying', form = form, query_result = query_result)
    return render_template("querying.html", title = 'Querying', value_dict = value_dict, form = form)

@app.route('/query_result')
def query_result():
    query_result = session.get('query_result', None)
    query_result = [['16', '233333', '228'], ['alpha', 'beta', 'chara']]
    return render_template("query_result.html", title = 'Query Result', query_result = query_result)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.is_submitted():
        flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
        print('Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
        #return redirect('/index')
        return 'Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data)
    return render_template('login.html',
        title = 'Sign In',
        form = form)


""" GET """
@app.route('/tasks', methods=['GET'])
def get_task():
    return jsonify({'tasks': tasks})

@app.route('/data/<string:attr>=<string:value>', methods=['GET'])
def part_task(attr, value):
    """
    task = list(filter(lambda t: t['id'] == task_id, tasks))
    if len(task) == 0:
        abort(404)  
    return str(task)
    """
    result = cllct.find_one({attr: value})
    js = json.dumps(result, indent=4, separators=(',', ': '))
    return attr+" "+value+" "+ str(js)

"""" POST """
@app.route('/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201

""" PUT """
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})

""" DELETE """
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})
    
""" 判斷自己執行非被當做引入的模組，因為 __name__ 這變數若被當做模組引入使用就不會是 __main__ """
if __name__ == '__main__':
    app.run()
