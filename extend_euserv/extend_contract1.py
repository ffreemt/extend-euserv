"""Extend contract from Notifications."""
# pylint: disable=too-many-locals, too-many-branches, unused-variable, unused-import, duplicate-code, too-many-statements

from typing import (
    # List,
    Optional,
    Tuple,
)

import asyncio
import re

# import more_itertools as mit
from pyquery import PyQuery as pq
import pyppeteer
from logzero import logger

from extend_euserv.config import Settings

# from extend_euserv.login_euserv import login_euserv

config = Settings()
URL = "https://support.euserv.com/"


# fmt: off
async def extend_contract(
        page: Optional[pyppeteer.page.Page] = None
) -> Tuple[str, Optional[str]]:
    # fmt: on
    """Extend contract from Notifications (alternative way, refer to exract_contract.

    //a[contains(text(),"Cover Page")]

    xpath_contracts = '//a[contains(text(),"Contracts")]'
    btn_contracts  = await page.waitForXPath(xpath_contracts)
    # await btn_contracts.click()
    # await page.waitForNavigation()
    done, pedning = await asyncio.wait([
        btn_contracts.click(),
        page.waitForNavigation()
    ])
    for task in done:
        err_flag = False
        try:
            await task
        except Exception as exc:
            err_flag = True
            logger.error(exc)
    if err_flag:
        raise Exception("err_flag: %s, see previous messages in the log." % err_flag)

    xpath_contracts = '//a[contains(text(),"Contracts")]'
    btn_contracts  = await page.waitForXPath(xpath_contracts)
    results = await asyncio.gather(
        btn_contracts.click(),
        page.waitForNavigation(),
        return_exceptions=True
    )
    for result_or_exc in results:
        if isinstance(result_or_exc, Exception):
            print("I caught:", repr(result_or_exc))
        else:
            print(result_or_exc)
    # https://stackoverflow.com/questions/42231161/asyncio-gather-vs-asyncio-wait

    xpath_vserver = '//div[@pg_caption="vServer"]'

    await page.waitForXPath('//a[contains(text(),"Contracts")]')
    bhandler = await page.xpath('//a[contains(text(),"Contracts")]')
    await bhandler[0].click()

    # vServer
    # //div[@id="kc2_order_customer_orders_tab_1"]
    # '//div[@pg_caption="vServer"]'

    xpath = '//div[@pg_caption="vServer"]'
    # await page.waitForXPath(xpath)
    # bhandler = await page.xpath(xpath)
    # combined
    bhandler, *_ = await page.waitForXPath(xpath)
    await bhandler.click()

    # Selection cell
    xpath_ = '//div[@class="kc2_order_action_container"]'
    await page.waitForXPath(xpath_)

    """

    # click Cover Page
    logger.info("Clicking Cover Page...")
    xpath_cpage = '//a[contains(text(),"Cover Page")]'
    try:
        btn_cpage = await page.waitForXPath(xpath_cpage, timout=45000)
    except Exception as exc:
        logger.error(exc)
        raise
    # await btn_cpage.click()
    # await page.waitForNavigation()
    try:
        done, pending = await asyncio.wait([
            btn_cpage.click(),
            page.waitForNavigation(),
        ])
    except Exception as exc:
        logger.error(exc)
        raise
    err_flag = False
    for task in done:
        err_flag = False
        try:
            await task
        except Exception as exc:
            err_flag = True
            logger.error(exc)
    if err_flag:
        raise Exception("err_flag: %s, see previous messages in the log." % err_flag)

    # check extend contract is present
    try:
        content = await (page.content())
    except Exception as exc:
        logger.error(exc)
        raise
    if "extend contract" not in content:
        msg = "Too early to extend ('extend contract' not appear in the page)."
        logger.info("Too early to extend ('extend contract' not appear in the page), exiting...")
        return (msg, None)

    # click "extend contract"
    logger.info("Clicking extend contract...")
    xpath = '//a[contains(text(),"extend contract")]'
    try:
        btn = await page.waitForXPath(xpath, timout=45000)
    except Exception as exc:
        logger.error(exc)
        raise
    try:
        done, pending = await asyncio.wait([
            btn.click(),
            page.waitForNavigation(),
        ])
    except Exception as exc:
        logger.error(exc)
        raise
    err_flag = False
    for task in done:
        err_flag = False
        try:
            await task
        except Exception as exc:
            err_flag = True
            logger.error(exc)
    if err_flag:
        raise Exception("err_flag: %s, see previous messages in the log." % err_flag)

    # ## click "Extend" in popup
    # //*[@id="kc2_customer_contract_details_change_plan_item_container_13448"]/tbody/tr/td[2]/input
    # //input[@type='submit']
    # //input[@value='Search'  # OK!

    logger.info("Clicking Extend in popup...")
    xpath = "//input[@value='Extend']"
    try:
        btn = await page.waitForXPath(xpath, timout=45000)
    except Exception as exc:
        logger.error(exc)
        raise
    try:
        done, pending = await asyncio.wait([
            btn.click(),
            # page.waitForNavigation(),  # should not check
        ])
    except Exception as exc:
        logger.error(exc)
        raise
    err_flag = False
    for task in done:
        err_flag = False
        try:
            await task
        except Exception as exc:
            err_flag = True
            logger.error(exc)
    if err_flag:
        raise Exception("err_flag: %s, see previous messages in the log." % err_flag)

    # # Send password
    logger.info("Supplying password to the form...")
    xpath = "//input[@name='password']"
    try:
        await page.type('input[name="password"]', config.password + "\n", {"delay": 20})
    except Exception as exc:
        logger.error(exc)
        raise

    _ = "#kc2_customer_contract_details_extend_contract_confirmation_dialog_main"
    try:
        content = await (page.content())
    except Exception as exc:
        logger.error(exc)
        raise
    doc = pq(content)
    info = doc(content)(_).text()
    logger.info("\n\tContract Extension Confirmation: [%s]", info)

    # Final confirm
    logger.info("Clicking Confirm...")
    xpath = "//input[@value='Confirm']"
    try:
        btn = await page.waitForXPath(xpath, timout=45000)
    except Exception as exc:
        logger.error(exc)
        raise
    try:
        done, pending = await asyncio.wait([
            btn.click(),
            # page.waitForNavigation(),  # should not check
        ])
    except Exception as exc:
        logger.error(exc)
        raise
    err_flag = False
    for task in done:
        err_flag = False
        try:
            await task
        except Exception as exc:
            err_flag = True
            logger.error(exc)
    if err_flag:
        raise Exception("err_flag: %s, see previous messages in the log." % err_flag)

    # check message "Thank you! The contract has been extended."
    try:
        content = await (page.content())
    except Exception as exc:
        logger.error(exc)
        raise

    _ = re.findall(r"Thank you[\w\s!.]+", content)
    msg = ""
    if _:
        msg, = _
        logger.info("\n\teuserv.de says: %s", msg)
    else:
        logger.warning("not able to fetch any message, something has likely gone awry.")

    # other info
    content = await page.content()
    doc = pq(content)('.kc2_content_table')

    try:
        res = pq(doc[0]).text()
    except Exception as exc:
        res = str(exc)
    info = res

    extra = pq(doc[1]).text()
    pairs = [*zip(extra.splitlines()[1:][::2], extra.splitlines()[1:][1::2])]
    res = '\n'.join(f"{elm[0]:33} {elm[1]}" for elm in pairs)

    logger.info("\n\n%s", info)
    logger.info("\n%s", res)

    return info, res
