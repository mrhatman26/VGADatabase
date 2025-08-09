Website:<br>
To run the website you need the following Python libraries to be installed:<br>
1. Flask: To run the website<br>
2. Flask Login: To handle users<br>
3. mysql-connector-python: To allow for connections to the database<br>
4. waitress: To run the website outside of a developmental environment.
<br>
(For the running of the website, I recommend using two command lines: One for the website and the other for the database)<br>
Next, you need to start the website itself using Python Flask and the database using MySQL.<br>
For Flask, you need to:<br>
1. Move to the "(5) Website" directory.<br>
2. Set the deployed and live variables in "global_vars.py":<br>
    >If deployed is True, the website will attempt to use a MySQL Docker container, else, it will use a local MySQL database instead.<br>
    (If using a Docker container, certain features such as dumping the database will be unavailable)<br>
    >If live is True, the website will run with the waitress library, else, it will be run in debug mode.<br>
3. Run the website with "app.py" or "python app.py".<br>
<br>
For the database, you have two options:<br>
A. Run in a Docker container using "run.bat":<br>
    >Make sure to set "deployed" in global_vars.py to True if using a Docker container.
    1. Move to the "(5) Website" directory.<br>
    2. Run the "run.bat" batch file.<br>
    3. Enter the password when requested.<br>
    4. Enter "SOURCE /vgdatabase.sql;"<br>
B. Run locally using MySQL:<br>
    >Make sure to set "deployed" in global_vars.py to False if using MySQL.
    1. Move to the "(5) Website" directory.<br>
    2. Log into MySQL (E.G: "mysql -u root -p")<br>
    3. Enter "SOURCE /vgdatabase.sql;"<br>
<br>
As stated previously, if using a Docker container, certain actions such as mysqldump will be unavailable using the website interface<br>
and must be done through the containers terminal instead.