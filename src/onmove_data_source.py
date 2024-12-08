#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DataSource abstract class."""

from datetime import timedelta
import pandas as pd
from data_source import DataSource


class OnMoveDataSource(DataSource):
    """
    Create OnMove data source.

    OnMove is a proprietary format used on OnMove running watches by Decathlon.
    It's made of two binary files:
        * OMH that contains a summary of the run with the date and time. This
          file will be considered as optional for now;
        * OMD that contains all the data (speed, positions etc) recorded
          every 5 seconds (in theory).
    The format has been retro-engineered and the files used in these classes
    are CSV. The Python script that converts these binary files to CSV will be
    included in this class as a method to directly handle the binary files at
    a later point.
    """

    def __init__(self, files: list):
        """Create the object."""
        self._OMDfile = files[0]
        self._OMHfile = files[1] if len(files) == 2 else None
        self._df = pd.DataFrame()
        self._read_data()
        self._clean_data()
        self._format_data()

    @property
    def dataframe(self) -> pd.DataFrame:
        """Access the dataframe."""
        return self._df

    @property
    def run_centre(self) -> (float, float):
        """Centre of the run positions."""
        return [self.dataframe["Latitude"].mean(),
                self.dataframe["Longitude"].mean()]

    @property
    def run_width(self) -> float:
        """Biggest distance between two positions of the run."""
        return max(self.dataframe["Latitude"].max()
                   - self.dataframe["Latitude"].min(),
                   self.dataframe["Longitude"].max()
                   - self.dataframe["Longitude"].min())

    def _read_data(self):
        """Read data."""
        self._df = pd.read_csv(self._OMDfile)

    def _clean_data(self):
        """Clean data."""
        if self._df.any:
            # Drop empty column, to be fixed in the binary to CSV script
            self._df = self._df.loc[:,
                                    ~self._df.columns.str.contains('^Unnamed')]
            self._df.drop_duplicates()

    def _format_data(self):
        """
        Format data.

        To be implemented once a common output format to OnMove and
        GPX inputs will be determined.

        Time in second
        Distance in meter
        Speed in km/h
        Position (lattitude, longitude) in degree
        Pace in Minute/km

        """
        self._df["RawPace"] = self._df["Speed"].apply(
            lambda x: round(60 / x, 2))
        # Convert decimal minutes to timedelta and then remove microseconds
        self._df["Pace"] = pd.to_timedelta(self._df["RawPace"].apply(
            lambda x: timedelta(minutes=x))).values.astype(
                "timedelta64[s]")
        self._df["Minute"] = self._df["Time"].apply(lambda x: x // 60)
        self._df["Hour"] = self._df["Time"].apply(lambda x: x // 3600)
        self._df["1km"] = self._df["Distance"].apply(lambda x: x // 1000)
        self._df["5km"] = self._df["Distance"].apply(lambda x: x // 5000)
        self._df["10km"] = self._df["Distance"].apply(lambda x: x // 10000)
        self._df["20km"] = self._df["Distance"].apply(lambda x: x // 20000)
        self._df["Half Marathon"] = self._df["Distance"].apply(
            lambda x: x // 21097.5)
        self._df["Marathon"] = self._df["Distance"].apply(
            lambda x: x // 42195)
