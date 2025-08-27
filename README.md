Scraping Program and Cleaner: In "(3) Scraping Program"<br>
To run the scraping program, make sure you are connected to the internet, then run "steam_scrape.py" in the command line. <br>
From there, enter the number of games you would like to scrape from Steam. After this, the program will run automatically.<br>
Note: The speed of the program is dependant on your machine, but it roughly takes an hour and a half to scrape 10,000 games.<br>
Once scraping is finished, the data collected will be saved to "scraped_steam_game_data.csv".
<br>
After the scraping program is finished, you will want to run "scraped_data_cleaner.py" in the command line to allow the data to be used for<br>
data analysis or in the website. This cleaning program will run automatically with no input needed. Once done, it will save the cleaned data to<br>
"cleaned_steam_data.csv".<br>
To use this data in the website, make sure to copy it to the "(5) Website" directory.<br>
<br>
Website: In "(5) Website"<br>
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
    > If deployed is True, the website will attempt to use a MySQL Docker container, else, it will use a local MySQL database instead.<br>
    (If using a Docker container, certain features, such as dumping the database, will be unavailable)<br>
    > If live is True, the website will run with the waitress library, else, it will be run in debug mode.<br>
3. Run the website with "app.py" or "python app.py".<br>
<br>
For the database, you have two options:<br>
A. Run in a Docker container using "run.bat":<br>
    > Make sure to set "deployed" in global_vars.py to True if using a Docker container.
    1. Move to the "(5) Website" directory.<br>
    2. Run the "run.bat" batch file.<br>
    3. Enter the password when requested.<br>
    4. Enter "SOURCE /vgdatabase.sql;"<br>
B. Run locally using MySQL:<br>
    > Make sure to set "deployed" in global_vars.py to False if using MySQL.
    1. Move to the "(5) Website" directory.<br>
    2. Log into MySQL (E.G: "mysql -u root -p")<br>
    3. Enter "SOURCE /vgdatabase.sql;"<br>
<br>
As stated previously, if using a Docker container, certain actions such as mysqldump will be unavailable using the website interface
and must be done through the containers terminal instead.