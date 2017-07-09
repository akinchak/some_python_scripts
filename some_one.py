import re
import csv
import itertools
from collections import Counter
from train_category import train_cat
from test_category import test_cat

WORDS_IGNORE = ['and', 'with', 'for', 'the', 'Hello', 'been', 'all', 'you',
                'can','I\'m', 'also', 'from', 'use', 'old', 'your', 'have',
                'care', 'love', 'that', 'them', 'are', 'walker', 'I\'ve', 'more',
                'any', 'help', 'will']

TEXT_OUT = '''
UID: {}\n
ABOUT USER: {}\n
REAL CATEGORY: {}\n
SCRIPT CATEGORY: {}
'''

with open('categories.csv') as f:
    csv_file = csv.reader(f)
    csv_file = [i for i in csv_file]

SECTIONS = [i[-1] for i in csv_file]


def text_split(text):
    text = re.split(r'[;,.:\s]\s*', text)
    text = [word for word in text if len(word) > 2 and word not in WORDS_IGNORE]
    return text

def words_count(all_words_in_one):
     all_words_count = Counter(all_words_in_one)
     words = [i[0] for i in all_words_count.most_common(15)]
     return words
  
# most frequent 15 words for specific category/section in user`s profile description
def top_words_for_section(section):
    ''' Argument (section) is string from SECTIONS:
       'writing_translation', 'graphic_design', etc. '''
    full_description_words = []
    all_words_in_one = []
    for i in train_cat:        
        if i[-1] == section:
            text = i[0]['user']['executor']['description']
            text =  text_split(text) 
            full_description_words.append(text)
    all_words_in_one = list(itertools.chain.from_iterable(full_description_words))
    words_top_fifteen = words_count(all_words_in_one)
    return words_top_fifteen


# new test_user dict with main info
def all_test_user_func():
    all_test_user_dict = {}
    for i in test_cat:
        pull = [] 
        user_uid = i[0]['user']['external_uid']
        all_test_user_dict[user_uid] = {}
        all_test_user_dict[user_uid]['user_category'] = i[-1]
        all_test_user_dict[user_uid]['user_info'] = i[0]['user']['executor']['description']
        text = all_test_user_dict[user_uid]['user_info']
        
        # find common words in test profile and top words in relative user category
        all_words_in_one =  text_split(text)  
        words_top_fifteen = words_count(all_words_in_one)   
        for section in SECTIONS:
            sec_top_words = top_words_for_section(section)        
            if set(sec_top_words) & set(words_top_fifteen):
                pull.append((len(set(sec_top_words) & set(words_top_fifteen)), section))
        pull.sort()

        # most relative category by 'script decision'
        script_cat = pull[-1][1]
        
        all_test_user_dict[user_uid]['user_script_category'] = script_cat        
    return all_test_user_dict

# simple example using all_test_user_func
'''
result = all_test_user_func()
for user_uid in result:
    print(user_uid, result[user_uid]['user_category'])
'''

# script for user info output by UID input 
all_test_user_dict = all_test_user_func()
all_test_uid = list(i for i in all_test_user_dict)

while True:
    user_uid = ''
    ask_yes_no = ''
    ask_yes_no = input('To Escape - choose "1" or choose "Enter" to continue: ')
    if ask_yes_no == '1':
        break
    while user_uid not in all_test_uid:
        user_uid = input('Please, enter correct User UID: ')

    user_info = all_test_user_dict[user_uid]['user_info']
    user_cat = all_test_user_dict[user_uid]['user_category']
    script_cat = all_test_user_dict[user_uid]['user_script_category']
    print(TEXT_OUT.format(user_uid, user_info, user_cat, script_cat))

input()

# counting equal category (real vs script) percent
'''
result = all_test_user_func()
num_equal = 0
num_not_equal = 0
for user_uid in result:
    if result[user_uid]['user_category'] == result[user_uid]['user_script_category']:
        num_equal += 1
    else:
        num_not_equal += 1
percent_equality = num_equal*100/(num_equal+num_not_equal)
percent_equality = int(percent_equality)
print('Percent of equal category is {}%'.format(percent_equality))
'''
