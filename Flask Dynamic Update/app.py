from flask import Flask, render_template, url_for, request, flash, session, redirect, abort, Response, jsonify
from wtforms import SelectField, SubmitField, SelectField, StringField
from flask_wtf import FlaskForm
import os, sys, time, random, datetime, secrets
import threading
from collections import OrderedDict

# import schedule

root = os.path.dirname(os.path.realpath(__file__))
os.chdir(root)
sys.path.append(root)

SECRET_KEY = os.urandom(32)
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

from wtforms import SelectField, SubmitField, SelectField, StringField
from flask_wtf import FlaskForm


class ExportingThread(threading.Thread):
    def __init__(self, id_=''):
        self.progress = 0
        self.id_ = id_  # just for debugging
        super().__init__()

    def run(self):
        # Your exporting stuff goes here ...
        print(f'#{self.id_} start')
        for _ in range(10):
            time.sleep(1)
            print(f'#{self.id_} ..working {_}')
            self.progress += 10
        print(f'#{self.id_} done')


exporting_threads = OrderedDict()
box_values = OrderedDict()

exporting_threads2 = OrderedDict()
box_values2 = OrderedDict()


# Ordered dict ?
# request last key?

def some_task_2(id_):
    # Your exporting stuff goes here ...
    progress = 0
    print(f'#{id_} start')
    for _ in range(10):
        time.sleep(1)
        print(f'#{id_} ..working {_}')
        progress += 10
    print(f'#{id_} done')


def some_task():
    # generate token
    return secrets.token_urlsafe(20)


@app.route('/_perpetual_stuff', methods=['GET'])
def perpetual_progress():
    return jsonify(result_perpetual=some_task())


@app.route('/_stuff', methods=['GET'])
def progress():
    # exporting_threads
    global box_values
    prev = list(exporting_threads.keys())[-1] if len(list(exporting_threads.keys())) > 0 else 0
    result = str(exporting_threads[prev].progress) if prev else 0
    # print(exporting_threads.keys())
    # print(prev)
    # str(exporting_threads[thread_id].progress)

    return jsonify(result=result)


@app.route('/_stuff2', methods=['GET'])
def progress2():
    # exporting_threads2
    global box_values
    prev = list(exporting_threads2.keys())[-1] if len(list(exporting_threads2.keys())) > 0 else 0
    print('prev', prev)
    # Measures time passed
    time_passed = 0
    if prev != 0:
        if exporting_threads2[prev].is_alive() == False:
            box_values2[prev]['Status'] = 'Finished'
            time_passed = 'Finished'
        else:
            time_passed = str(datetime.datetime.now() - datetime.datetime.strptime(
                box_values2[prev]['Start Date'], "%Y-%m-%d %H:%M:%S"))
    return jsonify(result2=time_passed)


@app.route('/', methods=['GET', 'POST'])
def default_page(error=None, values=None, status=None):
    interval = 2000  # 2 seconds
    interval2 = 5000  # 5 seconds

    # form1 = Form1()
    global exporting_threads
    global box_values

    # start new task
    # if new thread, stops all the previous threads. Therefore only 1 thread is allowed.
    # Just need one task in the background
    if request.method == 'POST':
        print(request.form, list(request.form.keys()))
        # for 1 thread only
        # thread_id = 1010
        # for multiple threads
        thread_id = random.randint(0, 10000)

        if 'submit_button_1' == list(request.form.keys())[0]:
            print('submit_button_1 pressed')
            # task with progress
            exporting_threads[thread_id] = ExportingThread(id_=thread_id)
            # start
            exporting_threads[thread_id].start()
            # Add text to box_values
            keys_ = ['ID', 'Status', 'Progress', 'Start Date', 'End Date', 'Duration']
            box_values[thread_id] = dict.fromkeys(keys_)
            box_values[thread_id]['ID'] = thread_id
            box_values[thread_id]['Status'] = 'running'
            box_values[thread_id]['Start Date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        elif 'submit_button_2' == list(request.form.keys())[0]:
            print('submit_button_2 pressed')
            # task with unknown progress, for any function
            exporting_threads2[thread_id] = threading.Thread(target=some_task_2, kwargs={'id_': thread_id})
            # start
            exporting_threads2[thread_id].start()
            # Add text to box_values2
            keys_ = ['ID', 'Status', 'Start Date', 'End Date', 'Duration']
            box_values2[thread_id] = dict.fromkeys(keys_)
            box_values2[thread_id]['ID'] = thread_id
            box_values2[thread_id]['Status'] = 'running'
            box_values2[thread_id]['Start Date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Add text to box_values
    for key in box_values.keys():
        # If status has not yet been changed
        box_values[key]['Progress'] = str(exporting_threads[key].progress)
        # If finished
        if box_values[key]['Status'] == 'running' and box_values[key]['Progress'] == '100':
            box_values[key]['Status'] = 'Finished' if str(exporting_threads[key].progress) == '100' else 'running'
            box_values[key]['End Date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            box_values[key]['Duration'] = str(datetime.datetime.strptime(box_values[key]['End Date'],
                                                                         "%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(
                box_values[key]['Start Date'], "%Y-%m-%d %H:%M:%S"))
    for key in exporting_threads2.keys():
        print('Alive or Dead:', key, exporting_threads2[key].is_alive())
        # If finished
        if exporting_threads2[key].is_alive() == False:
            box_values2[key]['Status'] = 'Finished'
            box_values2[key]['End Date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            box_values2[key]['Duration'] = str(datetime.datetime.strptime(box_values2[key]['End Date'],
                                                                          "%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(
                box_values2[key]['Start Date'], "%Y-%m-%d %H:%M:%S"))

    # progress of the last thread
    # for exporting_threads
    status = str(exporting_threads[list(exporting_threads.keys())[-1]].progress) if len(
        list(exporting_threads.keys())) > 0 else 0
    # thread1 =  list(exporting_threads.keys())[0] if  len(list(exporting_threads.keys())) > 0 else 0

    # check of finished
    # print(exporting_threads.keys(), ) #
    # for thread in threading.enumerate():
    #     print(thread.name)
    # print(box_values.keys())

    return render_template(f'main.html', bokS='', form1='form1', error=error, text2=box_values2,
                           text=box_values, status=status, interval=interval, interval2=interval, interval3=interval2)


if __name__ == '__main__':
    app.run()
