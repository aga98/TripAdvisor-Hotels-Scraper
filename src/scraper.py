from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver import ActionChains
import urllib.parse as urlparse
from urllib.parse import parse_qs
from datetime import datetime
from hotel import Hotel
import re


URL = "https://www.tripadvisor.es/Hotels-g187497-Barcelona_Catalonia-Hotels.html"
BASE_URL = "https://www.tripadvisor.es"

choose_driver = True  # If True, it will get driver from specified path. If False, it will look in PATH.
# Specify driver location. Download compatible version for your system from https://chromedriver.chromium.org/downloads
diver_path = '../drivers/windows/chromedriver.exe'

# configure selenium driver. We we use Chrome as driver
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')

if choose_driver:
    driver = webdriver.Chrome(diver_path, options=options)
    driver2 = webdriver.Chrome(diver_path, options=options)
else:
    driver = webdriver.Chrome(options=options)
    driver2 = webdriver.Chrome(options=options)


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
    if url is None:
        return [None, None]
    else:
        parsed = urlparse.urlparse(url)
        coords = parse_qs(parsed.query)['center'][0].split(',')
        return [float(coords[0]), float(coords[1])]


# checks if the hotel has a service or not
def hotel_has_service(services_div, service):
    if services_div is not None:
        services = services_div.next_sibling
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


# translates 5 bubbles score (ooooo) into a valid score (1-5)
def bubbles_2_score(bubbles_span):
    classes = bubbles_span.get('class')
    score = None
    for cls in classes:
        if cls.startswith('bubble'):
            score = int(cls.split('_')[1]) / 10.0
    return score


# gets current price per night. If multiple prices from different providers returns the cheapest
def get_price(offers):
    price_offers = []  # stores prices from different serivces: Expedia, Booking...
    for offer in offers:
        # clean and avoid confusion with old prices
        pos = re.search(r'[a-zA-Z]', offer.text)
        pos = len(offer.text) if pos is None else pos.start()
        prices = offer.text[:pos].replace('€', '').replace('.', '').strip().split()
        price = min([int(price) for price in prices])  # get price after sale
        price_offers.append(price)
    if len(price_offers) == 0:
        return None
    else:
        return min(price_offers)


# scrapes hotel url
def scrape_hotel(url):
    url = BASE_URL + url
    driver2.get(url)
    try:
        # wait until map is loaded in order to get coordinates
        WebDriverWait(driver2, 120).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, '#LOCATION > div.TXBgG7JJ > span > img'))
        )
    except TimeoutException:
        print('WARNING: Timeout Exception. Map coordinades will not be available.')
    html = driver2.page_source
    soup = BeautifulSoup(html, 'lxml')

    # ****** retrieve hotel attributes ******
    name = soup.select_one('._1mTlpMC3')
    name = None if name is None else name.text
    hotel = Hotel(name)
    print(name)  # for debug

    # stars and scores
    stars = soup.select_one('._2aZlo29m')
    hotel.stars = None if stars is None else float(stars.get('title')[:3].replace(',', '.'))
    score = soup.select_one('._3cjYfwwQ')
    hotel.score = None if score is None else float(score.text.replace(',', '.'))
    score_location = soup.find('div', attrs={'class': '_1h7NKZWM'}, text='Ubicación')
    hotel.score_location = None if score_location is None else bubbles_2_score(score_location.previous_sibling)
    score_cleaning = soup.find('div', attrs={'class': '_1h7NKZWM'}, text='Limpieza')
    hotel.score_cleaning = None if score_cleaning is None else bubbles_2_score(score_cleaning.previous_sibling)
    score_service = soup.find('div', attrs={'class': '_1h7NKZWM'}, text='Servicio')
    hotel.score_service = None if score_service is None else bubbles_2_score(score_service.previous_sibling)
    score_value_money = soup.find('div', attrs={'class': '_1h7NKZWM'}, text='Relación calidad-precio')
    hotel.score_value_money = None if score_value_money is None else bubbles_2_score(score_value_money.previous_sibling)
    ranking_in_city = soup.select_one('.rank')
    hotel.ranking_in_city = None if ranking_in_city is None else int(ranking_in_city.text[4:].replace('.', ''))

    # prices and more info
    prices = soup.select('.bookableOffer')
    hotel.price = get_price(prices)
    rooms = soup.find('div', attrs={'class': '_39sLqIkw'}, text='NÚMERO DE HABITACIONES')
    hotel.rooms = None if rooms is None else int(rooms.next_sibling.text)
    price_range = soup.find('div', attrs={'class': '_39sLqIkw'}, text='RANGO DE PRECIOS')
    hotel.price_range = None if price_range is None else price_range.next_sibling.text.split('(')[0].strip()
    style = soup.find('div', attrs={'class': '_2jJmIDsg'}, text='ESTILO DEL HOTEL')
    hotel.style = None if style is None else style.next_sibling.text

    # languages
    languages = soup.find('div', attrs={'class': '_2jJmIDsg'}, text='Idiomas que se hablan')
    langs_in_parent = False if languages is None else languages.parent.has_attr('data-ssrev-handlers')
    all_langages = '' if languages is None or not langs_in_parent else str(languages.parent.get('data-ssrev-handlers'))

    # spoken_languages = None if languages is None else languages.next_sibling.text
    # if 'más' in spoken_languages:
    #     menu = driver2.find_element_by_css_selector("._3l0ZMuFy")
    #     ActionChains(driver2).move_to_element_with_offset(menu, 5, 5).perform()
    #     tooltip = WebDriverWait(driver2, 10).until(
    #         ec.presence_of_element_located((By.CSS_SELECTOR, '._1QF7P5TQ')))  # NO LE GUSTA....
    #     print('tooltip', tooltip.get_attribute('innerHTML'))

    hotel.language_spanish = 'Español' in all_langages
    hotel.language_catalan = 'Catalán' in all_langages
    hotel.language_french = 'Francés' in all_langages
    hotel.language_english = 'Inglés' in all_langages
    hotel.language_italian = 'Italiano' in all_langages

    prat = soup.find('span', attrs={'class': '_1oeag8Dn'}, text='Aeropuerto de Barcelona-El Prat')
    hotel.prat_distance = None if prat is None else prat.next_sibling.find('span', attrs={'class', 'number'}).text

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
    maps_url = soup.select_one('#LOCATION > div.TXBgG7JJ > span > img')
    maps_url = None if maps_url is None else maps_url.get('src')
    [hotel.latitude, hotel.longitude] = get_coords_from_google_maps(maps_url)
    zone = soup.find('div', attrs={'class': '_39sLqIkw'}, text='UBICACIÓN')
    zone = None if zone is None else BeautifulSoup(re.sub(r'<span.*</span>', '>', str(zone.next_sibling)), 'lxml')
    hotel.zone = None if zone is None else zone.text.split('>')[-1]

    # services
    property_services = soup.find('div', attrs={'class': '_1mJdgpMJ'}, text='Servicios de la propiedad')
    room_services = soup.find('div', attrs={'class': '_1mJdgpMJ'}, text='Servicios de habitación')
    room_types = soup.find('div', attrs={'class': '_1mJdgpMJ'}, text='Tipos de habitación')
    hotel.swimming_pool = hotel_has_service(property_services, 'piscina')
    hotel.bar = hotel_has_service(property_services, 'bar')
    hotel.restaurant = hotel_has_service(property_services, 'restaurant')
    hotel.breakfast = hotel_has_service(property_services, 'desayuno')
    hotel.gym = hotel_has_service(property_services, 'gimnasio')
    hotel.admits_pets = hotel_has_service(property_services, 'mascota')
    hotel.reception_24h = hotel_has_service(property_services, 'recepción 24 horas')
    hotel.air_conditioning = hotel_has_service(room_services, 'aire')
    hotel.strongbox = hotel_has_service(room_services, 'caja fuerte')
    hotel.suites = hotel_has_service(room_types, 'Suites')
    hotel.sea_views_rooms = hotel_has_service(room_types, 'Vistas al mar')
    hotel.non_smoking_rooms = hotel_has_service(room_types, 'Habitaciones de no fumadores')
    hotel.landmarks_views_rooms = hotel_has_service(room_types, 'Vistas a sitios de interés turístico')
    hotel.city_views_rooms = hotel_has_service(room_types, 'Vistas a la ciudad')
    hotel.family_rooms = hotel_has_service(room_types, 'Habitaciones para familias')

    hotel.date = datetime.today()
    return hotel


def scrape():
    url = URL
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    total_pages = int(soup.select('.pageNumbers a')[-1].get('data-page-number'))
    # total_pages = 10  # for debug

    hotels = []
    # iterate over all pages
    for i in range(total_pages):
        print('\n*********** Page', i+1, '/', total_pages, '***********')
        hotel_divs = soup.select('.ppr_priv_hsx_hotel_list_lite .photo-wrapper > a')
        hotel_urls = list({a.get('href') for a in hotel_divs})  # use a set since sponsored hotels can be duplicated
        # iterate over all hotels in a page
        for hotel_url in hotel_urls:
            hotel = scrape_hotel(hotel_url)
            hotels.append(hotel)

        # ### navigate to next page ###
        next_page = soup.select_one(".next")
        # ensure we are not in last page
        if next_page.has_attr('href'):
            url = BASE_URL + next_page.get('href')
            driver.get(url)
            # wait until hotel list refreshes
            WebDriverWait(driver, 60).until(wait_for_style_property((By.ID, 'taplc_hotels_loading_box_0')))
            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')

    return hotels
