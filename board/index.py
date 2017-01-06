from django.contrib.algoliasearch import AlgoliaIndex


class PostIndex(AlgoliaIndex):
    fields = ('author', 'to_field', 'do_field', 'person', 'source_url', 'summary', 'pk')
    settings = {'attributesToIndex': ['author', 'to_field', 'do_field', 'person', 'source_url', 'summary', 'pk']}
    index_name = 'post_index'



    