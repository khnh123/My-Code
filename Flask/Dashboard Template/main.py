from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify

from wtforms import SelectField, SubmitField
from flask_wtf import FlaskForm
import numpy as np
from collections import OrderedDict

# My Files
from Flask_Template import Data as data


# request.path - get current page
# form.value.choices = data - change the values of SelectField or .....
# @app.route('/', methods=['GET', 'POST']) - if error "method not allowed"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cairocoders-ednalan'




# Forms
class Form1(FlaskForm):
    value0 =  SelectField('dates', choices=data.data, default=data.data[0], coerce=str)
    value1 = SelectField('list_2', choices=[key for key in data.list_2], default=[key for key in data.list_2][0])
    list_1 = data.array_numpy(step=1)
    value2 = SelectField('list_1', choices=list_1, default=list_1[0])
    value3 = SelectField('Colormaps', choices=data.cmaps['Sequential'], default=data.cmaps['Sequential'][-1])
    value4 = SelectField('Classes of colormaps', choices=data.cmaps.keys(), default='Sequential')

# Pages
@app.route('/')
def page_main(error=None, text=None):
    form1 = Form1()
    with open('cmap.html', "r", encoding='utf-8') as f:
        table = f.read()
    return render_template('page_main.html', bokS=table, form1=form1, error=error, text=text)


@app.route("/about")
def page_about():
    return render_template('about.html')


@app.route("/Page 1")
def page_1(error=None, text=None, table = ''):
    form1 = Form1()
    return render_template('Page 1.html', bokS=table, form1=form1, error=error, text=text)


@app.route("/Page 2")
def page_2(error=None, text=None):
    form1 = Form1()
    table = ''
    return render_template('Page 2.html', bokS=table, form1=form1, error=error, text=text)


@app.route("/Page 3-2")
@app.route("/Page 3-1")
def page_3(error=None, text=None):
    form1 = Form1()
    table = ''
    if request.path == '/Page 3-1':

        return render_template('Page 3-1.html', bokS=table, form1=form1, error=error, text=text)
    elif request.path == '/Page 3-2':

        return render_template('Page 3-2.html', bokS=table, form1=form1, error=error, text=text)


@app.route("/Page 4")
def page_4(error=None, text=None):
    form1 = Form1()
    table = ''

    return render_template('Page 4.html', bokS=table, form1=form1, error=error, text=text)


@app.route("/Page 5 tab1-1")
@app.route("/Page 5 tab1-2")
@app.route("/Page 5 tab1-3")
def page_5(error=None, text=None):
    form1 = Form1()
    table = ''
    if request.path == '/Page 5 tab1-1':
        return render_template('Page 5 tab1-1.html', bokS=table, form1=form1, error=error, text=text)
    elif request.path == '/Page 5 tab1-2':
        return render_template('Page 5 tab1-2.html', bokS=table, form1=form1, error=error, text=text)
    else:
        return render_template('Page 5 tab1-3.html', bokS=table, form1=form1, error=error, text=text)






# Update
@app.route("/Page 5 tab1-3", methods=['GET', 'POST'])
@app.route("/Page 5 tab1-2", methods=['GET', 'POST'])
@app.route("/Page 5 tab1-1", methods=['GET', 'POST'])
@app.route("/Page 4", methods=['GET', 'POST'])
@app.route("/Page 3-2", methods=['GET', 'POST'])
@app.route("/Page 3-1", methods=['GET', 'POST'])
@app.route("/Page 2", methods=['GET', 'POST'])
@app.route("/Page 1", methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def update_values():
    # available forms: form0, form1, form2
    error = None
    values = dict.fromkeys(keys)

    input = request.form.get("text", False)
    form1 = Form1()

    value0 = form1.value0.data
    value1 = form1.value1.data
    value2 = form1.value2.data
    value3 = form1.value3.data
    value4 = form1.value4.data

    if input:
        try:
            input = int(input)
            if 50 < input or input < 10:
                error = 'Values between max:50 - min:10'
                input = None
            else:
                values['input'] = input
        except ValueError:
            error = 'Must be an Int'
            input = None

    values['value0'] = value0
    values['value1'] = value1
    values['value2'] = value2
    values['value3'] = value3
    values['value4'] = value4
    values['page'] = request.path

    if request.method == 'POST':


        new_values_update(values, error)
        s = f'{input}, {value0}, {value1}, {value2},{value3},{value4}, {request.path}'
        print('Page: ', request.path)
        if error:
            print('Errors: ', error)  # , "Values:", s)
        if request.path == '/':
            return page_main(text=values, error=error)
        elif request.path == '/Page 1':
            return page_1(text=values, error=error)
        elif request.path == '/Page 2':
            return page_2(text=values, error=error)
        elif request.path == '/Page 4':
            return page_4(text=values, error=error)
        elif '/Page 3' in request.path:
            return page_3(text=values, error=error)
        elif '/Page 5' in request.path:
            return page_5(text=values, error=error)

    return render_template('page_main.html', text=input, form1=form1)


keys = ['input', 'value0', 'value1', 'value2', 'value3', 'value4', 'page']
cache = dict.fromkeys(keys)


def new_values_update(values, error):
    """
    - works with cache - dict
    - updates data for the table One_Candle_Select
    """

    print('new_values_One_Candle_Select', request.path)
    print('cache', cache)
    print('values', values)
    new_values = False
    values['input'] = 10 if values['input'] == None else values['input']
    cache['input'] = 10 if cache['input'] == None else cache['input']
    for key in keys:
        if cache[key] != values[key]:
            new_values = True
            old = cache[key]
            cache[key] = values[key] if key != 'input' or values[key] != None else cache[key]
            if old != cache[key]:
                print('New value -', f'old: {old}', '------>', f'new: {cache[key]}')
    if new_values and error == None:
        print('Updated')
        print('cache', cache)
        if request.path == '/':
            data.return_cmap(cmap_name=cache['value3'])
            print('Active tab -', request.path)


    else:
        print('No new values')



# dynamic select

@app.route('/<value>')
def dynamic_select(value):
    print('value:', value)
    if value in data.list_2:
        print("value1")
        data1 = data.array_numpy(step=data.list_2[value])
        return jsonify({"data1": data1})
    elif value in data.cmaps.keys():
        print("value4")
        data2 = data.cmaps[value]
        return jsonify({"data2": data2})





if __name__ == "__main__":
    app.run(debug=True)
