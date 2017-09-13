#!/bin/bash

process_count=`ps -ef | grep gscraper_v3 | wc -l`
if [ $process_count -gt '1' ]; then
  current_date=`date`
  echo $current_date ' Crawler still running... Process Count for gscraper_v3' $process_count  >>/var/log/google_cralwer_cron.log
else
  current_date=`date`
  timestamp=`date +"%Y%m%d%H%M"`
  echo $current_date " Starting crawl" >>/var/log/google_cralwer_cron.log;
  source /home/mehul/venv/scrapy1/bin/activate
  cd /home/mehul/crawlergoogle.crawlers/Google/gserp
  scrapy crawl gscraper_v3 --logfile=/var/log/gscraper_$timestamp.log >> /var/log/gscraper_$timestamp.output
  deactivate
fi
