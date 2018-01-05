"""
Type descriptions of Twitterverse and Query dictionaries
(for use in docstrings)

Twitterverse dictionary:  dict of {str: dict of {str: object}}
    - each key is a username (a str)
    - each value is a dict of {str: object} with items as follows:
        - key "name", value represents a user's name (a str)
        - key "location", value represents a user's location (a str)
        - key "web", value represents a user's website (a str)
        - key "bio", value represents a user's bio (a str)
        - key "following", value represents all the usernames of users this
          user is following (a list of str)

Query dictionary: dict of {str: dict of {str: object}}
   - key "search", value represents a search specification dictionary
   - key "filter", value represents a filter specification dictionary
   - key "present", value represents a presentation specification dictionary

Search specification dictionary: dict of {str: object}
   - key "username", value represents the username to begin search at (a str)
   - key "operations", value represents the operations to perform
   (a list of str)

Filter specification dictionary: dict of {str: str}
   - key "following" might exist, value represents a username (a str)
   - key "follower" might exist, value represents a username (a str)
   - key "name-includes" might exist, value represents a str to match
   (a case-insensitive match)
   - key "location-includes" might exist, value represents a str to match
   (a case-insensitive match)

Presentation specification dictionary: dict of {str: str}
   - key "sort-by", value represents how to sort results (a str)
   - key "format", value represents how to format results (a str)

"""


def process_data(file):
    """
    (file open for reading) -> Twitterverse dictionary

    precondition: the twitter data file(parameter 'file') is already opening
    for reading.

    This function aims to read the twitter data file and then return data
    in the file to twitterverse dictionary format.
    """
    twitter_dict = {}
    # Create an empty dictionary which is supposed to contain all data.
    current = file.readline().strip()
    while current != '':
        # Stop the loop until encountering an empty string.
        username = current
        twitter_dict[username] = {'name': file.readline().strip()}
        twitter_dict[username]['location'] = file.readline().strip()
        twitter_dict[username]['web'] = file.readline().strip()
        bio = ''
        # Create an empty string for bio.
        current = file.readline()
        while current != 'ENDBIO\n':
            # The loop ends at the line containing 'ENDBIO'.
            bio += current
            current = file.readline()
        twitter_dict[username]['bio'] = bio.strip()
        follow = []
        # Create an empty list for followers.
        current = file.readline().strip()
        while current != 'END':
            follow.append(current)
            current = file.readline().strip()
        twitter_dict[username]['following'] = follow
        current = file.readline().strip()
    return twitter_dict


def process_query(file):
    """(file open for reading) -> query dictionary
    precondition: the twitter data file(parameter 'file') is already opening
    for reading.

    This function aims to read the twitter data file and then return data
    in the file to query dictionary format.
    """
    twitter_query_dict = {}
    # create the outermost dict
    file.readline()
    twitter_query_dict['search'] = {'username': file.readline().strip()}
    operations = []
    current = file.readline().strip()
    while current != 'FILTER':
        # the loop stops when encounter the string 'FILTER'.
        operations.append(current)
        twitter_query_dict['search']['operations'] = operations
        current = file.readline().strip()
    twitter_query_dict['filter'] = {}
    # create a empty dictionary which is supposed to contain all filter values.
    current = file.readline().strip()
    while current.strip() != 'PRESENT':
        key, content = current.split()
        # Split the line into 2 parts to be the key and content respectively.
        twitter_query_dict['filter'][key] = content
        current = file.readline().strip()
    twitter_query_dict['present'] = {}
    current = file.readline().strip()
    while current.strip() != '':
        key, content = current.split()
        twitter_query_dict['present'][key] = content
        current = file.readline().strip()
    return twitter_query_dict


def all_followers(twitter_dict, username):
    """(Twitterverse dictionary, str) -> list of str

    precondition: the parameter 'twitter_dict' should in a valid \
    twitter dictionary format.

    This function aims to return a list that contains all usernames \
    which following the username provide by the second parameter \
    in the whole twitter dictionary that is provided by the first parameter.

    >>> twitter_dict = {'a': {'name': '', \
    'bio': '', \
    'location': '', \
    'web': '', \
    'following': ['b', 'c']}, \
    'b': {'name': '', \
    'bio': '', \
    'location': '', \
    'web': '', \
    'following': ['a', 'c']}, \
    'c': {'name':  '', \
    'bio': '', \
    'location': '', \
    'web': '', \
    'following': ['a', 'b']}}
    >>> username = 'c'
    >>> all_followers_c = all_followers(twitter_dict, username)
    >>> all_followers_c.sort()
    >>> all_followers_c
    ['a', 'b']
    >>> twitter_dict = {'Kinder': {'name': 'SuperBoy', \
    'bio': 'super_friendly', 'location': '666Spadina', \
    'web': 'kinderchen.com', \
    'following': ['Alan','Ken', 'tomCruise', 'Tracy']}, \
    'Ken': {'name': 'Ken', \
    'bio': 'friend_helper', \
    'location': 'Spadina', \
    'web': 'ken.com', \
    'following': ['Kinder', 'Alan', 'Adele', 'Tay']}, \
    'Tracy': {'name': 'tracy', \
    'bio': 'Kinder is my little brother', \
    'location': 'Wilson', \
    'web': 'www.tracy.com', \
    'following': ['Kinder']}, \
    'Alan': {'name': 'alanZ', \
    'bio': 'I need a doctor,but doctor lost his memory in S9E12', \
    'location': 'Spadina', \
    'web': 'AlanZhang.com', \
    'following': ['Kinder','Ken', 'tomCruise', \
    'Tracy', 'Hannibal', 'Breaking bad', 'Ianto Jones']}}
    >>> username = 'Kinder'
    >>> all_followers_Kinder = all_followers(twitter_dict, username)
    >>> all_followers_Kinder.sort()
    >>> all_followers_Kinder
    ['Alan', 'Ken', 'Tracy']
    """

    following = []
    for key in twitter_dict:
        all_foll = twitter_dict[key]['following']
        if username in all_foll:
            following.append(key)

    return following


def get_search_results(twitter_dict, spec_dict):
    """(Twitterverse dictionary, search specification dictionary) \
    -> list of str

    precondition: The first parameter represents the data in the \
    valid Twitterverse dictionary format, and the second parameter represents \
    the search specification in the valid search specification dictionary \
    format.

    Return a list of string that contains all usernames in twitter_dict that \
    match the criteria given in the spec_dict.
    >>> twitter_dict = {'a': {'name': 'a', \
    'bio': '', \
    'location': '', \
    'web': '', \
    'following': ['b']}, \
    'b': {'name': 'b', \
    'bio': '', \
    'location': '', \
    'web': '', \
    'following': ['c']}, \
    'c': {'name':  '', \
    'bio': '', \
    'location': '', \
    'web': '', \
    'following': ['b']}}
    >>> spec_dict = {'username':'a', 'operations': ['following']}
    >>> result = get_search_results(twitter_dict, spec_dict)
    >>> result.sort()
    >>> result
    ['b']

    >>> twitter_dict = {'Kinder': {'name': 'SuperBoy', \
    'bio': 'super_friendly', \
    'location': '666Spadina', \
    'web': 'kinderchen.com', \
    'following': ['Alan','Ken', 'tomCruise', 'Tracy']}, \
    'Ken': {'name': 'Ken', \
    'bio': 'friend_helper', \
    'location': 'Spadina', \
    'web': 'ken.com', \
    'following': ['Kinder', 'Alan', 'Adele', 'Tay']}, \
    'Tracy': {'name': 'tracy', \
    'bio': 'Kinder is my little brother', \
    'location': 'Wilson', \
    'web': 'www.tracy.com', \
    'following': ['Kinder']}, \
    'Alan': {'name': 'alanZ', \
    'bio': 'I need a doctor, but doctor lost his memory in S9E12', \
    'location': 'Spadina', \
    'web': 'AlanZhang.com', \
    'following': ['Kinder','Ken', 'tomCruise', \
    'Tracy', 'Hannibal', 'Breaking bad', 'Ianto Jones']}}
    >>> spec_dict = {'username': 'Kinder', 'operations': ['followers']}
    >>> result = get_search_results(twitter_dict, spec_dict)
    >>> result.sort()
    >>> result
    ['Alan', 'Ken', 'Tracy']
    """
    search_lst = [spec_dict['username']]
    op_lst = spec_dict['operations']
    while len(op_lst) != 0:
        current = []
        operation = op_lst.pop(0)
        if operation == 'following':
            for name in search_lst:
                current.extend(twitter_dict[name]['following'])
        else:
            for name in search_lst:
                current.extend(all_followers(twitter_dict, name))
        search_lst = current

    return list(set(search_lst))
    # Delete all the repeated elements in the list.


def get_filter_results(twitter_dict, usernames, filter_dict):
    """
    (Twitterverse dictionary, list of str, filter specification dictionary)
    -> list of str
    precondition: The first parameter represents the data \
    in the Twitterverse dictionary format, the second parameter represents \
    a list of usernames, and the third parameter represents \
    the filter specification in the filter specification dictionary format.

    Using the specified filters(Which is given by the third parameter) \
    to filter the given namelist(which is given by the second parameter).
    return a list of string which is the usernames that was kept after applied \
    the specified filters.

    >>> twitter_dict = {'a': {'name': '', \
    'bio': '', \
    'location': '', \
    'web': '', \
    'following': ['b', 'c']}, \
    'b': {'name': '', \
    'bio': '', \
    'location': '', \
    'web': '', \
    'following': ['a', 'c']}, \
    'c': {'name':  '', \
    'bio': '', \
    'location': '', \
    'web': '', \
    'following': ['a', 'b']}}

    >>> usernames = ['a', 'b', 'c']
    >>> filter_dict = {'following': 'b'}
    >>> result = get_filter_results(twitter_dict, usernames, filter_dict)
    >>> result.sort()
    >>> result
    ['a', 'c']
    >>> twitter_dict = {'Kinder': {'name': 'SuperBoy', \
    'bio': 'super_friendly', 'location': '666Spadina', \
    'web': 'kinderchen.com', \
    'following': ['Alan','Ken', 'tomCruise', 'Tracy']}, \
    'Ken': {'name': 'Ken', \
    'bio': 'friend_helper', \
    'location': 'Spadina', \
    'web': 'ken.com', \
    'following': ['Kinder', 'Alan', 'Adele', 'Tay']}, \
    'Tracy': {'name': 'tracy', \
    'bio': 'Kinder is my little brother', \
    'location': 'Wilson', \
    'web': 'www.tracy.com', \
    'following': ['Kinder']}, \
    'Alan': {'name': 'alanZ', \
    'bio': 'I need a doctor,but doctor lost his memory in S9E12', \
    'location': 'Spadina', \
    'web': 'AlanZhang.com', \
    'following': ['Kinder','Ken', 'tomCruise', \
    'Tracy', 'Hannibal', 'Breaking bad', 'Ianto Jones']}}
    >>> usernames = ['Alan', 'Ken', 'Kinder', 'Tracy']
    >>> filter_dict = {'location-includes': 'Spadina'}
    >>> result = get_filter_results(twitter_dict, usernames, filter_dict)
    >>> result.sort()
    >>> result
    ['Alan', 'Ken', 'Kinder']
    """
    if not len(filter_dict) == 0:
        name_list = []
        for user in usernames:
            s = True
            # Suppose s is true
            for key in filter_dict:
                if s is True:
                    if key == 'name-includes':
                        s = filter_dict['name-includes'] in twitter_dict[user]['name']
                    elif key == 'location-includes':
                        s = filter_dict['location-includes'] in twitter_dict[user]['location']
                    elif key == 'follower':
                        s = user in twitter_dict[filter_dict['follower']]['following']
                    elif key == 'following':
                        s = filter_dict['following'] in twitter_dict[user]['following']
            # To see if s is true
            if s:
                name_list.append(user)
        return name_list
    return usernames



def get_present_string(twitter_dict, usernames, pres_dict):
    """(Twitterverse dictionary, list of str,
    presentation specification dictionary) -> str

    precondition: The first parameter represents the data \
    in the Twitterverse dictionary format, the second parameter represents \
    a list of usernames, and the third parameter represents the presentation \
    specification in the presentation specification dictionary format.

    Format the results that get from the end of last function and present them.
    The format of representing is instructed by the presentation dictionary.
    Return the short format as a string transformed by a list of string \
    and the long format as a string.

    >>> twitter_dict = {'Kinder': {'name': 'SuperBoy', \
    'bio': 'super_friendly', 'location': '666Spadina', \
    'web': 'kinderchen.com', \
    'following': ['Alan','Ken', 'tomCruise', 'Tracy']}, \
    'Ken': {'name': 'Ken', \
    'bio': 'friend_helper', \
    'location': 'Spadina', \
    'web': 'ken.com', \
    'following': ['Kinder', 'Alan', 'Adele', 'Tay']},\
    'Tracy': {'name': 'tracy', \
    'bio': 'Kinder is my little brother', \
    'location': 'Wilson', \
    'web': 'www.tracy.com', \
    'following': ['Kinder']}, \
    'Alan': {'name': 'alanZ', \
    'bio': 'I need a doctor,but doctor lost his memory in S9E12', \
    'location': 'Spadina', \
    'web': 'AlanZhang.com', \
    'following': ['Kinder','Ken', 'tomCruise', \
    'Tracy', 'Hannibal', 'Breaking bad', 'Ianto Jones']}}
    >>> usernames = ['Alan', 'Ken']
    >>> pres_dict = {'sort-by': 'username', 'format': 'long'}
    >>> result = get_present_string(twitter_dict, usernames, pres_dict)
    >>> result
    "----------\\nAlan\\nname: alanZ\\nlocation: Spadina\\n\
website: AlanZhang.com\\n\
bio:\\nI need a doctor,but doctor lost his memory in S9E12\\n\
following: ['Kinder', 'Ken', 'tomCruise', 'Tracy', 'Hannibal', 'Breaking bad', 'Ianto Jones']\\n----------\\nKen\\nname: Ken\\nlocation: Spadina\\nwebsite: ken.com\\nbio:\\nfriend_helper\\nfollowing: ['Kinder', 'Alan', 'Adele', 'Tay']\
\\n----------\\n"
    >>> twitter_dict = {'a': {'name': 'a', \
    'bio': '', \
    'location': '', \
    'web': '', \
    'following': ['b', 'c']}, \
    'b': {'name': 'b', \
    'bio': '', \
    'location': '', \
    'web': '', \
    'following': ['a', 'c']}, \
    'c': {'name':  'c', \
    'bio': '', \
    'location': '', \
    'web': '', \
    'following': ['a', 'b']}}
    >>> usernames = ['a', 'b']
    >>> pres_dict = {'sort-by': 'name', 'format': 'short'}
    >>> result = get_present_string(twitter_dict, usernames, pres_dict)
    >>> result
    "['a', 'b']"
    """

    if pres_dict['sort-by'] == 'username':
        tweet_sort(twitter_dict, usernames, username_first)
    if pres_dict['sort-by'] == 'name':
        tweet_sort(twitter_dict, usernames, name_first)
    if pres_dict['sort-by'] == 'popularity':
        tweet_sort(twitter_dict, usernames, more_popular)
    if pres_dict['format'] == 'short':
        result = str(usernames)
    else:
        if len(usernames) == 0:
            result = '----------\n----------'
        else:
            result = ''
            for user in usernames:
                result = result + '----------\n' + \
                         user + '\n' + \
                         'name: ' + twitter_dict[user]['name'] + '\n' + \
                         'location: ' + twitter_dict[user]['location'] + '\n' \
                         + 'website: ' + twitter_dict[user]['web'] + '\n' + \
                         'bio:\n' + twitter_dict[user]['bio'] + \
                         '\nfollowing: ' + \
                         str(twitter_dict[user]['following']) + '\n'
            result += '----------\n'
            # collect the data of the all given user name.
    return result


# --- Sorting Helper Functions ---
def tweet_sort(twitter_data, results, cmp):
    """ (Twitterverse dictionary, list of str, function) -> NoneType

    Sort the results list using the comparison function cmp and the data in
    twitter_data.

    >>> twitter_data = {\
    'a':{'name':'Zed', 'location':'', 'web':'', 'bio':'', 'following':[]}, \
    'b':{'name':'Lee', 'location':'', 'web':'', 'bio':'', 'following':[]}, \
    'c':{'name':'anna', 'location':'', 'web':'', 'bio':'', 'following':[]}}
    >>> result_list = ['c', 'a', 'b']
    >>> tweet_sort(twitter_data, result_list, username_first)
    >>> result_list
    ['a', 'b', 'c']
    >>> tweet_sort(twitter_data, result_list, name_first)
    >>> result_list
    ['b', 'a', 'c']
    """

    # Insertion sort
    for i in range(1, len(results)):
        current = results[i]
        position = i
        while position > 0 and cmp(twitter_data, results[position - 1],
                                   current) > 0:
            results[position] = results[position - 1]
            position -= 1
        results[position] = current


def more_popular(twitter_data, a, b):
    """ (Twitterverse dictionary, str, str) -> int

    Return -1 if user a has more followers than user b, 1 if fewer followers,
    and the result of sorting by username if they have the same, based on the
    data in twitter_data.

    >>> twitter_data = {\
    'a':{'name':'', 'location':'', 'web':'', 'bio':'', 'following':['b']}, \
    'b':{'name':'', 'location':'', 'web':'', 'bio':'', 'following':[]}, \
    'c':{'name':'', 'location':'', 'web':'', 'bio':'', 'following':[]}}
    >>> more_popular(twitter_data, 'a', 'b')
    1
    >>> more_popular(twitter_data, 'a', 'c')
    -1
    """

    a_popularity = len(all_followers(twitter_data, a))
    b_popularity = len(all_followers(twitter_data, b))
    if a_popularity > b_popularity:
        return -1
    if a_popularity < b_popularity:
        return 1
    return username_first(twitter_data, a, b)


def username_first(twitter_data, a, b):
    """ (Twitterverse dictionary, str, str) -> int

    Return 1 if user a has a username that comes after user b's username
    alphabetically, -1 if user a's username comes before user b's username,
    and 0 if a tie, based on the data in twitter_data.

    >>> twitter_data = {\
    'a':{'name':'', 'location':'', 'web':'', 'bio':'', 'following':['b']}, \
    'b':{'name':'', 'location':'', 'web':'', 'bio':'', 'following':[]}, \
    'c':{'name':'', 'location':'', 'web':'', 'bio':'', 'following':[]}}
    >>> username_first(twitter_data, 'c', 'b')
    1
    >>> username_first(twitter_data, 'a', 'b')
    -1
    """

    if a < b:
        return -1
    if a > b:
        return 1
    return 0


def name_first(twitter_data, a, b):
    """ (Twitterverse dictionary, str, str) -> int

    Return 1 if user a's name comes after user b's name alphabetically,
    -1 if user a's name comes before user b's name, and the ordering of their
    usernames if there is a tie, based on the data in twitter_data.

    >>> twitter_data = {\
    'a':{'name':'Zed', 'location':'', 'web':'', 'bio':'', 'following':[]}, \
    'b':{'name':'Lee', 'location':'', 'web':'', 'bio':'', 'following':[]}, \
    'c':{'name':'anna', 'location':'', 'web':'', 'bio':'', 'following':[]}}
    >>> name_first(twitter_data, 'c', 'b')
    1
    >>> name_first(twitter_data, 'b', 'a')
    -1
    """

    a_name = twitter_data[a]["name"]
    b_name = twitter_data[b]["name"]
    if a_name < b_name:
        return -1
    if a_name > b_name:
        return 1
    return username_first(twitter_data, a, b)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
