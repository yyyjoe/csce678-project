import json
import hashlib
import string
import random
import re
from langdetect import detect
from instagram_web_api import Client as webClient


class MyClient(webClient):
	@staticmethod
	def _extract_rhx_gis(html):
		options = string.ascii_lowercase + string.digits
		text = ''.join([random.choice(options) for _ in range(8)])
		return hashlib.md5(text.encode())

def process_text(text):
	lang = None
	try:
		lang = detect(text)
	except:
		print('This text cannot be differentiated.')
		
	if lang == 'en':
		return text
	else:
		return ''

def get_user_post(username, postcount):
	web_api = MyClient(auto_patch=True, drop_incompat_keys=False)

	user_info = None
	try:
		user_info = web_api.user_info2(username)
	except:
		print('username: ' + username + ' is invalid.')
		return ''

	if not user_info:
		return ''

	user_id = user_info['id']
	user_post_count = user_info['counts']['media']		
	followed_by_count = user_info['counts']['followed_by']
	user_img_url = user_info['profile_picture']

	user_feed_info = web_api.user_feed(user_id, count=min(20, user_post_count))

	index = 0
	text_list = []
	for post in user_feed_info:
		caption = process_text(post['node']['caption']['text'])
		if len(caption) > 0:
			index += 1
			text_list.append(caption)
		if index >= int(postcount):
			break

	posts = '\n'.join(text_list)

	emoji_pattern = re.compile(u"(["                     # .* removed
u"\U0001F600-\U0001F64F"  # emoticons
u"\U0001F300-\U0001F5FF"  # symbols & pictographs
u"\U0001F680-\U0001F6FF"  # transport & map symbols
u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
u"(\\n)"
u"(#|@)"
                "])", flags= re.UNICODE) 

	posts = re.sub(r'[^a-zA-Z]+', ' ', posts, re.ASCII)
	posts = emoji_pattern.sub(u'', posts)

	return [[user_id,posts]]

def main():
	username = 'buzzfeedtasty'
	postcount = 10
	print(get_user_post(username, postcount))
	print("")
	username = 'leonardodicaprio'
	postcount = 10
	print(get_user_post(username, postcount))

if __name__ == "__main__":
	main()