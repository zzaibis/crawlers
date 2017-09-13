import urllib2
import base64
import json, time, random

server_ip = "http://104.197.75.34"
server_port = "8080"
username = 'tom'
password = 'pass2'
# domain = "google"


def get_start_urls(domain="yelp"):
    # SQL Input
    time.sleep(random.randint(1,20))
    request = urllib2.Request("%s:%s/%s" % (server_ip, server_port, domain))
    base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)
    response = urllib2.urlopen(request)
    return response.read()


def update_search_param_status(search_param_id, domain="yelp", status=2):
    data = json.dumps([{'id': search_param_id,'status': status}])

    request = urllib2.Request("%s:%s/%s" % (server_ip, server_port, domain),
                              data,
                              {'Content-Type': 'application/json'})

    base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)
    urllib2.urlopen(request)

def get_start_urls_biz(domain="yelpbiz"):
    # SQL Input
    time.sleep(random.randint(1,20))
    request = urllib2.Request("%s:%s/%s" % (server_ip, server_port, domain))
    base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)
    response = urllib2.urlopen(request)
    return response.read()


def update_search_param_status_biz(search_param_id, domain="yelpbiz", status=2):
    data = json.dumps([{'id': search_param_id,'status': status}])

    request = urllib2.Request("%s:%s/%s" % (server_ip, server_port, domain),
                              data,
                              {'Content-Type': 'application/json'})

    base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)
    urllib2.urlopen(request)

