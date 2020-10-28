import pandas as pd


def hotels_to_csv(hotels):
    data = {
        'name': [hotel.name for hotel in hotels],
        'stars': [hotel.stars for hotel in hotels],
        'score': [hotel.score for hotel in hotels],
        'ranking': [hotel.ranking_in_city for hotel in hotels],
        'price': [hotel.price for hotel in hotels],
        'price_range': [hotel.price_range for hotel in hotels],
        'opinions': [hotel.num_opinions for hotel in hotels],
        'opinions_excellent': [hotel.num_opinions_excellent for hotel in hotels],
        'opinions_good': [hotel.num_opinions_good for hotel in hotels],
        'opinions_normal': [hotel.num_opinions_normal for hotel in hotels],
        'opinions_bad': [hotel.num_opinions_bad for hotel in hotels],
        'opinions_awful': [hotel.num_opinions_awful for hotel in hotels],
        'num_qa': [hotel.num_qa for hotel in hotels],
        'nearby_restaurants': [hotel.nearby_restaurants for hotel in hotels],
        'nearby_attractions': [hotel.nearby_attractions for hotel in hotels],
        'zone': [hotel.zone for hotel in hotels],
        'latitude': [hotel.latitude for hotel in hotels],
        'longitude': [hotel.longitude for hotel in hotels],
        'has_swimming_pool': [hotel.swimming_pool for hotel in hotels],
        'has_bar': [hotel.bar for hotel in hotels],
        'has_restaurant': [hotel.restaurant for hotel in hotels],
        'has_breakfast': [hotel.breakfast for hotel in hotels],
        'has_gym': [hotel.gym for hotel in hotels],
        'has_ac': [hotel.air_conditioning for hotel in hotels],
        'admits_pets': [hotel.admits_pets for hotel in hotels],
        'rooms': [hotel.rooms for hotel in hotels],
        'timestamp': [hotel.date for hotel in hotels],
    }
    columns = list(data.keys())
    df = pd.DataFrame(data, columns=columns)
    df.drop_duplicates(subset=["name", "latitude", "longitude"]).to_csv('../data/tripadvisor_barcelona_hotels.csv',
                                                                        index=False)
