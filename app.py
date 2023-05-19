"""
Notes
Each of these is an endpoint to be recreated on the C# server. Of course, they are just dummy endpoints for helping test
the frontend and having a guide for implementation. Of course, these are changeable because everything changes when 
actual implementation happens. Each one has 2 fields: Backend entered, and frontend entered. If you finish using the 
endpoint, put in the date so we know there isn't anything else needed. That way, if you're working and need a change,
you know who to let know about it.
I also don't know exactly how dotnet expects the body to be received. I just have it using the request post data, but
it is worth figuring out if that works in the same way.
I also also don't know what it expects for firebase's user stuff. I have it in the body, that needs to be looked into
"""


from collections import UserString
from flask import Flask, request, jsonify
import json
import datetime
import uuid
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "http://localhost:8080"}})

# start of auth code

# USER object for testing
USER = {
        'id': 987,
        'email': 'test@gmail.com',
        'username': 'JoshuaOne',
        'coins': 123,
        'nativeLanguages':{
            'language':2,
            'level': 0
        },
        'learningLanguages':[{
            'language':1,
            'level':0,
        }],
        'gameBuckets':[{
            'language':1,
            'level':0,
        }],
        'wordModifier':5,
        'allowedWords':20
    }

# array of users for testing
USERS = [USER]

# POSTS a user. Since the login form only deals with a user's id,email,and password those are the only values we
# retrieve using request func
@app.route('/api/Users/', methods=['POST'])
def new_user():
    output_object = {'status': 'success'}

    post_data = request.get_json()
    add_user = {
        'id': post_data.get('id'),
        'email': post_data.get('email'),
        'username': post_data.get('username'),
        'coins': 123,
        'nativeLanguages':{
            'language': 0,
            'level': 0
        },
        'learningLanguages':[{
            'language': 0,
            'level':0,
        }],
        'gameBuckets':[{
            'language':1,
            'level':0,
        }],
        'wordModifier':5,
        'allowedWords':20
    }
    # add user to the "database" of users
    USERS.append(add_user)
    output_object['message'] = 'User added'
    return jsonify(output_object)

@app.route('/api/Users/<email>', methods=['GET'])
def get_user(email):
    return {
        'id': '12345',
        'email': email,
        'username': 'username',
        'coins': 123,
        'nativeLanguages':{
        },
        'learningLanguages':[{
            'language':1,
            'level':0,
        }],
        'gameBuckets':[{
            'language':1,
            'level':0,
        }],
        'wordModifier':5,
        'allowedWords':20
    }

# helper method to see if USERS is updating
@app.route('/api/all', methods=['GET'])
def get_all():
    return jsonify(USERS)

# updates a user by grabbing their ID and removing that user, then replaces that user with a copy
# of the user data that contains the updated language_id
@app.route('/api/Users/<language_id>/addLearningLanguage', methods=['PUT'])
def user_learning(language_id):
    output_object = {'status':'success'}
    if request.method == "PUT":
        post_data = request.get_json()
        user_to_remove = post_data.get('id')
        users_to_remove = []  # List to store users to be removed
        for user in USERS:
            if user["id"] == user_to_remove:
                users_to_remove.append(user)
                break  # Exit the loop after finding the user
        # Remove the users from the USERS list
        for user in users_to_remove:
            USERS.remove(user)
        put_user = {
        'id': 567,
        'email': post_data.get('email'),
        'username': post_data.get('username'),
        'coins': 123,
        'nativeLanguages':{
            'language': 0,
            'level': 0
        },
        'learningLanguages':[{
            'language': language_id,
            'level':0,
        }],
        'gameBuckets':[{
            'language':1,
            'level':0,
        }],
        'wordModifier':5,
        'allowedWords':20
    }
    USERS.append(put_user)
    output_object['message'] = "User's language learning updated"
    return jsonify(output_object)


@app.route('/api/Users/<language_id>/addNativeLanguage', methods=['PUT'])
def user_native(language_id):
    output_object = {'status':'success'}
    if request.method == "PUT":
        post_data = request.get_json()
        user_to_remove = post_data.get('id')
        users_to_remove = []  # List to store users to be removed
        for user in USERS:
            if user["id"] == user_to_remove:
                users_to_remove.append(user)
                break  # Exit the loop after finding the user
        # Remove the users from the USERS list
        for user in users_to_remove:
            USERS.remove(user)
        put_user =  {
        'id': 567,
        'email': post_data.get('email'),
        'username': post_data.get('username'),
        'coins': 123,
        'nativeLanguages':{
            'language': language_id,
            'level': 0
        },
        'learningLanguages':[{
            'language': 0,
            'level':0,
        }],
        'gameBuckets':[{
            'language':1,
            'level':0,
        }],
        'wordModifier':5,
        'allowedWords':20
    }
    USERS.append(put_user)
    output_object['message'] = "User's native language updated"
    return jsonify(output_object)


# end of auth code










# start of library code

@app.route('/api/Breakdown/Words/<lanugage_id>/<to_language_id>', methods=['POST'])
def breakdown_words(language_id, to_language_id):
    """
    Purpose: For a sentence, break into words and give info on each one including info about the users relationship to
    the word

    Possible implementation: For some languages (ZH, JP, KR), the python api should use a library to break the sentence
    apart. For the C# code, search each word using “forms” and find words that haven’t been used yet

    Backend Implemented:
    Frontend Implemented:
    """
    # PARAMETERS
    sentence = request.args.get('sentence')  # A string. The sentence to break down
    user_id = request.args.get('user_id')  # Possibly taken care of by firebase

    # RETURN
    return json.dumps({
        'language': language_id,  # Possible that this has changed. Should langauge detection be frontend or backend?
        'words': [{
            'word': 'Running',  # Just the word that was given
            'base': 'Run',  # The base word for the given word
            'base_id': 7253845,  # The user will want to reference this if they want to add the word to their lbrary
            'user_word_id': 578359234,
            # The ID of the user specific instance of the word. Null if the user doesn't have this word yet
            'last_used': f"{datetime.datetime.now()}",  # From the user word. -1 if there is no user grammar
            'times_used': 4,  # From the user word. -1 if there is no user word
            # Maybe just make this the user_word object?
            'translation': [
                {
                    'language_id': 3,  # The langauge it is translated into
                    'translation': 'Courir'  # The translation in that language
                }
            ],  # It is possible that they have multiple languages they speak, or a word has multiple translations.
            'tags': ['present continuous', 'verb'],  # The tags associated with the word
        }]  # Do this for each word in the sentence
    })


@app.route('/api/Breakdown/Grammars/<language_id>/<to_language_id>', methods=['POST'])
def breakdown_grammars(language_id, to_language_id):
    """
    Purpose: The frontend will check the most popular 100 grammars. Each is just a regex, and that should be fairly
    quick. However, the user can pay coins to check ALL created grammars. (Unless they are pro, then it is free).
    From there, the user can add teh grammar to their personal deck, or click the link to learn more about it.

    Possible implementation: Done in two parts: First, create a Tongues-searchable string by having first the base word,
    followed by / and then the tags. So "I am running" becomes "I/subject/pronoun be/verb/present/i-conjugation run/
    present-continuous". The grammars are a series of regexes that can be built by a GUI that are able to search these
    strings, and return the associated resources (If it detects /subject/ be/ /present-continuous/, link to a video
    or article explaining the present continous form)

    Backend Implemented:
    Frontend Implemented:
    """
    print("recieved")
    print(request.get_json())
    # Parameters
    sentence = request.args.get('sentence')  # A string. The sentence to break down
    user_id = request.args.get('user_id')  # Possibly taken care of by firebase

    # RETURN
    return json.dumps({
        'language': language_id,  # Possible that this has changed. Should langauge detection be frontend or backend?
        'grammars': [{
            'name': 'Present Continous',  # Just the word that was given
            'base_id': 7253845,  # The user will want to reference this if they want to add the word to their library
            'user_grammar_id': 578359234,
            # The ID of the user specific instance of the word. Null if the user doesn't have this word yet
            'last_used': f"{datetime.datetime.now()}",  # From the user grammar. -1 if there is no user grammar
            'times_used': 4,  # From the user word. -1 if there is no user word
            # Maybe just make this the user_grammar object?
            'links': [
                {
                    'language_id': to_language_id,
                    'description': "1 minute video by english speakers",  # The langauge it is translated into
                    'resource': 'http://example.com/present-continous'  # The translation in that language
                }
            ],
        }]  # Do this for each word in the sentence
    })


@app.route('/api/Breakdown/Analysis/<language_id>', methods=['POST'])
def breakdown_analysis(language_id):
    """
    Purpose: Not every grammar will be implemented because there are just so many that it could be infinate. If the user
    is not satisfied with the breakdown, they can send the sentence to an expert (or maybe chat-GPT) to recieve a more
    personalized breakdown. This should also go to a list of "unregistered sentences" so someone can figure out what the
    grammar is, and decide if we have it or not in our database and configure if not.


    Backend Implemented:
    Frontend Implemented:
    """

    # Parameters
    sentence = request.args.get('sentence')  # A string. The sentence to break down
    user_id = request.args.get('user_id')  # Possibly taken care of by firebase

    return json.dumps({
        'explaination': 'Basically, you\'re dumb'
        # We could do this if we go the chatGPT route. Otherwise, status:success and send it to a real person we hire
        # It might need to be reviewed by a real person anyways so we can be on top of new grammars
    })


@app.route('/api/Words/<language_id>/All', methods=['GET'])
def get_words(language_id):
    """
    Purpose: A user has a list of words that they are learning. Search allows us to search for specific text within
    our list, and the max and start index are for pagination purposes so we don't get the whole thing at once.

    Backend Implemented: 4/24/23 (not reviewed)
    Frontend Implemented:
    """

    # Parameters
    user_id = request.args.get('user_id')  # Possibly taken care of by firebase
    search = request.get_json['search']  # A string. Search base words
    max = request.args.get('max')  # An int. How many are expected (for pagination)
    start_index = request.args.get('start_index')  # An int. What index to start on (for pagination)

    # Returns userwords.
    return json.dumps([
        {
            'id': '57284305',  # The ID in mysql. This should be used to reference the word in the future.
            'publicId': '7589024758',  # The ID of the public word in mysql
            # Here, I would like to join the user word with the public word data. However, I don't know
            # what that will look like with the json. This is just a guess.
            'publicWord': {
                'id': '7589024758',  # The ID of the public word in mysql
                'word': 'Courir',
                'language': 3,
                'translations': [{
                    'language': 0,
                    'translation': 'run'
                }]
            },
            'word': 'run',
            'timesUsed': 12,
            'lastUsed': 'datetime_object',  # I don't know how this will actually show up.
            'archived': False
        }
    ])


@app.route('/api/Words/<user_word_id>', methods=['DELETE'])
def delete_word(user_word_id):
    """
    Purpose: Delete a use word. Puts it into archive, which means we don't have to search it when getting lists
    of words

    Backend Implemented: 4/24/23 (not reviewed)
    Frontend Implemented:
    """

    # Parameters
    user_id = request.args.get('user_id')  # Possibly taken care of by firebase

    # Return
    return json.dumps({'status': 'success'})


@app.route('/api/Words/<word_id>', methods=['POST'])
def post_word(word_id):  # Note: Public word ID
    """
    Purpose: If a user wants to add a word to their library, do so with the public word id.

    Backend Implemented: 4/24/23 (not reviewed)
    Frontend Implemented:
    """

    # Parameters
    user_id = request.args.get('user_id')  # Possibly taken care of by firebase

    # Return
    return json.dumps({'status': 'success'})


@app.route('/api/Words/Multiple', methods=['POST'])
def post_words():
    """
    Purpose: If a user wants to add a list of words to their library, do so with the public word ids.

    Backend Implemented: 4/24/23 (not reviewed)
    Frontend Implemented:
    """

    # Parameters
    user_id = request.args.get('user_id')  # Possibly taken care of by firebase
    words = request.args.get('words')  # A list of public word ids

    # Return
    # Returns userwords.
    return json.dumps([
        {
            'id': '57284305',  # The ID in mysql. This should be used to reference the word in the future.
            'publicId': '7589024758',  # The ID of the public word in mysql
            # Here, I would like to join the user word with the public word data. However, I don't know
            # what that will look like with the json. This is just a guess.
            'publicWord': {
                'id': '7589024758',  # The ID of the public word in mysql
                'word': 'Courir',
                'language': 3,
                'translations': [{
                    'language': 0,
                    'translation': 'run'
                }]
            },
            'word': 'run',
            'timesUsed': 0,
            'lastUsed': -1,  # I don't know how this will actually show up.
            'archived': False
        }
    ])


@app.route('/api/Grammars/<language_id>/All', methods=['GET'])
def get_grammars(language_id):
    """
    Purpose: A user has a list of grammars that they are learning. Search allows us to search for specific text within
    our descriptions, and the max and start index are for pagination purposes so we don't get the whole thing at once.

    Backend Implemented:
    Frontend Implemented:
    """

    # Parameters
    user_id = request.args.get('user_id')  # Possibly taken care of by firebase
    search = request.get_json['search']  # A string. Search base words
    max = request.args.get('max')  # An int. How many are expected (for pagination)
    start_index = request.args.get('start_index')  # An int. What index to start on (for pagination)

    # Returns usergrammars.
    return json.dumps([
        {
            'id': '57284305',  # The ID in mysql. This should be used to reference the grammar in the future.
            'publicId': '7589024758',  # The ID of the public grammar in mysql
            # Here, I would like to join the user grammar with the public grammar data. However, I don't know
            # what that will look like with the json. This is just a guess.
            'publicGrammar': {
                'id': '7589024758',  # The ID of the public grammar in mysql
                'description': 'there once was',
                'searchTerm': '/search with this regex/',
                'language': 3,
                'links': [{
                    'language': 3,
                    'link': 'https://example.com'
                }]
            },
            'timesUsed': 12,
            'lastUsed': 'datetime_object',  # I don't know how this will actually show up.
            'archived': False
        }
    ])


@app.route('/api/Grammars/<user_grammar_id>', methods=['DELETE'])
def delete_grammar(user_grammar_id):
    """
    Purpose: Delete a user grammar. Puts it into archive, which means we don't have to search it when getting lists
    of grammars

    Backend Implemented:
    Frontend Implemented:
    """

    # Parameters
    user_id = request.args.get('user_id')  # Possibly taken care of by firebase

    # Return
    return json.dumps({'status': 'success'})


@app.route('/api/Grammars/<grammar_id>', methods=['POST'])
def post_grammar(word_id):
    """
    Purpose: If a user wants to add a word to their library, do so with the public word id.

    Backend Implemented:
    Frontend Implemented:
    """

    # Parameters
    user_id = request.args.get('user_id')  # Possibly taken care of by firebase

    # Return
    return json.dumps({'status': 'success'})


@app.route('/api/Grammars/', methods=['POST'])
def new_grammar(word_id):
    """
    Purpose: Create a new grammar. This should be added to the users' grammar, as well as
    go to the moderation system.

    Backend Implemented:
    Frontend Implemented:
    """
    # Parameters
    user_id = request.get_json()['user_id']  # Possibly taken care of by firebase

    description = request.get_json()['description']  # Quick description
    searchTerm = request.get_json()['searchTerm']  # Regex search
    language = request.get_json()['language']  # Target Language
    from_language = request.get_json()['from_language']  # Language of link
    link = request.get_json()['link']

    # Return
    return json.dumps({'status': 'success'})


@app.route('/api/Packs', methods=['POST'])
def post_pack():
    """
    Purpose: When the user posts a pack, we want to put it into the public.

    Backend Implemented:
    Frontend Implemented:
    """

    # Parameters
    userId = request.args.get('userId')  # Possibly taken care of by firebase
    wordList = request.args.get('wordList')  # List of Public word IDs
    grammarList = request.args.get('grammarList')  # List of Grammar IDs
    description = request.args.get('description')  # String: A basic description
    link = request.args.get('link')  # String: The link to where the words were found
    level = request.args.get('level')  # INT
    tags = request.args.get('tags')  # An array of strings. We might not even use this.

    # Return
    return json.dumps({'status': 'success'})


@app.route('/api/Packs/<userId>', methods=['GET'])
def get_packs(userId):
    """
    Purpose: For a user to manage their own packs. See what packs they have created, and accept the
    money they have earned from it.

    Backend Implemented:
    Frontend Implemented:
    """

    # Parameters
    max = request.args.get('max')  # An int. How many are expected (for pagination)
    startIndex = request.args.get('startIndex')  # An int. What index to start on (for pagination)

    # Return
    return json.dumps([{
        'id': '5728903457',  # The ID
        'level': 6,
        'description': 'blah blah blah',
        'link': 'https://example.com',
        'words': [{
            'id': '7589024758',  # The ID of the public word in mysql
            'word': 'Courir',
            'language': 3,
            'translations': [{
                'language': 0,
                'translation': 'run'
            }]
        }],  # These are the public words. Maybe just do the first 5 for efficiency, and see the rest on the detail page
        'wordLength': 10,  # Only do this if we decide to just send the first 5 words
        'publicGrammar': {
            'id': '7589024758',  # The ID of the public grammar in mysql
            'description': 'there once was',
            'searchTerm': '/search with this regex/',
            'language': 3,
            'links': [{
                'language': 3,
                'link': 'https://example.com'
            }]
        },
        'grammarLength': 3,
        'owedCoins': 125,  # Coins not yet recieved
        'earnedCoins': 5000,  # All coins for this user
        'tags': ['Sports', 'Tech', 'Your Mom']
    }])


@app.route('/api/Packs/<packId>/accept_coins', methods=['POST'])
def accept_coins(packId):
    """
    Purpose: In the users' pack management, they can click a button and receive the coins for that pack.

    Backend Implemented:
    Frontend Implemented:
    """

    # Parameters

    # Return
    return json.dumps({'status': 'success'})


@app.route('/api/Packs/<packId>', methods=['DELETE'])
def delete_pack(packId):
    """
    Purpose: Delete a pack :(

    Backend Implemented:
    Frontend Implemented:
    """

    # Parameters

    # Return
    return json.dumps({'status': 'success'})


@app.route('/api/Packs/Imported', methods=['GET'])
def get_imported_packs():
    """
    Purpose: The packs that the user has imported in the past (Store as a foreign key or something like that)

    Backend Implemented:
    Frontend Implemented:
    """

    # Parameters
    userId = request.args.get('userId')  # Possibly taken care of by firebase
    max = request.args.get('max')  # An int. How many are expected (for pagination)
    startIndex = request.args.get('startIndex')  # An int. What index to start on (for pagination)

    # Return
    return json.dumps([{
        'id': '5728903457',  # The ID
        'level': 6,
        'description': 'blah blah blah',
        'link': 'https://example.com',
        'words': [{
            'id': '7589024758',  # The ID of the public word in mysql
            'word': 'Courir',
            'language': 3,
            'translations': [{
                'language': 0,
                'translation': 'run'
            }]
        }],  # These are the public words. Maybe just do the first 5 for efficiency, and see the rest on the detail page
        'wordLength': 10,  # Only do this if we decide to just send the first 5 words
        'publicGrammar': {
            'id': '7589024758',  # The ID of the public grammar in mysql
            'description': 'there once was',
            'searchTerm': '/search with this regex/',
            'language': 3,
            'links': [{
                'language': 3,
                'link': 'https://example.com'
            }]
        },
        'grammarLength': 3,
        'tags': ['Sports', 'Tech', 'Your Mom']
    }])


@app.route('/api/Packs', methods=['GET'])
def get_public_packs():  # Note: Public grammar ID
    """
    Purpose: See public popular or new packs

    Backend Implemented:
    Frontend Implemented:
    """

    # Parameters
    user_id = request.args.get('user_id')  # Possibly taken care of by firebase
    tag = request.args.get('tag')  # For searching by interests
    level = request.args.get('level')  # For searching by level
    max = request.args.get('max')  # An int. How many are expected (for pagination)
    startIndex = request.args.get('startIndex')  # An int. What index to start on (for pagination)

    # Return
    return json.dumps([{
        'id': '5728903457',  # The ID
        'level': 6,
        'description': 'blah blah blah',
        'link': 'https://example.com',
        'words': [{
            'id': '7589024758',  # The ID of the public word in mysql
            'word': 'Courir',
            'language': 3,
            'translations': [{
                'language': 0,
                'translation': 'run'
            }]
        }],  # These are the public words. Maybe just do the first 5 for efficiency, and see the rest on the detail page
        'wordLength': 10,  # Only do this if we decide to just send the first 5 words
        'publicGrammar': {
            'id': '7589024758',  # The ID of the public grammar in mysql
            'description': 'there once was',
            'searchTerm': '/search with this regex/',
            'language': 3,
            'links': [{
                'language': 3,
                'link': 'https://example.com'
            }]
        },
        'grammarLength': 3,
        'tags': ['Sports', 'Tech', 'Your Mom']
    }])


@app.route('/api/Packs/View/<packId>', methods=['GET'])
def view_pack(packId):  # Note: Public grammar ID
    """
    Purpose: If the user wants to see a more detailed view of a pack, view it here.
    Possibly add info on the creator, I don't know.

    Backend Implemented:
    Frontend Implemented:
    """

    # Parameters
    user_id = request.args.get('user_id')  # Possibly taken care of by firebase

    # Return
    return json.dumps({
        'id': '5728903457',  # The ID
        'level': 6,
        'description': 'blah blah blah',
        'link': 'https://example.com',
        'words': [{
            'id': '7589024758',  # The ID of the public word in mysql
            'word': 'Courir',
            'language': 3,
            'translations': [{
                'language': 0,
                'translation': 'run'
            }]
        }],
        'publicGrammar': {
            'id': '7589024758',  # The ID of the public grammar in mysql
            'description': 'there once was',
            'searchTerm': '/search with this regex/',
            'language': 3,
            'links': [{
                'language': 3,
                'link': 'https://example.com'
            }]
        },
        'tags': ['Sports', 'Tech', 'Your Mom']
    })


@app.route('/api/Packs/Import/<packId>', methods=['POST'])
def import_pack(packId):
    """
    Purpose: Take all the words and grammars belonging to this pack, and add them to the user's library.
    Add the pack to the user's imported packs as well, and increase the earned and total coins of the pack.

    Backend Implemented:
    Frontend Implemented:
    """

    # Parameters
    userId = request.get_json()['userId']

    # Return
    return json.dumps({'status': 'success'})


if __name__ == '__main__':
    app.run()


@app.route('/api/Words/<word_id>/use', methods=['POST'])
def use_word(word_id):
    """
    Purpose: When a user uses a word, we want to mark that it has been used, and
    that the last used date was today. Recalculate the scores for spaced repitition.

    Backend Implemented:
    Frontend Implemented:
    """

    # Parameters
    userId = request.get_json()['userId']

    # Return
    return json.dumps({'status': 'success'})


@app.route('/api/Moderation/Words', methods=['GET', 'PUT', 'POST'])
def moderation_manager(word_id):
    """
    Purpose: GET: Get all of the word changes that are in moderation.
    POST: Make a new request for the moderators to view
    PUT: Make a moderation decision. If approved, change the word accordingly.

    Backend Implemented:
    Frontend Implemented:
    """

    # Parameters
    userId = request.get_json()['userId']

    if request.method == "POST":
        new_translation = request.get_json()['new_translation']
        delete_translation = request.get_json()['delete_translation']
    elif request.method == "GET":
        max = request.get_json()['max']  # An int. How many are expected (for pagination)
        start_index = request.get_json()['start_index']  # An int. What index to start on (for pagination)
    else:
        decision = request.get_json()['decision']  # True or False
    # Return
    return json.dumps({'status': 'success'})


@app.route('/api/Moderation/Grammars', methods=['GET', 'PUT', 'POST'])
def moderation_manager_grammar(word_id):
    """
    Purpose: GET: Get all of the grammar changes that are in moderation.
    POST: Make a new request for the moderators to view
    PUT: Make a moderation decision. If approved, change the word accordingly.

    Backend Implemented:
    Frontend Implemented:
    """

    # Parameters
    userId = request.get_json()['userId']

    if request.method == "POST":
        new_link = request.get_json()['new_link']
        remove_link = request.get_json()['remove_link']
    elif request.method == "GET":
        max = request.get_json()['max']  # An int. How many are expected (for pagination)
        start_index = request.get_json()['start_index']  # An int. What index to start on (for pagination)
    else:
        decision = request.get_json()['decision']  # True or False
    # Return
    return json.dumps({'status': 'success'})


if __name__ == '__main__':
    app.run()
