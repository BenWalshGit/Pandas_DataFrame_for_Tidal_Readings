""" Module containing a class to process tidal data."""

import pandas as pd
import matplotlib.pyplot as plt

class Reader:
    """
    Class to process tidal data.

    data : pandas.DataFrame
        The underlying tide data.
    """

    def __init__(self, filename):
        """Read in the rainfall data from a named ``.csv``
           file using ``pandas``.

        The DataFrame data is stored in a class instance variable ``data``
        indexed by entry.

        Parameters
        ----------

        filename: str
            The file to be read

        Examples
        --------

        >>> Reader("tidalReadings.csv").data.loc[0].stationName
        'Bangor'
        """
        
        self.filename = filename
        self.data = pd.read_csv(filename)

        

    def station_tides(self, station_name, time_from=None, time_to=None):
        """Return the tide data at a named station as an ordered pandas Series,
         indexed by the dateTime data.

        Parameters
        ----------

        station_name: str or list of strs
            Station Name(s) to return
        time_from: str or None
            Time from which to report (ISO 8601 format)
        time_to: str or None
            Time up to which to report (ISO 8601 format)

        Returns
        -------

        pandas.DataFrame
            The relevant tide data indexed by dateTime and with columns the stationName(s)

        Examples
        --------

        >>> reader = Reader("tideReadings.csv")
        >>> tides = reader.station_tides(["Newlyn", "Bangor"])
        >>> tides.loc["2021-09-20T02:00:00Z", "Newlyn"]
        0.937

        """

        self.data['dateTime'] = pd.to_datetime(self.data['dateTime'])
        df = self.data.pivot(index = 'dateTime', columns = 'stationName', values = 'tideValue')
        sta_tid = df.loc[time_from:time_to, :]
        return sta_tid

    def max_tides(self, time_from=None, time_to=None):
        """Return the high tide data as an ordered pandas Series,
         indexed by station name data.

        Parameters
        ----------

        time_from: str or None
            Time from which to report (ISO 8601 format).
            If ``None``, then earliest value used.
        time_to: str or None
            Time up to which to report (ISO 8601 format)
            If ``None``, then latest value used.

        Returns
        -------

        pandas.Series
            The relevant tide data indexed by stationName.

        Examples
        --------

        >>> reader = Reader("tideReadings.csv")
        >>> tides = reader.max_tides()
        >>> tides["Newlyn"]
        2.376
        """
        self.data['tideValue'] = pd.to_numeric(self.data['tideValue'], errors= 'coerce').fillna(0).astype('float')
        self.data['dateTime'] = pd.to_datetime(self.data['dateTime'])
        df = self.data.loc[time_from: time_to, :]
        df = self.data.groupby('stationName').apply(lambda df: df.tideValue.max())
        return df

    def min_tides(self, time_from=None, time_to=None):
        """Return the low tide data as an ordered pandas Series,
         indexed by station name data.

        Parameters
        ----------

        time_from: str or None
            Time from which to report (ISO 8601 format)
            If ``None``, then earliest value used.
        time_to: str or None
            Time up to which to report (ISO 8601 format)
            If ``None``, then latest value used.

        Returns
        -------

        pandas.Series
            The relevant tide data indexed by stationName.

        Examples
        --------

        >>> reader = Reader("tideReadings.csv")
        >>> tides = reader.min_tides()
        >>> tides["Newlyn"]
        -2.231
        """

        self.data['tideValue'] = pd.to_numeric(self.data['tideValue'], errors= 'coerce').fillna(0).astype('float')
        self.data['dateTime'] = pd.to_datetime(self.data['dateTime'])
        df = self.data.loc[time_from: time_to, :]
        df = self.data.groupby('stationName').apply(lambda df: df.tideValue.min())
        return df


    def mean_tides(self, time_from=None, time_to=None):
        """Return the mean tide data as an ordered pandas Series,
         indexed by station name data.

        Parameters
        ----------

        time_from: str or None
            Time from which to report (ISO 8601 format)
        time_to: str or None
            Time up to which to report (ISO 8601 format)

        Returns
        -------

        pandas.Series
            The relevant tide data indexed by stationName.

        Examples
        --------

        >>> reader = Reader("tideReadings.csv")
        >>> tides = reader.mean_tides()
        >>> tides["Newlyn"]
        0.19242285714285723
        """

        self.data['tideValue'] = pd.to_numeric(self.data['tideValue'], errors= 'coerce').fillna(0).astype('float')
        self.data['dateTime'] = pd.to_datetime(self.data['dateTime'])
        df = self.data.loc[time_from: time_to, :]
        df = self.data.groupby('stationName').apply(lambda df: df.tideValue.mean())
        return df



    def station_graph(self, station_name, time_from=None, time_to=None):
        """Return a matplotlib graph of the tide data at a named station,
        indexed by the dateTime data.

        Parameters
        ----------

        station_name: str
            Station Name
        time_from: str or None
            Time from which to report (ISO 8601 format)
        time_to: str or None
            Time up to which to report (ISO 8601 format)

        Returns
        -------

        matplotlib.figure.Figure
            Labelled graph of station tide data.
        """

        self.data['tideValue'] = pd.to_numeric(self.data['tideValue'], errors= 'coerce').fillna(0).astype('float')
        df = self.data.pivot(index = 'dateTime', columns = 'stationName', values = 'tideValue')
        df1 = df.loc[time_from: time_to, :]
        df1[station_name].plot()
        plt.xlabel('Time & Date')
        plt.ylabel('Tide Height(m)')
        plt.title(station_name)
        plt.xticks(rotation = 90)

        return plt.show()
    def add_data(self, date_time, station_name, tide_value):
        """Add data to the reader DataFrame.

        Parameters
        ----------
        date_time: str
            Time of reading in ISO 8601 format
        station_name: str
            Station Name
        time_value: float
            Observed tide in m

        Examples
        --------

        >>> reader = Reader("tideReadings.csv")
        >>> original_len = len(reader.data.index)
        >>> reader.add_data("2021-09-20T02:00:00Z",
                            "Newlyn", 1.465)
        >>> len(reader.data.index) = original_len + 1
        True
        """

    def add_data(self, date_time, station_name, tide_value):

            df1 = self.data
            df2 = pd.DataFrame({'dateTime': [date_time], 'stationName': [station_name],'tideValue': [tide_value]})
            frame = [df1, df2]
            print(pd.concat(frame, ignore_index = True))
            return pd.concat(frame, ignore_index = True)
        

    def write_data(self, filename):
        """Write data to disk in .csv format.

        Parameters
        ----------

        filename: str
            filename to write to.
        """

        return self.data.to_csv(filename)








if __name__ == "__main__":
    reader = Reader("tideReadings.csv")
    try:
        print(len(reader.data.index))
    except TypeError:
        print("No data loaded.")
