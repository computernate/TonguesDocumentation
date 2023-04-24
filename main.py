from flask import Flask, request
import json
import datetime

app = Flask(__name__)

"""
Notes
Each of these is an endpoint to be recreated on the C# server. Of course, they are just dummy endpoints for helping test
the frontend and having a guide for implementation. Of course, these are changeable because everything changes when 
actual implementation happens. Each one has 2 fields: Backend entered, and frontend entered. If you finish using the 
endpoint, put in the date so we know there isn't anything else needed. That way, if you're working and need a change,
you know who to let know about it.
I also don't know exactly how dotnet expects the body to be received. I just have it using the request post data, but
it is worth figuring out if that works in the same way.
"""


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
    sentence = request.get_json()['sentence']  # A string. The sentence to break down
    user_id = request.get_json()['user_id']  # Possibly taken care of by firebase

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
    sentence = request.get_json()['sentence']  # A string. The sentence to break down
    user_id = request.get_json()['user_id']  # Possibly taken care of by firebase

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
    sentence = request.get_json()['sentence']  # A string. The sentence to break down
    user_id = request.get_json()['user_id']  # Possibly taken care of by firebase

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
    user_id = request.get_json()['user_id']  # Possibly taken care of by firebase
    search = request.get_json['search']  # A string. Search base words
    max = request.get_json()['max']  # An int. How many are expected (for pagination)
    start_index = request.get_json()['start_index']  # An int. What index to start on (for pagination)

    # Returns userwords.
    return json.dumps([
        {
            'id': '57284305',  # The ID in mysql. This should be used to reference the word in the future.
            'publicId': '7589024758',  # The ID of the public word in mysql
            # Here, I would like to join the user word with the public word data. However, I don't know
            # what that will look like with the json. This is just a guess.
            'publicWord':{
                'id': '7589024758',  # The ID of the public word in mysql
                'word':'Courir',
                'language':3,
                'translations':[{
                    'language':0,
                    'translation':'run'
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
    user_id = request.get_json()['user_id']  # Possibly taken care of by firebase

    # Return
    return json.dumps({'status': 'success'})


@app.route('/api/Words/<word_id>', methods=['POST'])
def post_word(word_id): #Note: Public word ID
    """
    Purpose: If a user wants to add a word to their library, do so with the public word id.

    Backend Implemented: 4/24/23 (not reviewed)
    Frontend Implemented:
    """

    # Parameters
    user_id = request.get_json()['user_id']  # Possibly taken care of by firebase

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
    user_id = request.get_json()['user_id']  # Possibly taken care of by firebase
    words = request.get_json()['words'] #A list of public word ids

    # Return
    # Returns userwords.
    return json.dumps([
        {
            'id': '57284305',  # The ID in mysql. This should be used to reference the word in the future.
            'publicId': '7589024758',  # The ID of the public word in mysql
            # Here, I would like to join the user word with the public word data. However, I don't know
            # what that will look like with the json. This is just a guess.
            'publicWord':{
                'id': '7589024758',  # The ID of the public word in mysql
                'word':'Courir',
                'language':3,
                'translations':[{
                    'language':0,
                    'translation':'run'
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
    user_id = request.get_json()['user_id']  # Possibly taken care of by firebase
    search = request.get_json['search']  # A string. Search base words
    max = request.get_json()['max']  # An int. How many are expected (for pagination)
    start_index = request.get_json()['start_index']  # An int. What index to start on (for pagination)

    # Returns usergrammars.
    return json.dumps([
        {
            'id': '57284305',  # The ID in mysql. This should be used to reference the grammar in the future.
            'publicId': '7589024758',  # The ID of the public grammar in mysql
            # Here, I would like to join the user grammar with the public grammar data. However, I don't know
            # what that will look like with the json. This is just a guess.
            'publicGrammar':{
                'id': '7589024758',  # The ID of the public grammar in mysql
                'description':'there once was',
                'searchTerm':'/search with this regex/',
                'language':3,
                'links':[{
                    'language':3,
                    'link':'https://example.com'
                }]
            },
            'timesUsed': 12,
            'lastUsed': 'datetime_object',  # I don't know how this will actually show up.
            'archived': False
        }
    ])


@app.route('/api/Grammars/<user_grammar_id>', methods=['DELETE'])
def delete_word(user_grammar_id):
    """
    Purpose: Delete a user grammar. Puts it into archive, which means we don't have to search it when getting lists
    of grammars

    Backend Implemented:
    Frontend Implemented:
    """

    # Parameters
    user_id = request.get_json()['user_id']  # Possibly taken care of by firebase

    # Return
    return json.dumps({'status': 'success'})


@app.route('/api/Grammars/<grammar_id>', methods=['POST'])
def post_grammar(word_id): #Note: Public grammar ID
    """
    Purpose: If a user wants to add a word to their library, do so with the public word id.

    Backend Implemented:
    Frontend Implemented:
    """

    # Parameters
    user_id = request.get_json()['user_id']  # Possibly taken care of by firebase

    # Return
    return json.dumps({'status': 'success'})



if __name__ == '__main__':
    app.run()
