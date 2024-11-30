from elasticsearch import Elasticsearch
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
 # 시각화 구현중
es = Elasticsearch(["http://han-box.co.kr:9200"], basic_auth=())

res = es.search(index="hot_deals", body={"query": {"match_all": {}}}, size=100)
data = [{"_id": doc["_id"], **doc["_source"]} for doc in res['hits']['hits']]

df = pd.DataFrame(data)

