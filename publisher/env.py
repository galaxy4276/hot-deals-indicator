import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname((os.path.abspath(__file__)))

print(BASE_DIR)

load_dotenv(os.path.join(BASE_DIR, ".env"))

env = {
    "CLIENT_ID": os.environ["CLIENT_ID"],
    "REDIRECT_URI": os.environ["REDIRECT_URI"],
    "KAKAO_ID": os.environ["KAKAO_ID"],
    "KAKAO_PASSWORD": os.environ["KAKAO_PASSWORD"],
    "ELASTIC_ID": os.environ["ELASTIC_ID"],
    "ELASTIC_PASSWORD": os.environ["ELASTIC_PASSWORD"],
    "ELASTIC_HOST": os.environ["ELASTIC_HOST"],
    "KIBANA_HOST": os.environ["KIBANA_HOST"],
}
