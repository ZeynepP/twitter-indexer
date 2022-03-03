# Small project to index archived trends and tweets  

The data is from Twitter API V1.0, this code is not compatible with V2.0.

Internal archive format for Tweets : 
[timestamp_archived_date, tweet_id/internal_code, tweet_data from REST API ] \

Internal archive format for Trends : 
[timestamp_archived_date, internal_code, trends_data from REST API ]

### Running elasticsearch and kibana on docker :
    #create a network named elastic
    docker network create elastic

    docker run -d  --name elasticsearch --network elastic  -p 9200:9200 -p 9300:9300 -v  /rex/ssd/zpehlivan/twitter_2018-03/elastic/data:/usr/share/elasticsearch/data -e xpack.security.enabled=false -e discovery.type=single-node    docker.rech.ina.fr/elasticsearch:7.5.2
    docker run -d  --name kb-container --network elastic  -p 5601:5601 -e ELASTICSEARCH_HOSTS=http://elasticsearch:9200 docker.rech.ina.fr/kibana/kibana:7.5.2

### Running indexer on docker :
* Update config file
* Run temp-docker  https://github.com/ZeynepP/DockerTemp with correct mounted volumes
  

    #create a network named elastic
    docker run -d  -v /rex/ssd/zpehlivan/twitter_2018-03/trends/:/usr/src/temp/data -v /rex/ssd/zpehlivan/twitter_2018-03/twitter_indexer/:/usr/src/temp  -ti  --rm   --name tindexer   docker.rech.ina.fr/zpehlivan/temp-docker:latest
      
### TODO:
* Add index name, es etc. as params to script.
