# Music_Streaming_App

I have developed this application as part of my coursework for Modern Application Development-1 during my pursuit of a Bachelor's degree in Data Science and Applications.

Hello Welcome to "ReadMe", I am Aditya Shanker Srivastava (23f1001545).


---------------- Software specifications for the web app ----------------

--> To run this files we need a IDE(or text editor), python3, A terminal and a GUI for SQLite3 to see the changes in Database.
--> Below are the softwares that I have used,
    IDE : Visual Studio Code
    Teminal : Terminal in Visual Studio Code
    GUI for SQLite3 : DB Browser for SQLite

Note: All the above things should be installed in the machine to run the code successfully and please give a glance on requirements.txt also.

---------------- Instructions to run the web app ----------------

--> Unzip the Project file.
--> Open the unzipped folder in IDE (Visual Studio Code is preferable).
--> Now open the terminal(powershell) in IDE and create a virtual environment by running the below commands one by one, 
    pip install virtualenv
    virtualenv env

    Now, write the below command to activate the virtual environment,
    .\env\Scripts\activate.ps1

Note: If the above commands are not running, then open Windows powershell by run as administrator and write the below command in it,
    Set-ExecutionPolicy unrestricted
    after that enter A
    close it and back to the IDE's terminal(powershell)

    Then install flask in virtual environment by writing the below command in terminal(powershell),
    pip install flask

    Then install sqlalchemy in virtual environment by writing the below command in terminal(powershell),
    pip install flask-sqlalchemy
    
    After that if you are in Visual Studio Code, Add a extension for jinja2 named as "jinja2 snippet kit".
    Else write the below command in terminal(powershell)
    pip install Jinja2

    Now we are set to go, just run app.py by clicking the button in IDE or
    just type the below command in the terminal(powershell),
    python .\app.py

--------------------- Test the web application -----------------------

--> Now the web app is running in the Browser.

------- For Admin Dasgboard -------
--> Credentials for admin are:
    UserName: admin
    Password: 123

    Login with the above Username and Password, it will redirect you to the admin dashboard of the application where you can monitor app statistics like total users/creators/albums, statistics on how songs are performing, ability to flag or remove songs/albums that breach company policy. 


------- For User -------
--> If you are confused that where to start with, use the below credentials for login-
    UserName: user2
    Password: User

    Or you can signup with your Username and Password

    Now you can search songs, play songs, upload songs and be a creator, create a playlist and album.
