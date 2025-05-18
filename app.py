from flask import Flask, render_template, url_for, request, redirect, abort
from flask_login import LoginManager, current_user, login_user, logout_user
#from user import User

'''Server Vars'''
app = Flask(__name__) #Create the flask application

'''General Routes'''
#Home/Index
@app.route('/')
def home():
    return render_template('home.html', page_name="Home")

#Error Pages
#These pages are only shown when the website encounters an error.
#404 is page not found.
@app.errorhandler(404)
def page_invalid(e):
    add_access_log(request.remote_addr, log_get_user(), "/404/ (page_invalid)", False, False)
    return render_template('errors/404.html'), 404
@app.errorhandler(405)
def page_wrong_method(e):
    add_access_log(request.remote_addr, log_get_user(), "/405/ (page_wrong_method)", False, False)
    abort(404)
#For simplicity, if the website encounters a 405 error, it will redirect and show as a 404 instead.

#Favicon
#Apparently supposed to be the icon used when a page is bookmarked.
#Even though this supresses the "favicon.ico" 404 error, it does not show this icon when bookmarked.
@app.route('/favicon.ico')
def favicon():
    add_access_log(request.remote_addr, log_get_user(), "/favicon.ico (favicon)", False, False)
    return url_for("static", filename="favicon.ico")

#Launch Website
if __name__ == '__main__':
    if deployed is True:
        from waitress import serve
        serve(app, host="0.0.0.0", port=5000)
    else:
        app.run(host="0.0.0.0", debug=True)