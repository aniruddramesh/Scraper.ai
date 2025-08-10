from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
import time

def _clean_soup_text(soup):
    for tag in soup(['script', 'style', 'noscript', 'iframe']):
        tag.decompose()
    text = soup.get_text(separator="\n")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)

def scrape_with_requests(url, timeout=10):
    resp = requests.get(url, timeout=timeout, headers={"User-Agent": "Mozilla/5.0"})
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    main = soup.find('main') or soup.find('article') or soup
    return _clean_soup_text(main)

def scrape_with_selenium(url, headless=True, wait=3):
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    try:
        driver.get(url)
        time.sleep(wait)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        main = soup.find('main') or soup.find('article') or soup
        return _clean_soup_text(main)
    finally:
        driver.quit()

def scrape_page(url, prefer_selenium=True, max_chars=200000):
    try:
        if prefer_selenium:
            text = scrape_with_selenium(url)
        else:
            text = scrape_with_requests(url)
    except Exception:
        text = scrape_with_requests(url)
    if len(text) > max_chars:
        text = text[:max_chars] + "\n\n[TRUNCATED]"
    return text
