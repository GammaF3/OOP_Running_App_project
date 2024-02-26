import math


class Account:
    #
    #   class Account: manipulates and outputs data from a specific runner's account
    #   Used in outside functions that create and delete accounts
    #   Uses a list of Run objects as attributes
    #   phone number used in outside functions?
    #   weight_kg, height_cm, age, isMale: used to calculate calories via bmr
    #   formula to calculate calories found here: https://www.medicinenet.com/how_to_calculate_calories_burned_during_exercise/article.htm
    #   calories burned in a run = Run duration [minutes] * (MET value of run [determined by speed] * BMR * weight_kg) / 200
    #   BMR [basal metabolic rate]:
    #   Men: BMR = 88.362 + (13.397 x weight in kg) + (4.799 x height in cm) – (5.677 x age in years)
    #   Women: BMR = 447.593 + (9.247 x weight in kg) + (3.098 x height in cm) – (4.330 x age in years)
    #   formula for bmr here: https://www.garnethealth.org/news/basal-metabolic-rate-calculator#:~:text=Your%20basal%20metabolism%20rate%20is,4.330%20x%20age%20in%20years)
    #

    def __init__(self, username, password, all_runs, phone_number, first_name, last_name, isMale, weight_kg, height_cm,
                 age, total_dist_mi, total_calories_burned):
        self.username = username
        self.password = password
        self.all_runs = list(all_runs)  # List of type Run
        self.phone_number = phone_number  # Phone number of account holder,
        # required to track location to determine mileage
        self.first_name = first_name  # The first name of the account holder, displayed on front end
        self.last_name = last_name  # The last name of the account holder, displayed on front end
        self.isMale = isMale
        self.weight_kg = weight_kg
        self.height_cm = height_cm
        self.age = age
        if isMale:
            self.bmr = 88.362 + (13.397 * self.weight_kg) + (4.799 * self.height_cm) - (5.677 * age)
        else:
            self.bmr = 447.593 + (9.247 * weight_kg) + (3.098 * height_cm) - (4.330 * age)
        self.total_dist_mi = total_dist_mi
        self.total_calories_burned = total_calories_burned

    @staticmethod
    def null_account():
        null = Account('', '', [], '', '', '', False, 0.0, 0.0, 0, 0.0, 0)
        return null

    @staticmethod
    def new_account(username, password, phone_number, first_name, last_name, isMale, weight_kg, height_cm,
                    age):  # used when making new account
        new = Account(username=username, password=password, all_runs=list(), phone_number=phone_number,
                      first_name=first_name, last_name=last_name, isMale=isMale, weight_kg=weight_kg,
                      height_cm=height_cm, age=age, total_dist_mi=0.0, total_calories_burned=0.0)
        return new

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def get_all_runs(self):
        return self.all_runs

    def get_run(self, i):
        return self.all_runs[i]

    def get_phone_number(self):
        return self.phone_number

    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name

    def get_isMale(self):
        return self.isMale

    def get_weight_kg(self):
        return self.weight_kg

    def get_weight_lbs(self):
        return self.weight_kg * 2.20462262

    def get_height_cm(self):
        return self.height_cm

    def get_height_inch(self):
        return self.height_cm * 0.393701

    def get_age(self):
        return self.age

    def get_total_dist_mi(self):
        return self.total_dist_mi

    def get_total_calories_burned(self):
        return self.total_calories_burned

    def set_username(self, string):
        self.username = string

    def set_password(self, string):
        self.password = string

    def set_all_runs(self, list_Run):  # list_Run: list of type Run
        self.all_runs = list(list_Run)

    def append_run(self, __Run):  # __Run: Run object
        self.all_runs.append(__Run)

    def insert_run(self, index, __Run):
        self.all_runs.insert(index, __Run)

    def pop_run(self, index):
        self.all_runs.pop(index)

    def set_first_name(self, string):
        self.first_name = string

    def set_last_name(self, string):
        self.last_name = string


class Run:
    #
    #   class Run: stores data about runs a user makes
    #   Uses phone_number from Account
    #   self.coordinates_list: In order to accurately track data, we need to sample the coordinates from the runner
    #   multiple times during their run. coordinates_list is a list of two-element tuples which each contain a latitude
    #   and longitude string respectively.
    #
    #   Because it uses strings, coordinate_list is a 3D array:
    #   self.coordinates_list[sample][0 for lat, 1 for lng][str]
    #
    def __init__(self, coordinates_list, distance_mi, duration_sec):
        self.coordinates_list = list(coordinates_list)
        self.dist_mi = distance_mi
        self.duration_sec = duration_sec

    def get_coordinates_list(self):
        return self.coordinates_list

    def get_coordinates(self, i):
        return self.coordinates_list[i]

    def set_coordinates_list(self, listof_tupleof_string):
        self.coordinates_list = listof_tupleof_string

    def append_coordinates(self, __tuple):
        self.coordinates_list.append(__tuple)

    def calculate_miles(self):
        # Use distance equation to calculate mileage between each sample: a to b, b to c, etc., then add them all up
        # will need to see how the lat and lng data will be formatted, then use that formatting
        # because distance between degrees of longitude is shorter when closer to poles and
        # longer when close to the equator, needs trig
        # Longitude: 1 deg = 111.320*cos(latitude) km, or the coefficient for miles is 69.1712130439
        total_dist_mi = 0
        for i in range(1, len(self.coordinates_list)):
            first_lat_float = float(
                self.coordinates_list[i - 1][0]['''slice string for compatible casting here''']
            )
            second_lat_float = float(
                self.coordinates_list[i][0]['''slice string for compatible casting here''']
            )
            first_lng_float = float(
                self.coordinates_list[i - 1][1]['''slice string for compatible casting here''']
            )
            second_lng_float = float(
                self.coordinates_list[i][1]['''slice string for compatible casting here''']
            )
            average_longitude_degrees = (first_lng_float + second_lng_float) / 2

            # in miles_between_samples, math.cos() uses radians, so need to convert degrees of latitude to radians.
            miles_between_samples = math.sqrt(69 * ((second_lat_float - first_lat_float) ** 2) +
                                              ((69.1712130439 * math.cos(math.radians(average_longitude_degrees))) * (second_lng_float - first_lng_float) ** 2))
            total_dist_mi += miles_between_samples
