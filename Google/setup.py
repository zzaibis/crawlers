from setuptools import setup, find_packages

setup(
    name='ad',
    version='1.0',
    packages=find_packages(),
    entry_points={'scrapy': ['settings = ad.settings']}, requires=['scrapy']
)


# http://stackoverflow.com/questions/22646323/windows-scrapyd-deploy-is-not-recognized