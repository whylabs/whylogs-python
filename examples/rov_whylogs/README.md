# Fault Detection of an Underwater Drone with Kafka and whylogs

This is the project's repository for the following article:

https://towardsdatascience.com/monitoring-of-an-underwater-drone-3c5c8a6d1a21

You can follow along the post with the ROV-whylogs.ipynb. It has essentialy the same content. The only differences are that some pieces of code that are meant to run endlessly were changed to run only once in the notebook. Besides that, the code for the monitoring dashboard is present only in the notebook, while the results are discussed only in the blog content. 

To start the kafka related container simply run:

```
docker-compose -f kafka_files/docker-compose.yml up -d   
```

