from classification_model import __version__ as model_version


def test_package_version_exists():
    # Просто проверяем, что версия определена и не пустая
    assert model_version is not None
    assert len(model_version) > 0
