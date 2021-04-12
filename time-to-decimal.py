#!/usr/bin/env python3

import argparse
import datetime
import os
import locale

parser = argparse.ArgumentParser()
parser.add_argument("calculation", nargs="?", help="The term to calculate, e.g \"9:00 17:00 -30m\"")
parser.add_argument("-c", "--calc-command", help="The command to execute with the result.")
parser.add_argument("-l", "--locale", help="Overwrite the locale to use when formating the result.", nargs=1)
parser.add_argument("-n", "--notify", help="Use desktop-notify to send notification of result.", action="store_const", const=True)
args = parser.parse_args()

if args.calculation == None:
    exit()

if args.locale != None:
    locale.setlocale(locale.LC_ALL, args.locale)

try:
    if args.notify:
        import desktop_notify

    tokens = args.calculation.split(" ")
    sum = 0.0
    startDate = None
    endDate = None 

    for token in tokens:
        if "m" in token:
            value = token.replace("+", "").replace("-", "").replace("m", "")
            value = int(value) * 60 / 3600
            if "-" in token:
                sum -= value
            else:
                sum += value
        elif startDate == None:
            startDate = datetime.datetime.strptime(token, "%H:%M")
        else:
            endDate = datetime.datetime.strptime(token, "%H:%M")
            duration = endDate - startDate
            sum = sum + (duration.seconds / 3600)
            startDate = None
            endDate = None

    if (startDate != None):
        print("Odd number of time data")
        exit(1)

    result = locale.format_string("%.2f", sum)

    if args.notify:
        notify = desktop_notify.glib.Notify(result)
        notify.set_timeout(2000)
        notify.show_async()

    if args.calc_command != None:
        os.system(args.calc_command.replace("{result}", result))
    else:
        print(result)

except ImportError:
    print("Error importing desktop-notify module")
    exit(1)
except:
    print("Error")
    exit(1)