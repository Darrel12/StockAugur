import urllib.request
from datetime import datetime, date


class Quote(object):
    DATE_FMT = '%Y-%m-%d'
    TIME_FMT = '%H:%M:%S'

    def __init__(self):
        self.symbol = ''
        self.Date, self.time, self.Open, self.High, self.Low, self.Close, self.Volume = ([] for _ in range(7))

    def append(self, dt, open_, high, low, close, volume):
        self.Date.append(dt.date())
        self.time.append(dt.time())
        self.Open.append(float(open_))
        self.High.append(float(high))
        self.Low.append(float(low))
        self.Close.append(float(close))
        self.Volume.append(int(volume))

    def to_csv(self):
        return ''.join(["{0},{1:.2f},{2:.2f},{3:.2f},{4:.2f},{5}\n".format(self.Date[bar].strftime('%d-%b-%y'),
                                                                           self.Open[bar], self.High[bar],
                                                                           self.Low[bar], self.Close[bar],
                                                                           self.Volume[bar])
                        for bar in range(len(self.Close))])

    def write_csv(self, filename):
        with open(filename, 'w') as f:
            f.write("Date,Open,High,Low,Close,Volume\n")
            f.write(self.to_csv())

    def read_csv(self, filename):
        self.symbol = ''
        self.Date, self.time, self.Open, self.High, self.Low, self.Close, self.Volume = ([] for _ in range(7))
        for line in open(filename, 'r'):
            symbol, ds, ts, open_, high, low, close, volume = line.rstrip().split(',')
            self.symbol = symbol
            dt = datetime.strptime(ds + ' ' + ts, self.DATE_FMT + ' ' + self.TIME_FMT)
            self.append(dt, open_, high, low, close, volume)
        return True

    def __repr__(self):
        return self.to_csv()


class GoogleQuote(Quote):
    """ 
    Daily quotes from Google. Date format='yyyy-mm-dd' 
    """

    def __init__(self, symbol, start_date, end_date=datetime.today().isoformat()):
        super().__init__()
        self.symbol = symbol.upper()
        start = date(int(start_date[0:4]), int(start_date[5:7]), int(start_date[8:10]))
        end = date(int(end_date[0:4]), int(end_date[5:7]), int(end_date[8:10]))
        url_string = "http://www.google.com/finance/historical?q={0}".format(self.symbol)
        url_string += "&startdate={0}&enddate={1}&output=csv".format(
            start.strftime('%b%%20%d,%%20%Y'), end.strftime('%b%%20%d,%%20%Y'))  # %%20 represnts a space for the url
        print("url_string:", url_string)
        csv = urllib.request.urlopen(url_string).readlines()
        # csv.reverse()  # put the data in ascending order
        for bar in range(1, len(csv) - 1):
            ds, open_, high, low, close, volume = csv[bar].decode().rstrip().split(',')
            open_, high, low, close = [float(x) for x in [open_, high, low, close]]
            dt = datetime.strptime(ds, '%d-%b-%y')
            self.append(dt, open_, high, low, close, volume)
