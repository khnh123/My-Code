from bokeh.models.widgets import Div, Paragraph, PreText
from bokeh.plotting import figure
from bokeh.models.tools import *
from bokeh.models import Asterisk, LinearAxis, Select, ColumnDataSource, HoverTool, CustomJS, ColumnDataSource, \
    HoverTool, BoxAnnotation, Legend
from bokeh.layouts import column, row, gridplot
from bokeh.io import curdoc
from bokeh.plotting import figure, output_file, show

import pandas as pd
import re
from bs4 import BeautifulSoup
import time

import prepare_df_Trading_Variables as prepare


def plot_fig(df, name=None):
    # bokeh serve --show bokeh_MAs_Diff_Select.py

    instrument_name = name

    # Select the datetime format for the x axis depending on the timeframe
    xaxis_dt_format = '%d %b %Y, %H:%M:%S'
    # for e in range(len(df['Date'])):
    #    df['Date'][e] = str(df['Date'][e])

    hover = HoverTool()
    hover.tooltips = [("series name", "@legend")]
    TOOLS = ['pan', 'wheel_zoom', 'box_zoom', 'reset', 'save', 'xwheel_zoom', 'ywheel_pan', CrosshairTool()]

    # Use wheel_zoom to interact like in tradingview

    # 1
    # Add window
    window1 = figure(  # sizing_mode='stretch_both', # to fit everything in one window
        title="Open to High", title_location="right",
        tools=TOOLS,
        active_drag='pan',
        active_scroll='wheel_zoom',
        x_axis_type='linear',
        #  x_range=Range1d(df.index[0], df.index[-1], bounds="auto"),# fix the zoom
        plot_height=500,
        plot_width=500,
    )

    # Add on extra lines (e.g. moving averages) here
    # fig.line(df.index, <your data>)

    data1 = ColumnDataSource(
        data=dict(x=df.index, y=df['Open to High'], legend_label=["series 1"] * len(df)))
    line1 = window1.line("x", "y", line_color="purple", source=data1, legend_label="Open to High")

    # fig - fig is done, now adding indicator figures

    # 2
    # Add window
    window2 = figure(  # sizing_mode='stretch_both',
        title="Open to Low", title_location="right",
        tools=TOOLS,
        active_drag='pan',
        active_scroll='xwheel_zoom',
        x_axis_type='linear',
        # x_range=Range1d(df.index[0], df.index[-1], bounds="auto"),
        plot_height=500,
        plot_width=500,

    )
    window2.xaxis.visible = True
    data1 = ColumnDataSource(data=dict(x=df.index, y=df['Open to Low'], legend_label=["series 1"] * len(df)))
    line2 = window2.line("x", "y", line_color="purple", source=data1, legend_label="Open to Low")
    # Add extra data to indicator window
    window2.add_layout(LinearAxis(), 'right')

    # 3
    # Add indicator window
    window3 = figure(  # sizing_mode='stretch_both',
        title="Candle body (Open to Close)", title_location="right",
        tools=TOOLS,
        active_drag='pan',
        active_scroll='xwheel_zoom',
        x_axis_type='linear',
        # x_range=Range1d(df.index[0], df.index[-1], bounds="auto"),
        plot_height=500,
        plot_width=500,

    )
    window3.xaxis.visible = True
    data1 = ColumnDataSource(
        data=dict(x=df.index, y=df['Candle body (Open to Close)'], legend_label=["series 1"] * len(df)))
    line3 = window3.line("x", "y", line_color="purple", source=data1, legend_label="Candle body (Open to Close)")
    window3.add_layout(LinearAxis(), 'right')

    # 4
    # Add indicator window
    window4 = figure(  # sizing_mode='stretch_both',
        title="Range", title_location="right",
        tools=TOOLS,
        active_drag='pan',
        active_scroll='xwheel_zoom',
        x_axis_type='linear',
        # x_range=Range1d(df.index[0], df.index[-1], bounds="auto"),
        plot_height=500,
        plot_width=500,

    )
    window4.xaxis.visible = True

    data1 = ColumnDataSource(data=dict(x=df.index, y=df['Total Range'], legend_label=["series 1"] * len(df)))
    line4 = window4.line("x", "y", line_color="purple", source=data1, legend_label="Total Range")
    # Add extra data to indicator window
    window4.add_layout(LinearAxis(), 'right')
    ###########
    # End of adding windows

    # Set up the hover tooltip to display some useful data
    # for window1
    window1.add_tools(HoverTool(
        renderers=[line1],
        tooltips=[
            ("X", "@x"),
            ("Y", "@y"),
        ],
    ))
    # for window2
    window2.add_tools(HoverTool(
        renderers=[line2],
        tooltips=[
            ("X", "@x"),
            ("Y", "@y"),
        ],
    ))
    # for window3
    window3.add_tools(HoverTool(
        renderers=[line3],
        tooltips=[
            ("X", "@x"),
            ("Y", "@y"),
        ],
    ))
    # for window4
    window4.add_tools(HoverTool(
        renderers=[line4],
        tooltips=[
            ("X", "@x"),
            ("Y", "@y"),
        ],
    ))

    window1.legend.click_policy = "hide"
    window2.legend.click_policy = "hide"
    window3.legend.click_policy = "hide"
    window4.legend.click_policy = "hide"

    # Add Divs
    pre = PreText(
        text="""Your text is initialized with the 'text' argument. The remaining Paragraph arguments are 'width' and 'height'.""",
        width=500, height=100)

    desc = describe_df(df)
    div = Div(
        text=df_to_html(desc),
        width=200, height=100)

    # Finalise the figure
    fig = gridplot([[window1, window2], [window3, window4]])  # include here to add indicator window
    #layout = row(column(pre, fig), column(pre, div))
    #show(layout)

    return fig



css = """
<html>
      <head><title>HTML Pandas Dataframe with CSS</title></head>
      <style>
.mystyle {
    font-size: 11pt;
    font-family: Arial;
    border-collapse: collapse;
    border: 1px solid silver;
width: 800px;
max-heigth: 229px;
   margin: 10px;
}

.mystyle td, th{
font-size: 11pt;
    padding: 5px;
    height: 5px;
max-height: 5px;
}

.mystyle thead, th { 
font-size: 11pt;
 background-color: #e4f0f5;
   # width: 100%;
    #height: 100%;
    overflow:hidden;
border-spacing:10px;
max-width: 100px;
heigth: 5px;
}

.mystyle tr:nth-child {
    background: #E0E0E0;
}

.mystyle tr:hover {
    background: lightblue;
    cursor: pointer;
}

.mystyle caption {
    padding: 5px;
    caption-side: top
}
 </style>
"""


def df_to_html(df):
    # html format
    pd.set_option('colheader_justify', 'center')  # FOR TABLE <th>
    html = (df.style
            # .set_caption('')
            .set_table_attributes('class="dataframe mystyle"')
            .render()
            )
    html
    html_string = '''
    <html>
      <head><title>HTML Pandas Dataframe with CSS</title></head>
      <link rel="stylesheet" type="text/css" href="df_style_1.css"/>
      <body>
      {table}
      </body>
    </html>
    '''
    #html = html_string.format(table=df.to_html(classes='mystyle'))
    html = css + df.to_html(classes='mystyle')
    # OUTPUT AN HTML FILE
    with open('myhtml2.html', 'w') as f:
        f.write(html)
    return html


def html_to_object(html_file_path=None, page=None):
    """

    :param html_file_path:
    :return:
    """
    if html_file_path:
        page = open(html_file_path, "r")

    TAG_RE_head = re.compile(r'<+.[head>]+>')  # remove <head> tag
    TAG_RE_body = re.compile(r'<+.[body>]+>')  # remove <head> tag

    def remove_tags(text, TAG_RE):
        return TAG_RE.sub('', text)

    soup = BeautifulSoup(page, 'lxml')

    style = remove_tags(str(soup.head), TAG_RE_head)
    table = remove_tags(str(soup.body), TAG_RE_body)

    return style, table


def format_df(df):
    # Format dataframe
    df = df.rename(columns=lambda x: x[0].upper() + x[1:])
    df['Open'] = pd.to_numeric(df['Open'], errors='coerce')
    df['High'] = pd.to_numeric(df['High'], errors='coerce')
    df['Low'] = pd.to_numeric(df['Low'], errors='coerce')
    df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
    # Convert tom time format and merge
    df['Date'] = df['Date'] + " " + df['Time']
    df['Date'] = pd.to_datetime(df['Date'])

    df['Open'] = df['Open'].astype(float)
    df['High'] = df['High'].astype(float)
    df['Low'] = df['Low'].astype(float)
    df['Close'] = df['Close'].astype(float)
    df = df.drop(['Time', 'TimeFrame', 'Instrument'], axis=1)
    return df


def calculate_stats(df):
    """
    1. Open to High
    2. Open to Low
    3. Candle body (Open to Close)
    4. Total Range



    """
    df['Open to High'] = df['High'] - df['Open']
    df['Open to Low'] = df['Open'] - df['Low']
    df['Candle body (Open to Close)'] = abs(df['Open'] - df['Close'])
    df['Total Range'] = df['High'] - df['Low']


def describe_df(df):
    """
    Input:
    1. df - dataframe
    Output:
    1. new df
    """
    df = df.describe()  # this prevents from formatting df
    # create new df
    dict_names = ('count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max')
    col_names = ('Open', 'High', 'Low', 'Close', 'Open to High', 'Open to Low',
                 'Candle body (Open to Close)', 'Total Range')
    df_new = pd.DataFrame(index=dict_names, columns=col_names)
    df_new = df_new.fillna('NaN')  # with 0s rather than NaNs
    # copy and format data from df:
    for col in df.columns:
        a = df[col].tolist()
        a[0] = str(a[0]).split('.')[0]
        a[1:] = [round(s, 5) for s in a[1:]]
        df_new[col] = a
    return df_new

def exec_main(instrument_name,timeframe, last=None ):
    df = prepare.get_format_df(instrument_name, timeframe, last=last)
    calculate_stats(df)
    return df

def main():
    # create df
    pd.set_option('max_columns', 100)


    #df_to_html(df)
#    fig = plot_fig(df, name='GBPUSD')
    # show the results
    # output to static HTML file
   # output_file("log_lines.html")

    instrument_list = ["EURUSD", "EURCAD", "EURAUD", "EURNZD", "EURJPY",
                       "GBPUSD", "GBPCAD", "GBPAUD", "GBPNZD", "GBPJPY"]

    timeframe = {
        'H1': '1 hours',
        'H4': '4 hours',
        'D1': '1 day',
        'W1': '1 week',
    }

    path = 'C:\My Files\My Files\Study - (Courses)\#Education - Computer Science - Notion\Python\Chart py\MT5 data'

    def update_plot2(attrname, old, new):
        try:
            curdoc().clear()
            t0 = time.time()
            print('_______________________________________Update')
            # plot graphs
            df = exec_main(select2.value, timeframe['D1'], last=None)
            fig = plot_fig(df, name=select2.value)

            t1 = time.time()
            timer.text = '(Execution time: %s seconds)' % round(t1 - t0, 4)
            desc = describe_df(df)
            div = Div(
                text=df_to_html(desc),
                width=200, height=100)
            print(select2.value)
        except FileNotFoundError:
            print("No such instrument or Timeframe")
            return 0
        layout = column(
            row(select2, timer),
            row(column(pre, fig), column(pre, div))
        )
        curdoc().add_root(layout)

    # initial data
    instrument_name = 'GBPJPY'
    t0_main = time.time()

    # plot graphs
    df = exec_main(instrument_name, timeframe['D1'], last=None)
    fig = plot_fig(df, name=instrument_name)

    pre = PreText(
        text="""Your text is initialized with the 'text' argument. The remaining Paragraph arguments are 'width' and 'height'.""",
        width=500, height=100)

    # plot tables
    desc = describe_df(df)
    div = Div(
        text=df_to_html(desc),
        width=200, height=100)

    # plot Select
    select2 = Select(title="Instrument", options=instrument_list, value=instrument_name)
    select2.on_change('value', update_plot2)

    # Plot Layout & run # row(div2, div22)
    timer = Paragraph()
    layout = column(
        row(select2, timer),
        row(column(pre, fig), column(pre, div))
    )
    curdoc().title = "Dashboard Demo"
    curdoc().theme = 'caliber'
    t1_main = time.time()
    timer.text = '(Execution time: %s seconds)' % round(t1_main - t0_main, 4)
    print(timer.text)
    curdoc().add_root(layout)


main()

# bokeh serve --show test_Analytics_Trading_2.py
# bokeh serve --show test_Analytics_Trading_2
