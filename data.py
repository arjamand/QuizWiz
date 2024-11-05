import requests

parameters = {
    "amount": 10,
    "type": "boolean",
    "catagory": 17,
    "difficulty" : "easy",
}

questions_requests = requests.get(url="https://opentdb.com/api.php", params=parameters)
questions_requests.raise_for_status()
question_data = questions_requests.json()["results"]
questions_requests.close()
