from GoogleQuoting import GoogleQuote
from Graphing import graphIt


def main():
    file_name = input("output filename: ") + ".csv"
    symbol = input("Symbol: ")
    date = input("Date (yyyy-mm-dd): ")
    data = GoogleQuote(symbol, date)
    data.write_csv(file_name)
    graphIt(file_name)

main()
