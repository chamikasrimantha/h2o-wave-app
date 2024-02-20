from app import prepare_data
import unittest
import random


def get_random_tuple():
    length_of_data = len(prepare_data())
    index = random.randrange(length_of_data)
    return prepare_data()[index]


class TestApp(unittest.TestCase):
    def setUp(self):
        # Add any common setup code here
        pass

    def test_is_list(self):
        self.assertTrue(type(prepare_data()) == list)
        self.assertFalse(type(prepare_data()) == tuple)
        self.assertFalse(type(prepare_data()) == str)

    def test_list_is_not_empty(self):
        self.assertTrue(len(prepare_data()) > 0)
        self.assertFalse(len(prepare_data()) <= 0)

    def test_is_element_tuple(self):
        random_tuple = get_random_tuple()
        self.assertTrue(type(random_tuple) == tuple)
        self.assertFalse(type(random_tuple) == str)
        self.assertFalse(type(random_tuple) == int)

    def test_is_title_string(self):
        random_tuple = get_random_tuple()
        self.assertTrue(type(random_tuple[0]) == str)
        self.assertFalse(type(random_tuple[0]) == "")
        self.assertFalse(type(random_tuple[0]) == int)
        self.assertFalse(type(random_tuple[0]) == list)
        self.assertFalse(type(random_tuple[0]) == float)

    def test_is_hero_string(self):
        random_tuple = get_random_tuple()
        self.assertFalse(type(random_tuple[1]) == float)
        self.assertFalse(type(random_tuple[1]) == int)
        self.assertTrue(type(random_tuple[1]) == str)
        self.assertFalse(type(random_tuple[1]) == list)

    def test_is_genre_string(self):
        random_tuple = get_random_tuple()
        self.assertFalse(type(random_tuple[1]) == float)
        self.assertFalse(type(random_tuple[1]) == int)
        self.assertTrue(type(random_tuple[1]) == str)
        self.assertFalse(type(random_tuple[1]) == list)
    
    def test_is_year_string(self):
        random_tuple = get_random_tuple()
        self.assertFalse(type(random_tuple[1]) == float)
        self.assertFalse(type(random_tuple[1]) == int)
        self.assertTrue(type(random_tuple[1]) == str)
        self.assertFalse(type(random_tuple[1]) == list)
    
    def test_is_rating_string(self):
        random_tuple = get_random_tuple()
        self.assertFalse(type(random_tuple[1]) == float)
        self.assertFalse(type(random_tuple[1]) == int)
        self.assertTrue(type(random_tuple[1]) == str)
        self.assertFalse(type(random_tuple[1]) == list)

    


if __name__ == '__main__':
    unittest.main()
