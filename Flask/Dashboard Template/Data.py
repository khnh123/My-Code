
from wtforms import SelectField, SubmitField
from flask_wtf import FlaskForm
import numpy as np
from collections import OrderedDict

import matplotlib as matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# request.path - get current page
# form.value.choices = data - change the values of SelectField or .....
# @app.route('/', methods=['GET', 'POST']) - if error "method not allowed"

html_string_2 = '''
<meta name="viewport" content="user-scalable=no, initial-scale=1, maximum-scale=1, minimum-scale=1" />

<p style="background-color:{color}; margin-top:0px; margin-bottom:0px; font-size:5pt">{text}</p>
'''

def color_map(value, cmap_name='plasma', vmin=0, vmax=1, bg=False):
    norm = plt.Normalize(vmin, vmax)
    norm = matplotlib.colors.Normalize(vmin=vmin, vmax=vmax)
    cmap = cm.get_cmap(cmap_name)  # PiYG
    rgb = cmap(norm(value))[:3]  # will return rgba, we take only first 3 so we get rgb
    color = matplotlib.colors.rgb2hex(rgb)
    if bg:
        return 'background-color: %s' % color
    else:
        return color

def return_cmap(cmap_name = 'autumn_r'):
    file = open('cmap.html', "w")
    values = [num for num in range(0, 50)]
    for val in values:
        c = color_map(abs(val), cmap_name, vmin=0, vmax=50)
        # print(c)
        html = html_string_2.format(color=c, text=val)
        file.write(html)
    file.close()

with open('test1.txt', "r", encoding='utf-8') as f:
    data = [elem.replace("\n", "") for elem in f.readlines() if elem != "\n"]

def array_numpy(step=1):
    return np.arange(start=0, stop=100+step, step=step).tolist()


list_2 = {
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
}

cmaps = OrderedDict()

cmaps['Perceptually Uniform Sequential'] = [
            'viridis', 'plasma', 'inferno', 'magma', 'cividis']

cmaps['Sequential'] = [
            'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
            'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
            'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']

cmaps['Sequential (2)'] = [
            'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink',
            'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia',
            'hot', 'afmhot', 'gist_heat', 'copper']

cmaps['Diverging'] = [
            'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu',
            'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic']

cmaps['Cyclic'] = ['twilight', 'twilight_shifted', 'hsv']

cmaps['Qualitative'] = ['Pastel1', 'Pastel2', 'Paired', 'Accent',
                        'Dark2', 'Set1', 'Set2', 'Set3',
                        'tab10', 'tab20', 'tab20b', 'tab20c']

cmaps['Miscellaneous'] = [
            'flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern',
            'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg',
            'gist_rainbow', 'rainbow', 'jet', 'nipy_spectral', 'gist_ncar']


