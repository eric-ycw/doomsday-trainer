import datetime as dt
import calendar
import time
import random
from configparser import SafeConfigParser

CURRENT_DATE = dt.date.today()
CURRENT_YEAR = CURRENT_DATE.year

settings = SafeConfigParser()
settings.read('settings.ini')
only_current_year = settings['Main'].getboolean('only_current_year')
only_current_century = settings['Main'].getboolean('only_current_century')
allow_past_dates = settings['Main'].getboolean('allow_past_dates')
allow_future_dates = settings['Main'].getboolean('allow_future_dates')
year_range = settings['Main'].getint('year_range')

def set_date_range():
    if only_current_year:
        startdate = dt.date(CURRENT_YEAR, 1, 1)
        enddate = dt.date(CURRENT_YEAR, 12, 31)
    elif only_current_century:
        startdate = dt.date(CURRENT_YEAR - CURRENT_YEAR % 100, 1, 1)
        enddate = dt.date(CURRENT_YEAR - CURRENT_YEAR % 100 + 99, 12, 31)
    else:
        startdate = CURRENT_DATE - dt.timedelta(days=year_range*365)
        enddate = CURRENT_DATE + dt.timedelta(days=year_range*365)

    if not allow_past_dates:
        startdate = CURRENT_DATE
    if not allow_future_dates:
        enddate = CURRENT_DATE

    if startdate >= enddate:
        raise Exception('Invalid date range')
    return startdate, enddate

def get_random_date(startdate, enddate):
    day_num = (enddate - startdate).days
    return startdate + dt.timedelta(days=random.randint(0, day_num))

def train():
    startdate, enddate = set_date_range()
    train_date = get_random_date(startdate, enddate)
    day = train_date.weekday()

    print(train_date)
    start_time = time.time()
    answer = input('Input day of week (0 for Sunday, 1 for Monday etc.): ')
    end_time = time.time()
    total_time = end_time - start_time

    correct = False
    if answer == 'exit':
        return answer
    if answer.isdigit():
        if 0 <= int(answer) <= 7:
            if not int(answer) == 0 and not int(answer) == 7 and int(answer) == day + 1:
                correct = True
            elif (int(answer) == 0 or int(answer) == 7) and day == 6:
                correct = True
    if correct:
        print('Correct! Your time was', total_time, 'seconds.\n')
    else:
        print('Incorrect. The answer is', calendar.day_name[day] + '.\n')

def print_info():
    print('\n1. Find the anchor day of the century')
    print('Formula: 5 * (c mod 4) mod 7 + Tuesday')
    print('e.g. Anchor day of the 21st century = 5 * (20 mod 4) mod 7 + Tuesday')
    print('                                    = Tuesday')
    print('Note: c = floor(year / 100)')
    print('\n2. Find the year\'s doomsday')
    print('Formula: (floor(y / 12) + y mod 12 + floor(y mod 12 / 4)) mod 7 + anchor')
    print('          where y is the last two digits of the year')
    print('e.g. Doomsday of 2018 = (floor(18 / 12) + 18 mod 12 + floor(18 mod 12 / 4)) mod 7 + Tuesday')
    print('                      = (1 + 6 + 1) mod 7 + Tuesday')
    print('                      = Wednesday')
    print('\n3. Choose closest fixed date and count number of days between them')
    print('Fixed dates are dates that always lies on doomsday')
    print('Examples include 4/4, 6/6, 8/8, 10/10, 12/12 and the last day of February')
    print('With this in mind, we can easily find the day of week of any target date through simple subtraction')
    print('e.g. Day of week of 12th May, 2018 = Doomsday + (12/5 - 4/4) mod 7 or Doomsday - (6/6 - 12/5) mod 7')
    print('                                   = Wednesday + 38 mod 7 or Wednesday - 25 mod 7')
    print('                                   = Saturday')

def main():
    print('Type "help" to view commands')
    print('You can change trainer settings in settings.ini')
    print('Dates are given in y/m/d format')
    command = input('')
    while True:
        if command == 'help':
            print('train - Start training')
            print('info - Show the steps of the doomsday algorithm')
            print('exit - Exit the application or stop training')
        elif command == 'train':
            while True:
                if train() == 'exit':
                    break
        elif command == 'info':
            print_info()
        elif command == 'exit':
            return
        else:
            print('Invalid command')
        command = input('\n')

main()
