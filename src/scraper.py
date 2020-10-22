from bs4 import BeautifulSoup
from selenium import webdriver
import config as config
from sys import platform
import urllib.parse as urlparse
from urllib.parse import parse_qs
import time
from datetime import datetime
from hotel import Hotel


# configure selenium driver. We we use Chrome as driver
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')

# working with chrome version 86
if platform == 'linux' or platform == 'linux2':  # linux
    driver = webdriver.Chrome('../drivers/chromedriver_linux', chrome_options=options)
    driver2 = webdriver.Chrome('../drivers/chromedriver_linux', chrome_options=options)
elif platform == 'darwin':  # mac
    driver = webdriver.Chrome('../drivers/chromedriver_mac', chrome_options=options)
    driver2 = webdriver.Chrome('../drivers/chromedriver_mac', chrome_options=options)
elif platform == 'win32':  # windows
    driver = webdriver.Chrome('../drivers/chromedriver.exe', chrome_options=options)
    driver2 = webdriver.Chrome('../drivers/chromedriver.exe', chrome_options=options)



def get_coords_from_google_maps(url):
    parsed = urlparse.urlparse(url)
    coords = parse_qs(parsed.query)['center'][0].split(',')
    return [float(coords[0]), float(coords[1])]


def hotel_has_service(services_div, service):
    services = services_div.select('div')
    for serv in services:
        if service.lower() in serv.text.lower():
            return True
    return False


def scrape_hotel(url):
    url = config.BASE_URL + url
    driver2.get(url)
    time.sleep(2)  # wait time to load google maps API

    html = driver2.page_source
    soup = BeautifulSoup(html, 'lxml')

    # retrieve hotel attributes
    name = soup.select_one('._1mTlpMC3').text
    hotel = Hotel(name)

    stars = soup.select_one('._2aZlo29m')
    hotel.stars = float(stars.get('title')[:3].replace(',', '.')) if stars is not None else None
    # price_range =
    score = soup.select_one('._3cjYfwwQ')
    hotel.score = float(score.text.replace(',', '.')) if score is not None else None
    ranking_in_city = soup.select_one('.rank')
    hotel.ranking_in_city = int(ranking_in_city.text[4:].replace('.', '')) if ranking_in_city is not None else None
    # rooms =

    # opinions
    num_opinions = soup.select_one('._1aRY8Wbl')
    hotel.num_opinions = int(num_opinions.text.replace('.', '')) if num_opinions is not None else None
    num_opinions_excellent = soup.select_one('._2lcHrbTn > li:nth-child(1) ._3fVK8yi6')
    hotel.num_opinions_excellent = int(num_opinions_excellent.text.replace('.', '')) \
        if num_opinions_excellent is not None else None
    num_opinions_good = soup.select_one('._2lcHrbTn > li:nth-child(2) ._3fVK8yi6')
    hotel.num_opinions_good = int(num_opinions_good.text.replace('.', '')) if num_opinions_good is not None else None
    num_opinions_normal = soup.select_one('._2lcHrbTn > li:nth-child(3) ._3fVK8yi6')
    hotel.num_opinions_normal = int(num_opinions_normal.text.replace('.', '')) \
        if num_opinions_normal is not None else None
    num_opinions_bad = soup.select_one('._2lcHrbTn > li:nth-child(4) ._3fVK8yi6')
    hotel.num_opinions_bad = int(num_opinions_bad.text.replace('.', '')) if num_opinions_bad is not None else None
    num_opinions_awful = soup.select_one('._2lcHrbTn > li:nth-child(5) ._3fVK8yi6')
    hotel.num_opinions_awful = int(num_opinions_awful.text.replace('.', '')) if num_opinions_awful is not None else None
    num_qa = soup.select('._1aRY8Wbl')[1]
    hotel.num_qa = int(num_qa.text.replace('.', '')) if num_qa is not None else None

    # nearby
    nearby_restaurants = soup.select('.oPMurIUj')[1]
    hotel.nearby_restaurants = int(nearby_restaurants.text.replace('.', '')) if nearby_restaurants is not None else None
    nearby_attractions = soup.select('.oPMurIUj')[2]
    hotel.nearby_attractions = int(nearby_attractions.text.replace('.', '')) if nearby_attractions is not None else None

    # location
    maps_url = soup.select_one('#LOCATION > div.TXBgG7JJ > span > img').get('src')
    [hotel.latitude, hotel.longitude] = get_coords_from_google_maps(maps_url)
    # zone =

    # services
    hotel.swimming_pool = hotel_has_service(soup.select('._1nAmDotd')[0], 'piscina')
    hotel.bar = hotel_has_service(soup.select('._1nAmDotd')[0], 'bar')
    hotel.restaurant = hotel_has_service(soup.select('._1nAmDotd')[0], 'restaurant')
    hotel.breakfast = hotel_has_service(soup.select('._1nAmDotd')[0], 'desayuno')
    hotel.gym = hotel_has_service(soup.select('._1nAmDotd')[0], 'gimnasio')
    hotel.admits_pets = hotel_has_service(soup.select('._1nAmDotd')[0], 'mascota')
    hotel.air_conditioning = hotel_has_service(soup.select('._1nAmDotd')[1], 'aire')
    hotel.date = datetime.today()
    return hotel


def scrape():
    """ Scrapes Trip Advisor's hotels

    :return:
    """
    url = config.URL
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    total_pages = int(soup.select('.pageNumbers a')[-1].get('data-page-number'))
    total_pages = 1

    # iterate over all pages
    for _ in range(total_pages):
        hotel_divs = soup.select('.ppr_priv_hsx_hotel_list_lite .photo-wrapper > a')
        hotel_urls = list({a.get('href') for a in hotel_divs})  # use a set since sponsored hotels can be duplicated
        for url in hotel_urls[:1]:
            hotel = scrape_hotel(url)
            print(hotel)

        # navigate to next page
        button = driver.find_element_by_class_name("next")
        button.click()
        # time.sleep(5)
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')







