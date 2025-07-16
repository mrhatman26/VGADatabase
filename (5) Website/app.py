import ast
from flask import Flask, render_template, url_for, request, redirect, abort
from flask_login import LoginManager, current_user, login_user, logout_user
from db_handler_users import *
from db_handler_admin import *
from action_logger import *
from version_handler import *
from user import User
#from user import User

'''Server Vars'''
version = update_version()
print(version, flush=True)
app = Flask(__name__) #Create the flask application
app.secret_key = "SeeThatMountain?YouCanClimbItJERSAIKGYHJIOERHGJ"
deployed = False

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
@app.route('/')
def home():
    access_log(request.remote_addr, get_user(), "/ (Home)")
    return render_template('home.html', page_name="Home", c_version=version)

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
            error_log(request.remote_addr, userdata["user_name"], "Server error during login", e)
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
        try:
            userdata = ast.literal_eval(userdata)
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
            error_log(request.remote_addr, userdata["user_name"], "Server error during user creation", e)
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
    
'''Admin Routes'''
#Main
@app.route("/admin/")
def admin_main():
    if current_user.is_authenticated:
        if current_user.is_admin:
            access_log(request.remote_addr, get_user(), "/admin/ (Admin: Main)", admin=True)
            return render_template("admin/admin_main.html", page_name="Admin: Main", c_version=version)
        else:
            access_log(request.remote_addr, get_user(), "/admin/ (Admin: Main)", failed=True, admin=True)
            abort(404)
    else:
        access_log(request.remote_addr, get_user(), "/admin/ (Admin: Main)", failed=True, admin=True)
        abort(404)

#User Management
@app.route("/admin/management/users/")
def admin_user_management():
    if current_user.is_authenticated:
        if current_user.is_admin:
            access_log(request.remote_addr, get_user(), "/admin/management/users/ (Admin: User Management)", admin=True)
            return render_template("admin/admin_user_management.html", page_name="Admin: User Management", c_version=version, userdata=user_get_all())
        else:
            access_log(request.remote_addr, get_user(), "/admin/management/users/ (Admin: User Management)", failed=True, admin=True)
            abort(404)
    else:
        access_log(request.remote_addr, get_user(), "/admin/management/users/ (Admin: User Management)", failed=True, admin=True)
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
            access_log(request.remote_addr, get_user(), "/admin/management/users/swap_admin/user_id=" + user_id + " (Admin: Swap Admin Status)", admin=True, failed=True)
            abort(404)
            admin_swap_log(request.remote_addr, get_user(), failed=True)
    else:
        access_log(request.remote_addr, get_user(), "/admin/management/users/swap_admin/user_id=" + user_id + " (Admin: Swap Admin Status)", admin=True, failed=True)
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
            access_log(request.remote_addr, get_user(), "/admin/management/users/swap_mod/user_id=" + user_id + " (Admin: Swap Mod Status)", admin=True, failed=True)
            admin_swap_log(request.remote_addr, get_user(), failed=True, isMod=True)
            abort(404)
    else:
        access_log(request.remote_addr, get_user(), "/admin/management/users/swap_mod/user_id=" + user_id + " (Admin: Swap Mod Status)", admin=True, failed=True)
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
            access_log(request.remote_addr, get_user(), "/admin/management/users/delete/useer_id=" + str(user_id) + " (Admin: User Delete)", admin=True)
            abort(404)
    else:
        access_log(request.remote_addr, get_user(), "/admin/management/users/delete/useer_id=" + str(user_id) + " (Admin: User Delete)", admin=True)
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