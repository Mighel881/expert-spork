from dotenv import load_dotenv
import os
import praw
from pymongo import MongoClient


load_dotenv()
database = MongoClient('mongodb+srv://<username>:{}@cluster0.1sdlk.mongodb.net/<project_name>?retryWrites=true&w=majority'.format(os.getenv('DATABASE_PASSWORD')))
reddit = praw.Reddit('<praw.ini bot config>')


def start():
    subreddit = reddit.subreddit('memes')
    for submission in subreddit.search('good bot'):
        submission.comment_sort = 'new'
        submission.comments.replace_more(limit=0)
        comments = submission.comments.list()

        for comment in comments:
            if is_added_to_passed_server(submission.id + comment.id) == False:
                if is_added_to_done_server(submission.id + comment.id) == False:
                    if contains_good_bot(comment.body):
                        if comment.reply('silly human') != None:
                            print(comment.body)
                            add_to_done_server(submission.id + comment.id)
                    else:
                        add_to_passed_server(submission.id + comment.id)


def contains_good_bot(body):
    return True if body.lower() == 'good bot' else False

def add_to_done_server(id):
    database.good_bot_reply.submissions.update_one({'id' : 'submission_ids'}, {'$push' : {'done_ids' : id.lower()}})

def add_to_passed_server(id):
    database.good_bot_reply.submissions.update_one({'id' : 'submission_ids'}, {'$push' : {'passed_ids' : id.lower()}})

def is_added_to_done_server(id):
    return database.good_bot_reply.submissions.count_documents({'done_ids' : id.lower()}) > 0

def is_added_to_passed_server(id):
    return database.good_bot_reply.submissions.count_documents({'passed_ids' : id.lower()}) > 0


start()
