import asyncio
URL = "https://support.euserv.com/"

import os
from save_tempfile import save_tempfile

os.environ['EUSERV_EMAIL'] = "yucongo@gmail.com"
os.environ['EUSERV_PASSWORD'] = "k52!p!HQeqs2.Sa"

from extend_euserv.login_euserv import login_euserv

async def main():
    page = await login_euserv()
    
    
asyncio.run(main())

# page.evaluate(pageFunction: str, *args: Any, force_expr: bool = False) -> Any
res = await page.evaluate("""()=>document.getElementsByTagName("div").length""")
# 70

# await page.evaluate("""()=>document.getElementsByTagName("div")""")

el = await page.evaluate("""
