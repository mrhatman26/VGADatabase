from misc import get_time

#Access and errors
def access_log(ip, username, wwAccessed, failed=False, admin=False, default=False, no_auth=False):
    log_file = open("static/logs.txt", "at")
    text = get_time()
    if admin is False:
        if failed is False:
            text = text + ": " + ip + " (User: " + username + ") successfully accessed " + wwAccessed
        else:
            if default is False:
                if no_auth is False:
                    text = text + ": " + ip + " (User: " + username + ") FAILED to access " + wwAccessed
                else:
                    text = text + ": " + ip + " (User: " + username + ") FAILED to access " + wwAccessed + " as the user was not authorised"
            else:
                if no_auth is False:
                    text = text + ": " + ip + " (User: " + username + ") FAILED to access " + wwAccessed + " (The default page was returned instead)"
                else:
                    text = text + ": " + ip + " (User: " + username + ") FAILED to access " + wwAccessed + " as the user was not authorised (The default page was returned instead)"
    else:
        if failed is False:
            text = text + " (ADMIN): " + ip + " (User: " + username + ") successfully accessed admin resource " + wwAccessed
        else:
            if default is False:
                if no_auth is False:
                    text = text + " (ADMIN): " + ip + " (User: " + username + ") FAILED to access admin resource" + wwAccessed
                else:
                    text = text + " (ADMIN): " + ip + " (User: " + username + ") FAILED to access admin resource" + wwAccessed + " as the user was not logged in."
            else:
                if no_auth is False:
                    text = text + " (ADMIN): " + ip + " (User: " + username + ") FAILED to access admin resource" + wwAccessed + " (The default page was returned instead)"
                else:
                    text = text + " (ADMIN): " + ip + " (User: " + username + ") FAILED to access admin resource" + wwAccessed + " as the user was not logged in (The default page was returned instead)"
    log_file.write(text)
    log_file.close()

def error_log(ip, username, wFailed, theException=None, admin=False):
    log_file = open("static/logs.txt", "at")
    text = get_time()
    if admin is False:
        if theException is None:
            text = text + ": " + ip + " (User: " + username + ") encountered the following error: " + wFailed + "\nNo exception information available."
        else:
            text = text + ": " + ip + " (User: " + username + ") encountered the following error: " + wFailed + "\nException:\n" + str(theException)
    else:
        if theException is None:
            text = text + " (ADMIN): " + ip + " (User: " + username + ") encountered the following error: " + wFailed + "\nNo exception information available."
        else:
            text = text + " (ADMIN): " + ip + " (User: " + username + ") encountered the following error: " + wFailed + "\nException:\n" + str(theException)
    log_file.write(text)
    log_file.close()

#Games
def new_game_log(ip, username, new_game_name=None, failed=False):
    log_file = open("static/logs.txt", "at")
    text = get_time()
    if failed is False:
        text = text + ip + " (User: " + username + ") successfully added a new game titled '" + new_game_name + "'"
    else:
        if new_game_name is not None:
            text = text + ip + " (User: " + username + ") FAILED to add a new game titled '" + new_game_name + "'"
        else:
            text = text + ip + " (User: " + username + ") FAILED to add a new game with an unknown title"
    log_file.write(text)
    log_file.close()

def game_approve_log(ip, username, game_name, denied=False, failed=False, already_approved=False):
    log_file = open("static/logs.txt", "at")
    text = get_time()
    if denied is False:
        if failed is False:
            text = text + ": " + ip + " (User: " + username + ") successfully approved the game titled" + game_name
        else:
            if already_approved is False:
                text = text + ": " + ip + " (User: " + username + ") FAILED to approve the game titled" + game_name
            else:
                text = text + ": " + ip + " (User: " + username + ") FAILED to approve the game titled" + game_name + " as it was already approved"
    else:
        if failed is False:
            text = text + ": " + ip + " (User: " + username + ") successfully denied the game titled" + game_name
        else:
            if already_approved is False:
                text = text + ": " + ip + " (User: " + username + ") FAILED to deny the game titled" + game_name
            else:
                text = text + ": " + ip + " (User: " + username + ") FAILED to deny the game titled" + game_name + " as it was already denied"        
    log_file.write(text)
    log_file.close()

#Users
def new_user_log(ip, newUser, failed=False, admin=False):
    log_file = open("static/logs.txt", "at")
    text = get_time()
    if admin is False:
        if failed is False:
            text = text + ": " + ip + " successfully created a new account with the username of " + str(newUser)
        else:
            text = text + ": " + ip + " FAILED to created a new account with the username of " + str(newUser)
    else:
        if failed is False:
            text = text + " (ADMIN): " + ip + " successfully created a new account with the username of " + str(newUser) + " with admin status applied"
        else:
            text = text + " (ADMIN): " + ip + " FAILED to created a new account with the username of " + str(newUser) + " with admin status applied"
    log_file.write(text)
    log_file.close()

def login_log(ip, username, failed=False, logout=False, admin=False, auto=False):
    log_file = open("static/logs.txt", "at")
    text = get_time()
    if admin is False:
        if failed is False:
            if logout is False:
                text = text + ": " + ip + " successfully logged in as " + username
            else:
                text = text + ": " + ip + " (User: " + username + ") successfully logged out of their account"
        else:
            if logout is False:
                text = text + ": " + ip + " FAILED to log in as " + username
            else:
                text = text + ": " + ip + " (User: " + username + ") FAILED to log out of their account"
    else:
        if failed is False:
            if logout is False:
                text = text + " (ADMIN): " + ip + " successfully logged in as " + username
            else:
                if auto is True:
                    text = text + " (ADMIN): " + ip + " (User: " + username + ") was automatically logged out of their account"
                else:
                    text = text + " (ADMIN): " + ip + " (User: " + username + ") successfully logged out of their account"
        else:
            if logout is False:
                text = text + " (ADMIN): " + ip + " FAILED to log in as " + username
            else:
                text = text + " (ADMIN): " + ip + " (User: " + username + ") FAILED to log out of their account"
    log_file.write(text)
    log_file.close()

def modify_user_log(ip, username, failed=False, admin=False):
    log_file = open("static/logs.txt", "at")
    text = get_time()
    if admin is False:
        if failed is False:
            text = text + ": " + ip + " successfully modified the account of " + username
        else:
            text = text + ": " + ip + " FAILED to modify the account of " + username
    else:
        if failed is False:
            text = text + " (ADMIN): " + ip + " successfully modified the account of " + username
        else:
            text = text + " (ADMIN): " + ip + " FAILED to modify the account of " + username
    log_file.write(text)
    log_file.close()

def admin_swap_log(ip, username, failed=False, isMod=False, swappedTo=False):
    log_file = open("static/logs.txt", "at")
    text = get_time()
    if isMod is False:
        if failed is False:
            text = text + " (ADMIN): " + ip + " (User: " + username + ") successfully swapped admin status to " + str(swappedTo)
        else:
            text = text + " (ADMIN): " + ip + " (User: " + username + ") FAILED to swap admin status"
    else:
        if failed is False:
            text = text + " (ADMIN): " + ip + " (User: " + username + ") successfully swapped moderator status to " + str(swappedTo)
        else:
            text = text + " (ADMIN): " + ip + " (User: " + username + ") FAILED to swap moderator status"
    log_file.write(text)
    log_file.close()

def delete_user_log(ip, username, failed=False, admin=False):
    log_file = open("static/logs.txt", "at")
    text = get_time()
    if admin is False:
        if failed is False:
            text = text + ": " + ip + " successfully deleted the account of " + username
        else:
            text = text + ": " + ip + " FAILED to delete the account of " + username
    else:
        if failed is False:
            text = text + " (ADMIN): " + ip + " successfully deleted the account of " + username
        else:
            text = text + " (ADMIN): " + ip + " FAILED to delete the account of " + username
    log_file.write(text)
    log_file.close()

#Developers
def new_developer_log(ip, username, new_developer_name=None, failed=False):
    log_file = open("static/logs.txt", "at")
    text = get_time()
    if failed is False:
        text = text + ip + " (User: " + username + ") successfully added a new developer named '" + new_developer_name + "'"
    else:
        if new_developer_name is not None:
            text = text + ip + " (User: " + username + ") FAILED to add a new developer named '" + new_developer_name + "'"
        else:
            text = text + ip + " (User: " + username + ") FAILED to add a new developer with an unknown name"
    log_file.write(text)
    log_file.close()

def developer_approve_log(ip, username, developer_name, denied=False, failed=False, already_approved=False):
    log_file = open("static/logs.txt", "at")
    text = get_time()
    if denied is False:
        if failed is False:
            text = text + ": " + ip + " (User: " + username + ") successfully approved the developer named" + developer_name
        else:
            if already_approved is False:
                text = text + ": " + ip + " (User: " + username + ") FAILED to approve the developer named" + developer_name
            else:
                text = text + ": " + ip + " (User: " + username + ") FAILED to approve the developer named" + developer_name + " as it was already approved"
    else:
        if failed is False:
            text = text + ": " + ip + " (User: " + username + ") successfully denied the developer named" + developer_name
        else:
            if already_approved is False:
                text = text + ": " + ip + " (User: " + username + ") FAILED to deny the developer named" + developer_name
            else:
                text = text + ": " + ip + " (User: " + username + ") FAILED to deny the developer named" + developer_name + " as it was already denied"        
    log_file.write(text)
    log_file.close()

#Tags
def new_tag_log(ip, username, new_tag_name=None, failed=False):
    log_file = open("static/logs.txt", "at")
    text = get_time()
    if failed is False:
        text = text + ip + " (User: " + username + ") successfully added a new tag named '" + new_tag_name + "'"
    else:
        if new_tag_name is not None:
            text = text + ip + " (User: " + username + ") FAILED to add a new tag named '" + new_tag_name + "'"
        else:
            text = text + ip + " (User: " + username + ") FAILED to add a new tag with an unknown name"
    log_file.write(text)
    log_file.close()

def tag_approve_log(ip, username, tag_name, denied=False, failed=False, already_approved=False):
    log_file = open("static/logs.txt", "at")
    text = get_time()
    if denied is False:
        if failed is False:
            text = text + ": " + ip + " (User: " + username + ") successfully approved the tag named" + tag_name
        else:
            if already_approved is False:
                text = text + ": " + ip + " (User: " + username + ") FAILED to approve the tag named" + tag_name
            else:
                text = text + ": " + ip + " (User: " + username + ") FAILED to approve the tag named" + tag_name + " as it was already approved"
    else:
        if failed is False:
            text = text + ": " + ip + " (User: " + username + ") successfully denied the tag named" + tag_name
        else:
            if already_approved is False:
                text = text + ": " + ip + " (User: " + username + ") FAILED to deny the tag named" + tag_name
            else:
                text = text + ": " + ip + " (User: " + username + ") FAILED to deny the tag named" + tag_name + " as it was already denied"        
    log_file.write(text)
    log_file.close()

def tag_type_change_log(ip, username, tag_name, new_type, failed=False):
    log_file = open("static/logs.txt", "at")
    text = get_time()
    if failed is False:
        text = text + ": " + ip + " (User: " + username + ") successfully changed the tag type of " + tag_name + " to " + new_type
    else:
        text = text + ": " + ip + " (User: " + username + ") FAILED to change the tag type of " + tag_name + " to " + new_type
    log_file.write(text)
    log_file.close()

def tag_update_game_log(ip, username, game_name, failed=False, tag_not_exist=False):
    log_file = open("static/logs.txt", "at")
    text = get_time()
    if failed is False:
        text = text + ": " + ip + " (User: " + username + ") successfully updated the tags of " + game_name
    else:
        if tag_not_exist is False:
            text = text + ": " + ip + " (User: " + username + ") FAILED to update the tags of " + game_name
        else:
            text = text + ": " + ip + " (User: " + username + ") FAILED to update the tags of " + game_name + " because one of the tags entered did not exist"
    log_file.write(text)
    log_file.close()