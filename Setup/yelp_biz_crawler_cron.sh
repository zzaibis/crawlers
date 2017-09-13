#!/bin/bash

process_count=`ps -ef | grep yelpbiz | wc -l`
processes=`ps -ef | grep yelpbiz`
echo $processes >> /var/log/yelpbiz_cralwer_cron.log
if [ $process_count -gt '1' ]; then
  current_date=`date`
  echo $current_date ' Crawler still running... Process Count for yelp' $process_count  >>/var/log/yelpbiz_cralwer_cron.log
else
  current_date=`date`
  timestamp=`date +"%Y%m%d%H%M"`
  echo $current_date " Starting crawl" >>/var/log/yelp_biz_cralwer_cron.log;
  source /home/mehul/venv/scrapy1/bin/activate
  cd /home/mehul/crawlergoogle.crawlers/Yelp/yelpspider
  scrapy crawl yelpbiz --logfile /var/log/yelpbiz_$timestamp.log
  deactivate
fi

