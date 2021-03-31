"""Fetch contracts info and update links."""
# pylint:

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
from extend_euserv.login_euserv import login_euserv

config = Settings()
URL = "https://support.euserv.com/"


# fmt: off
async def extend_contracts(
        page: pyppeteer.page.Page,
        contract_info: bool = True
) -> Tuple[str, Optional[str]]:
    # fmt: on
    """Fetch and update contracts info and their update links if any.

    page: pyppeteer.page.Page
    contract_info: bool = True

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

    if page.url != "https://support.euserv.com/index.iphp":
        logger.warning(
            "\n page.url %s != 'https://support.euserv.com/index.iphp'\n"
            "We are probably on the wrong page or "
            "euserv.com has changed page layout. "
            "We proceed nevertheless. ",
            page.url
        )

    try:
        await page.goto("https://support.euserv.com/index.iphp")
    except Exception as exc:
        logger.error("%s, trying to relog in...", exc)
        try:
            page = await login_euserv()
        except Exception as exc:
            logger.error("%s, exiting", exc)
            raise SystemExit(1) from exc

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
        btn_contracts = await page.waitForXPath(xpath_contracts)
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

    # table data n in contract table
    td_n = "#kc2_order_customer_orders_tab_content_1 > table > tbody > tr:nth-child(2) > td:nth-child(%s)"
    del td_n

    td_ = '#kc2_order_customer_orders_tab_content_1 > table > tbody > tr:nth-child(2) > td'

    doc = pq(content)
    # info = doc(td_n % 1).text() + ": " + _(td_n % 2).text()

    info = []
    for elm in doc(td_)[:4]:  # first three entries
        try:
            _ = pq(elm).text()
            # remove anything after \n$('form
            _ = re.sub(re.escape("\n$('form") + r"[\s\S]+$", "", _)
            info.append(_)
        except Exception as exc:
            logger.debug(exc)

    logger.info("\n\tinfo: %s", info)

    extend_not_ready = False
    if "possible from" in "\n".join(info):
        extend_not_ready = True
        logger.info("Cant be extended yet...")

    if contract_info or extend_not_ready:
        return "\n".join(info), None

    # Select Button: '//div[@class="kc2_order_action_container"]'
    # //div[@class="kc2_order_action_container"]/span/form/input
    # //*[@id="kc2_order_customer_orders_tab_content_1"]/table/tbody/tr[2]/td[4]/div/span/form/input[1]

    xpath = '//*[@id="kc2_order_customer_orders_tab_content_1"]/table/tbody/tr[2]/td[4]/div/span/form/input'

    # extend contract button
    xpath = '//*[@id="kc2_order_customer_orders_tab_content_1"]/table/tbody/tr[2]/td[4]/div/div[2]/form/input[1]'
    del xpath

    selector = "#kc2_order_customer_orders_tab_content_1 > table > tbody > tr.kc2_order_upcoming_todo_row > td:nth-child(4) > div > div.kc2_order_extend_contract_term_container"

    # "exetend contract" button
    selector = "div > div.kc2_order_extend_contract_term_container"

    _ = await page.evaluate(f"""document.querySelectorAll('{selector}').length""", force_expr=True)

    # Nothing to extend
    if _ < 1:
        logger.info("Info: %s", info)
        logger.info(" Nothing to extend yet...")
        return "\n".join(info), None

    if _ > 1:
        logger.warning("There are %s items, the current version of extend_euserv only extends the first item.", _)

    try:
        # bhandler = await page.waitForXPath(xpath)
        bhandler = await page.waitForSelector(selector)
    except Exception as exc:
        logger.error(exc)
        raise

    # Cliking [extend contract] button
    try:
        logger.info("Cliking [extend contract] button")
        done, pending = await asyncio.wait([
            bhandler.click(),
            page.waitForNavigation({"timeout": 40 * 1000}),
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

    # #kc2_customer_contract_details_change_plan_item_container_13448 > tbody > tr > td:nth-child(2) > input
    # //*[@id="kc2_customer_contract_details_change_plan_item_container_13448"]/tbody/tr/td[2]/input

    # //input[contains(text(), 'Extend')]  NOK

    confirm = '.kc2_customer_contract_details_change_plan_item_action_button'

    try:
        _ = await page.waitForSelector(confirm)
    except Exception as exc:
        logger.error(exc)
        raise

    # send password
    try:
        await page.type('input[name="password"]', config.password + "\n", {"delay": 20})
    except Exception as exc:
        logger.error(exc)
        raise

    # final confirm
    try:
        await page.type('input[name="password"]', config.password + "\n", {"delay": 20})
    except Exception as exc:
        logger.error(exc)
        raise

    content = await page.content()
    doc = pq(content)('.kc2_content_table')

    try:
        res = pq(doc[0]).text()
    except Exception as exc:
        res = str(exc)
    info.append(res)

    extra = pq(doc[1]).text()
    pairs = [*zip(extra.splitlines()[1:][::2], extra.splitlines()[1:][1::2])]
    res = '\n'.join(f"{elm[0]:33} {elm[1]}" for elm in pairs)

    logger.info("\n" + "\n".join(info))
    logger.info("\n" + res)

    # return contracts, full_links
    # return info, "TODO"
    return "\n".join(info), res

_ = """
In [305]: pq(doc[1]).text()
Out[305]: extra = 'Contract data:\nContract ID:\n337738\nPlan/Service:\nvServer VS2-free v2.1\nArticle code:\n13448\nOrder reference ID:\nn/a\nDomains included in contract:\nkeine Domains vorhanden\nOrdered on:\n02.12.2020\nfrom IP: 113.254.98.199\nLast change on:\n31.03.2021\ne.g. by plan change\nProviding status:\nready\nProvided on:\n02.12.2020\nContract started on:\n02.12.2020\nStart of current contract period:\n02.03.2021\nMinimum contract period:\n1 month(s)\nEnd of contract period:\n02.05.2021\nContract term extension:\nThe contract ends automatically on 02.05.2021 if it is not extended manually.'
"""
