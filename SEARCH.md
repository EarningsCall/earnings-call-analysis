# Earnings Call Search

TODO: Add details here.

### Install ElasticSearch

https://www.elastic.co/guide/en/elasticsearch/reference/current/run-elasticsearch-locally.html

```sh
docker network create elastic
docker pull docker.elastic.co/elasticsearch/elasticsearch:8.13.4
docker run \
  --name elasticsearch \
  --net elastic \
  -p 9200:9200 \
  -p 9300:9300 \
  -e "discovery.type=single-node" \
  -e "xpack.security.enabled=false" \
  -t docker.elastic.co/elasticsearch/elasticsearch:8.13.4
```


Start Kibana

```sh
docker pull docker.elastic.co/kibana/kibana:8.13.4
docker run \
  --name kibana \
  --net elastic \
  -p 5601:5601 \
  docker.elastic.co/kibana/kibana:8.13.4
```
