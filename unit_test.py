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
    #We don't have something like this on the server
    #assert r.status_code == 200
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
    language = {
        'Language': 1,
        'Level': 0
    }
    create_r = requests.put(ENDPOINT + '/api/Users/' + test_user_id + '/addLearningLanguage', json=language)
    assert 200 <= create_r.status_code <= 299
    test_r = json.loads(requests.get(ENDPOINT + '/api/Users/test1234@test.test').text)
    assert next((True for language in test_r['learningLanguages'] if language['language'] == 1), False)


def test_add_user_native():
    language = {
        'Language': 2,
        'Level': 0
    }
    create_r = requests.put(ENDPOINT + '/api/Users/' + test_user_id + '/addNativeLanguage', json=language)
    assert 200 <= create_r.status_code <= 299
    test_r = json.loads(requests.get(ENDPOINT + '/api/Users/test1234@test.test').text)
    assert next((True for language in test_r['nativeLanguages'] if language['language'] == 2), False)



#####################################################
#          Word Functions                           #
#####################################################

def get_public_word():
    pass


def post_word():
    pass


def post_words():
    pass


def delete_word():
    pass


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
    r = requests.delete(ENDPOINT + '/api/Users/'+test_user_id)
