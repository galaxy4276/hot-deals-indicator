from elasticsearch import Elasticsearch

es = Elasticsearch(["http://han-box.co.kr:9200"], basic_auth=("", ""))

index_exists = es.indices.exists(index="hot_deals")
print(f"hot_deals 인덱스 존재 여부: {index_exists}")

mapping = es.indices.get_mapping(index="hot_deals")
print(f"hot_deals 매핑: {mapping}")

sample_query = {
    "query": {"match_all": {}},
    "size": 1
}
sample_results = es.search(index="hot_deals", body=sample_query)
print(f"샘플 데이터: {sample_results}")