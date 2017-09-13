#!/bin/bash

process_count=`ps -ef | grep yelpspider | wc -l`
processes=`ps -ef | grep yelpspidere`
echo $processes >> /var/log/yelp_cralwer_cron.log
if [ $process_count -gt '1' ]; then
  current_date=`date`
  echo $current_date ' Crawler still running... Process Count for yelp' $process_count  >>/var/log/yelp_cralwer_cron.log
else
  current_date=`date`
  timestamp=`date +"%Y%m%d%H%M"`
  echo $current_date " Starting crawl" >>/var/log/yelp_cralwer_cron.log;
  source /home/mehul/venv/scrapy1/bin/activate
  cd /home/mehul/crawlergoogle.crawlers/Yelp/yelpspider
  scrapy crawl yelpspider --logfile=/var/log/yelp_$timestamp.log >> /var/log/yelp_$timestamp.output
  deactivate
fi

