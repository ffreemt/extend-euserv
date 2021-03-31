"""Login to https://support.euserv.com/."""
# pylint:

from typing import Optional

import os
from time import sleep
from random import randint
import asyncio
import dotenv
import pyppeteer
from logzero import logger
from extend_euserv.get_ppbrowser import get_ppbrowser, BROWSER
from extend_euserv.config import Settings

# load .env to os.environ
# dotenv.load_dotenv()

CONFIG = Settings()
URL = "https://www.noip.com/members/dns/"
URL = "https://support.euserv.com/"


# fmt: off
async def login_euserv(
        email: Optional[str] = "",
        password: Optional[str] = "",
        browser=BROWSER,
) -> pyppeteer.page.Page:
    # fmt: on
    """Login to https://support.euserv.com/.

    return a pyppeteer.page.Page for subsequent processing.
    """
    try:
        _ = await browser.newPage()
    except Exception as exc:
        logger.error(exc)
        logger.info("Getting a new ppbrowser...")
        browser = await get_ppbrowser()

    try:
        page = await browser.newPage()
    except Exception as exc:
        logger.error(exc)
        raise

    ubound = 3
    idx = 0
    err_flag = False
    while idx < ubound:
        idx += 1  # retry ubound times
        logger.debug("Going to %s", URL)
        done, pending = await asyncio.wait([
            page.goto(URL),
            page.waitForNavigation(),
        ])
        err_flag = False
        for task in done:
            try:
                await task
            except Exception as exc:
                logger.error(exc)
                err_flag = True
        if err_flag:
            logger.info("Retry #%s", idx)
            sleep(randint(1, 10))
        else:
            break
    if err_flag:
        raise SystemError("err_flag: %s, check previous error messages in the log" % err_flag)  # return

    # We give it another try
    try:
        _ = await page.waitForSelector(".td-title", {"timeout": 20000})

        # already logged in
        if "Logout" in (await page.content()):
            logger.info("Already logged in.")
            raise SystemExit(" Change this to return page ")
            # return page
    except Exception as exc:
        logger.error("Not logged in yet, exc: %s, proceed", exc)

    # proceed
    # wait for form/submit
    logger.debug("Trying logging in...")
    try:
        await page.waitForSelector(".td-title", {"timeout": 20000})
    except TimeoutError:
        logger.error(TimeoutError)
        raise
    except Exception as exc:
        logger.error("Unable to fetch the page, network problem or euserv has changed page layout, %s, existing", exc)
        raise SystemExit(1) from exc

    if not email:
        # email = os.environ.get("EUSERV_EMAIL")
        email = CONFIG.email
    if not password:
        # password = os.environ.get("EUSERV_PASSWORD")
        password = CONFIG.password

    if not email:
        logger.error('Supply email address login_euserv(email="...") or set it in .env or as ENVIRONMENT (set/export EUSERV_EMAILE="...")')
        raise SystemExit(1)

    if not password:
        logger.error('Supply password, e.g., login_euserv(password="...") or set it in .env or as ENVIRONMENT (set/export EUSERV_EMAILE="...")')
        raise SystemExit(1)

    logger.info("\nemail: %s \npassword: %s", "*" * 6 + email[6:], "*" * (len(password) + 3))

    logger.debug("Logging in with email and password")
    try:
        await page.type('input[name="email"]', email, {"delay": 20})
        await page.type('input[name="password"]', password + "\n", {"delay": 20})
        # await handle.type('input[name="email"]', email, {"delay": 20})
        # await handle.type('input[name="password"]', password, {"delay": 20})

        # bhandle = await page.xpath('//*[@id="clogs"]/button')
        # await bhandle[0].click()
    except Exception as exc:
        logger.error("Oh no, exc: %s, exiting", exc)
        raise SystemExit(1)

    # wait for page to load
    # kc2_order_customer_orders_tab_1 vServer
    logger.info("Waiting for 'Cover Page' to load...")
    try:
        # _ = await page.waitForSelector('#kc2_order_customer_orders_tab_1', {"timeout": 45000})
        # _ = await page.waitForSelector('#kc2_order_customer_orders_tab_1', {"timeout": 45000})
        _ = await page.waitForXPath('//*[contains(text(),"Cover Page")]', {"timeout": 45000})
    except Exception as exc:
        logger.error("No go, exc: %s, exiting", exc)
        if "Login failed" in (await page.content()):
            logger.error("""
                Login failed.
                Please check email address/customer ID and password.""")
        # raise Exception(str(exc))
        logger.warning("Bad news: we are _not_ in, closing the page")
        await page.close()

        return page  # use page.isClosed() to check

    # if "vServer" in (await page.content()):
    if "Cover Page" in (await page.content()):
        logger.info("Good news: we are in.")
    else:
        logger.warning("Something is not right, maybe euserv's page layout is changed?")

    return page
