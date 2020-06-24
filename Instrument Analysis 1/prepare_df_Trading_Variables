
from datetime import datetime, timedelta
import pytz
import pandas as pd


# initial format data
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
    # df = df.drop(['Time','TimeFrame', 'Instrument'], axis=1)
    return df


# time check
def timeframe(df):
    if (pd.to_datetime(df['Date'][1]) - pd.to_datetime(df['Date'][0])) != timedelta(days=1):
        if (pd.to_datetime(df['Date'][1]) - pd.to_datetime(df['Date'][0])) != timedelta(weeks=1):
            # Convert tom time format and merge
            df['Date'] = df['Date'] + " " + df['Time']


def check_if_closed(df):
    # print(df['Close'][len(df) - 1])
    if df['Close'][len(df) - 1] == "Open":
        df = df.drop(df.index[[len(df) - 1]])
    else:
        """
        Potential error if last 2 rows from different weeks - Weekend in between - date delta is different
        :param df:
        :return: Drops last row if candle has not closed
        """
        # time_of_the_last_candle
        most_recent_quote = pd.to_datetime(df['Date'][len(df) - 1])
        prev_most_recent_quote = pd.to_datetime(df['Date'][len(df) - 2])
        print('_______________________________________')
        print('most_recent_quote', most_recent_quote)
        print('prev_most_recent_quote', prev_most_recent_quote)

        '''Get time of last candle close'''
        timediff = most_recent_quote - prev_most_recent_quote  # also used for rates_frame["TimeFrame"] = str(timediff)
        candle_close_time = most_recent_quote + timediff
        print("timediff: ", timediff, type(timediff))
        print("candle_close_time: ", candle_close_time, type(candle_close_time))

        '''Get current time'''
        # set time zone to UTC
        timezone = pytz.timezone('Europe/Riga')
        # getting datetime of specified timezone
        current_time = datetime.now(tz=timezone).strftime('%Y-%m-%d %H:%M:%S')
        # check_if_candle_closed
        if pd.to_datetime(current_time) > candle_close_time:
            print("Candle has closed", df['TimeFrame'][0])
        else:
            print("Candle has Not closed!", df['TimeFrame'][0])
            df = df.drop(df.index[[len(df) - 1]])
        # return df
    return df


def exec_format(file, last=None):
    df = pd.read_csv(file)
    timeframe(df)
    df = check_if_closed(df)
    df = format_df(df)
    # Custom Slice the dataframe
    if last:
        print('Quotes until: ', last)
        try:
            indx = df[df['Date'] == last].index.item()
            df = df[0:indx + 1]
        except:
            print('Date is not Found, empty list - Perhaps day is a Weekend')

    df.reset_index(drop=True, inplace=True)  # reset index
    return df


# for last, checks H4 candle
def h4_time(a2):
    """
    Finds closest H4 candle
    Input: a2 - <class 'datetime.datetime'>
    Output: replaces %H if necessary
    """
    t = (0, 4, 8, 12, 16, 20)
    if (int(a2.hour)) % 4 != 4:
        delta = [abs(int(a2.hour) - i) for i in t if int(a2.hour) >= i]
        min_delta = delta.index(min(delta))
        a2 = a2.replace(hour=t[min_delta])
    return a2


def get_format_df(instrument_name, timeframe,  last=None):
    """
    func: returns formatted df from file
    Input:
    1. instrument_name - string
    2. timeframe - string
    3. last=None - Bool - time of the last candle
    """
    path = 'C:\My Files\My Files\Study - (Courses)\#Education - Computer Science - Notion\Python\Chart py\MT5 data'
    instrument_name = instrument_name
    # Open files
    file = path + '\_raw_{}-{}.csv'.format(instrument_name, timeframe)
    df = exec_format(file, last=last)
    return df


# main func
def get_format_dfs(instrument_name, last=None):
    """
    func: returns formatted dfs from files
    """
    path = 'C:\My Files\My Files\Study - (Courses)\#Education - Computer Science - Notion\Python\Chart py\MT5 data'
    instrument_name = instrument_name

    # Open files
    file_h1 = path + '\_raw_{}-{}.csv'.format(instrument_name, '1 hours')
    file_h4 = path + '\_raw_{}-{}.csv'.format(instrument_name, '4 hours')
    file_d1 = path + '\_raw_{}-{}.csv'.format(instrument_name, '1 day')

    last_h1 = None
    last_h4 = None
    last_d1 = None

    if last:
        date1 = datetime.strptime(last, '%Y-%m-%d %H:%M:%S')
        last_h1 = str(date1)
        last_h4 = str(h4_time(date1))
        last_d1 = str(date1.replace(hour=0))

    df_h1 = exec_format(file_h1, last=last_h1)
    df_h4 = exec_format(file_h4, last=last_h4)
    df_d1 = exec_format(file_d1, last=last_d1)

    return df_h1, df_h4, df_d1

