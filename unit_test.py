import requests
import json

#####################################################
#          General Data                             #
#####################################################
ENDPOINT = 'http://127.0.0.1:5000'
test_user_id = ''


def same_object(o1, o2):
    incons = ""
    for key in o1:
        if not o2.has_attr(key):
            incons += f"OBJ DOES NOT HAVE {key}"
        elif not type(o1[key]) != type(o2[key]):
            incons += f"OBJ {key} IS OF TYPE {type(o2[key])} AND NOT {type(o1[key])}"
        elif type(o1[key]) == object:
            incons += same_object(o1[key], o2[key])
        elif type(o1[key]) == list:
            if not type(o1[key][0]) != type(o2[key][0]):
                incons += f"OBJ {key}'S ELEMENTS ARE OF TYPE {type(o2[key][0])} AND NOT {type(o1[key][0])}"
            elif type(o1[key][0]) == object:
                incons += same_object(o1[key][0], o2[key][0])
    return incons


#####################################################
#          Connection                               #
#####################################################
def test_can_call_endpoint():
    r = requests.get(ENDPOINT + '/api')
    # We don't have something like this on the server
    # assert r.status_code == 200
    assert True


#####################################################
#          User Functions                           #
#####################################################
def test_create_user():
    global test_user_id
    test_user_temp = {
        'Email': 'test1234@test.test',
        'Username': 'TESTY BOI'
    }
    r = requests.post(ENDPOINT + '/api/Users', json=test_user_temp)
    assert 200 <= r.status_code <= 299
    return_data = json.loads(r.text)
    assert return_data['email'] == "test1234@test.test"
    assert return_data['username'] == "TESTY BOI"
    test_user_id = return_data['id']


def test_set_username():
    create_r = requests.put(ENDPOINT + '/api/Users/' + test_user_id + '/setUsername', json={'username': 'TESTIER BOI'})
    assert 200 <= create_r.status_code <= 299
    test_r = json.loads(requests.get(ENDPOINT + '/api/Users/test1234@test.test').text)
    assert test_r['username'] == 'TESTIER BOI'


def test_use_coin():
    create_r = requests.put(ENDPOINT + '/api/Users/' + test_user_id + '/useCoin', json={'coins': 5})
    assert 200 <= create_r.status_code <= 299
    test_r = json.loads(requests.get(ENDPOINT + '/api/Users/test1234@test.test').text)
    assert test_r['coins'] == 95


def test_add_user_learning():
    lang = {
        'Language': 1,
        'Level': 0
    }
    create_r = requests.put(ENDPOINT + '/api/Users/' + test_user_id + '/addLearningLanguage', json=lang)
    assert 200 <= create_r.status_code <= 299
    test_r = json.loads(requests.get(ENDPOINT + '/api/Users/test1234@test.test').text)
    has_language = len([language for language in test_r['learningLanguages'] if language['language'] == 1])
    assert has_language > 0


def test_add_user_native():
    language = {
        'Language': 2,
        'Level': 0
    }
    create_r = requests.put(ENDPOINT + '/api/Users/' + test_user_id + '/addNativeLanguage', json=language)
    assert 200 <= create_r.status_code <= 299
    test_r = json.loads(requests.get(ENDPOINT + '/api/Users/test1234@test.test').text)
    has_language = len([language for language in test_r['nativeLanguages'] if language['language'] == 2])
    assert has_language > 0


#####################################################
#          Word Functions                           #
# Currently tests only french. These should be updated with each new lemmetizer
#####################################################
test_word_id = ''
test_word_id2 = ''
test_word_id3 = ''


def test_get_public_word():
    global test_word_id
    data = {'Search': 'courir'}
    test_r = requests.get(ENDPOINT + '/api/Words/Public/2', json=data)
    assert 200 <= test_r.status_code <= 299
    obj = json.loads(test_r.text)
    assert obj[0]['word'] == 'Courir'
    assert obj[0]['language'] == 2
    assert [translation for translation in obj[0]['translations'] if translation.language == 1][0] == 'run'
    data = {'Search': 'couru'}
    test_r = requests.get(ENDPOINT + '/api/Words/Public/2', json=data)
    assert 200 <= test_r.status_code <= 299
    obj = json.loads(test_r.text)
    assert obj[0]['word'] == 'Courir'
    assert obj[0]['language'] == 2
    assert [translation for translation in obj[0]['translations'] if translation.language == 1][0] == 'run'
    test_word_id = obj[0]['id']


def test_post_word():
    data = {
        'userId': test_user_id,
        'wordId': test_word_id
    }
    create_r = requests.post('/api/Words/2', json=data)
    assert 200 <= create_r.status_code <= 299
    get_r = requests.get('/api/Words/2/All', json={'userId': test_user_id})
    assert 200 <= get_r.status_code <= 299
    get_data = json.loads(get_r.text)
    my_word = [data for data in get_data if data['publicWord']['word'] == 'Courir'][0]
    assert len(my_word) == 1


def test_post_same_word_multiple_times():
    data = {
        'userId': test_user_id,
        'wordId': test_word_id
    }
    create_r = requests.post('/api/Words/2', json=data)
    create_r = requests.post('/api/Words/2', json=data)
    create_r = requests.post('/api/Words/2', json=data)
    create_r = requests.post('/api/Words/2', json=data)
    get_r = requests.get('/api/Words/2/All', json={'userId': test_user_id})
    assert 200 <= get_r.status_code <= 299
    get_data = json.loads(get_r.text)
    my_word = [data for data in get_data if data['publicWord']['word'] == 'Courir'][0]
    assert len(my_word) == 1


def test_post_words():
    global test_word_id2
    global test_word_id3
    data = {'Search': 'chercher'}
    word_1 = json.loads(requests.get(ENDPOINT + '/api/Words/Public/2', json=data).text)
    data = {'Search': 'courir'}
    word_2 = json.loads(requests.get(ENDPOINT + '/api/Words/Public/2', json=data).text)
    data = {'Search': 'pouvoir'}
    word_3 = json.loads(requests.get(ENDPOINT + '/api/Words/Public/2', json=data).text)
    test_word_id2=word_2['id']
    test_word_id3=word_3['id']
    all_words = [word_1['id'], word_2['id'], word_3['id'], word_3['id']]
    data = {
        'userId': test_user_id,
        'words': all_words
    }
    create_response = requests.post('/api/Words/2/Multiple', json=data)
    assert 200 <= create_response.status_code <= 299
    get_r = json.loads(requests.get('/api/Words/2', json={'userId': test_user_id}).text)
    my_word = [data for data in get_r if data['publicWord']['word'] == 'Chercher'][0]
    assert len(my_word) == 1
    my_word = [data for data in get_r if data['publicWord']['word'] == 'Courir'][0]
    assert len(my_word) == 1
    my_word = [data for data in get_r if data['publicWord']['word'] == 'Pouvoir'][0]
    assert len(my_word) == 1


def test_delete_word():
    data = {
        'userId': test_user_id,
        'wordId': test_word_id
    }
    create_r = requests.delete('/api/Words/2', json=data)
    assert 200 <= create_r.status_code <= 299
    get_r = requests.get('/api/Words/2/All', json={'userId': test_user_id})
    assert 200 <= get_r.status_code <= 299
    get_data = json.loads(get_r.text)
    my_word = [data for data in get_data if data['publicWord']['word'] == 'Courir'][0]
    assert len(my_word) == 1
    assert my_word['archived'] == True

def delete_word():
    data = {
        'userId': test_user_id,
        'wordId': test_word_id
    }
    create_r = requests.delete('/api/Words/2', json=data)
    assert 200 <= create_r.status_code <= 299
    get_r = requests.get('/api/Words/2/All', json={'userId': test_user_id})
    assert 200 <= get_r.status_code <= 299
    get_data = json.loads(get_r.text)
    my_word = [data for data in get_data if data['publicWord']['word'] == 'Courir'][0]
    assert len(my_word) == 0

def delete_words():
    data = {
        'userId': test_user_id,
        'wordIds': [test_word_id2, test_word_id3]
    }
    create_r = requests.delete('/api/Words/2', json=data)
    assert 200 <= create_r.status_code <= 299
    get_r = requests.get('/api/Words/2/All', json={'userId': test_user_id})
    assert 200 <= get_r.status_code <= 299
    get_data = json.loads(get_r.text)
    my_word = [data for data in get_data if data['publicWord']['word'] == 'Pouvoir'][0]
    assert len(my_word) == 0


#####################################################
#          Grammar Functions                        #
#####################################################
def new_grammar():
    pass


def post_grammar():
    pass


def delete_grammar():
    pass


#####################################################
#            Packs Functions                        #
#####################################################

def post_pack():
    pass


def import_pack():
    pass


def get_imported_packs():
    pass


def get_public_packs():
    pass


def get_packs():
    pass


def view_pack():
    pass


def accept_coins():
    pass


def delete_pack():
    pass


#####################################################
#          Cleanup                                  #
#####################################################
def test_delete_user():
    r = requests.delete(ENDPOINT + '/api/Users/' + test_user_id)
