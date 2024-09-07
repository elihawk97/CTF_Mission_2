import requests

def send_request():
    url = 'http://localhost:8080'
    # Hidden data to send in the request
    hidden_data = "secret_key=StrongerTogether"
    headers = {'Content-Type': 'application/encrypted.code.hamas.aza'}

    # Send a POST request with hidden data
    response = requests.post(url, data=hidden_data, headers=headers)

    print("Server response:", response.text)

if __name__ == "__main__":
    send_request()
