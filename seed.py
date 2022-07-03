from app import app
from models import db, Villager
import requests
import json

db.drop_all()
db.create_all()

BASE_URL = 'http://acnhapi.com/v1/villagers'

# TODO: Replace range to range(1, 391)
for idx in range(1, 5):
    resp = requests.get(f"{BASE_URL}/{idx}")
    data = json.loads(resp.text)
    name = data["name"]["name-USen"]
    image_url = data["image_uri"]

    new_villager = Villager(name = name, image_url = image_url)

    db.session.add(new_villager)

db.session.commit()