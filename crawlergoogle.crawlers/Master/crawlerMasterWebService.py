#!/usr/bin/env python
import web
import re
import base64
import json, requests
import peewee
from playhouse.shortcuts import model_to_dict, dict_to_model
import datetime
from bson import json_util
import datetime

googleCrawlerSlaveMaxLoad = 50
bingCrawlerSlaveMaxLoad = 50
googleImageCrawlerSlaveMaxLoad = 50
GoogleImageWordCrawlerSlaveMaxLoad = 50

yelpCrawlerSlaveMaxLoad = 5

db = peewee.MySQLDatabase("crawler", host="localhost", user="root", password="gghhjj1")

# serp_param.status
# 0 = pending
# 1 = in-progress
# 2 = completed
# 3 = failed


class GoogleSearchParams(peewee.Model):
    search_word = peewee.CharField()
    search_With_file_type = peewee.BooleanField(null=True, default=False)
    search_file_type = peewee.CharField(null=True, default=None)
    status = peewee.IntegerField(null=False, default=0)  # 0 -> Pending, 1 -> Running, 2 -> Completed, 3 -> Deferred
    priority = peewee.IntegerField(default=3)
    search_group = peewee.CharField(default="default")
    no_of_pages_per_keyword = peewee.IntegerField(default=4)
    slave_server_ip = peewee.CharField(null=True)
    started_at = peewee.DateTimeField(null=True)
    completed_at = peewee.DateTimeField(null=True)
    created_at = peewee.DateTimeField(default=datetime.datetime.utcnow())

    class Meta:
        database = db


class GoogleImageSearchParams(peewee.Model):
    search_image_url = peewee.CharField()
    search_image_name = peewee.CharField(null=True, default=None)
    status = peewee.IntegerField(null=False, default=0)  # 0 -> Pending, 1 -> Running, 2 -> Completed, 3 -> Deferred
    priority = peewee.IntegerField(default=3)
    search_group = peewee.CharField(default="default")
    image_server_ip = peewee.CharField(null=True,default="localhost")
    image_base_path = peewee.CharField(null=True,default="images")  # defaults to http://localhost/images/image_name
    no_of_pages_per_keyword = peewee.IntegerField(default=4)
    slave_server_ip = peewee.CharField(null=True)
    started_at = peewee.DateTimeField(null=True)
    completed_at = peewee.DateTimeField(null=True)
    created_at = peewee.DateTimeField(default=datetime.datetime.utcnow())

    class Meta:
        database = db


class GoogleImageWordSearchParams(peewee.Model):
    image_search_word = peewee.CharField(null=True, default=None)
    status = peewee.IntegerField(null=False, default=0)  # 0 -> Pending, 1 -> Running, 2 -> Completed, 3 -> Deferred
    priority = peewee.IntegerField(default=3)
    search_group = peewee.CharField(default="default")
    no_of_pages_per_keyword = peewee.IntegerField(default=4)
    slave_server_ip = peewee.CharField(null=True)
    started_at = peewee.DateTimeField(null=True)
    completed_at = peewee.DateTimeField(null=True)
    created_at = peewee.DateTimeField(default=datetime.datetime.utcnow())

    class Meta:
        database = db


class BingSearchParams(peewee.Model):
    search_word = peewee.CharField()
    search_With_file_type = peewee.BooleanField(null=True, default=False)
    search_file_type = peewee.CharField(null=True, default=None)
    status = peewee.IntegerField(null=False, default=0)  # 0 -> Pending, 1 -> Running, 2 -> Completed, 3 -> Deferred
    priority = peewee.IntegerField(default=3)
    search_group = peewee.CharField(default="default")
    no_of_pages_per_keyword = peewee.IntegerField(default=4)
    slave_server_ip = peewee.CharField(null=True)
    started_at = peewee.DateTimeField(null=True)
    completed_at = peewee.DateTimeField(null=True)
    created_at = peewee.DateTimeField(default=datetime.datetime.utcnow())

    class Meta:
        database = db

class YelpSearchParams(peewee.Model):
    search_url = peewee.CharField()
    visit_details_page = peewee.BooleanField(default=False)  # false - does not visit details page by default
    no_of_pages_to_visit = peewee.IntegerField(default=-1)  # -1 - visits all search pages by default
    status = peewee.IntegerField(null=False, default=0)  # 0 -> Pending, 1 -> Running, 2 -> Completed, 3 -> Deferred
    priority = peewee.IntegerField(default=0)  # lowest to highest priority
    search_group = peewee.CharField(default="default")
    slave_server_ip = peewee.CharField(null=True)
    started_at = peewee.DateTimeField(null=True)
    completed_at = peewee.CharField(null=True)
    created_at = peewee.DateTimeField(default=datetime.datetime.utcnow())

    class Meta:
        database = db


class YelpBizParams(peewee.Model):
    search_url = peewee.CharField()
    status = peewee.IntegerField(null=False, default=0)  # 0 -> Pending, 1 -> Running, 2 -> Completed, 3 -> Deferred
    priority = peewee.IntegerField(default=0)  # lowest to highest priority
    search_group = peewee.CharField(default="default")
    slave_server_ip = peewee.CharField(null=True)
    started_at = peewee.DateTimeField(null=True)
    completed_at = peewee.CharField(null=True)
    created_at = peewee.DateTimeField(default=datetime.datetime.utcnow())

    class Meta:
        database = db



if not GoogleSearchParams.table_exists():
    db.create_table(GoogleSearchParams, safe=True)  # Create if not exists
if not GoogleImageSearchParams.table_exists():
    db.create_table(GoogleImageSearchParams, safe=True)  # Create if not exists
if not GoogleImageWordSearchParams.table_exists():
    db.create_table(GoogleImageWordSearchParams, safe=True)  # Create if not exists
if not BingSearchParams.table_exists():
    db.create_table(BingSearchParams, safe=True)
if not YelpSearchParams.table_exists():
    db.create_table(YelpSearchParams, safe=True)  # Create if not exists
if not YelpBizParams.table_exists():
    db.create_table(YelpBizParams, safe=True)


urls = (
    '/google', 'Google',
    '/gimages', 'GImages',
    '/gimagesbyword', 'GImagesByWord',
    '/linkedin', 'LinkedIn',
    '/yelp', 'Yelp',
    '/gmaps', 'GoogleMaps',
    '/login', 'Login',
    '/bing', 'Bing',
    '/yelpbiz', 'YelpBiz'
)

app = web.application(urls, globals())

allowed = (
    ('crawlme', ':6c5/V:YjNn?c%Q?'),
    ('tom', 'pass2')
)


class Google:
    def GET(self):
        if web.ctx.env.get('HTTP_AUTHORIZATION') is not None:
            result = []
            for serp_param in GoogleSearchParams.select().where(GoogleSearchParams.status == 0).order_by(
                    GoogleSearchParams.priority.asc()).limit(googleCrawlerSlaveMaxLoad):
                serp_param.status = 1
                serp_param.started_at = datetime.datetime.now()
                serp_param.slave_server_ip = web.ctx.ip
                serp_param.save()
                print model_to_dict(serp_param)
                result.append(model_to_dict(serp_param))
                # add to result dict, model_to_dict(serp_param)
            return json.dumps(result, default=json_util.default)
            # return json.dumps(model_to_dict(serp_param))
        else:
            raise web.seeother('/login')

    def POST(self):
        if web.ctx.env.get('HTTP_AUTHORIZATION') is not None:
            data = web.data()  # you can get data use this method
            print data
            completed_search = json.loads(data)
            for search in completed_search:
                print search["id"]
                serp_param = GoogleSearchParams.get(GoogleSearchParams.id == search["id"])
                # serp_param.status = 2  # Completed
                serp_param.status = search['status']
                serp_param.completed_at = datetime.datetime.now()
                serp_param.save()
        else:
            raise web.seeother('/login')


class Bing:
    def GET(self):
        if web.ctx.env.get('HTTP_AUTHORIZATION') is not None:
            result = []
            for serp_param in BingSearchParams.select().where(BingSearchParams.status == 0).order_by(
                    BingSearchParams.priority.asc()).limit(bingCrawlerSlaveMaxLoad):
                serp_param.status = 1
                serp_param.started_at = datetime.datetime.now()
                serp_param.slave_server_ip = web.ctx.ip
                serp_param.save()
                print model_to_dict(serp_param)
                result.append(model_to_dict(serp_param))
                # add to result dict, model_to_dict(serp_param)
            return json.dumps(result, default=json_util.default)
            # return json.dumps(model_to_dict(serp_param))
        else:
            raise web.seeother('/login')

    def POST(self):
        if web.ctx.env.get('HTTP_AUTHORIZATION') is not None:
            data = web.data()  # you can get data use this method
            print data
            completed_search = json.loads(data)
            for search in completed_search:
                print search["id"]
                serp_param = BingSearchParams.get(BingSearchParams.id == search["id"])
                # serp_param.status = 2  # Completed
                serp_param.status = search['status']
                serp_param.completed_at = datetime.datetime.now()
                serp_param.save()
        else:
            raise web.seeother('/login')


class GImages:
    def GET(self):
        if web.ctx.env.get('HTTP_AUTHORIZATION') is not None:
            result = []
            for serp_param in GoogleImageSearchParams.select().where(GoogleImageSearchParams.status == 0).order_by(
                    GoogleSearch.priority.asc()).limit(googleImageCrawlerSlaveMaxLoad):
                serp_param.status = 1  # Running
                serp_param.started_at = datetime.datetime.now()
                serp_param.slave_server_ip = web.ctx.ip
                serp_param.save()
                print model_to_dict(serp_param)
                result.append(model_to_dict(serp_param))
                # add to result dict, model_to_dict(serp_param)
            return json.dumps(result, default=json_util.default)
            # return json.dumps(model_to_dict(serp_param))
        else:
            raise web.seeother('/login')

    def POST(self):
        if web.ctx.env.get('HTTP_AUTHORIZATION') is not None:
            data = web.data()  # you can get data use this method
            print data
            completed_search = json.loads(data)
            for search in completed_search:
                print search["id"]
                serp_param = GoogleImageSearchParams.get(GoogleImageSearchParams.id == search["id"])
                # serp_param.status = 2  # Completed
                serp_param.status = search['status']
                serp_param.completed_at = datetime.datetime.now()
                serp_param.save()
        else:
            raise web.seeother('/login')


class GImagesByWord:
    def GET(self):
        if web.ctx.env.get('HTTP_AUTHORIZATION') is not None:
            result = []
            for serp_param in GoogleImageWordSearchParams.select().where(GoogleImageWordSearchParams.status == 0).order_by(
                    GoogleSearch.priority.asc()).limit(GoogleImageWordCrawlerSlaveMaxLoad):
                serp_param.status = 1  # Running
                serp_param.started_at = datetime.datetime.now()
                serp_param.slave_server_ip = web.ctx.ip
                serp_param.save()
                print model_to_dict(serp_param)
                result.append(model_to_dict(serp_param))
                # add to result dict, model_to_dict(serp_param)
            return json.dumps(result, default=json_util.default)
            # return json.dumps(model_to_dict(serp_param))
        else:
            raise web.seeother('/login')

    def POST(self):
        if web.ctx.env.get('HTTP_AUTHORIZATION') is not None:
            data = web.data()  # you can get data use this method
            print data
            completed_search = json.loads(data)
            for search in completed_search:
                print search["id"]
                serp_param = GoogleImageWordSearchParams.get(GoogleImageWordSearchParams.id == search["id"])
                # serp_param.status = 2  # Completed
                serp_param.status = search['status']
                serp_param.completed_at = datetime.datetime.now()
                serp_param.save()
        else:
            raise web.seeother('/login')


class Yelp:
    def GET(self):
        if web.ctx.env.get('HTTP_AUTHORIZATION') is not None:
            result = []
            for serp_param in YelpSearchParams.select().where(YelpSearchParams.status == 0).order_by(
                    YelpSearchParams.priority.asc()).limit(yelpCrawlerSlaveMaxLoad):
                serp_param.status = 1
                serp_param.started_at = datetime.datetime.now()
                serp_param.slave_server_ip = web.ctx.ip
                serp_param.save()
                print model_to_dict(serp_param)
                result.append(model_to_dict(serp_param))
                # add to result dict, model_to_dict(serp_param)
            return json.dumps(result, default=json_util.default)
            # return json.dumps(model_to_dict(serp_param))
        else:
            raise web.seeother('/login')

    def POST(self):
        if web.ctx.env.get('HTTP_AUTHORIZATION') is not None:
            data = web.data()  # you can get data use this method
            print data
            completed_search = json.loads(data)
            for search in completed_search:
                print search["id"]
                serp_param = YelpSearchParams.get(YelpSearchParams.id == search["id"])
                # serp_param.status = 2  # Completed
                serp_param.status = search['status']
                serp_param.completed_at = datetime.datetime.now()
                serp_param.save()
        else:
            raise web.seeother('/login')


class YelpBiz:
    def GET(self):
        if web.ctx.env.get('HTTP_AUTHORIZATION') is not None:
            result = []
            for serp_param in YelpBizParams.select().where(YelpBizParams.status == 0).order_by(
                    YelpBizParams.priority.asc()).limit(yelpCrawlerSlaveMaxLoad):
                serp_param.status = 1
                serp_param.started_at = datetime.datetime.now()
                serp_param.slave_server_ip = web.ctx.ip
                serp_param.save()
                print model_to_dict(serp_param)
                result.append(model_to_dict(serp_param))
                # add to result dict, model_to_dict(serp_param)
            return json.dumps(result, default=json_util.default)
            # return json.dumps(model_to_dict(serp_param))
        else:
            raise web.seeother('/login')

    def POST(self):
        if web.ctx.env.get('HTTP_AUTHORIZATION') is not None:
            data = web.data()  # you can get data use this method
            print data
            completed_search = json.loads(data)
            for search in completed_search:
                print search["id"]
                serp_param = YelpBizParams.get(YelpBizParams.id == search["id"])
                # serp_param.status = 2  # Completed
                serp_param.status = search['status']
                serp_param.completed_at = datetime.datetime.now()
                serp_param.save()
        else:
            raise web.seeother('/login')



class Login:
    def GET(self):
        auth = web.ctx.env.get('HTTP_AUTHORIZATION')
        authreq = False
        if auth is None:
            authreq = True
        else:
            auth = re.sub('^Basic ', '', auth)
            username, password = base64.decodestring(auth).split(':')
            if (username, password) in allowed:
                raise web.seeother('/')
            else:
                authreq = True
        if authreq:
            web.header('WWW-Authenticate', 'Basic realm="Auth example"')
            web.ctx.status = '401 Unauthorized'
            return

    def POST(self):
        auth = web.ctx.env.get('HTTP_AUTHORIZATION')
        authreq = False
        if auth is None:
            authreq = True
        else:
            auth = re.sub('^Basic ', '', auth)
            username, password = base64.decodestring(auth).split(':')
            if (username, password) in allowed:
                raise web.seeother('/')
            else:
                authreq = True
        if authreq:
            web.header('WWW-Authenticate', 'Basic realm="Auth example"')
            web.ctx.status = '401 Unauthorized'
            return


if __name__ == '__main__':
    app.run()
