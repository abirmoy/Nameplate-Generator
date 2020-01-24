# Nameplate Generator
This is a digital nameplate generating system purely written on Python3 using Flask framework
It's a look alike yet not idendical website that I developed for BMW R&D center Beijing,China during my internship back in 2019-2020.

# Functionality
The system lets user sign in and sign up then create, update, delete degital nameplate. 
In nameplate user can select background and upload photo

1. Flask login
2. Flask signup
3. SQL lite
4. Flask Photo upload



# How to run
Command for running without virtual environment
flask run

For virtual environment
Step 1: Creating Virtual environment Windows: python -m venv name_of_venv Linux: python3 -m venv name_of_venv

Step 2: Activate virtual environment Windows: cd venv/Scripts activate or activate.bat Linux: source venv/bin/activate

Step 3: install pip dependencies from requirements.txt file

Windows: pip install -r requirements.txt Linux: pip3 install -r requirements.txt

Step 4: runing flask flask run

Step 5: By default flask runs on port 5000 http://localhost:5000 or http://127.0.0.1:5000