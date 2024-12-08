#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Data Source Factory."""

from enum import Enum

from abc import ABC
from onmove_data_source import OnMoveDataSource


# TODO StrEnum in Python 3.11
class DataType(Enum):
    """Types of Data Source."""

    ON_MOVE = "OnMove"
    GPX = "GPX"


class DataSourceFactory(ABC):
    """Data Source Factory."""

    @staticmethod
    def create_data_source(data_type: DataType, files: list):
        """Call the OnMove DataSource factory."""
        factory_mapping = {
            DataType.ON_MOVE.value: OnMoveDataSource
            # DataType.GPX.value: GPXDataSourceFactory.create_data_source,
            }

        factory = factory_mapping.get(data_type.value)

        if factory is None:
            raise ValueError("Invalid data type")
        return factory(files)
