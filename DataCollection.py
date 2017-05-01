from googlefinance import getQuotes
import json
from datetime import datetime
from time import sleep, monotonic
import schedule


# 52200 seconds = 14.5 hours (time from 4:00pm to 6:30am) -> when I want program sleeping
# 34200 seconds = 9.5 hours  (time from 6:30am to 4:00pm) -> When I want program running

# run this script each day at 6:30 am
# it will run for 34200 seconds (6:30am to 4:00pm)
def main():
    schedule.every().day.at("06:30").do(capture)

    while True:
        schedule.run_pending()
        sleep(1)


def capture():
    print("capturing")
    # get first live quote
    results = [getQuotes('AAPL')]

    # 32400 seconds from now
    t_end = monotonic() + 32400

    try:
        # run the capture until the current time >= t_end
        while monotonic() < t_end:
            # get next live quote
            result = getQuotes('AAPL')
            print(json.dumps(result, indent=2))

            # save subsequent live quotes if the timestamp has changed since the last request
            if getDateTime(result[0]) > getDateTime(results[-1][0]):
                results.append(result)
                # print(json.dumps(result, indent=2))
    finally:
        print("saving results...")
        f = open("output.txt", "a")
        for result in results:
            f.write(json.dumps(result, indent=2))
        print("finished")


def getDateTime(result):
    # extract the date and time to a datetime object for comparison
    dt = datetime.strptime(result["LastTradeDateTime"], "%Y-%m-%dT%H:%M:%SZ")
    return dt


main()
