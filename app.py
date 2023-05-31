from flask import Flask, request
import json
import datetime
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


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


@app.route('/api/Users/', methods=['POST'])
@cross_origin()
def new_user():
    return None

@app.route('/api/Users/<email>', methods=['GET'])
@cross_origin()
def get_user(email):
    return {
        'id': '12345',
        'email': email,
        'username': 'username',
        'coins': 123,
        'nativeLanguages':[{
            'language':1,
            'level':0,
        }],
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

@app.route('/api/Users/<language_id>/addLearningLanguage', methods=['Put'])
@cross_origin()
def user_learning(language_id):
    return None

@app.route('/api/Users/<language_id>/addNativeLanguage', methods=['Put'])
@cross_origin()
def user_native(language_id):
    return None


@app.route('/api/Breakdown/Words/<lanugage_id>/<to_language_id>', methods=['POST'])
@cross_origin()
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
@cross_origin()
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
@cross_origin()
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
@cross_origin()
def get_words(language_id):
    """
    Purpose: A user has a list of words that they are learning. Search allows us to search for specific text within
    our list, and the max and start index are for pagination purposes so we don't get the whole thing at once.

    Backend Implemented: 4/24/23 (not reviewed)
    Frontend Implemented:
    """

    # Parameters
    user_id = request.args.get('user_id')  # Possibly taken care of by firebase
    search = request.args.get('search')  # A string. Search base words
    max = request.args.get('max')  # An int. How many are expected (for pagination)
    start_index = request.args.get('start_index')  # An int. What index to start on (for pagination)

    # Returns userwords.
    current_date = datetime.datetime.now().isoformat()  # Get the current date and time as a string
    WORD1 = {
    'id': '57284305',  # The ID in mysql. This should be used to reference the word in the future.
            'publicId': '7589024758',  # The ID of the public word in mysql
            # Here, I would like to join the user word with the public word data. However, I don't know
            # what that will look like with the json. This is just a guess.
            'publicWord': {
                'id': '7589024758',  # The ID of the public word in mysql
                'word': 'Courir',
                'language': 3,
                'translations': [{
                    'language': 1,
                    'translation': 'run'
                }]
            },
            'word': 'run',
            'timesUsed': 12,
            'lastUsed': current_date,  # I don't know how this will actually show up.
            'archived': False
    }
    WORD2 = {
        'id': '60282305',  # The ID in mysql. This should be used to reference the word in the future.
        'publicId': '5559024758',  # The ID of the public word in mysql
        # Here, I would like to join the user word with the public word data. However, I don't know
        # what that will look like with the json. This is just a guess.
        'publicWord': {
            'id': '5559024758',  # The ID of the public word in mysql
            'word': 'Manger',
            'language': 3,
            'translations': [{
                'language': 1,
                'translation': 'eat'
            }]
        },
        'word': 'eat',
        'timesUsed': 10,
        'lastUsed': current_date,  # I don't know how this will actually show up.
        'archived': False
    }
    WORD3 = {
        'id': '77282305',  # The ID in mysql. This should be used to reference the word in the future.
        'publicId': '7759024758',  # The ID of the public word in mysql
        # Here, I would like to join the user word with the public word data. However, I don't know
        # what that will look like with the json. This is just a guess.
        'publicWord': {
            'id': '7779024758',  # The ID of the public word in mysql
            'word': 'Coup',
            'language': 3,
            'translations': [{
                'language': 1,
                'translation': 'kick'
            }]
        },
        'word': 'kick',
        'timesUsed': 1000,
        'lastUsed': current_date,  # I don't know how this will actually show up.
        'archived': False
    }
    WORDS = [WORD3, WORD2, WORD1]
    return json.dumps(WORDS)

@app.route('/api/Words/<user_word_id>', methods=['PUT'])
@cross_origin()
def put_time(user_word_id):
    """
    Puprose: In order to calculate when a user last used a word, we have to be able to store the date of when they last accessed
    a word and perform some basic calculations with the current date in order to display the difference between when the word
    was last accessed and when it is currently accessed

    NOTE: I'm not 100% sure how multiple cards are going to be handled so for now I'm just going to implement this for CARD1
    """

@app.route('/api/Words/<user_word_id>', methods=['DELETE'])
@cross_origin()
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
@cross_origin()
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


@app.route('/api/Words/Public/<language>', methods=['GET'])
@cross_origin()
def get_public_word(language):
    """
    Purpose: A user can search for a word and get the public word. For example, search will be "running" and
    this function should return "run". In the backend, add any words that don't exist yet to our database.

    Backend Implemented: 4/24/23 (not reviewed)
    Frontend Implemented:
    """

    # Parameters
    user_id = request.args.get('user_id')  # Possibly taken care of by firebase
    search = request.args.get('search')  # This is the FORM. It is also an array of strings

    # Return
    return json.dumps([{
        'id': '7589024758',  # The ID of the public word in mysql
        'word': 'Courir',
        'language': 3,
        'translations': [{
            'language': 1,
            'translation': 'run'
        }]
    }])


@app.route('/api/Words/<language>/Multiple', methods=['POST'])
@cross_origin()
def post_words(language):
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
@cross_origin()
def get_grammars(language_id):
    """
    Purpose: A user has a list of grammars that they are learning. Search allows us to search for specific text within
    our descriptions, and the max and start index are for pagination purposes so we don't get the whole thing at once.

    Backend Implemented:
    Frontend Implemented:
    """

    # Parameters
    user_id = request.args.get('user_id')  # Possibly taken care of by firebase
    search = request.args.get('search')  # A string. Search base words
    max = request.args.get('max')  # An int. How many are expected (for pagination)
    start_index = request.args.get('start_index')  # An int. What index to start on (for pagination)

    # Returns usergrammars.
    GRAMMAR1 = {
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
        'timesUsed': 11,
        'lastUsed': 'datetime_object',  # I don't know how this will actually show up.
        'archived': False
    }
    GRAMMAR2 = {
        'id': '66284305',  # The ID in mysql. This should be used to reference the grammar in the future.
        'publicId': '7789024758',  # The ID of the public grammar in mysql
        # Here, I would like to join the user grammar with the public grammar data. However, I don't know
        # what that will look like with the json. This is just a guess.
        'publicGrammar': {
            'id': '7789024758',  # The ID of the public grammar in mysql
            'description': 'once upon',
            'searchTerm': '/search with this regex/',
            'language': 3,
            'links': [{
                'language': 3,
                'link': 'https://example.com'
            },
                {
                    'language':3,
                    'link': 'exampleTWO.com'
                }
            ]
        },
        'timesUsed': 1,
        'lastUsed': 'datetime_object',  # I don't know how this will actually show up.
        'archived': False
    }
    GRAMMARS = [GRAMMAR1, GRAMMAR2]
    return json.dumps(GRAMMARS)


@app.route('/api/Grammars/<user_grammar_id>', methods=['DELETE'])
@cross_origin()
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
    # {'status': 'success'}
    return json.dumps(user_grammar_id)


@app.route('/api/Grammars/<grammar_id>', methods=['POST'])
@cross_origin()
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
@cross_origin()
def new_grammar(word_id):
    """
    Purpose: Create a new grammar. This should be added to the users' grammar, as well as
    go to the moderation system.

    Backend Implemented:
    Frontend Implemented:
    """
    # Parameters
    user_id = request.args.get('user_id')  # Possibly taken care of by firebase

    description = request.args.get('description')  # Quick description
    searchTerm = request.args.get('searchTerm')  # Regex search
    language = request.args.get('language')  # Target Language
    from_language = request.args.get('from_language')  # Language of link
    link = request.args.get('link')

    # Return
    return json.dumps({'status': 'success'})


@app.route('/api/Packs', methods=['POST'])
@cross_origin()
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
@cross_origin()
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
@cross_origin()
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
@cross_origin()
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
@cross_origin()
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
@cross_origin()
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
@cross_origin()
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
@cross_origin()
def import_pack(packId):
    """
    Purpose: Take all the words and grammars belonging to this pack, and add them to the user's library.
    Add the pack to the user's imported packs as well, and increase the earned and total coins of the pack.

    Backend Implemented:
    Frontend Implemented:
    """

    # Parameters
    userId = request.args.get('userId')

    # Return
    return json.dumps({'status': 'success'})


if __name__ == '__main__':
    app.run()


@app.route('/api/Words/<word_id>/use', methods=['POST'])
@cross_origin()
def use_word(word_id):
    """
    Purpose: When a user uses a word, we want to mark that it has been used, and
    that the last used date was today. Recalculate the scores for spaced repitition.

    Backend Implemented:
    Frontend Implemented:
    """

    # Parameters
    userId = request.args.get('userId')

    # Return
    return json.dumps({'status': 'success'})


@app.route('/api/Moderation/Words', methods=['GET', 'PUT', 'POST'])
@cross_origin()
def moderation_manager(word_id):
    """
    Purpose: GET: Get all of the word changes that are in moderation.
    POST: Make a new request for the moderators to view
    PUT: Make a moderation decision. If approved, change the word accordingly.

    Backend Implemented:
    Frontend Implemented:
    """

    # Parameters
    userId = request.args.get('userId')

    if request.method == "POST":
        new_translation = request.args.get('new_translation')
        delete_translation = request.args.get('delete_translation')
    elif request.method == "GET":
        max = request.args.get('max')  # An int. How many are expected (for pagination)
        start_index = request.args.get('start_index')  # An int. What index to start on (for pagination)
    else:
        decision = request.args.get('decision')  # True or False
    # Return
    return json.dumps({'status': 'success'})


@app.route('/api/Moderation/Grammars', methods=['GET', 'PUT', 'POST'])
@cross_origin()
def moderation_manager_grammar(word_id):
    """
    Purpose: GET: Get all of the grammar changes that are in moderation.
    POST: Make a new request for the moderators to view
    PUT: Make a moderation decision. If approved, change the word accordingly.

    Backend Implemented:
    Frontend Implemented:
    """

    # Parameters
    userId = request.args.get('userId')

    if request.method == "POST":
        new_link = request.args.get('new_link')
        remove_link = request.args.get('remove_link')
    elif request.method == "GET":
        max = request.args.get('max')  # An int. How many are expected (for pagination)
        start_index = request.args.get('start_index')  # An int. What index to start on (for pagination)
    else:
        decision = request.args.get('decision')  # True or False
    # Return
    return json.dumps({'status': 'success'})

@app.route('/api')
@cross_origin()
def homepage():
    return "<h1>The server is working (API)</h1>"


if __name__ == '__main__':
    app.run()
