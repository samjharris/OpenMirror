##############################################################################################
# news.py ####################################################################################
##############################################################################################
# Helper functions for interfacting with the Yahoo News RSS feed. ############################
##############################################################################################

import feedparser
from bs4 import BeautifulSoup
#pip install beautifulsoup4

##############################################################################################
# get_news_rss() #############################################################################
##############################################################################################
# Use feedparser library to get Yahoo News RSS feed. #########################################
##############################################################################################
####Returns: 
#'data.entries' - a neat dict containing Yahoo News info we want
#                 *Note that there should always be 50 entries, so we
#                  don't need to worry about index errors too much
def get_news_rss():
	news_rss_url = "https://news.yahoo.com/rss"
	try:
		data = feedparser.parse(news_rss_url)
		return (data.entries)
	except:
		data = []
		return (data)

##############################################################################################
# cycle_news_rss() ###########################################################################
##############################################################################################
# Get 4 posts from RSS data ##################################################################
# (Cycle through 12 top posts, 4 at a time) ##################################################
##############################################################################################
###Params: 
#'entries' - data.entries object from parsed RSS feed
#'cur' - int 0-2, represents which chunk of posts are active
###Returns:
#'posts' - object containing active posts
#'cur' - updated chunk index
def cycle_news_rss(entries, cur):
	posts = {'p1':entries[0 + (4*cur)],
			 'p2':entries[1 + (4*cur)],
			 'p3':entries[2 + (4*cur)],
			 'p4':entries[3 + (4*cur)]}

	cur = (cur+1)%3
	return (posts, cur)

##############################################################################################
# get_post_title() ###########################################################################
##############################################################################################
# Get title of argument post #################################################################
##############################################################################################
###Params:
#'post' - post to extract data from
###Returns:
#'' - Article title
def get_post_title(post):
	return (post.title)

##############################################################################################
# get_post_time() ############################################################################
##############################################################################################
# Get published datetime of argument post (ISO Standard) #####################################
##############################################################################################
###Params:
#'post' - post to extract data from
###Returns:
#'' - post's ISO DATETIME
def get_post_time(post):
	return (post.published)

##############################################################################################
# get_post_preview() #########################################################################
##############################################################################################
# Get summary of argument post, stripped of HTML tags. This ##################################
# will often be a long paragraph, so we limit the length in ##################################
# main.py. ###################################################################################
##############################################################################################
###Params:
#'post' - post to extract data from
###Returns:
#'' - Article preview, stripped of HTML tags
def get_post_preview(post):
	return (BeautifulSoup(posts['p1'].summary, 'html.parser').text)

##############################################################################################
# get_post_imgurl() ##########################################################################
##############################################################################################
# Get link to the thumbnail argument post, for rendering and##################################
# display in main.py. Yahoo uses a standard size of 86x130, ##################################
# so we throw a warning if the returned image is different. ##################################
##############################################################################################
###Params:
#'post' - post to extract data from
###Returns:
#'' - URL to the post's 86x130 (expected dimensions) jpg thumbnail 
def get_post_imgurl(post):
	if post.media_content[0]['height'] != '86' and post.media_content[0]['width'] != '130':
		print("Warning in news.py: Yahoo News RSS image is not the expected size. Ignoring.")
	return (post.media_content[0]['url'])

