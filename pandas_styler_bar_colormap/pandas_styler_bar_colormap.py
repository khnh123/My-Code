import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib as matplotlib
import pandas as pd


def color_map_color(value, cmap_name='Wistia', vmin=0, vmax=1):
    # value to colormap color
    # norm = plt.Normalize(vmin, vmax)
    norm = matplotlib.colors.Normalize(vmin=vmin, vmax=vmax)
    cmap = cm.get_cmap(cmap_name)  # PiYG
    rgb = cmap(norm(abs(value)))[:3]  # will return rgba, we take only first 3 so we get rgb
    color = matplotlib.colors.rgb2hex(rgb)
    return color


def show_colormap(cmap_name='Wistia'):
    cmap = cm.get_cmap(cmap_name)
    fig = plt.figure(figsize=(8, 2))
    ax1 = fig.add_axes([0.05, 0.80, 0.9, 0.15])
    norm = matplotlib.colors.Normalize(vmin=0, vmax=1)
    cb1 = matplotlib.colorbar.ColorbarBase(ax1, cmap=cmap, norm=norm, orientation='horizontal')
    plt.show()


def style_df(df):
    # Example
    rows = 10
    indx = list(df.index)[-rows:]  # indecies of the last 10 rows
    # Colormap for the last 10 rows in Compare Body %
    last10 = df['Column'][-rows:]  # values to color
    colors = [color_map_color(e, cmap_name='autumn_r', vmin=100, vmax=1000) for e in last10]  # colors
    values = [pd.IndexSlice[indx[i], 'Column'] for i in range(rows)]  # for .bar subset

    html = (df.style
            .bar(subset=values[0], color=colors[0], vmax=1000, vmin=0, align='left', width=100)
            .bar(subset=values[1], color=colors[1], vmax=1000, vmin=0, align='left', width=100)
            .bar(subset=values[2], color=colors[2], vmax=1000, vmin=0, align='left', width=100)

            )
    html
    return html

