from flask import Flask, render_template, request
from wtforms import SelectField
from flask_wtf import FlaskForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cairocoders-ednalan'

with open(r'C:\Users\khini\PycharmProjects\untitled1\test1.txt', "r", encoding='utf-8') as f:
    data = [elem.replace("\n", "") for elem in f.readlines() if elem != "\n"]
    # print(data, type(data))


class Form(FlaskForm):
    value = SelectField('country', choices=data)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = Form()
    form.value.choices = data

    if request.method == 'POST':
        value = form.value.data
        print(value)
        return '<h1>Instrument : {}</h1>'.format(value)
    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
