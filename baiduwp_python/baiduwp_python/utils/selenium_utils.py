import time

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service

from baiduwp_python.settings.settings import logger
from .singleton_utils import singleton
from baiduwp_python.settings.config import selenium_executable_path


@singleton
class SeleniumDriver:
    def __init__(self, executable_path):
        options = ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("disable-gpu")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("blink-settings=imagesEnabled=false")
        options.add_argument("--disable-extensions")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--headless")
        s = Service(executable_path=executable_path)
        self.driver = Chrome(service=s, options=options)

    def get_driver(self):
        return self.driver

    def __del__(self):
        if self.driver:
            self.driver.quit()


def get_html_by_selenium(url):
    try:
        driver = SeleniumDriver(selenium_executable_path).get_driver()
        driver.get(url)
        time.sleep(3)
        return driver.execute_script("return document.documentElement.outerHTML")
    except Exception as e:
        logger.error(f"get_html_by_selenium() meet error: {e}")
        return ""
