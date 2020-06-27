
import matplotlib as mpl
import matplotlib.cm as cm


import matplotlib as matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm



def color_map(value):
    norm = plt.Normalize(0, 1)
    norm = matplotlib.colors.Normalize(vmin=0, vmax=1)
    cmap = cm.get_cmap(cmap_name)  # PiYG
    rgb = cmap(norm(value))[:3]  # will return rgba, we take only first 3 so we get rgb
    color = matplotlib.colors.rgb2hex(rgb)
    return color


html_string = '''
<meta name="viewport" content="user-scalable=no, initial-scale=1, maximum-scale=1, minimum-scale=1" />

<p style="background-color:{color};">This is a paragraph. {text}</p>
'''

if __name__ == "__main__":

    cmap_name = 'seismic'
    file = open(f'{cmap_name}_cmap.html', "w")

    values = [	0.0030, 0.2997 , 0.0002 , -0.9131 , 0.913, 1 , -1, 0 ]
    values = [num/100 for num in range(1, 100)]
    for val in values:
        c = color_map(abs(val))
        print(c)
        html = html_string.format(color=c, text=val )
        file.write(html)

    file.close()
