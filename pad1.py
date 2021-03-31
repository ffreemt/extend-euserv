"""window.navigator.webdriver."""
from typing import Optional, Union

from pathlib import Path
import asyncio
from pyppeteer import launch

executable_path: Optional[Union[str, Path]] = None

# half-hearted attempt to use an existing chrome
if Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe").exists():
    executable_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
elif Path(r"D:\Program Files (x86)\Google\Chrome\Application\chrome.exe").exists():
    executable_path = r"D:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

_ = """
    await page.evaluateOnNewDocument('''() => {
        Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
        })
        }
    ''')
"""

# https://github.com/DIYgod/RSSHub/issues/6680
# ignoreDefaultArgs: ["--enable-automation"]
# window.navigator.webdriver

async def main():
    browser = await launch(
        executablePath=executable_path,
        headless=False,
        args=[
            "--disable-infobars",
        ],
        ignoreDefaultArgs=[
            "--enable-automation",
        ],
    )
    page = await browser.newPage()

    await page.goto('http://exercise.kingname.info')
    input('检查完毕后按下回车键关闭窗口...')
    await browser.close()

asyncio.run(main())