from django.apps import AppConfig
#import django.contrib.algoliasearch as AlgoliaSearch
from django.contrib import algoliasearch

from .index import PostIndex


class BoardConfig(AppConfig):
    name = 'board'

    def ready(self):
        Post = self.get_model('Post')
        algoliasearch.register(Post, PostIndex)