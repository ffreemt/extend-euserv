"""Extend euserv expiry date."""
# pylint: disable=too-many-locals, too-many-statements

import asyncio
from time import sleep
from random import randint

# from pprint import pprint
import logzero
from logzero import logger

from absl import app, flags

from extend_euserv.get_ppbrowser import BROWSER

# from extend_euserv.get_ppbrowser import LOOP
from extend_euserv.login_euserv import login_euserv
from extend_euserv.extend_contract import extend_contract
from extend_euserv.config import Settings
from extend_euserv import __version__

CONFIG = Settings()
try:
    LOOP = asyncio.get_running_loop()
except Exception:
    try:
        LOOP = asyncio.get_event_loop()
    except Exception:
        try:
            LOOP = asyncio.new_event_loop()
            asyncio.set_event_loop(LOOP)
        except Exception as exc:
            logger.error(exc)
            raise SystemExit(1) from exc

FLAGS = flags.FLAGS
flags.DEFINE_string(
    "username",
    "",  # use euserv_USERNAME environ var (can be set in .env) if empty
    "euserv email address",
    short_name="u",
)
flags.DEFINE_string(
    "password",  # use euserv_PASSOWRD environ var (can be set in .env) if empty
    "",  # filename dir if empty
    "euserv password",
    short_name="p",
)

flags.DEFINE_boolean(
    "info",
    False,
    "print account info and exit",
    short_name="i",
)
flags.DEFINE_boolean(
    "sleepon",
    False,
    "turn on sleep in two places",
    short_name="s",
)
flags.DEFINE_boolean(
    "debug",
    False,
    "print verbose debug messages",
    short_name="d",
)
flags.DEFINE_boolean("version", False, "print version and exit", short_name="V")


def proc_argv(_):  # pylint: disable=too-many-branches  # noqa: C901
    """Proc_argv in absl."""

    if FLAGS.version:
        print(
            "extend_euserv %s 20210401, brought to you by mu@qq41947782" % __version__
        )
        raise SystemExit(0)

    if FLAGS.debug or CONFIG.debug:
        logzero.loglevel(10)  # logging.DEBUG
    else:
        logzero.loglevel(20)  # logging.INFO

    # args = dict((elm, getattr(FLAGS, elm)) for elm in FLAGS)
    logger.debug(
        "\n\t available args: %s", dict((elm, getattr(FLAGS, elm)) for elm in FLAGS)
    )

    args = ["username", "password", "info", "debug"]

    debug = FLAGS.debug
    if debug:
        # [[elm, getattr(FLAGS, elm)] for elm in args]
        _ = []
        for elm in args:
            val = getattr(FLAGS, elm)
            if elm in ["username", "password"]:
                val = "*" * len(val)  # mask val
            _.append([elm, val])
        logger.debug("\n\t args: %s", _)

    if FLAGS.sleepon:
        # inject a random delay
        delay = randint(1, 240)  # 4 minutes
        logger.info(" Sleeping for %s s", delay)
        sleep(delay)

    username = FLAGS.username
    password = FLAGS.password
    try:
        page = LOOP.run_until_complete(login_euserv(username, password))
        # or setup .env or os.environ['euserv_password'] ['euserv_email']
        # CONFIG = Settings()
        # page = LOOP.run_until_complete(login_euserv(CONFIG.email, CONFIG.password))
    except Exception as exc:
        logger.error("login: %s", exc)
        logger.error("Unable to login it appears, exiting")
        raise SystemExit(1) from exc

    info = FLAGS.info
    contract_info = info
    if info:
        logger.info("Feching contract info...")
    else:
        # extend contract if possible
        logger.info("Extending contract if possible ...")

    msg, extra = LOOP.run_until_complete(
        extend_contract(page, contract_info=contract_info)
    )

    logger.info("\n%s\n", msg)
    if extra:
        logger.info("\n%s", extra)

    try:
        LOOP.run_until_complete(page.close())
        LOOP.run_until_complete(BROWSER.close())
    finally:
        ...
        # LOOP.close()


def main():
    """Main.

    testing in ipython
    FLAGS(shlex.split("app -u un -p pw")) or
    import os
    os.environ['ppbrowser_headful'] = '1'
    os.environ['euserv_password'] = 'pw'  # snippets-euserv
    os.environ['euserv_email'] = 'emaill'
    os.environ['euserv_headful'] = '1'

    CONFIG = Settings()
    """
    app.run(proc_argv)


if __name__ == "__main__":
    main()
