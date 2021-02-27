"""Fetch contracts info and update links."""
# pylint:

from typing import List, Optional, Tuple

import asyncio
import re
import more_itertools as mit
from pyquery import PyQuery as pq
import pyppeteer
from logzero import logger

URL = "https://support.euserv.com/"


# fmt: off
async def fetch_contracts(
        page: pyppeteer.page.Page,
        contract_info: bool = True
) -> Tuple[str, Optional[str]]:
    # fmt: on
    """Fetch contracts info and their update links if any.

    return info, links

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
    #

    if page.isClosed():
        logger.warning("Invalid page handle provided, return ([], [])...")
        # return [], []

    # make sure we are on the right page
    # if page.url != URL:  # no go
    if False:
        try:
            done, pending = await asyncio.wait([
                page.goto(URL),
                page.waitForNavigation()
            ])
        except Exception as exc:
            logger.error("%s, exiting", exc)
            # return [str(exc)], [""]

        err_flag = False
        for task in pending:
            err_flag = False
            try:
                await task
            except Exception as exc:
                logger.error(exc)
                err_flag = True
        if err_flag:
            raise Exception("err_flag: %s, see previous messages in the log", err_flag)

    # retrieve page text
    # content = await page.content()

    # click Contracts
    logger.info("Clicking Contracts...")
    xpath_contracts = '//a[contains(text(),"Contracts")]'
    try:
        btn_contracts  = await page.waitForXPath(xpath_contracts)
    except Exception as exc:
        logger.error(exc)
        raise
    # await btn_contracts.click()
    # await page.waitForNavigation()
    try:
        done, pedning = await asyncio.wait([
            btn_contracts.click(),
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

    # click vServer
    logger.info("Clicking vServer...")
    xpath_vserver = '//div[@pg_caption="vServer"]'
    # await page.waitForXPath(xpath)
    # bhandler = await page.xpath(xpath)
    # combined
    try:
        bhandler = await page.waitForXPath(xpath_vserver)
    except Exception as exc:
        logger.error(exc)
        raise

    try:
        done, pending = await asyncio.wait([
            bhandler.click(),
            # page.waitForNavigation({"timeout": 60 * 1000}),
        ])
    except Exception as exc:
        logger.error(exc)
        raise
    for task in done:
        err_flag = False
        try:
            await task
        except Exception as exc:
            err_flag = True
            logger.error(exc)
    if err_flag:
        raise Exception("err_flag: %s, see previous messages in the log." % err_flag)

    # contract table
    xpath_table = '//*[@id="kc2_order_customer_orders_tab_content_1"]/table'
    try:
        page.waitForXPath(xpath_table, {"timeout": 60 * 1000})
    except Exception as exc:
        logger.error(exc)
        raise

    selector = '#kc2_order_customer_orders_tab_content_1 > table'
    try:
        content = await (page.content())
    except Exception as exc:
        logger.error(exc)
        raise

    # table data n
    td_n = "#kc2_order_customer_orders_tab_content_1 > table > tbody > tr:nth-child(2) > td:nth-child(%s)"

    _ = pq(content)
    info = _(td_n % 1).text() + ": " + _(td_n % 4).text()
    logger.info("\n\tinfo: %s", info)

    if contract_info:
        return info, None

    # Select Button: '//div[@class="kc2_order_action_container"]'
    # //div[@class="kc2_order_action_container"]/span/form/input
    # //*[@id="kc2_order_customer_orders_tab_content_1"]/table/tbody/tr[2]/td[4]/div/span/form/input[1]

    xpath = '//*[@id="kc2_order_customer_orders_tab_content_1"]/table/tbody/tr[2]/td[4]/div/span/form/input'
    try:
        bhandler = await page.waitForXPath(xpath)
    except Exception as exc:
        logger.error(exc)
        raise

    try:
        done, pending = await asyncio.wait([
            bhandler.click(),
            page.waitForNavigation({"timeout": 60 * 1000}),
        ])
    except Exception as exc:
        logger.error(exc)
        raise
    for task in done:
        err_flag = False
        try:
            await task
        except Exception as exc:
            err_flag = True
            logger.error(exc)
    if err_flag:
        raise Exception("err_flag: %s, see previous messages in the log." % err_flag)

    # return contracts, full_links
    return info, "TODO"
