import requests
"""
dEYphETfy9UKERzDAgZQmgj8R3hjIgqbMLCQKJ7l
Example: https://api.nasa.gov/planetary/apod?api_key=dEYphETfy9UKERzDAgZQmgj8R3hjIgqbMLCQKJ7l

"""

# r = requests.get('https://api.nasa.gov/neo/rest/v1/neo/browse?api_key=dEYphETfy9UKERzDAgZQmgj8R3hjIgqbMLCQKJ7l')
# print(r.text)

r = requests.put('http://192.168.2.32:8080/api/delivery/boxes/close', json={"box_id": "61eedccb818c905a54c21289", "box_state":"closed"})
print(r.text)
