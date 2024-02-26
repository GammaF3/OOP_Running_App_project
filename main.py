from flask import Flask, request

RUN = Flask(__name__)

@RUN.route('/abc', methods=['POST'])
def receive_data():
    if request.method == 'POST':
        try:
            data = request.json
            print("Received data:", data)
            print(type(data))
            return "Data received successfully!"
        except Exception as e:
            print("Failed to parse JSON:", e)
            return "Failed to parse JSON"
    else:
        return "Invalid request method"

RUN.run(host='0.0.0.0', port=5000)
