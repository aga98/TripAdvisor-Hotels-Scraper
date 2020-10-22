class Hotel:
    def __init__(self, name):
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
        s = ('Name: ' + self.name + '\n'
             + 'stars: ' + str(self.stars) + '\n'
             + 'score: ' + str(self.score) + '\n'
             + 'ranking_in_city: ' + str(self.ranking_in_city) + '\n'
             + 'num_opinions: ' + str(self.num_opinions) + '\n'
             + 'num_opinions_excellent: ' + str(self.num_opinions_excellent) + '\n'
             + 'num_opinions_good: ' + str(self.num_opinions_good) + '\n'
             + 'num_opinions_normal: ' + str(self.num_opinions_normal) + '\n'
             + 'num_opinions_bad: ' + str(self.num_opinions_bad) + '\n'
             + 'num_opinions_awful: ' + str(self.num_opinions_awful) + '\n'
             + 'num_qa: ' + str(self.num_qa) + '\n'
             + 'nearby_restaurants: ' + str(self.nearby_restaurants) + '\n'
             + 'nearby_attractions: ' + str(self.nearby_attractions) + '\n'
             + 'latitude: ' + str(self.latitude) + '\n'
             + 'longitude: ' + str(self.longitude) + '\n'
             + 'swimming_pool: ' + str(self.swimming_pool) + '\n'
             + 'bar: ' + str(self.bar) + '\n'
             + 'restaurant: ' + str(self.restaurant) + '\n'
             + 'breakfast: ' + str(self.breakfast) + '\n'
             + 'gym: ' + str(self.gym) + '\n'
             + 'admits_pets: ' + str(self.admits_pets) + '\n'
             + 'air_conditioning: ' + str(self.air_conditioning) + '\n'
             + 'date: ' + str(self.date) + '\n')
        return s
