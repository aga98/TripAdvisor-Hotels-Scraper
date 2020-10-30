class Hotel:
    def __init__(self, name):
        self.reception_24h = None
        self.strongbox = None
        self.suites = None
        self.sea_views_rooms = None
        self.non_smoking_rooms = None
        self.landmarks_views_rooms = None
        self.city_views_rooms = None
        self.family_rooms = None
        self.style = None
        self.score_location = None
        self.score_cleaning = None
        self.score_service = None
        self.score_value_money = None
        self.price = None
        self.price_range = None
        self.rooms = None
        self.zone = None
        self.swimming_pool = None
        self.longitude = None
        self.bar = None
        self.latitude = None
        self.restaurant = None
        self.gym = None
        self.breakfast = None
        self.admits_pets = None
        self.air_conditioning = None
        self.date = None
        self.nearby_attractions = None
        self.nearby_restaurants = None
        self.num_qa = None
        self.num_opinions_awful = None
        self.num_opinions_bad = None
        self.num_opinions_good = None
        self.num_opinions_excellent = None
        self.num_opinions = None
        self.ranking_in_city = None
        self.score = None
        self.num_opinions_normal = None
        self.stars = None
        self.name = name

    def __str__(self):
        s = ("------------------------------------------------------------\n"
             + 'Name: ' + self.name + '\n'
             + 'Stars: ' + str(self.stars) + '\n'
             + 'Score: ' + str(self.score) + '\n'
             + 'Score Location: ' + str(self.score_location) + '\n'
             + 'Score Cleaning: ' + str(self.score_cleaning) + '\n'
             + 'Score Service: ' + str(self.score_service) + '\n'
             + 'Score Value for Money: ' + str(self.score_value_money) + '\n'
             + 'Ranking_in_city: ' + str(self.ranking_in_city) + '\n'
             + 'Price: ' + str(self.price) + '\n'
             + 'Price Range: ' + str(self.price_range) + '\n'
             + 'Num. Opinions: ' + str(self.num_opinions) + '\n'
             + 'Num. Opinions Excellent: ' + str(self.num_opinions_excellent) + '\n'
             + 'Num. Opinions Good: ' + str(self.num_opinions_good) + '\n'
             + 'Num. Opinions Normal: ' + str(self.num_opinions_normal) + '\n'
             + 'Num. Opinions Bad: ' + str(self.num_opinions_bad) + '\n'
             + 'Num. Opinions Awful: ' + str(self.num_opinions_awful) + '\n'
             + 'Num. QA: ' + str(self.num_qa) + '\n'
             + 'Nearby Restaurants: ' + str(self.nearby_restaurants) + '\n'
             + 'Nearby Attractions: ' + str(self.nearby_attractions) + '\n'
             + 'Zone: ' + str(self.zone) + '\n'
             + 'Latitude: ' + str(self.latitude) + '\n'
             + 'Longitude: ' + str(self.longitude) + '\n'
             + 'Swimming_pool: ' + str(self.swimming_pool) + '\n'
             + 'Bar: ' + str(self.bar) + '\n'
             + 'Restaurant: ' + str(self.restaurant) + '\n'
             + 'Breakfast: ' + str(self.breakfast) + '\n'
             + 'Gym: ' + str(self.gym) + '\n'
             + 'Admits_pets: ' + str(self.admits_pets) + '\n'
             + 'Reception 24h: ' + str(self.reception_24h) + '\n'
             + 'Strong box: ' + str(self.strongbox) + '\n'
             + 'Air_conditioning: ' + str(self.air_conditioning) + '\n'
             + 'Rooms: ' + str(self.rooms) + '\n'
             + 'Suites: ' + str(self.suites) + '\n'
             + 'Sea View rooms: ' + str(self.sea_views_rooms) + '\n'
             + 'Non-smoking rooms: ' + str(self.non_smoking_rooms) + '\n'
             + 'Landmark View rooms: ' + str(self.landmarks_views_rooms) + '\n'
             + 'City View rooms: ' + str(self.city_views_rooms) + '\n'
             + 'Family rooms: ' + str(self.family_rooms) + '\n'
             + 'Style: ' + str(self.style) + '\n'
             + 'Date: ' + str(self.date) + '\n'
             + "------------------------------------------------------------\n")
        return s
