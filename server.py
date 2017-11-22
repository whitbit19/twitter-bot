from flask import Flask, render_template, request, jsonify, flash, redirect
import twitter, os, markov

api = twitter.Api(
    consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
    consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
    access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
    access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

app = Flask(__name__)

app.secret_key = os.environ['APP_SECRET_KEY']

tweets = {}

@app.route('/')
def index():

    return render_template('/homepage.html')


@app.route('/search_user.json')
def searches_user():

    username = request.args.get('username')

    tweets['username'] = username

    try:
        statuses = api.GetUserTimeline(screen_name=username,
                                       include_rts=False,
                                       count=200)
        
        text = ' '.join([s.text for s in statuses])

        chains = markov.make_chains(text, 3)

        random_text = markov.make_text(chains, 3)

        tweets.setdefault(username, [])

        tweets[username].append(random_text)

        print tweets[username]

    
    except twitter.TwitterError:
        tweets[username] = ['Please enter a valid public user!']
        print tweets[username]

    return jsonify(tweets)



if __name__ == '__main__':
    app.debug = True
    
    app.run(port=5000, host='0.0.0.0')