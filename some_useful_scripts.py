# Nested Sequence To Flat
from collections import Iterable

def nested_to_flat(items,  exc_for=(str, bytes)):
    for i in items:
        if isinstance(i, Iterable) and not isinstance(i, exc_for):
            yield from nested_to_flat(i)
        else:
            yield i

# example
'''
>>> items = [1, 2, [3, 4, [5, 6], 7], 8]
>>> flat_items = [i for i in nested_to_flat(items)]
>>> flat_items
[1, 2, 3, 4, 5, 6, 7, 8]
>>> items = ['mother', 'father', ['sister', 'brother']]
>>> flat_items = [i for i in nested_to_flat(items)]
>>> flat_items
['mother', 'father', 'sister', 'brother']
'''


# Remove Duplicates But Preserve The Order
def move_and_preserve_order(items):
	new_items = set()
	for item in items:
		if item not in new_items:
			yield item
			new_items.add(item)

# example
'''
>>> words = ['one', 'two', 'one', 'three', 'two', 'one', 'six', 'six']
>>> list(set(words))
['two', 'one', 'three', 'six']
>>> list(move_and_preserve_order(words))
['one', 'two', 'three', 'six']
'''


# Replace Text And Match The Case
def correct_case(word):
	def to_replace(letter):
		text = letter.group()
		if text.isupper():
			return word.upper()
		elif text.islower():
			return word.lower()
		elif text[0].isupper():
			return word.capitalize()
		else:
			return word
	return to_replace

# example
'''
>>> text = 'LOREM IPSUM, Lorem Ipsum, lorem ipsum'
>>> re.sub('ipsum', 'dolor', text, flags=re.IGNORECASE)
'LOREM dolor, Lorem dolor, lorem dolor'
>>> re.sub('ipsum', correct_case('dolor'), text, flags=re.IGNORECASE)
'LOREM DOLOR, Lorem Dolor, lorem dolor'
'''


# Queue That Sorts Items By A Given Priority
import heapq

class HighPriority:
	def __init__(self):
		self.queue = []
		self.enum = 0
	def inside(self, item, number):
		heapq.heappush(self.queue, (-number, self.enum, item))
		self.enum += 1
	def outside(self):
		return heapq.heappop(self.queue)[-1]


class Item:
	def __init__(self, name):
		self.name = name
	def __repr__(self):
		return 'Item({})'.format(self.name)

# example
'''
>>> member = HighPriority()
>>> member.inside(Item('one'), 2)
>>> member.inside(Item('two'), 4)
>>> member.inside(Item('three'), 1)
>>> member.inside(Item('four'), 5)
>>> member.outside()
Item(four)
>>> member.outside()
Item(two)
>>> member.outside()
Item(one)
>>> member.outside()
Item(three)
'''

