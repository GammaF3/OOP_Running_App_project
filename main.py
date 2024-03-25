from flask import Flask, request
import math


class Run:
    #
    #   class Run: stores data about runs a user makes
    #   self.data_list: In order to accurately track data, we need to sample the coordinates from the runner
    #   multiple times during their run. data_list is the list of data samples in the form of dictionaries
    #   throughout a runner's run. Each sample returns a dictionary.
    #   sample_interval: time between the data points are taken. I left it as a variable in case we want
    #   to change it later (could vary between 3 and 30 seconds. The app says cell phone battery is
    #   severely effected by extended use, so we might want to take that into account).
    #   TODO: Find a way to return total time for a run.
    #       For now, we can just use durations that are multiples of the sample_interval.
    #

    def __init__(self, sample_interval: int):
        self.coordinates_list = []
        self.sample_interval = sample_interval
        # Add more data as needed

    def add_coordinates(self, data: dict):
        self.coordinates_list.append(list((data['lat'], data['lon'])))

    def calculate_run_duration_sec(self):
        duration = len(self.coordinates_list) * self.sample_interval
        # duration += time between last sample and stop time
        return duration

    def calculate_miles_between_samples(self):
        # Use distance equation to calculate mileage between each sample: a to b, b to c, etc.
        # Returns a list of miles between samples so that we can call this function to calculate MET
        # will need to see how the lat and lng data will be formatted, then use that formatting
        # because distance between degrees of longitude is shorter when closer to poles and
        # longer when close to the equator, needs trig
        # Longitude: 1 deg = 111.320*cos(latitude) km, or the coefficient for miles is 69.1712130439
        miles_between_samples = []
        for i in range(1, len(self.coordinates_list)):
            first_lat_float = (
                float(self.coordinates_list[i - 1][0])
            )
            second_lat_float = (
                float(self.coordinates_list[i][0])
            )
            first_lng_float = (
                float(self.coordinates_list[i - 1][1])
            )
            second_lng_float = (
                float(self.coordinates_list[i][1])
            )
            average_latitude_degrees = (first_lat_float + second_lat_float) / 2

            # in miles_between_samples, math.cos() uses radians, so need to convert degrees of latitude to radians.
            miles_between_two_samples = math.sqrt(69 * ((second_lat_float - first_lat_float) ** 2) +
                                                  ((69.1712130439 * math.cos(
                                                      math.radians(average_latitude_degrees))) * (
                                                               second_lng_float - first_lng_float) ** 2))
            miles_between_samples.append(miles_between_two_samples)
        return miles_between_samples

    def calculate_mph_between_samples(self):
        speeds_between_samples = []
        distances_mi = self.calculate_miles_between_samples()
        for distance in distances_mi:
            speeds_between_samples.append((distance / self.sample_interval) * (
                        36000 / self.sample_interval))  # 36000 converts miles per second to miles per hour
        return speeds_between_samples

    def average_speed_mph(self):  # throughout entire run
        list_of_mph = self.calculate_mph_between_samples()
        return sum(list_of_mph) / len(list_of_mph)

    def get_sample_interval(self):
        return self.sample_interval


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
    #   To calculate MET function, I took samples from this website https://exrx.net/Calculators/WalkRunMETs
    #   and graphed them on Desmos, created lines of best fit, then created the MET function.
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

    def set_first_name(self, first_name):
        self.first_name = first_name

    def set_last_name(self, last_name):
        self.last_name = last_name

    def set_weight_kg(self, weight_kg):
        self.weight_kg = weight_kg

    def calculate_calories_burned(self, __Run: Run):
        # Functions obtained using lines of best fit in Desmos.
        # Change in functions is caused by a natural change in gait from walking to running.
        # #   calories burned in a run =
        # Run duration [minutes] * (MET value of run [determined by speed] * BMR * weight_kg) / 200
        list_of_METs = []
        list_of_mph = __Run.calculate_mph_between_samples()
        for speed in list_of_mph:
            if speed < 4.5:
                list_of_METs.append(1.47022 ** speed + -0.173639 * speed + 0.423387)
            else:
                list_of_METs.append(1.53223 * speed + 0.992667)
        calories_burned = 0
        for met in list_of_METs:
            calories_burned += __Run.get_sample_interval() * (met * self.bmr * self.get_weight_kg()) / 200
        return calories_burned


RUN = Flask(__name__)


@RUN.route('/abc', methods=['POST'])
def receive_data():
    if request.method == 'POST':
        try:
            data = request.json
            print("Received data:", data)
            print(type(data))
            return data
        except Exception as e:
            print("Failed to parse JSON:", e)
            return None
    else:
        print('Invalid request method')
        return None


RUN.run(host='0.0.0.0', port=5000)
