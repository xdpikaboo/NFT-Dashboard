import os

os.system(
  '''
  pip install -r requirements.txt &&
  apt-get update &&
  apt install chromium-chromedriver &&
  cp /usr/lib/chromium-browser/chromedriver /usr/bin
  '''
)

from selenium import webdriver
from fake_useragent import UserAgent
userAgent = UserAgent().random
options = webdriver.ChromeOptions()
options.add_argument('-headless')
options.add_argument('-no-sandbox')
options.add_argument('-disable-dev-shm-usage')
options.add_argument(f'user-agent={userAgent}')
options.add_argument("--incognito")
options.add_argument('start-maximized')
# open it, go to a website, and get results
wd = webdriver.Chrome('chromedriver',options=options)
wd.get("https://api-mainnet.magiceden.io/rpc/getCollectionEscrowStats/degods")
print(wd.page_source)