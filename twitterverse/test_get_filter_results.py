import unittest
import twitterverse_functions as tf

twitter_dict = {'Kinder': {'name': 'SuperBoy',
        'bio': 'super_friendly', 'location': '666Spadina', 'web': 'kinderchen.com',
         'following': ['Alan','Ken', 'tomCruise', 'Tracy']},
         'Ken': {'name': 'Ken', 'bio': 'friend_helper', 'location': 'Spadina',
     'web': 'ken.com', 'following': ['Kinder', 'Alan', 'Adele', 'Tay']},
        'Tracy': {'name': 'tracy', 'bio': 'Kinder is my little brother',
        'location': 'Wilson', 'web': 'www.tracy.com', 'following': ['Kinder']},
      'Alan': {'name': 'alanZ', 'bio': 'I need a doctor, \
      but doctor lost his memory in S9E12', 'location': 'Spadina',
      'web': 'AlanZhang.com', 'following': ['Kinder','Ken', 'tomCruise',
       'Tracy', 'Hannibal', 'Breaking bad', 'Ianto Jones']}}

class TestGetFilterResults(unittest.TestCase):
    """
    Example unittest method for get_filter_results.
    """
    def test_filter_1(self):
        """Test get_filter_results with usernames = ['Kinder', 'Ken', 'Alan', \
        'Tracy'] and filter_dict = {}
        """
        usernames = ['Kinder', 'Ken', 'Alan', 'Tracy']
        filter_dict = {}

        actual = tf.get_filter_results(twitter_dict, usernames, filter_dict)
        expected = ['Kinder', 'Ken', 'Alan', 'Tracy']
        self.assertEqual(actual, expected)

    def test_filter_2(self):
        """Test get_filter_results with usernames = ['Kinder', 'Ken', 'Alan', \
        'Tracy'] and filter_dict = {'name-includes': 'K', 'location-includes': \
        'Spadina', 'following': 'Kinder', 'follower': 'Alan'}
        """
        usernames = ['Kinder', 'Ken', 'Alan', 'Tracy']
        filter_dict = {'name-includes': 'Ken', 'location-includes': 'Spadina',
                       'following': 'Kinder', 'follower': 'Alan'}

        actual = tf.get_filter_results(twitter_dict, usernames, filter_dict)
        expected = ['Ken']
        self.assertEqual(actual, expected)

    def test_filter_3(self):
        """Test get_filter_results with usernames = ['Kinder', 'Ken', 'Alan', \
        'Tracy'] and filter_dict = {'name-includes': 'K', 'location-includes': \
        'Spadina','following': 'Kinder', 'follower': 'Tracy'}
        """

        usernames = ['Kinder', 'Ken', 'Alan', 'Tracy']
        filter_dict = {'name-includes': 'Ken', 'location-includes': 'Spadina',
                       'following': 'Kinder', 'follower': 'Tracy'}

        actual = tf.get_filter_results(twitter_dict, usernames, filter_dict)
        expected = []
        self.assertEqual(actual, expected)

    def test_filter_4(self):
        """Test get_filter_results with usernames = ['Kinder', 'Ken', 'Alan', \
        'Tracy'] and filter_dict = {'location-includes': 'i','following': 'K', \
        'follower': 'Ken'}
        """

        usernames = ['Kinder', 'Ken', 'Alan', 'Tracy']
        filter_dict = {'location-includes': 'i',
                       'following': 'K', 'follower': 'Ken'}

        actual = tf.get_filter_results(twitter_dict, usernames, filter_dict)
        expected = []
        self.assertEqual(actual, expected)

    def test_filter_5(self):
        """Test get_filter_results with usernames = ['Kinder', 'Ken', 'Alan', \
        'Tracy'] and {'location-includes': 'Wilson'}
        """

        usernames = ['Kinder', 'Ken', 'Alan', 'Tracy']
        filter_dict = {'location-includes': 'Wilson'}

        actual = tf.get_filter_results(twitter_dict, usernames, filter_dict)
        expected = ['Tracy']
        self.assertEqual(actual, expected)

    def test_filter_6(self):
        """Test get_filter_results with usernames = ['Kinder', 'Ken', 'Alan', \
        'Tracy'] and {'location-includes': 'Spadina'}
        """

        usernames = ['Kinder', 'Ken', 'Alan', 'Tracy']
        filter_dict = {'location-includes': 'Spadina'}

        actual = tf.get_filter_results(twitter_dict, usernames, filter_dict)
        expected = ['Kinder', 'Ken', 'Alan']
        self.assertEqual(actual, expected)

    def test_filter_7(self):
        """Test get_filter_results with usernames = ['Kinder', 'Ken', 'Alan', \
        'Tracy'] and filter_dict = {'following': 'Kinder'}
        """

        usernames = ['Kinder', 'Ken', 'Alan', 'Tracy']
        filter_dict = {'following': 'Kinder'}

        actual = tf.get_filter_results(twitter_dict, usernames, filter_dict)
        expected = ['Ken', 'Alan', 'Tracy']
        self.assertEqual(actual, expected)

    def test_filter(self):
        """Test get_filter_results with usernames = ['Kinder', 'Ken', 'Alan', \
        'Tracy'] and filter_dict = {'follower': 'Alan'}
        """
        usernames = ['Kinder', 'Ken', 'Alan', 'Tracy']
        filter_dict = {'follower': 'Alan'}

        actual = tf.get_filter_results(twitter_dict, usernames, filter_dict)
        expected = ['Kinder', 'Ken', 'Tracy']
        self.assertEqual(actual, expected)




if __name__ == '__main__':
    unittest.main(exit=False)
