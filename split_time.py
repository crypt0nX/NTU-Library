import pandas as pd
import datetime
from dateutil import parser


def split_time_ranges(from_time, to_time, frequency):
    from_time, to_time = pd.to_datetime(from_time), pd.to_datetime(to_time)
    time_range = list(pd.date_range(from_time, to_time, freq='%sS' % frequency))
    if to_time not in time_range:
        time_range.append(to_time)
    time_range = [item.strftime("%H:%M") for item in time_range]
    time_ranges = []
    for item in time_range:
        f_time = item
        t_time = (parser.parse(item) + datetime.timedelta(seconds=frequency))
        if t_time >= to_time:
            t_time = to_time.strftime("%H:%M")
            time_ranges.append([f_time, t_time])
            break
        time_ranges.append([f_time, t_time.strftime("%H:%M")])
    return time_ranges

'''
if __name__ == '__main__':
    from_time = '08:00'
    to_time = '22:00'
    frequency = 60 * 60 * 6
    time_ranges = split_time_ranges(from_time, to_time, frequency)
    print(time_ranges)
'''