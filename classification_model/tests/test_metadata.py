from classification_model import __version__ as model_version
from classification_model.config.core import config

def test_package_version_matches_config():
    # Тест просто проверяет, что версия в коде совпадает с версией в конфиге
    # Это гарантирует, что конфиги загружаются правильно
    assert model_version == config.package_config.version
