#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Data Analyser."""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype

from data_source import DataSource


class AnalyserFactory:
    """Concret Factory for Analyser."""

    @staticmethod
    def create_analyser(data_source: DataSource):
        """Create on OnMoveDataSource object."""
        return Analyser(data_source)


# -----------------------------------------------------------------------------
class Analyser:
    """Analyser."""

    def __init__(self, data_source: DataSource):
        """Create the object."""
        self._data_source = data_source
        self._df = self._data_source.dataframe
        self._summary = self._generate_summary()

    def compress_by(self, col: str) -> pd.DataFrame():
        """Compress data according to a column."""
        if col in self.kpi():
            # return self._df.groupby(col).agg(self._mean)
            return self._df.groupby(col).mean().reset_index()

    def _generate_summary(self) -> dict:
        """Generate summary."""
        stats = ["mean", "std", "median", "min", "max"]
        return self._df.agg(
            {
                "Speed": stats,
                "Pace": stats,
                }
            ).to_dict()

    @property
    def summary(self) -> dict:
        """Summary."""
        return self._summary

    @staticmethod
    def kpi():
        """Columns of interest for analysis."""
        return ["Minute", "Hour", "1km", "5km", "10km", "20km", "HM", "M"]

    @staticmethod
    def plot(self, x: str, y: str):
        """Plot columns."""
        self._df.plot(x=x, y=y, kind="bar", figsize=(10, 10))
        plt.show()

    @staticmethod
    def _mean(col):
        """Mean function to deal with str columns."""
        if is_numeric_dtype(col):
            return col.mean()
        else:
            return col.unique() if col.nunique() == 1 else np.nan
