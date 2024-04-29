import math


def vincenty_formula(lat1, lon1, lat2, lon2):
    # calculate dist traveled on surface of ellipsoid
    # for use with calculate_miles_between_samples
    # uses WGS-84 standard
    # from wikipedia: https://en.wikipedia.org/wiki/Vincenty%27s_formulae
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)
    a = 6378137.0
    f = 1/298.257223563
    b = (1 - f) * a
    U_1 = math.atan((1 - f) * math.tan(lat1))
    U_2 = math.atan((1 - f) * math.tan(lat2))
    L = abs(lon2 - lon1)
    lambda_previous = 0
    _lambda = L
    iterations = 0
    while _lambda - lambda_previous > 10e-12 and iterations < 1000:
        sin_sigma = math.sqrt((math.cos(U_2) * math.sin(_lambda))**2 + (math.cos(U_1) * math.sin(U_2) - math.sin(U_1) * math.cos(U_2) * math.cos(_lambda))**2)
        cos_sigma = math.sin(U_1) * math.sin(U_2) + math.cos(U_1) * math.cos(U_2) * math.cos(_lambda)
        sigma = math.asin(sin_sigma)
        try:
            sin_alpha = (math.cos(U_1) * math.cos(U_2) * math.sin(_lambda)) / sin_sigma
        except ZeroDivisionError:
            return 0  # if sinSigma == 0 then the two points are identical (which should not happen when running)
        cos_alpha_squared = 1 - sin_alpha**2
        if cos_alpha_squared != 0:
            cos__2sigma_m = math.cos(sigma) - (2 * math.sin(U_1) * math.sin(U_2)) / cos_alpha_squared
        else:
            cos__2sigma_m = math.cos(sigma) - (2 * math.sin(U_1) * math.sin(U_2)) / 1 - sin_alpha**2
        C = (f/16) * cos_alpha_squared * (4 + f * (4 - 3 * cos_alpha_squared))
        lambda_previous = _lambda
        _lambda = L + (1 - C) * f * sin_alpha * (sigma + C * sin_sigma * (cos__2sigma_m + C * cos_sigma * (-1 + 2 * (cos__2sigma_m**2))))
        iterations += 1
    u_squared = cos_alpha_squared * ((a**2 - b**2) / b**2)
    A = 1 + (u_squared / 16384) * (4096 + u_squared * (-768 + u_squared * (320 - 175 * u_squared)))
    B = (u_squared / 1024) * (356 + u_squared * (-128 + u_squared * (74 - 47 * u_squared)))
    delta_sigma = B * sin_sigma * (cos__2sigma_m + .25 * B * (cos_sigma * (-1 + 2 * cos__2sigma_m**2) - (B/6) * cos__2sigma_m * (-3 + 4 * sin_sigma**2) * (-3 + 4 * cos__2sigma_m**2)))
    s = b * A * (sigma - delta_sigma)
    return s


class Goal:
    def __init__(self, description='Total <goal type>', goal_value=0, current_value=0):
        self.description = description
        self.goal_value = goal_value
        self.current_value = current_value

    def get_description(self):
        return self.description

    def get_goal_value(self):
        return self.goal_value

    def get_current_value(self):
        return self.current_value

    def __str__(self):
        return f'{self.description}: {self.current_value}/{self.goal_value}'

    def increment_current_value(self, amount):
        self.current_value += amount


class CalorieGoal(Goal):
    def __init__(self, goal_value_cal=0):
        super().__init__('Total calories burned (Cal)', goal_value_cal)


class KilometersGoal(Goal):
    def __init__(self, goal_value_km=0):
        super().__init__('Total kilometers run', goal_value_km)


class MilesGoal(Goal):
    def __init__(self, goal_value_mi=0):
        super().__init__('Total miles run', goal_value_mi)


class TimeGoal(Goal):
    def __init__(self, goal_value=0):
        super().__init__('Total running time', goal_value)
        self.current_value = {
            'days': 0,
            'hours': 0,
            'minutes': 0,
            'seconds': 0
        }
        self.goal_value = {
            'days': 0,
            'hours': 0,
            'minutes': 0,
            'seconds': 0
        }
        goal_value_sec = goal_value
        if goal_value_sec >= 86400:
            self.goal_value['days'] = goal_value_sec // 86400
            goal_value_sec = self.get_goal_value() % 86400
        if goal_value_sec >= 3600:
            self.goal_value['hours'] = goal_value_sec // 3600
            goal_value_sec = goal_value_sec % 3600
        if goal_value_sec >= 60:
            self.goal_value['minutes'] = goal_value_sec % 60
            goal_value_sec = goal_value_sec // 60
        self.goal_value['seconds'] = goal_value_sec

    def increment_current_value(self, amount):
        if amount >= 86400:
            self.current_value['days'] += amount // 86400
            amount = amount % 86400
        if amount >= 3600:
            self.current_value['hours'] = amount // 3600
            amount = amount % 3600
        if amount >= 60:
            self.current_value['minutes'] = amount % 60
            amount = amount // 60
        self.current_value['seconds'] = amount

    def get_goal_value_str(self):
        return f"{self.goal_value['days']}D {self.goal_value['hours']}H {self.goal_value['minutes']}M {self.goal_value['seconds']}S"

    def get_current_value_str(self):
        return f"{self.current_value['days']}D {self.current_value['hours']}H {self.current_value['minutes']}M {self.current_value['seconds']}S"

    def __str__(self):
        return f"{self.description}: {self.get_current_value_str()} / {self.get_goal_value_str()}"


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

    def __init__(self, coordinates_list: list[tuple[int, int]] = None, date_time: str = 'mm/dd/yyyy hh:mm:ss', seconds_elapsed: int = 4212, sample_interval=20):
        if coordinates_list is None:
            coordinates_list = [(0, 0)]
            self.distance_mi = 10
        else:
            self.distance_mi = sum(self.calculate_miles_between_samples())
        self.coordinates_list = coordinates_list[:]
        self.date_time = date_time
        self.seconds_elapsed = seconds_elapsed
        self.sample_interval = sample_interval

    def get_coordinates_list(self):
        return self.coordinates_list

    def add_coordinates(self, data: dict):
        self.coordinates_list.append((data['lat'], data['lon']))

    def calculate_miles_between_samples(self):  # returns a list of the distances between each sample; a to b, b to c, etc
        to_return = []
        for i in range(1, len(self.coordinates_list)):
            to_return.append(vincenty_formula(self.coordinates_list[i][0], self.coordinates_list[i][1], self.coordinates_list[i-1][0], self.coordinates_list[i-1][1]))
        return to_return

    def calculate_mph_between_samples(self):  # needed in addition to average_speed_mph to calculate calories burned
        speeds_between_samples = []
        if len(self.coordinates_list) <= 1:  # for default constructor
            distances_mi = [.0831212 for x in range(240)]  # comes out at about 8 min/mi
        else:
            distances_mi = self.calculate_miles_between_samples()
        for distance in distances_mi:
            speeds_between_samples.append((distance / self.sample_interval) * (36000 / self.sample_interval))  # 36000 converts miles per second to miles per hour
        return speeds_between_samples

    def average_speed_mph(self):  # throughout entire run
        list_of_mph = self.calculate_mph_between_samples()
        return sum(list_of_mph) / len(list_of_mph)

    def average_pace_mi(self):  # minutes / mile
        return 60 / self.average_speed_mph()

    def get_sample_interval(self):
        return self.sample_interval

    def get_date_time(self):
        return self.date_time

    def get_distance_mi(self):
        return self.distance_mi

    def get_seconds_elapsed(self):
        return self.seconds_elapsed

    def str_time_elapsed(self):
        seconds = self.seconds_elapsed
        to_return = ''
        unit_dict = {
            'years': 31536000,
            'months': 2628003,
            'weeks': 604800,
            'days': 86400,
            'hours': 3600,
            'minutes': 60,
            'seconds': 1
        }
        for unit in unit_dict:
            if seconds >= unit_dict[unit]:
                to_return += f'{seconds // unit_dict[unit]} {unit}'
                seconds = seconds % unit_dict[unit]
                if seconds != 0:
                    to_return += ', '
                else:
                    break
        return to_return


class Account:
    #
    #   class Account: manipulates and outputs data from a specific runner's account
    #   Used in outside functions that create and delete accounts
    #   Uses a list of Run objects as attributes
    #   phone number used in outside functions?
    #   weight_kg, height_cm, age, isMale: used to calculate calories via bmr
    #   formula to calculate calories found here: https://www.medicinenet.com/how_to_calculate_calories_burned_during_exercise/article.htm
    #   'Total calories burned in 1 second = (3.5 times the metabolic equivalent or MET multiplied by your body weight in kilograms)/12000.'
    #   calories burned in a run = Run duration [minutes] * (MET value of run [determined by speed] * BMR * weight_kg) / 200
    #   BMR [basal metabolic rate]:
    #   Men: BMR = 88.362 + (13.397 x weight in kg) + (4.799 x height in cm) – (5.677 x age in years)
    #   Women: BMR = 447.593 + (9.247 x weight in kg) + (3.098 x height in cm) – (4.330 x age in years)
    #   formula for bmr here: https://www.garnethealth.org/news/basal-metabolic-rate-calculator#:~:text=Your%20basal%20metabolism%20rate%20is,4.330%20x%20age%20in%20years)
    #   To calculate MET function, I took samples from this website https://exrx.net/Calculators/WalkRunMETs
    #   and graphed them on Desmos, created lines of best fit, then created the MET function.
    #
    #

    def __init__(self, username='username', password='12345', all_runs: list[Run] = None, all_goals: list[Goal] = None,
                 phone_number='0000000000', first_name='firstname', last_name='lastname', isMale=True, weight_kg=75, height_cm=180,
                 age=18, calorie_goals_completed=0, distance_goals_completed=0, time_goals_completed=0):
        if all_runs is None:
            all_runs = [Run(), Run(), Run(), Run(), Run(), Run(), Run(), Run(), Run(), Run(), Run(), Run()]
        if all_goals is None:
            all_goals = [CalorieGoal(), TimeGoal(), MilesGoal(), KilometersGoal()]
        self.username = username
        self.password = password
        self.all_runs = list(all_runs)  # List of type Run
        self.all_goals = list(all_goals)
        self.phone_number = phone_number  # Phone number of account holder,
        # required to track location to determine mileage
        self.first_name = first_name  # The first name of the account holder, displayed on front end
        self.last_name = last_name  # The last name of the account holder, displayed on front end
        self.isMale = isMale
        if isMale:
            bmr = 88.362 + (13.397 * weight_kg) + (4.799 * height_cm) - (5.677 * age)
        else:
            bmr = 447.593 + (9.247 * weight_kg) + (3.098 * height_cm) - (4.330 * age)
        self.bmr = bmr
        self.weight_kg = weight_kg
        self.height_cm = height_cm
        self.age = age
        self.runs_completed = len(all_runs)
        self.goals_completed = calorie_goals_completed + time_goals_completed + distance_goals_completed
        self.calorie_goals_completed = calorie_goals_completed
        self.time_goals_completed = time_goals_completed
        self.distance_goals_completed = distance_goals_completed
        self.total_dist_mi = sum([run.get_distance_mi() for run in all_runs])
        self.total_calories_burned = sum([self.calculate_calories_burned(run) for run in all_runs])
        self.total_time_running_sec = sum([run.get_seconds_elapsed() for run in all_runs])

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def get_all_runs(self):
        return self.all_runs

    def get_run(self, i):
        return self.all_runs[i]

    def get_all_goals(self):
        return self.all_goals

    def get_goal(self, i):
        return self.all_goals[i]

    def get_runs_completed(self):
        return self.runs_completed

    def get_goals_completed(self):
        return self.goals_completed

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

    def get_total_time_running_sec(self):
        return self.total_time_running_sec

    def str_total_time_running_sec(self):
        seconds = self.total_time_running_sec
        to_return = ''
        unit_dict = {
            'years': 31536000,
            'months': 2628003,
            'weeks': 604800,
            'days': 86400,
            'hours': 3600,
            'minutes': 60,
            'seconds': 1
        }
        for unit in unit_dict:
            if seconds >= unit_dict[unit]:
                to_return += f'{seconds // unit_dict[unit]} {unit}'
                seconds = seconds % unit_dict[unit]
                if seconds != 0:
                    to_return += ', '
                else:
                    break
        return to_return

    def get_distance_goals_completed(self):
        return self.distance_goals_completed

    def get_calorie_goals_completed(self):
        return self.calorie_goals_completed

    def get_time_goals_completed(self):
        return self.time_goals_completed

    def get_bmr(self):
        return self.bmr

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

    def pop_run(self, index=-1):
        self.all_runs.pop(index)

    def set_all_goals(self, list_Goal):
        self.all_goals = list(list_Goal)

    def append_goal(self, __Goal):
        self.all_goals.append(__Goal)

    def insert_goal(self, index, __Goal):
        self.all_goals.insert(index, __Goal)

    def pop_goal(self, index=-1):
        self.all_goals.pop(index)

    def set_first_name(self, first_name):
        self.first_name = first_name

    def set_last_name(self, last_name):
        self.last_name = last_name

    def set_weight_kg(self, weight_kg):
        self.weight_kg = weight_kg

    def __str__(self):
        return (f'{type(self)} at {id(self)}: {self.get_username()}, {self.get_password()}, {self.get_first_name()}, '
                f'{self.get_last_name()}, {self.get_weight_kg()}, {self.get_age()}, {self.get_all_runs()}, '
                f'{self.get_height_cm()}, {self.get_isMale()}, {self.get_phone_number()}, {self.get_total_calories_burned()}, '
                f'{self.get_total_dist_mi()}')

    def calculate_calories_burned(self, __Run: Run):
        # Functions obtained using lines of best fit in Desmos.
        # Change in functions is caused by a natural change in gait from walking to running.
        # #   calories burned in a run =
        # Run duration [minutes] * (MET value of run [determined by speed] * BMR * weight_kg) / 200
        # under 4.5: MET = 1.50766**speed - 0.173639speed + 0.423387
        list_of_METs = []
        list_of_mph = list(__Run.calculate_mph_between_samples())
        for speed in list_of_mph:
            if speed < 4.5:
                list_of_METs.append((1.50766 ** speed) - (0.173639 * speed) + 0.423387)
            else:
                list_of_METs.append(1.53223 * speed + 0.992667)
        calories_burned = 0
        for met in list_of_METs:
            calories_burned += __Run.get_sample_interval() * ((3.5 * met) * self.get_weight_kg() / 12000)
        return calories_burned


if __name__ == "__main__":
    pass