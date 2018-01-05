import twitterverse_functions as tf
f = open('small_data.txt', 'r')
d = tf.process_data(f)
print(d)
f.close()
usernames = ['tomCruise', 'katieH']
pres_dict = {'sort-by': 'username', 'format': 'long'}
print(tf.get_present_string(d, usernames, pres_dict))
