import unittest
from elasticsearch import Elasticsearch

class TestElasticsearch(unittest.TestCase):
    def test_main(self):
        es = Elasticsearch("http://localhost:9200")

        