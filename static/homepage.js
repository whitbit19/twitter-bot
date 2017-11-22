$('#user-search').on('submit', findsUser)

function findsUser(evt) {

    evt.preventDefault();

    var formInputs = {
        'username': $('#username').val()
    };

    $.get('/search_user.json', formInputs, generatesTweets);

}

function generatesTweets(results) {
    
    var user = results.username;

    var tweets = results[user];

    $('#tweets').empty();

    for(var i = tweets.length-1; i > -1; i--) {
        $('#tweets').append('<li>' + tweets[i] + '</li>')
    }
}

