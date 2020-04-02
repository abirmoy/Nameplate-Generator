# Nameplate Generator
This is a digital namecard generating system written on Python3 using Flask framework

# Functionality
The system lets user sign in and sign up then create, update, delete degital nameplate. 
In nameplate user can select background photo

1. Flask login
2. Flask signup
3. SQL lite
4. Flask Photo upload



# How to run
Command for running without virtual environment
$flask run

For virtual environment
Step 1: Creating Virtual environment 
$Windows: python -m venv name_of_venv 
$Linux: python3 -m venv name_of_venv

Step 2: Activate virtual environment 
Windows: $cd name_of_venv/Scripts activate or activate.bat 
Linux: $source name_of_venv/bin/activate

Step 3: install pip dependencies from requirements.txt file

Windows: $pip install -r requirements.txt 
Linux: $pip install -r requirements.txt

Step 4: runing flask $flask run

Step 5: By default flask runs on port 5000 therefore system can be access from http://localhost:5000 or http://127.0.0.1:5000
