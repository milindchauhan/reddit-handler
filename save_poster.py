import praw

def crosspost(post, subreddit):
	'''crosspost a Submission instance to a given subreddit'''
	try:
		post.crosspost(subreddit, send_replies=False)
	except:
		pass


def submit_comment(post, subreddit):
	'''submit a given Comment instance to a given subreddit'''

	#extracting post author name
	try:
		pa_name = post.author.name 
	except:
		pa_name = '[deleted]'

	#get the title and body ready for the comment post.
	title_string='''{0} commented on "{1}"'''.format(pa_name, post.submission.title)
	body_string="{0} \n\n[link to submission that the comment belongs to](https://www.reddit.com{1}) \n\n[link to comment](https://www.reddit.com{2})".format(post.body, post.submission.permalink, post.permalink)
	print(title_string,'\n\n')

	#initialize Subreddit instance
	subreddit_instance = reddit.subreddit(subreddit)
	
	#post comment
	try:	
		subreddit_instance.submit(title=title_string,selftext=body_string)
	except:
		pass

def set_of_post_ids(list_of_posts):
	'''creates a set of ids of posts from the list given to it'''
	set_of_posts = set()

	for post in list_of_posts:
		set_of_posts.add(post.id)

	return set_of_posts

def update_savedposts_subreddit(subreddit, post_limit = 100):
	'''
	************** W A R N I N G *****************************
	this is wrong. I was checking for new posts from saved by hashing ids of posts in
	the subreddit to be updated and comparing the post ids from saved to see if they were
	in the set. If they were that would mean they're old post.

	but there is a problem. When a saved post is posted to the subreddit, it will have a 
	different id than the saved post which is not the desired behavior.
	'''
	#initialize Reddit instance with 'save_poster' settings field in the ini file
	reddit = praw.Reddit('save_poster')

	id_set = set_of_post_ids(reddit.subreddit(subreddit).new(limit = post_limit))

	for post in reddit.user.me().saved(limit = 500):
		if post.id not in set_of_post_ids:
			if isinstance(post,praw.models.Submission):
				'''Submission instance: crosspost it'''
				print(post.title,'\n\n')
				#crosspost_saved_posts(post, subreddit)	

			else:
				'''Comment instance: post it'''
				print(post.submission.title)
				#submit_comment(post, subreddit)
				


def main():
	#subreddit name to be passed
	subreddit = 'name of the subreddit you want to post in'

	#update your subreddit assigned for storing saved posts
	update_savedposts_subreddit(subreddit)
	
	

if __name__ == '__main__':
	main()
	
