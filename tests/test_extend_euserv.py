from extend_euserv import __version__

from logzero import logger


# pytest --log-cli-level=10 tests\test_extend_euserv.py
def test_version():
    logger.debug("debug version: %s", __version__)  # pytest -s
    logger.info("info version: %s", __version__)
    print("print version: %s" % __version__)
    assert __version__[:3] == "0.1"
