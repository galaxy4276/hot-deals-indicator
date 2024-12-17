from typing import Union

from fastapi import FastAPI
from elasticsearch import Elasticsearch
from env import env

app = FastAPI()
es = Elasticsearch(
    ["http://han-box.co.kr:9200"],
    basic_auth=(env["ELASTIC_ID"], env["ELASTIC_PASSWORD"])
)


@app.get("/")
def read_root():
    return 'Elastic Search with FastAPI'

# ID 검색은 수정 필요
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
        # Elasticsearch 쿼리 구성
    query = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"_id": item_id}}
                ]
            }
        }
    }
    
    # q 매개변수가 제공된 경우, 이름과 링크 필드에서 검색
    if q:
        query["query"]["bool"]["must"].append({
            "multi_match": {
                "query": q,
                "fields": ["name", "link"]
            }
        })
    
    # 쿼리 실행
    result = es.search(index="hot_deals", body=query)
    
    # Elasticsearch 응답에서 관련 데이터 추출
    hits = result['hits']['hits']
    if hits:
        item = hits[0]['_source']
        return {
            "id": item.get('id'),
            "name": item.get('name'),
            "link": item.get('link'),
            "price": item.get('price'),
            "dateCreated": item.get('dateCreated')
        }
    else:
        return {"error": "아이템을 찾을 수 없습니다"}
    
# '단어'가 포함된 items 긁어오는 부분
@app.get("/search")
def search_items(q: str):
    query = {
        "query": {
            "wildcard": {
                "name": f"*{q}*"
            }
        }
    }
    
    result = es.search(index="hot_deals", body=query)
    
    hits = result['hits']['hits']
    items = [{
        "id": hit['_source'].get('id'),
        "name": hit['_source'].get('name'),
        "link": hit['_source'].get('link'),
        "price": hit['_source'].get('price'),
        "dateCreated": hit['_source'].get('dateCreated')
    } for hit in hits]
    return {"items": items}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)