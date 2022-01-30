import unittest
import pytest
from redis_connect.connect import RedisConnect, URL_DESIGNATION

TEST_KEY = ['cq3o0', 'asf24', '239fj2']
TEST_VALUES = ["www.google.com", "www.turner.com", "www.blog.com/six"]


# @pytest.mark.integtest
class TestConnectInteg(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.redis = RedisConnect(db=2)

    @classmethod
    def tearDownClass(cls) -> None:
        for key in TEST_KEY:
            cls.redis.delete(key)

    def test_connect_success(self):
        self.redis._store_url(f"{URL_DESIGNATION}:{TEST_KEY[0]}", TEST_VALUES[0])
        self.redis._store_url(f"{URL_DESIGNATION}:{TEST_KEY[1]}", TEST_VALUES[1])

        result = self.redis.get(TEST_KEY[0])
        self.assertEqual(TEST_VALUES[0], result)

    def test_connect_no_key(self):
        result = self.redis.get("key_not_exist")
        self.assertIsNone(result)

    def test_queue_tiny_urls(self):
        self.redis.queue_tiny_urls(TEST_KEY, 3)
        result_list = []
        for _ in range(len(TEST_KEY)):
            result_list.append(self.redis.get_tiny_url())
        self.assertEqual(set(result_list), set(TEST_KEY))

