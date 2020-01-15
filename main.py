import requests
import csv
import praw
import pylast
import config as cfg
from pprint import pprint
from datetime import datetime as DT
import os, sys

# create a lastfm instance
def lastfm_login():
    API_KEY = cfg.lastfm['LASTFM_KEY']
    API_SECRET = cfg.lastfm['LASTFM_SECRET']

    username = cfg.lastfm['LASTFM_USERNAME']
    password_hash = pylast.md5(cfg.lastfm['LASTFM_PASSWORD'])

    network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET,
     username=username, password_hash=password_hash)
    return network

# creat a reddit oauth instance
def refresh_oauth_login_token():
    reddit = praw.Reddit(client_id = cfg.reddit['client_id'], 
    client_secret = cfg.reddit['client_secret'],
    user_agent = cfg.reddit['user_agent'],
    username = cfg.reddit['username'],
    password = cfg.reddit['password'])
    return reddit

def get_reddit_submissions(reddit):
    return reddit.subreddit('test_py_bots').new(limit=2)

def get_lastfm_artist(last_fm,artist_name):
    return last_fm.get_artist(artist_name)

def reply_to_submission(last_fm,reddit,submission):
    submission_title = reddit.submission(id=submission.id).title
    submission_url = reddit.submission(id=submission.id).url
    artist_name = submission_title.split(' -')[0]
    artist = get_lastfm_artist(last_fm, artist_name)
    listeners = artist.get_listener_count()
    if listeners > 250000:
        comment = 'Sorry bud, the artist you posted is too popular'
        flag_for_removal(reddit, submission)
    else:
        desc = artist.get_bio_summary()
        plays = artist.get_playcount()
        top_tags = artist.get_top_tags(limit = 5)
        tag_str = ''
        last_fm_url = artist.get_url()
        for tag in top_tags:
            tag_str += tag.item.get_name()
        comment = '**' + artist_name + '** \n\n'
        comment += '>' + desc + '\n\n'
        comment += '[last.fm]('+ last_fm_url +'): ' + str(format(listeners)) + ' listeners,' + str(format(plays)) + ' plays \n\n'
        comment += 'tags: *' + tag_str + '* \n\n'
    submission.reply(comment)

def flag_for_removal(reddit, submission):
    print('TODO logic to remove submission')

def main():
    os.chdir(sys.path[0])
    reddit = refresh_oauth_login_token()
    last_fm = lastfm_login()
    submissions = get_reddit_submissions(reddit)
    for post in submissions:
        reply_to_submission(last_fm,reddit,post)

if __name__ == "__main__": 
    main() 