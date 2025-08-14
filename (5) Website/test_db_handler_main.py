from db_handler_main import *
from db_handler_admin import game_approve_user_link, tag_approve_user_link
from test_db_handler_users import TempUser, create_temp_user, delete_temp_user

class TempGame():
    def __init__(self):
        self.name = "TestGame"
        self.aka = "TG"
        self.desc = "This is a test game"
        self.rdate = "2011/04/19"
        self.rstate = "Released"
        self.alt_name = "GameTest"
        self.alt_desc = "This game is a test"
        self.alt_aka = "GT"
        self.alt_rdate = "2001/02/09"
        self.creation_dict = {"game_title": self.name, "game_aka": self.aka, "game_desc": self.desc, "game_rdate": self.rdate, "game_rstate": self.rstate}
        self.modify_dict = {"game_title": self.alt_name, "game_aka": self.alt_aka, "game_desc": self.alt_desc, "game_rdate": self.alt_rdate, "game_rstate": self.rstate}
        self.id = None

class TempTag():
    def __init__(self):
        self.name = "TestTag"
        self.desc = "This is a test tag"
        self.type = "Normal"
        self.unused_bool = False
        self.alt_name = "TagTest"
        self.alt_desc = "This tag is a test"
        self.alt_type = "Genre"
        self.creation_dict = {"tag_name": self.name, "tag_desc": self.desc, "tag_type": self.type, "tag_isNSFW": self.unused_bool}
        self.modify_dict = {"tag_name": self.alt_name, "tag_desc": self.alt_desc, "tag_type": self.alt_type, "tag_isNSFW": self.unused_bool}
        self.id = None
        

def create_temp_game(temp_user):
    temp_game = TempGame()
    game_create_new(temp_game.creation_dict, temp_user.id)
    temp_game.id = game_get_id(temp_game.name)
    return temp_game

def create_temp_tag(temp_user):
    temp_tag = TempTag()
    tag_add_new(temp_tag.creation_dict, temp_user.id)
    temp_tag.id = tag_get_id(temp_tag.name)
    return temp_tag

def delete_temp_game(temp_game):
    game_delete(temp_game.id)
    del temp_game

def delete_temp_tag(temp_tag):
    tag_delete(temp_tag.id)
    del temp_tag

def test_game_get_id():
    assert game_get_id("3689458943283924") is None
    temp_user = create_temp_user()
    temp_game = create_temp_game(temp_user)
    assert game_get_id(temp_game.name) == temp_game.id
    delete_temp_game(temp_game)
    delete_temp_user(temp_user)
    del temp_game
    del temp_user

def test_game_get_name():
    assert game_get_name(-1) is None
    temp_user = create_temp_user()
    temp_game = create_temp_game(temp_user)
    assert game_get_name(temp_game.id) == temp_game.name.lower()
    delete_temp_game(temp_game)
    delete_temp_user(temp_user)
    del temp_game
    del temp_user

def test_game_get_single():
    assert game_get_single(-1) is None
    temp_user = create_temp_user()
    temp_game = create_temp_game(temp_user)
    game_data = game_get_single(temp_game.id)
    assert len(game_data) == 7
    #Game ID
    assert game_data["game_id"] is not None
    assert game_data["game_id"] == temp_game.id
    #Game Title
    assert game_data["game_title"] is not None
    assert game_data["game_title"] == temp_game.name.lower().title()
    #Game AKA
    if game_data["game_aka"] is not None:
        assert game_data["game_aka"] == temp_game.aka
    #Game Desc
    if game_data["game_desc"] is not None:
        assert game_data["game_desc"] == temp_game.desc
    #Game rdate
    if game_data["game_rdate"] is not None:
        assert game_data["game_rdate"] == temp_game.rdate
    #Game rstate
    if game_data["game_rstate"] is not None:
        assert game_data["game_rstate"] == temp_game.rstate
    assert game_data["game_url"] is None
    delete_temp_game(temp_game)
    delete_temp_user(temp_user)
    del temp_game
    del temp_user

def test_game_check_exists():
    assert game_check_exists("testgame") is False
    temp_user = create_temp_user()
    temp_game = create_temp_game(temp_user)
    assert game_check_exists(temp_game.name) is True
    delete_temp_game(temp_game)
    delete_temp_user(temp_user)
    del temp_game
    del temp_user

def test_game_create_new():
    assert game_create_new({}, -1) is False
    temp_user = create_temp_user()
    temp_game = TempGame()
    assert game_create_new(temp_game.creation_dict, temp_user.id) is True
    temp_game.id = game_get_id(temp_game.name)
    delete_temp_game(temp_game)
    delete_temp_user(temp_user)
    del temp_game
    del temp_user

def test_game_get_unapproved():
    temp_user = create_temp_user()
    temp_game = create_temp_game(temp_user)
    games = game_get_unapproved()
    game_unapproved = False
    for game in games:
        if game["game_id"] == temp_game.id:
            game_unapproved = True
    assert game_unapproved is True
    game_approve_user_link(temp_game.id)
    games = game_get_unapproved()
    game_unapproved = False
    for game in games:
        if game["game_id"] == temp_game.id:
            game_unapproved = True
    assert game_unapproved is False
    delete_temp_game(temp_game)
    delete_temp_user(temp_user)
    del temp_game
    del temp_user

def test_game_delete():
    temp_user = create_temp_user()
    temp_game = create_temp_game(temp_user)
    assert game_check_exists(temp_game.name) is True
    game_delete(temp_game.id)
    assert game_check_exists(temp_game.name) is False
    delete_temp_user(temp_user)
    del temp_game
    del temp_user

def test_tag_check_exists():
    assert tag_check_exists("4635734674587346") is False
    temp_user = create_temp_user()
    temp_tag = create_temp_tag(temp_user)
    assert tag_check_exists(temp_tag.name) is True
    delete_temp_tag(temp_tag)
    delete_temp_user(temp_user)
    del temp_tag
    del temp_user

def test_tag_get_id():
    assert tag_get_id("7834657854392") is None
    temp_user = create_temp_user()
    temp_tag = create_temp_tag(temp_user)
    assert tag_get_id(temp_tag.name) == temp_tag.id
    delete_temp_tag(temp_tag)
    delete_temp_user(temp_user)
    del temp_tag
    del temp_user

def test_tag_get_name():
    assert tag_get_name(-1) is None
    temp_user = create_temp_user()
    temp_tag = create_temp_tag(temp_user)
    assert tag_get_name(temp_tag.id) == temp_tag.name
    delete_temp_tag(temp_tag)
    delete_temp_user(temp_user)
    del temp_tag
    del temp_user

def test_tag_get_all():
    assert tag_get_name(-1) is None
    temp_user = create_temp_user()
    temp_tag = create_temp_tag(temp_user)
    tags = tag_get_all()
    assert tags is not None
    tag_found = False
    for tag in tags:
        assert tag is not None
        if tag == temp_tag.name:
            tag_found = True
    assert tag_found is True
    delete_temp_tag(temp_tag)
    delete_temp_user(temp_user)
    del temp_tag
    del temp_user

def test_tag_get_individual():
    assert tag_get_individual(-1) is None
    temp_user = create_temp_user()
    temp_tag = create_temp_tag(temp_user)
    tag_data = tag_get_individual(temp_tag.id)
    assert tag_data is not None
    assert len(tag_data) == 5
    #Tag ID
    assert tag_data["tag_id"] is not None
    assert type(tag_data["tag_id"]) == int
    assert tag_data["tag_id"] == temp_tag.id
    #Tag Name
    assert tag_data["tag_name"] is not None
    assert type(tag_data["tag_name"]) == str
    assert tag_data["tag_name"] == temp_tag.name.lower().title()
    #Desc
    if tag_data["tag_desc"] is not None:
        assert type(tag_data["tag_desc"]) == str
        assert tag_data["tag_desc"] == temp_tag.desc
    #Type
    assert tag_data["tag_type"] is not None
    assert type(tag_data["tag_type"]) == str
    assert tag_data["tag_type"] == temp_tag.type
    #Unusued Bool
    assert tag_data["tag_isNSFW"] is not None
    assert type(tag_data["tag_isNSFW"]) == bool
    assert tag_data["tag_isNSFW"] == temp_tag.unused_bool
    delete_temp_tag(temp_tag)
    delete_temp_user(temp_user)
    del temp_tag
    del temp_user

def test_tag_add_new():
    assert tag_add_new({}, -2) is False
    temp_user = create_temp_user()
    temp_tag = TempTag()
    assert tag_add_new(temp_tag.creation_dict, temp_user.id) is True
    temp_tag.id = tag_get_id(temp_tag.name)
    delete_temp_tag(temp_tag)
    delete_temp_user(temp_user)
    del temp_tag
    del temp_user

def test_tag_delete():
    temp_user = create_temp_user()
    temp_tag = create_temp_tag(temp_user)
    assert tag_check_exists(temp_tag.name) is True
    assert tag_delete(temp_tag.id) is True
    assert tag_check_exists(temp_tag.name) is False
    delete_temp_user(temp_user)
    del temp_tag
    del temp_user

def test_tag_get_unapproved():
    temp_user = create_temp_user()
    temp_tag = create_temp_tag(temp_user)
    tags = tag_get_unapproved()
    unapproved = False
    for tag in tags:
        if tag["tag_id"] == temp_tag.id:
            unapproved = True
    assert unapproved is True
    tag_approve_user_link(temp_tag.id)
    tags = tag_get_unapproved()
    unapproved = False
    if tags is not None:
        for tag in tags:
            if tag["tag_id"] == temp_tag.id:
                unapproved = True
    assert unapproved is False
    delete_temp_tag(temp_tag)
    delete_temp_user(temp_user)
    del temp_tag
    del temp_user

def test_tag_type_change():
    temp_user = create_temp_user()
    temp_tag = create_temp_tag(temp_user)
    assert tag_get_individual(temp_tag.id)["tag_type"] == temp_tag.type
    assert tag_type_change({"type_newtype": temp_tag.alt_type, "type_tag_id": temp_tag.id}) is True
    assert tag_get_individual(temp_tag.id)["tag_type"] == temp_tag.alt_type
    delete_temp_tag(temp_tag)
    delete_temp_user(temp_user)
    del temp_tag
    del temp_user