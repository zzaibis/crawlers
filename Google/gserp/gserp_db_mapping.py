# __author__ = 'Dharmesh Pandav'
import peewee

import datetime

db = peewee.MySQLDatabase("gserp", host="localhost", user="root", password="gghhhjj1")

# db = peewee.SqliteDatabase("gserp.db")


class SearchResult(peewee.Model):
    rank = peewee.CharField()
    url = peewee.CharField(max_length=1000)
    title = peewee.CharField(max_length=1000)
    short_description = peewee.CharField(max_length=5000)
    search_file_type = peewee.CharField(null=True)
    search_word = peewee.CharField()
    search_word_id = peewee.CharField()
    search_page_no = peewee.CharField()
    missing_word = peewee.CharField()
    search_url = peewee.CharField(max_length=1000)
    created_at = peewee.DateTimeField()

    class Meta:
        database = db


class SearchParams(peewee.Model):
    search_word = peewee.CharField()
    search_With_file_type = peewee.BooleanField(null=True, default=False)
    search_file_type = peewee.CharField(null=True, default=None)
    no_of_pages_to_visit = peewee.IntegerField(default=1)  # -1 - visits all search pages by default
    status = peewee.CharField(null=False, default="pending")
    priority = peewee.IntegerField(default=0)  # lowest to highest priority
    search_group = peewee.CharField(default="default")
    slave_server_ip = peewee.CharField(null=True)
    started_at = peewee.DateTimeField(null=True)
    completed_at = peewee.CharField(null=True)
    created_at = peewee.DateTimeField(default=datetime.datetime.utcnow())

    class Meta:
        database = db


# class SearchParams(peewee.Model):
#     search_word = peewee.CharField()
#     search_With_file_type = peewee.BooleanField(null=True, default=False)
#     search_file_type = peewee.CharField(null=True, default=None)
#     status = peewee.CharField(null=False, default="pending")
#     created_at = peewee.DateTimeField(default=datetime.datetime.utcnow())
#
#     class Meta:
#         database = db


class SearchImageResult(peewee.Model):
    rank = peewee.CharField(null=True)
    url = peewee.CharField(null=True, max_length=5000)
    title = peewee.CharField(null=True)
    image_url = peewee.CharField(null=True, max_length=5000)
    short_description = peewee.CharField(null=True)
    search_image_name = peewee.CharField(null=True)
    search_image_id = peewee.CharField(null=True)
    search_page_no = peewee.CharField(null=True)
    search_url = peewee.CharField(null=True, max_length=5000)
    created_at = peewee.CharField(null=True)

    class Meta:
        database = db


class SearchImageParams(peewee.Model):
    search_image_url = peewee.CharField()
    search_image_name = peewee.CharField(null=True, default=None)
    status = peewee.CharField(null=False, default="pending")
    created_at = peewee.DateTimeField(default=datetime.datetime.utcnow())

    class Meta:
        database = db


class ImageSearchByWordResult(peewee.Model):
    image_url = peewee.CharField(null=True, max_length=5000)
    image_provider = peewee.CharField(null=True, max_length=5000)
    search_word_id = peewee.CharField(null=True)
    search_word = peewee.CharField(null=True)

    class Meta:
        database = db


class ImageSearchParams(peewee.Model):
    search_word = peewee.CharField(null=True)
    status = peewee.CharField(null=True)

    class Meta:
        database = db
