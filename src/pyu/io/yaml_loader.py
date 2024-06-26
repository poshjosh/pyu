import logging
import os
from collections.abc import Iterable
from typing import Callable, Union

from .file import load_yaml
from .variable_parser import replace_all_variables

logger = logging.getLogger(__name__)


class YamlLoader:
    @staticmethod
    def default_transform_function() -> Callable[[dict], dict]:
        return lambda config: replace_all_variables(config, dict(os.environ))

    def __init__(self, 
                 config_path: Union[str, Iterable],
                 transform: Callable[[dict], dict] = None,
                 prefix: str = '',
                 suffix: str = '',
                 extension: str = 'yaml'):
        self.__config_path = config_path \
            if isinstance(config_path, str) else os.path.join(*config_path)
        self.__transform = self.default_transform_function() if transform is None else transform
        self.__prefix = prefix
        self.__suffix = suffix
        self.__extension = extension

    def load_app_config(self, path: str = None) -> dict[str, any]:
        if not path:
            path = self.get_app_config_path()
        return self.load_from_path(path)

    def load_logging_config(self, path: str = None) -> dict[str, any]:
        if not path:
            path = self.get_logging_config_path()
        return self.load_from_path(path)

    def load_config(self, path: [str]) -> dict[str, any]:
        return self.load_from_path(self.get_path(path))

    def load_from_path(self, path: str, default: Union[dict[str, any], None] = None) \
            -> dict[str, any]:
        try:
            return self.__transform(load_yaml(path))
        except Exception as ex:
            if default is None:
                raise ex
            logger.warning(f'Failed to read: {path}')
            return default

    def get_app_config_path(self) -> str:
        return self.get_path('app')

    def get_logging_config_path(self) -> str:
        return self.get_path('logging')

    def get_path(self, path: Union[str, Iterable]) -> str:
        path = path if isinstance(path, str) else os.path.join(*path)
        return os.path.join(self.__config_path,
                            f'{self.__prefix}{path}{self.__suffix}.{self.__extension}')
