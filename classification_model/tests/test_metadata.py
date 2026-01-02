from classification_model import __version__ as model_version
from classification_model.config.core import config

def test_package_version_exists():
    # Просто проверяем, что версия определена и не пустая
    assert model_version is not None
    assert len(model_version) > 0