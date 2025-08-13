import pytest
import mysql.connector
from db_handler_users import *
from db_config import get_db_config
from db_handler_admin import admin_swap_stat
from misc import to_bool

#Before running these tests, please make sure the database has been started.

#Test Vars
class TempUser():
    def __init__(self):
        self.name = "TestUser"
        self.password = "TestPassword"
        self.email = "TestUser@example.com"
        self.alt_name = "UserTest"
        self.alt_email = "UserTest@example.co.uk"
        self.alt_password = "alt_password"
        self.creation_dict = {"user_name": self.name, "user_email": self.email, "user_password": self.password}
        self.modify_dict = {"user_name": self.alt_name, "user_email": self.alt_email, "user_password": self.alt_password}
        self.id = None

def create_temp_user():
    temp_user = TempUser()
    user_add_new(temp_user.creation_dict)
    temp_user.id = user_get_id(temp_user.name)
    return temp_user

def delete_temp_user(temp_user):
    user_delete(temp_user.id)

#Tests
def test_user_add_new():
    assert user_add_new({}) is False
    temp_user = TempUser()
    assert user_add_new(temp_user.creation_dict) is True
    temp_user.id = user_get_id(temp_user.name)
    delete_temp_user(temp_user)
    del temp_user

def test_user_check_exists():
    assert user_check_exists("882793897532918204875923190284879532190") is False
    temp_user = create_temp_user()
    assert user_check_exists(temp_user.name) is True
    delete_temp_user(temp_user)
    del temp_user

def test_user_check_reconfirm():
    assert user_check_reconfirm(-2) is None or user_check_reconfirm(-2) == []
    temp_user = create_temp_user()
    print(user_check_reconfirm(temp_user.id))
    assert user_check_reconfirm(temp_user.id)[0] == temp_user.id
    delete_temp_user(temp_user)
    del temp_user

def test_user_login_passcheck():
    assert user_login_passcheck({"user_name": "TestUser", "user_password": "NoPass"}) is False
    temp_user = create_temp_user()
    assert user_login_passcheck({"user_name": "TestUser", "user_password": "NoPass"}) is False
    assert user_login_passcheck({"user_name": "TestUser", "user_password": "TestPassword"}) is True
    delete_temp_user(temp_user)
    del temp_user

def test_user_check_admin():
    result = user_check_admin("948593028493480")
    assert result[0] is False and result[1] is False
    temp_user = create_temp_user()
    result = user_check_admin(temp_user.name)
    assert result[0] is False and result[1] is False
    admin_swap_stat(temp_user.id, swap_mod=True)
    result = user_check_admin(temp_user.name)
    assert result[0] is True and result[1] is False
    admin_swap_stat(temp_user.id)
    result = user_check_admin(temp_user.name)
    assert result[0] is True and result[1] is True
    delete_temp_user(temp_user)
    del temp_user

def test_user_get_id():
    assert user_get_id("879452857352789") is None
    temp_user = create_temp_user()
    assert user_get_id(temp_user.name) == temp_user.id
    delete_temp_user(temp_user)
    del temp_user

def test_user_get_username():
    assert user_get_username(-2) is None
    temp_user = create_temp_user()
    assert user_get_username(temp_user.id) == temp_user.name
    delete_temp_user(temp_user)
    del temp_user

def test_user_get_all():
    temp_user = create_temp_user()
    temp_user_exists = False
    users = user_get_all()
    for user in users:
        assert len(user) == 5
        #ID
        assert user["user_id"] is not None
        assert type(user["user_id"]) == int
        if user["user_id"] == temp_user.id:
            temp_user_exists = True
        #Email
        assert user["user_email"] is not None
        assert type(user["user_email"]) == str
        #Desc
        if user["user_desc"] is not None:
            assert type(user["user_desc"]) == str
        #IsAdmin
        assert user["user_isAdmin"] is not None
        assert type(user["user_isAdmin"]) == int
        #IsMod
        assert user["user_isMod"] is not None
        assert type(user["user_isMod"]) == int
    assert temp_user_exists is True
    delete_temp_user(temp_user)
    del temp_user

def test_user_single_get_all():
    assert user_single_get_all(-2) is None
    temp_user = create_temp_user()
    user_data = user_single_get_all(temp_user.id)
    assert len(user_data) == 3
    assert user_data["user_id"] == temp_user.id
    assert user_data["user_email"] == temp_user.email
    assert user_data["user_desc"] is None
    delete_temp_user(temp_user)
    del temp_user

def test_user_get_email():
    assert user_get_email(-2) is None
    temp_user = create_temp_user()
    assert user_get_email(temp_user.id) == temp_user.email
    delete_temp_user(temp_user)
    del temp_user

def test_user_modify_username():
    assert user_modify_username(-2, None) is False
    temp_user = create_temp_user()
    assert user_modify_username(temp_user.id, temp_user.alt_name) is True
    assert user_get_username(temp_user.id) == temp_user.alt_name
    delete_temp_user(temp_user)
    del temp_user

def temp():
    user_check_exists("blah")

temp()