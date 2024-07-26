# Bayesion Technical Evaluation
This is a repo for the technical evaluation for a Forward Deployed Software Engineer position at Bayesion

The objective is to create a API/Database service that stores data regarding music artist and their albums.

The user should be able to:
- Create an Artist
- Create an album
- Generate a list of all Artists
- Generate a list of all albums for a given Artist
    - Allow user to filter on release date and price


# Install and Run locally (Windows Machines, using Powershell)
- Open a terminal window
- Navigate to the directory where you want to run the project
- Copy the project directory to your local computer
- You will probably want to create a virtual environment to install the requirements
    - create the virtual envrionment: `python -m venv venv`
    - activate the virtual environment: `venv\Scripts\Activate.ps1`
    - install requirements: `pip install -r requirements.txt`
    - run the project: `uvicorn app.main:app --host localhost --port 7777 --reload`

# Documentaton
Enter `http://localhost:7777/docs` into a browser for Swagger documentation