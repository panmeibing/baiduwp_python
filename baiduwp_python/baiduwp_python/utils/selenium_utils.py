import time

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service

from baiduwp_python.settings.settings import logger
# from .singleton_utils import singleton
from baiduwp_python.settings.config import selenium_executable_path


def get_chrome_driver(executable_path):
    driver = None
    try:
        options = ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("disable-gpu")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("blink-settings=imagesEnabled=false")
        options.add_argument("--disable-extensions")
        options.add_argument("--ignore-certificate-errors")
        # options.add_argument("--headless")
        s = Service(executable_path=executable_path)
        driver = Chrome(service=s, options=options)
        source_str = """Object.defineProperty(navigator, 'webdriver', {get: () => undefined })"""
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": source_str})
    except Exception as e:
        logger.error(e)
    return driver


def get_html_by_selenium(url, bduss):
    try:
        driver = get_chrome_driver(selenium_executable_path)
        driver.get("https://www.baidu.com")
        driver.add_cookie({"name": "BDUSS", "value": bduss})
        driver.refresh()
        time.sleep(1)
        driver.get(url)
        print("get_cookies: ", driver.get_cookies())
        # time.sleep(5)
        return driver.execute_script("return document.documentElement.outerHTML")
    except Exception as e:
        logger.error(f"get_html_by_selenium() meet error: {e}")
        return ""


if __name__ == '__main__':
    bd_uss = "ZYOTJVTU1oM01PendPT0NYOHkxemZRTjJmVnhlZG1mMlhFaE5FdUFqVW5kSkprSVFBQUFBJCQAAAAAAAAAAAEAAACgtwcpsfnA5LXEz6PN-zEyMwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACfnamQn52pkWT"
    html_str = get_html_by_selenium("https://pan.baidu.com/s/1TlDb_fQ6NlaTMUEZbib4Bw?pwd=bk8d", bd_uss)
    print("html_str:", html_str)
