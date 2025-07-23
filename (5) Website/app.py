import ast, traceback
from flask import Flask, render_template, url_for, request, redirect, abort
from flask_login import LoginManager, current_user, login_user, logout_user
from datetime import datetime as dt
from db_handler_users import *
from db_handler_admin import *
from db_handler_main import *
from db_handler_links import *
from db_loader import *
from action_logger import *
from version_handler import *
from user import User
from global_vars import deployed
from misc import get_current_page, test_datetime
#from user import User

'''Server Vars'''
version = update_version()
print("Version is now:", version, flush=True)
admin_reset_increment()
app = Flask(__name__) #Create the flask application
app.secret_key = "SeeThatMountain?YouCanClimbItJERSAIKGYHJIOERHGJ"

'''Login Manager'''
login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_fuser(id):
    user_check = user_check_reconfirm(id)
    if len(user_check) <= 0:
        return None
    else:
        return User(user_check[0], user_check[1], user_check[2], user_check[3])

def get_user():
    try:
        if hasattr(current_user, 'username'):
            return current_user.username
        else:
            return "Annonymous"
    except:
        return "Annonymous"

'''General Routes'''
#Home/Index
@app.route("/")
def home():
    access_log(request.remote_addr, get_user(), "/ (Home)")
    return render_template('home.html', page_name="Home", c_version=version)

#Games
#Game List
@app.route("/games/")
@app.route("/games/pid=<pid>")
def game_list(pid=0, no_results=10):
    try:
        pid = int(pid)
        games = game_get_selection(pid)
        current_page = get_current_page(pid, no_results)
        access_log(request.remote_addr, get_user(), "/games/pid=" + str(pid) + " (Games List)")
        return render_template("games/game_list.html", page_name="All Games", c_version=version, game_list=games[0], no_pages=games[1], no_results=no_results, pid=pid, current_page=current_page, total_results=games[2])
    except Exception as e:
        try:
            games = game_get_selection(0)
            access_log(request.remote_addr, get_user(), "/games/pid=" + str(pid) + " (Games List)", failed=True, default=True)
            error_log(request.remote_addr, get_user(), "An error occurred while trying to show the selected game page", theException=traceback.format_exc())
            current_page = get_current_page(pid, no_results)
            return render_template("games/game_list.html", page_name="All Games", c_version=version, game_list=games[0], no_pages=games[1], no_results=no_results, pid=pid, current_page=current_page, total_results=games[2])
        except:
            access_log(request.remote_addr, get_user(), "/games/pid=" + str(pid) + " (Games List)", failed=True, default=True)
            error_log(request.remote_addr, get_user(), "An error occurred while trying to show the default game page. Are there no games?", theException=traceback.format_exc())
            return render_template("games/game_list.html", page_name="All Games", c_version=version)
    
#Individual Game Page
@app.route("/games/game_id=<game_id>")
def game_page(game_id=0):
    try:
        game_data = game_get_single(game_id)
        game_title = "No Game?"
        if game_data is not None:
            game_title = game_data["game_title"]
        access_log(request.remote_addr, get_user(), "/games/game_id=" + str(game_id))
        approval=game_get_approved(game_id)
        denial=game_get_denied(game_id)
        denial_reason = game_get_denial_reason(game_id)
        if denial is False:
            if game_check_release_date(game_id, game_data["game_rdate"]) is True:
                game_data = game_get_single(game_id)
        return render_template("games/individual_game.html", page_name=game_title, game_data=game_data, is_approved=approval, denied=denial, denial_desc=denial_reason, c_version=version)
    except Exception as e:
        error_log(request.remote_addr, get_user(), "An error occurred when trying to load an invididual game page", traceback.format_exc())
        access_log(request.remote_addr, get_user(), "/games/game_id=" + str(game_id), failed=True)
        abort(404)

#Add Game Page
@app.route("/games/add/")
def game_add_new():
    if current_user.is_authenticated:
        access_log(request.remote_addr, get_user(), "/games/add/ (Add New Game)")
        return render_template("games/game_add.html", page_name="Add New Game", c_version=version)
    else:
        access_log(request.remote_addr, get_user(), "/games/add/ (Add New Game)", failed=True, no_auth=True)
        return redirect("/users/login/")
#Validate new game
@app.route("/games/add/validate", methods=["POST"])
def game_add_new_validate():
    if current_user.is_authenticated:
        access_log(request.remote_addr, get_user(), "/games/add/validate/ (New Game Validation)")
        game_data = request.get_data()
        game_data = game_data.decode()
        game_data = ast.literal_eval(game_data)
        try:
            if test_datetime(game_data["game_rdate"]) is True:
                if game_check_exists(game_data["game_title"]) is False:
                    if game_create_new(game_data, current_user.id) is True:
                        new_game_log(request.remote_addr, get_user(), game_data["game_title"])
                        return "success"
                    else:
                        error_log(request.remote_addr, get_user(), "An error occurred while trying to create a new game")
                        new_game_log(request.remote_addr, get_user(), game_data["game_title"], failed=True)
                        return "servererror"
                else:
                    error_log(request.remote_addr, get_user(), "New game already exissts")
                    new_game_log(request.remote_addr, get_user(), game_data["game_title"], failed=True)
                    return "gameexists"
            else:
                error_log(request.remote_addr, get_user(), "Game release date is an invalid date")
                new_game_log(request.remote_addr, get_user(), game_data["game_title"], failed=True)
                return "invaliddate"
        except Exception as e:
            new_game_log(request.remote_addr, get_user(), new_game_name=game_data["game_title"], failed=True)
            error_log(request.remote_addr, get_user(), "There was an error while trying to add a new game", theException=traceback.format_exc())
            return "servererror"
    else:
        access_log(request.remote_addr, get_user(), "/games/add/validate/ (New Game Validation)", failed=True, no_auth=True)
        new_game_log(request.remote_addr, get_user(), failed=True)
        return "servererror"
    
#Developers & Publishers (Devpubs)
#Developer List 
@app.route("/developers/")
@app.route("/developers/pid=<pid>")
def developer_list(pid=0, no_results=10):
    try:
        pid = int(pid)
        devpubs = devpub_get_selection(pid)
        current_page = get_current_page(pid, no_results)
        access_log(request.remote_addr, get_user(), "/developers/pid=" + str(pid) + " (Developers List)")
        return render_template("devpubs/developer_list.html", page_name="All Developers", c_version=version, devpub_list=devpubs[0], no_pages=devpubs[1], no_results=no_results, pid=pid, current_page=current_page, total_results=devpubs[2])
    except Exception as e:
        try:
            devpubs = devpub_get_selection(0)
            access_log(request.remote_addr, get_user(), "/developers/pid=" + str(pid) + " (Developers List)", failed=True, default=True)
            error_log(request.remote_addr, get_user(), "An error occurred while trying to show the selected developer page", theException=traceback.format_exc())
            current_page = get_current_page(pid, no_results)
            return render_template("devpubs/developer_list.html", page_name="All Developers", c_version=version, devpub_list=devpubs[0], no_pages=devpubs[1], no_results=no_results, pid=pid, current_page=current_page, total_results=devpubs[2])
        except:
            access_log(request.remote_addr, get_user(), "/developers/pid=" + str(pid) + " (Developers List)", failed=True, default=True)
            error_log(request.remote_addr, get_user(), "An error occurred while trying to show the default developer page. Are there no developers?", theException=traceback.format_exc())
            return render_template("devpubs/developer_list.html", page_name="All Developers", c_version=version)
        
#Developer List 
@app.route("/publishers/")
@app.route("/publishers/pid=<pid>")
def publisher_list(pid=0, no_results=10):
    try:
        pid = int(pid)
        devpubs = devpub_get_selection(pid, is_pub=True)
        current_page = get_current_page(pid, no_results)
        access_log(request.remote_addr, get_user(), "/publishers/pid=" + str(pid) + " (publishers List)")
        return render_template("devpubs/publisher_list.html", page_name="All publishers", c_version=version, devpub_list=devpubs[0], no_pages=devpubs[1], no_results=no_results, pid=pid, current_page=current_page, total_results=devpubs[2])
    except Exception as e:
        try:
            devpubs = devpub_get_selection(pid, is_pub=True)
            access_log(request.remote_addr, get_user(), "/publishers/pid=" + str(pid) + " (publishers List)", failed=True, default=True)
            error_log(request.remote_addr, get_user(), "An error occurred while trying to show the selected publishers page", theException=traceback.format_exc())
            current_page = get_current_page(pid, no_results)
            return render_template("devpubs/publisher_list.html", page_name="All publishers", c_version=version, devpub_list=devpubs[0], no_pages=devpubs[1], no_results=no_results, pid=pid, current_page=current_page, total_results=devpubs[2])
        except:
            access_log(request.remote_addr, get_user(), "/publishers/pid=" + str(pid) + " (publishers List)", failed=True, default=True)
            error_log(request.remote_addr, get_user(), "An error occurred while trying to show the default publishers page. Are there no publishers?", theException=traceback.format_exc())
            return render_template("devpubs/publisher_list.html", page_name="All Developers", c_version=version)

#Add Devpub
@app.route("/devpubs/add/")
def devpub_add():
    if current_user.is_authenticated:
        access_log(request.remote_addr, get_user(), "/devpubs/add/ (Add Devpub)")
        return render_template("devpubs/devpub_add.html", page_name="Add New Developer/Publisher", c_version=version)
    else:
        access_log(request.remote_addr, get_user(), "/devpubs/add/ (Add Devpub)", no_auth=True, failed=True)
        return redirect("/users/login/")
#Devpub Validate
@app.route("/devpubs/add/validate/", methods=["POST"])
def debpub_add_validate():
    if current_user.is_authenticated:
        access_log(request.remote_addr, get_user(), "/devpubs/add/validate/ (Add Devpub Validate)")
        devpub_data = request.get_data()
        devpub_data = devpub_data.decode()
        devpub_data = ast.literal_eval(devpub_data)
        func_to_use = None
        try:
            if test_datetime(devpub_data["developer_foundDate"]) is False or test_datetime(devpub_data["developer_defunctDate"]) is False:
                return "invaliddate"
            if devpub_check_exists(devpub_data["developer_name"], devpub_data["developer_isPub"]) is False:
                if devpub_add_new(devpub_data, current_user.id) is True:
                    new_developer_log(request.remote_addr, get_user(), devpub_data["developer_name"])
                    return "success"
                else:
                    error_log(request.remote_addr, get_user(), "An error occurred while trying to add a new developer")
                    new_developer_log(request.remote_addr, get_user(), devpub_data["developer_name"], failed=True)
                    return "servererror"
            else:
                error_log(request.remote_addr, get_user(), "The new developer already exists")
                new_developer_log(request.remote_addr, get_user(), devpub_data["developer_name"], failed=True)
                return "developerexists"
        except Exception as e:
            new_developer_log(request.remote_addr, get_user(), devpub_data["developer_name"], failed=True)
            error_log(request.remote_addr, get_user(), "There was an error while attempting to create a new developer", theException=traceback.format_exc())
            return "servererror"
    else:
        access_log(request.remote_addr, get_user(), "/devpubs/add/validate/ (Add Devpub Validate)", failed=True, no_auth=True)
        return redirect("/users/login/")

'''User Routes'''
#Login
@app.route("/users/login/")
def user_login():
    if current_user.is_authenticated:
        access_log(request.remote_addr, get_user(), "/users/login/ (Login)", failed=True)
        return redirect("/")
    else:
        access_log(request.remote_addr, get_user(), "/users/login/ (Login)")
        return render_template("users/login.html", page_name="Login", c_version=version)
@app.route("/users/login/validate/", methods=["POST"])
def user_login_validate():
    if current_user.is_authenticated:
        access_log(request.remote_addr, get_user(), "/users/login/validate/ (Login Validation)", failed=True)
        return redirect("/")
    else:
        userdata = request.get_data()
        userdata = userdata.decode()
        try:
            userdata = ast.literal_eval(userdata)
            if user_check_exists(userdata["user_name"]):
                if user_login_passcheck(userdata):
                    admin_stat = user_check_admin(userdata["user_name"])
                    print(user_get_id(userdata["user_name"]), flush=True)
                    login_user(User(user_get_id(userdata["user_name"]), userdata["user_name"], admin_stat[0], admin_stat[1]))
                    login_log(request.remote_addr, userdata["user_name"])
                    return "success"
                else:
                    login_log(request.remote_addr, userdata["user_name"], failed=True)
                    error_log(request.remote_addr, userdata["user_name"], "user_login_validate failed to validate login")
                    return "usernotexist"
            else:
                login_log(request.remote_addr, userdata["user_name"], failed=True)
                error_log(request.remote_addr, userdata["user_name"], "User does not exist")
                return "usernotexist"
        except Exception as e:
            login_log(request.remote_addr, userdata["user_name"], failed=True)
            error_log(request.remote_addr, userdata["user_name"], "Server error during login", theException=traceback.format_exc())
            return "servererror"

#Signup
@app.route("/users/signup/")
def user_signup():
    if current_user.is_authenticated:
        access_log(request.remote_addr, get_user(), "/users/signup/ (Signup)", failed=True)
        return redirect("/")
    else:
        access_log(request.remote_addr, get_user(), "/users/signup/ (Signup)")
        return render_template("users/signup.html", page_name="Signup", c_version=version)
@app.route("/users/signup/validate/", methods=["POST"])
def user_signup_validate():
    if current_user.is_authenticated:
        access_log(request.remote_addr, get_user(), "/users/signup/validate/ (Signup Validation)", failed=True)
        return redirect("/")
    else:
        access_log(request.remote_addr, get_user(), "/users/signup/validate/ (Signup Validation)")
        userdata = request.get_data()
        userdata = userdata.decode()
        userdata = ast.literal_eval(userdata)
        try:
            if user_check_exists(userdata["user_name"]) is False:
                if user_add_new(userdata) is True:
                    new_user_log(request.remote_addr, userdata["user_name"])
                    return "success"
                else:
                    new_user_log(request.remote_addr, userdata["user_name"], failed=True)
                    error_log(request.remote_addr, userdata["user_name"], "user_add_new failed to create a new user")
                    return "servererror"
            else:
                new_user_log(request.remote_addr, userdata["user_name"], failed=True)
                error_log(request.remote_addr, userdata["user_name"], "User already exists")
                return "userexists"
        except Exception as e:
            new_user_log(request.remote_addr, userdata["user_name"], failed=True)
            error_log(request.remote_addr, userdata["user_name"], "Server error during user creation", theException=traceback.format_exc())
            return "servererror"
        
#Logout
@app.route("/users/logout/")
def user_logout():
    if current_user.is_authenticated:
        access_log(request.remote_addr, get_user(), "/users/logout/ (Logout)")
        login_log(request.remote_addr, get_user(), logout=True)
        logout_user()
        return redirect("/")
    else:
        access_log(request.remote_addr, get_user(), "/users/logout/ (Logout)", failed=True)
        return redirect("/")
    
'''Mod Routes'''
#Main
@app.route("/mod/")
def mod_main():
    if current_user.is_authenticated:
        if current_user.is_mod:
            access_log(request.remote_addr, get_user(), "/mod/ (Mod: Main)")
            return render_template("mod/mod_main.html", page_name="Mod: Main", c_version=version)
        else:
            access_log(request.remote_addr, get_user(), "/mod/ (Mod: Main)", failed=True)
            abort(404)
    else:
        access_log(request.remote_addr, get_user(), "/mod/ (Mod: Main)", failed=True)
        abort(404)

#Game Approvals
@app.route("/mod/approvals/games/")
def mod_approval_games():
    if current_user.is_authenticated:
        if current_user.is_mod:
            games = game_get_unapproved()
            access_log(request.remote_addr, get_user(), "/mod/approvals/games/ (Mod: Game Approvals)")
            return render_template("mod/mod_approvals_games.html", page_name="Mod: Game Approvals", c_version=version, game_data=games)
        else:
            abort(404)
    else:
        abort(40)
#Validate
@app.route("/mod/approvals/games/game_id=<game_id>")
def mod_approval_games_validate(game_id=0):
    if current_user.is_authenticated:
        if current_user.is_mod:
            access_log(request.remote_addr, get_user(), "/mod/approvals/games/game_id=" + str(game_id) + " (Mod: Game Approvals Validate)")
            if game_get_approved(game_id) is False:
                if game_approve_user_link(game_id) is True:
                    game_approve_log(request.remote_addr, get_user(), game_get_name(game_id))
                else:
                    error_log(request.remote_addr, get_user(), "An error occurred while trying to approve a game")
                    game_approve_log(request.remote_addr, get_user(), game_get_name(game_id), failed=True)
            else:
                error_log(request.remote_addr, get_user(), "The game is already approved")
                game_approve_log(request.remote_addr, get_user(), game_get_name(game_id), failed=True, already_approved=True)
            return redirect("/games/game_id=" + str(game_id))
        else:
            access_log(request.remote_addr, get_user(), "/mod/approvals/games/game_id=" + str(game_id) + " (Mod: Game Approvals Validate)", failed=True, no_auth=True)
            abort(404)
    else:
        access_log(request.remote_addr, get_user(), "/mod/approvals/games/game_id=" + str(game_id) + " (Mod: Game Approvals Validate)", failed=True, no_auth=True)
        abort(404)
#Deny
@app.route("/mod/approvals/games/deny/", methods=["POST"])
def mod_approval_games_deny():
    if current_user.is_authenticated:
        if current_user.is_mod:
            access_log(request.remote_addr, get_user(), "mod/approvals/games/deny/ (Mod: Game Approvals Deny)")
            deny_data = request.get_data()
            deny_data = deny_data.decode()
            deny_data = ast.literal_eval(deny_data)
            deny_data["denial_game_title"] = game_get_name(deny_data["denial_game_id"])
            try:
                if game_get_denied(deny_data["denial_game_id"]) is False:
                    if game_deny_user_link(deny_data) is True:
                        game_approve_log(request.remote_addr, get_user(), deny_data["denial_game_title"], denied=True)
                        return "success"
                    else:
                        error_log(request.remote_addr, get_user(), "An error occurred while trying to deny a game")
                        game_approve_log(request.remote_addr, get_user(), deny_data["denial_game_title"], denied=True, failed=True)
                        return "servererror"
                else:
                    error_log(request.remote_addr, get_user(), "The game is already denied")
                    game_approve_log(request.remote_addr, get_user(), deny_data["denial_game_title"], failed=True, already_approved=True, denied=True)
                    return "alreadydenied"
            except Exception as e:
                error_log(request.remote_addr, get_user(), "An error occurred while trying to deny a game", theException=traceback.format_exc())
                game_approve_log(request.remote_addr, get_user(), deny_data["denial_game_title"], failed=True, denied=True)
                return "servererror"
        else:
            access_log(request.remote_addr, get_user(), "mod/approvals/games/deny/ (Mod: Game Approvals Deny)", failed=True, no_auth=True)
            abort(404)
    else:
        access_log(request.remote_addr, get_user(), "mod/approvals/games/deny/ (Mod: Game Approvals Deny)", failed=True, no_auth=True)
        abort(404)

    
'''Admin Routes'''
#Main
@app.route("/admin/")
def admin_main():
    if current_user.is_authenticated:
        if current_user.is_admin:
            access_log(request.remote_addr, get_user(), "/admin/ (Admin: Main)", admin=True)
            return render_template("admin/admin_main.html", page_name="Admin: Main", c_version=version)
        else:
            access_log(request.remote_addr, get_user(), "/admin/ (Admin: Main)", failed=True, admin=True, no_auth=True)
            abort(404)
    else:
        access_log(request.remote_addr, get_user(), "/admin/ (Admin: Main)", failed=True, admin=True, no_auth=True)
        abort(404)

#User Management
@app.route("/admin/management/users/")
def admin_user_management():
    if current_user.is_authenticated:
        if current_user.is_admin:
            access_log(request.remote_addr, get_user(), "/admin/management/users/ (Admin: User Management)", admin=True)
            return render_template("admin/admin_user_management.html", page_name="Admin: User Management", c_version=version, userdata=user_get_all())
        else:
            access_log(request.remote_addr, get_user(), "/admin/management/users/ (Admin: User Management)", failed=True, admin=True, no_auth=True)
            abort(404)
    else:
        access_log(request.remote_addr, get_user(), "/admin/management/users/ (Admin: User Management)", failed=True, admin=True, no_auth=True)
        abort(404)
#Swap Admin Status
@app.route("/admin/management/users/swap_admin/user_id=<user_id>")
def admin_swap_admin_status(user_id=None):
    if current_user.is_authenticated:
        if current_user.is_admin:
            access_log(request.remote_addr, get_user(), "/admin/management/users/swap_admin/user_id=" + user_id + " (Admin: Swap Admin Status)", admin=True)
            admin_swap_stat(user_id)
            admin_swap_log(request.remote_addr, get_user(), swappedTo=user_check_admin(get_user())[1])
            if str(current_user.id) != user_id:
                return redirect("/admin/management/users/")
            else:
                return redirect("/")
        else:
            access_log(request.remote_addr, get_user(), "/admin/management/users/swap_admin/user_id=" + user_id + " (Admin: Swap Admin Status)", admin=True, failed=True, no_auth=True)
            abort(404)
            admin_swap_log(request.remote_addr, get_user(), failed=True)
    else:
        access_log(request.remote_addr, get_user(), "/admin/management/users/swap_admin/user_id=" + user_id + " (Admin: Swap Admin Status)", admin=True, failed=True, no_auth=True)
        admin_swap_log(request.remote_addr, get_user(), failed=True)
        abort(404)
#Swap Mod Status
@app.route("/admin/management/users/swap_mod/user_id=<user_id>")
def admin_swap_mod_status(user_id=None):
    if current_user.is_authenticated:
        if current_user.is_admin:
            access_log(request.remote_addr, get_user(), "/admin/management/users/swap_mod/user_id=" + user_id + " (Admin: Swap Mod Status)", admin=True)
            admin_swap_stat(user_id, swap_mod=True)
            admin_swap_log(request.remote_addr, get_user(), swappedTo=user_check_admin(get_user())[0], isMod=True)
            return redirect("/admin/management/users/")
        else:
            access_log(request.remote_addr, get_user(), "/admin/management/users/swap_mod/user_id=" + user_id + " (Admin: Swap Mod Status)", admin=True, failed=True, no_auth=True)
            admin_swap_log(request.remote_addr, get_user(), failed=True, isMod=True)
            abort(404)
    else:
        access_log(request.remote_addr, get_user(), "/admin/management/users/swap_mod/user_id=" + user_id + " (Admin: Swap Mod Status)", admin=True, failed=True, no_auth=True)
        admin_swap_log(request.remote_addr, get_user(), failed=True, isMod=True)
        abort(404)
#Delete User
@app.route("/admin/management/users/delete/user_id=<user_id>")
def admin_user_delete(user_id):
    if current_user.is_authenticated:
        if current_user.is_admin:
            access_log(request.remote_addr, get_user(), "/admin/management/users/delete/user_id=" + str(user_id) + " (Admin: User Delete)", admin=True)
            user_delete(user_id)
            if user_id == current_user.id:
                login_log(request.remote_addr, get_user(), logout=True, admin=True, auto=True)
                logout_user()
                return redirect("/")
            else:
                return redirect("/admin/management/users/")
        else:
            access_log(request.remote_addr, get_user(), "/admin/management/users/delete/user_id=" + str(user_id) + " (Admin: User Delete)", admin=True, failed=True, no_auth=True)
            abort(404)
    else:
        access_log(request.remote_addr, get_user(), "/admin/management/users/delete/user_id=" + str(user_id) + " (Admin: User Delete)", admin=True, failed=True, no_auth=True)
        abort(404)

#Database Management
@app.route("/admin/management/databasae/")
def admin_database_manage():
    if current_user.is_authenticated:
        if current_user.is_admin:
            access_log(request.remote_addr, get_user(), "/admin/management/databasae/ (Admin: Database Management)", admin=True)
            return render_template("admin/admin_database_management.html", page_name="Admin: Database Management", c_version=version)
        else:
            access_log(request.remote_addr, get_user(), "/admin/management/databasae/ (Admin: Database Management)", admin=True, failed=True, no_auth=True)
            abort(404)
    else:
        access_log(request.remote_addr, get_user(), "/admin/management/databasae/ (Admin: Database Management)", admin=True, failed=True, no_auth=True)
        abort(404)
#Load Data From CSV
@app.route("/admin/management/database/load_csv/")
def admin_load_csv():
    if current_user.is_authenticated:
        if current_user.is_admin:
            access_log(request.remote_addr, get_user(), "/admin/management/database/load_csv/ (Admin: Load From CSV)", admin=True)
            return render_template("confirmation.html", page_name="Are you sure?", message="Are you sure you want to load from CSV? This may take a long time and the server will hang until it is done.", dir_to_use="admin_load_csv_confirmed", dir_to_return="admin_database_manage", yes_message="Yes, load the CSV", no_message="No, return to database management", c_version=version) #Finish this
        else:
            access_log(request.remote_addr, get_user(), "/admin/management/database/load_csv/ (Admin: Load From CSV)", admin=True, failed=True, no_auth=True)
            abort(404)
    else:
        access_log(request.remote_addr, get_user(), "/admin/management/database/load_csv/ (Admin: Load From CSV)", admin=True, failed=True, no_auth=True)
        abort(404)
#Confirmed
@app.route("/admin/management/database/load_csv/confirmed/")
def admin_load_csv_confirmed():
    if current_user.is_authenticated:
        if current_user.is_admin:
            access_log(request.remote_addr, get_user(), "/admin/management/database/load_csv/confirmed/ (Admin: Load From CSV Confirmed)", admin=True)
            read_scraped_data(current_user.id)
            return redirect("/admin/")
        else:
            access_log(request.remote_addr, get_user(), "/admin/management/database/load_csv/confirmed/ (Admin: Load From CSV Confirmed)", admin=True, failed=True, no_auth=True)
            abort(404)
    else:
        access_log(request.remote_addr, get_user(), "/admin/management/database/load_csv/confirmed/ (Admin: Load From CSV Confirmed)", admin=True, failed=True, no_auth=True)
        abort(404)
            

#Error Pages
#These pages are only shown when the website encounters an error.
#404 is page not found.
@app.errorhandler(404)
def page_invalid(e):
    return render_template('errors/404.html'), 404
@app.errorhandler(405)
def page_wrong_method(e):
    abort(404)
#For simplicity, if the website encounters a 405 error, it will redirect and show as a 404 instead.

#Favicon
#Apparently supposed to be the icon used when a page is bookmarked.
#Even though this supresses the "favicon.ico" 404 error, it does not show this icon when bookmarked.
@app.route('/favicon.ico')
def favicon():
    return url_for("static", filename="favicon.ico")

#Launch Website
if __name__ == '__main__':
    if deployed is True:
        from waitress import serve
        serve(app, host="0.0.0.0", port=5000)
    else:
        app.run(host="0.0.0.0", debug=True)