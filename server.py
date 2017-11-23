from flask import Flask, render_template, request, jsonify, flash, redirect
import twitter, os, markov

api = twitter.Api(
    consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
    consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
    access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
    access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

app = Flask(__name__)

app.secret_key = os.environ['APP_SECRET_KEY']

#cache tweets with a dict as long as server is not reset
tweets = {}

@app.route('/')
def index():
    """Renders username input form and tweets."""
    return render_template('/homepage.html')


@app.route('/search_user.json')
def searches_user():
    """Gets username input and generates tweet via Markov chains.
    
    Validates twitter user: if user is not private, does not exist,
    or does not have enough tweets.

    """

    username = request.args.get('username')
    
    size = int(request.args.get('chain-size'))

    tweets['username'] = username

    try:
        statuses = api.GetUserTimeline(screen_name=username,
                                       include_rts=False,
                                       count=200)
        
        text = ' '.join([s.text for s in statuses])

        if len(text) < size:
            tweets[username] = ['Invalid user! User is either not public \
                               or does not have enough tweets.']
        
        else:
            chains = markov.make_chains(text, size)

            random_text = markov.make_text(chains, size)

            tweets.setdefault(username, [])

            tweets[username].append(random_text)

    
    except twitter.TwitterError:
        tweets[username] = ['Please enter a valid Twitter user!']

    return jsonify(tweets)



if __name__ == '__main__':
    app.debug = True
    
    app.run(port=5000, host='0.0.0.0')