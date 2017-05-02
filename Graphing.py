import plotly
from plotly import offline
import plotly.graph_objs as go

# Scientific libraries
from numpy import array
from scipy import stats
import pandas as pd

from datetime import datetime
import copy


def graphIt(inFile):
    data = pd.read_csv(inFile)
    # data.head()

    # convert the date strings to datetime objects
    data.Date = pd.to_datetime(data.Date)

    # create a data entry to measure the time difference in dates (from today) to calculate regression
    data['days_since'] = (data.Date - pd.to_datetime(data.Date.iloc[-1])).astype('timedelta64[D]')

    # Make a deep copy of the date differences
    days_since = copy.deepcopy(data.days_since)
    # Reverse the values as a list to have them in ascending order (can't reverse the original)
    days_since = pd.Series(days_since.tolist()[::-1])
    # store the reversed values back in their original location in the correct order
    data['days_since'] = array(days_since)

    # Generated linear fit based on the daily closing stock values
    slope, intercept, r_value, p_value, std_err = stats.linregress(days_since, data.Close)

    # Generate the best fit line based on the above data
    # It works by determining the line based on each x-value (ascending ordered difference of dates)
    line = slope * data.days_since + intercept

    # Creating the dataset, and generating the scatter data
    trace1 = go.Scatter(
        x=data.Date,
        y=data.Close,
        mode='markers',
        marker=go.Marker(color='rgba(255, 127, 14, 0.3)',
                         size=data.Volume,
                         sizemode="area",
                         sizeref=1533489.10625),
        name='Data',
        text=data.Volume
    )

    # Generating the best fit line
    trace2 = {
        "x": data.Date,
        "y": line,
        "line": {
            "color": "rgb(255, 0, 255)",
            "dash": "dot",
            "width": 2
        },
        "marker": {
            "color": "rgb(0, 0, 255)",
            "line": {
                "color": "#000",
                "width": 0
            },
            "opacity": 1
        },
        "name": "Predicted Trend",
        "opacity": 0.61,
        "type": "scatter",
        "uid": "73f5bd",
        "xaxis": "x",
        "yaxis": "y"
    }

    # lowest closing market value to highest closing market value
    height_range = [data.Close.min() - data.Close.max() / 10, data.Close.max() + data.Close.max() / 10]
    # just below day 0 to number of days
    # width_range = [-days_since.max()/10, days_since.max() + days_since.max()/10]
    width_range = [data.Date.min() - pd.to_timedelta(6, unit='M'), data.Date.max() + pd.to_timedelta(6, unit='M')]

    # annotation to show the R^2 value and slope-intercept form of the line
    # TODO turn this into a dict within the layout
    # TODO or add it to the line as text
    annotation = go.Annotation(
        x=data.Date,
        y=line,
        text='$R^2 = {},\\Y = {}X + {}$'.format(pow(r_value, 2), slope, intercept),
        showarrow=False,
        font=go.Font(size=200)
    )

    layout = go.Layout(
        title=inFile[:len(inFile)-4],
        plot_bgcolor='rgb(229, 229, 229)',
        xaxis=go.XAxis(zerolinecolor='rgb(255,255,255)',
                       gridcolor='rgb(255,255,255)',
                       type="date",
                       range=width_range),

        yaxis=go.YAxis(zerolinecolor='rgb(255,255,255)',
                       gridcolor='rgb(255,255,255)',
                       type="linear",
                       range=height_range),

        annotations=[annotation]
    )

    data = [trace1, trace2]
    fig = go.Figure(data=data, layout=layout)

    offline.plot(fig, filename='index.html')
