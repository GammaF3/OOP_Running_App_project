from flask import Flask, request
import datetime


def main():
    # Instance of the Flask application
    RUN = Flask(__name__)
    # Switches
    switch1 = True

    @RUN.route('/abc', methods=['POST'])
    def receive_data():
        if request.method == 'POST':
            try:
                data = request.json
                print("Received data:", data)
                print(type(data))
                print(data.get('lat'))
                print(data.get('lon'))

                # Save latitude and longitude to Coordinates.txt
                with open("Coordinates.txt", "a") as file:
                    file.write(f"Latitude: {data.get('lat')}, Longitude: {data.get('lon')}\n")

                # Save current hours and minutes to Entry_times.txt
                current_time = datetime.datetime.now()
                hours = current_time.hour
                minutes = current_time.minute
                with open("Entry_times.txt", "a") as file:
                    file.write(f"Entry time: {hours}:{minutes}\n")

                return data
            except Exception as e:
                print("Failed to parse JSON:", e)
                return "Failed to parse JSON", 405
        else:
            return "Method not allowed", 404

    RUN.run(host='0.0.0.0', port=5000)

    def get_time_():
        # Get the current time
        current_time = datetime.datetime.now()
        # Extract hours and minutes
        hours = current_time.hour
        minutes = current_time.minute

        return hours, minutes


if __name__ == "__main__":
    main()
