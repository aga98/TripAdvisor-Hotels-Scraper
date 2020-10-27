from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
import urllib.parse as urlparse
from urllib.parse import parse_qs
from datetime import datetime
from hotel import Hotel
import re


URL = "https://www.tripadvisor.es/Hotels-g187497-Barcelona_Catalonia-Hotels.html"
BASE_URL = "https://www.tripadvisor.es"

choose_driver = True  # Choose location of the chrome driver. If False, it will get the look in PATH.
# Specify driver location. Download compatible version for your system from https://chromedriver.chromium.org/downloads
diver_path = '../drivers/windows/chromedriver.exe'

# configure selenium driver. We we use Chrome as driver
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')

if choose_driver:
    driver = webdriver.Chrome(diver_path, chrome_options=options)
    driver2 = webdriver.Chrome(diver_path, chrome_options=options)
else:
    driver = webdriver.Chrome(chrome_options=options)
    driver2 = webdriver.Chrome(chrome_options=options)


# class to wait until next page of hotels is fully loaded --> checks for a change in CSS style
class wait_for_style_property(object):
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, drv):
        try:
            element = ec._find_element(drv, self.locator)
            return element.value_of_css_property("display") == "none"
        except StaleElementReferenceException:
            return False


# extracts coordinates from map image url
def get_coords_from_google_maps(url):
    parsed = urlparse.urlparse(url)
    coords = parse_qs(parsed.query)['center'][0].split(',')
    return [float(coords[0]), float(coords[1])]


# checks if the hotel has a service or not
def hotel_has_service(services_div, service):
    if services_div is not None:
        services = services_div.select('div')
        for serv in services:
            if service.lower() in serv.text.lower():
                return True
    return False


# get "about the hotel" information
def get_about_info(about_div, info):
    if about_div is not None:
        descendants = about_div.select('div')
        for i in range(len(descendants)):
            if info in descendants[i].text.lower():
                return str(descendants[i+1])
    return None


# scrapes hotel url
def scrape_hotel(url):
    url = BASE_URL + url
    driver2.get(url)
    # wait until map is loaded in order to get coordinates
    WebDriverWait(driver2, 60).until(
        ec.presence_of_element_located((By.CSS_SELECTOR, '#LOCATION > div.TXBgG7JJ > span > img'))
    )
    html = driver2.page_source
    soup = BeautifulSoup(html, 'lxml')

    # retrieve hotel attributes
    name = soup.select_one('._1mTlpMC3').text
    hotel = Hotel(name)
    print(name)  # for debug
    stars = soup.select_one('._2aZlo29m')
    hotel.stars = None if stars is None else float(stars.get('title')[:3].replace(',', '.'))
    score = soup.select_one('._3cjYfwwQ')
    hotel.score = None if score is None else float(score.text.replace(',', '.'))
    ranking_in_city = soup.select_one('.rank')
    hotel.ranking_in_city = None if ranking_in_city is None else int(ranking_in_city.text[4:].replace('.', ''))
    about = soup.select_one('._2t2gK1hs > div')
    rooms = get_about_info(about, 'número de habitaciones')
    hotel.rooms = None if rooms is None else BeautifulSoup(rooms, 'lxml').text
    price_range = get_about_info(about, 'rango de precios')
    hotel.price_range = None if price_range is None else BeautifulSoup(price_range, 'lxml').text.split('(')[0].strip()
    # price = soup.select_one('.offers > div:nth-child(1) > div > div:nth-child(2) > div > div')
    # hotel.price = price.text if price is not None else None
    hotel.price = None

    # opinions
    num_opinions = soup.select_one('._1aRY8Wbl')
    hotel.num_opinions = None if num_opinions is None else int(num_opinions.text.replace('.', ''))
    num_opinions_excellent = soup.select_one('._2lcHrbTn > li:nth-child(1) ._3fVK8yi6')
    hotel.num_opinions_excellent = None if num_opinions_excellent is None else int(num_opinions_excellent.text
                                                                                   .replace('.', ''))

    num_opinions_good = soup.select_one('._2lcHrbTn > li:nth-child(2) ._3fVK8yi6')
    hotel.num_opinions_good = None if num_opinions_good is None else int(num_opinions_good.text.replace('.', ''))
    num_opinions_normal = soup.select_one('._2lcHrbTn > li:nth-child(3) ._3fVK8yi6')
    hotel.num_opinions_normal = None if num_opinions_normal is None else int(num_opinions_normal.text.replace('.', ''))
    num_opinions_bad = soup.select_one('._2lcHrbTn > li:nth-child(4) ._3fVK8yi6')
    hotel.num_opinions_bad = None if num_opinions_bad is None else int(num_opinions_bad.text.replace('.', ''))
    num_opinions_awful = soup.select_one('._2lcHrbTn > li:nth-child(5) ._3fVK8yi6')
    hotel.num_opinions_awful = None if num_opinions_awful is None else int(num_opinions_awful.text.replace('.', ''))
    num_qa = soup.select('._1aRY8Wbl')
    hotel.num_qa = None if len(num_qa) == 0 else int(num_qa[1].text.replace('.', ''))

    # nearby
    nearby = soup.select('.oPMurIUj')
    hotel.nearby_restaurants = None if len(nearby) == 0 else int(nearby[1].text.replace('.', ''))
    hotel.nearby_attractions = None if len(nearby) == 0 else int(nearby[2].text.replace('.', ''))

    # location
    maps_url = soup.select_one('#LOCATION > div.TXBgG7JJ > span > img').get('src')
    [hotel.latitude, hotel.longitude] = get_coords_from_google_maps(maps_url)
    zone = get_about_info(about, 'ubicación')
    zone = None if zone is None else BeautifulSoup(re.sub(r'<span.*</span>', '>', zone), 'lxml')
    hotel.zone = None if zone is None else zone.text.split('>')[-1]

    # services
    services = soup.select('._1nAmDotd')
    property_services = None if len(services) == 0 else services[0]
    room_services = None if len(services) <= 1 else services[1]
    hotel.swimming_pool = hotel_has_service(property_services, 'piscina')
    hotel.bar = hotel_has_service(property_services, 'bar')
    hotel.restaurant = hotel_has_service(property_services, 'restaurant')
    hotel.breakfast = hotel_has_service(property_services, 'desayuno')
    hotel.gym = hotel_has_service(property_services, 'gimnasio')
    hotel.admits_pets = hotel_has_service(property_services, 'mascota')
    hotel.air_conditioning = hotel_has_service(room_services, 'aire')
    hotel.date = datetime.today()
    return hotel


def scrape():
    url = URL
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    total_pages = int(soup.select('.pageNumbers a')[-1].get('data-page-number'))
    # total_pages = 1  # for debug

    hotels = []
    # iterate over all pages
    for i in range(total_pages):
        print('\n*********** Page', i+1, '/', total_pages, '***********')
        hotel_divs = soup.select('.ppr_priv_hsx_hotel_list_lite .photo-wrapper > a')
        hotel_urls = list({a.get('href') for a in hotel_divs})  # use a set since sponsored hotels can be duplicated
        # iterate over all hotels in a page
        for url in hotel_urls:
            hotel = scrape_hotel(url)
            hotels.append(hotel)

        # navigate to next page
        button = driver.find_element_by_class_name("next")
        button.click()

        # wait until hotel list refreshes
        WebDriverWait(driver, 60).until(wait_for_style_property((By.ID, 'taplc_hotels_loading_box_0')))
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')

    return hotels
