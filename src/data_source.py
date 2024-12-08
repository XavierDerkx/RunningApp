#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DataSource abstract class."""

from abc import ABC, abstractmethod
from datetime import timedelta


class DataSource(ABC):
    """Create abstract data source."""

    @property
    @abstractmethod
    def dataframe(self):
        """Container for the data (dataframe)."""
        pass

    @property
    @abstractmethod
    def run_centre(self) -> list:
        """
        Centre of the run positions.

        To be used to centre the map.
        """

    @property
    @abstractmethod
    def run_width(self) -> float:
        """
        Biggest distance between two positions of the run.

        To be used to determine the approriate default zoom on the map.
        """
        pass

    @abstractmethod
    def _read_data(self):
        """Read data."""
        pass

    @abstractmethod
    def _clean_data(self):
        """Clean data."""
        pass

    @abstractmethod
    def _format_data(self):
        """Format data."""
        pass

    @staticmethod
    def float2minsec(time: float) -> str:
        """Convert float to MM:SS."""
        return timedelta(minutes=time)
