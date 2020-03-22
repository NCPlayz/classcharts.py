import re
from bs4 import BeautifulSoup


def sanitise(content):
    return re.sub("\n\n+", "\n", BeautifulSoup(content, "lxml").text).strip()