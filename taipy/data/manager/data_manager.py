import logging
from typing import Dict, List

from taipy.configuration import ConfigurationManager
from taipy.data import CSVDataSource, EmbeddedDataSource
from taipy.data.data_source import DataSource
from taipy.data.data_source_config import DataSourceConfig
from taipy.data.data_source_model import DataSourceModel
from taipy.data.scope import Scope
from taipy.exceptions import InvalidDataSourceType

"""
A Data Manager is responsible for keeping track and retrieving Taipy DataSources.
The Data Manager will facilitate data access between Taipy Modules.
"""


class DataManager:
    # This represents a database table that maintains our DataSource References.
    __DATA_SOURCE_MODEL_DB: Dict[str, DataSourceModel] = {}
    __DATA_SOURCE_CONFIG_DB: Dict[str, DataSourceConfig] = {}
    __DATA_SOURCE_CLASSES = {EmbeddedDataSource, CSVDataSource}
    __DATA_SOURCE_CLASS_MAP = {v.type(): v for v in __DATA_SOURCE_CLASSES}

    def delete_all(self):
        self.__DATA_SOURCE_MODEL_DB: Dict[str, DataSourceModel] = {}
        self.__DATA_SOURCE_CONFIG_DB: Dict[str, DataSourceConfig] = {}

    def register_data_source_config(self, data_source_config: DataSourceConfig):
        self.__DATA_SOURCE_CONFIG_DB[data_source_config.name] = data_source_config

    def get_data_source_config(self, name) -> DataSourceConfig:
        return self.__DATA_SOURCE_CONFIG_DB[name]

    def create_data_source(self, data_source_config: DataSourceConfig) -> DataSource:
        data_source_config &= ConfigurationManager.data_manager_configuration
        try:
            data_source = self.__DATA_SOURCE_CLASS_MAP[data_source_config.type](
                name=data_source_config.name,
                scope=data_source_config.scope,
                properties=data_source_config.properties,
            )
        except KeyError:
            logging.error(f"Cannot create Data source. " f"Type {data_source_config.type} does not exist.")
            raise InvalidDataSourceType(data_source_config.type)
        self.save_data_source(data_source)
        return data_source

    def save_data_source(self, data_source: DataSource):
        self.create_data_source_model(
            data_source.id,
            data_source.name,
            data_source.scope,
            data_source.type(),
            data_source.properties,
        )

    def get_data_source(self, data_source_id: str) -> DataSource:
        model = self.fetch_data_source_model(data_source_id)
        return self.__DATA_SOURCE_CLASS_MAP[model.type](
            name=model.name,
            scope=model.scope,
            id=model.id,
            properties=model.data_source_properties,
        )

    def get_data_sources(self) -> List[DataSource]:
        return [self.get_data_source(model.id) for model in self.__DATA_SOURCE_MODEL_DB.values()]

    def create_data_source_model(self, id: str, name: str, scope: Scope, type: str, properties: dict):
        self.__DATA_SOURCE_MODEL_DB[id] = DataSourceModel(
            id,
            name,
            scope,
            type,
            properties,
        )

    def fetch_data_source_model(self, id) -> DataSourceModel:
        return self.__DATA_SOURCE_MODEL_DB[id]