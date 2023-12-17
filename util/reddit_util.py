import praw

def initialize_reddit(config):
    client_id = config['REDDIT']['CLIENT_ID']
    client_secret = config['REDDIT']['CLIENT_SECRET']
    password = config['REDDIT']['PASSWORD']
    username = config['REDDIT']['USERNAME']

    return praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        password=password,
        username=username,
        user_agent='Azuracast Request Bot v1.0 by ARandomBoiIsMe'
    )

# I hate everything about this.
def get_new_comments(reddit, submission_id, last_comment=None):
    comments = reddit.submission(id=submission_id).comments

    if last_comment is None:
        return comments
    
    new_comments = []
    
    for comment in comments:
        if comment.created_utc > last_comment.created_utc:
            new_comments.append(comment)

    return new_comments
