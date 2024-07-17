# gudlift-registration

1. Why

   This is a proof of concept (POC) project to show a light-weight version of our competition booking platform. The aim is the keep things as light as possible, and use feedback from the users to iterate.

2. Getting Started

   This project uses the following technologies:

   - Python v3.x+

   - [Flask](https://flask.palletsprojects.com/en/1.1.x/)

     Whereas Django does a lot of things for us out of the box, Flask allows us to add only what we need.

   - [Virtual environment](https://virtualenv.pypa.io/en/stable/installation.html)

     This ensures you'll be able to install the correct packages without interfering with Python on your machine.

     Before you begin, please ensure you have this installed globally.

3. Installation

   - After cloning, change into the directory and type `python -m venv env`. This will then set up a a virtual python environment within that directory.

   - Next, type <code>source env/bin/activate</code>. You should see that your command prompt has changed to the name of the folder. This means that you can install packages in here without affecting affecting files outside. To deactivate, type <code>deactivate</code>

   - Rather than hunting around for the packages you need, you can install in one step. Type <code>pip install -r requirements.txt</code>. This will install all the packages listed in the respective file. If you install a package, make sure others know by updating the requirements.txt file. An easy way to do this is <code>pip freeze > requirements.txt</code>

   - Flask requires that you set an environmental variable to the python file. However you do that, you'll want to set the file to be <code>server.py</code>. Check [here](https://flask.palletsprojects.com/en/1.1.x/quickstart/#a-minimal-application) for more details($env:FLASK_APP = "server.py" )

   - You should now be ready to test the application. In the directory, type either <code>flask run</code> or <code>python -m flask run</code>. The app should respond with an address you should be able to go to using your browser.

4. Current Setup

   The app is powered by [JSON files](https://www.tutorialspoint.com/json/json_quick_guide.htm). This is to get around having a DB until we actually need one. The main ones are:

   - competitions.json - list of competitions
   - clubs.json - list of clubs with relevant information. You can look here to see what email addresses the app will accept for login.

5. Testing

   You are free to use whatever testing framework you like-the main thing is that you can show what tests you are using.

   We also like to show how well we're testing, so there's a module called
   [coverage](https://coverage.readthedocs.io/en/coverage-5.1/) you should add to your project.

# Install the project on windows

```sh
- git clone https://github.com/AymericSandoz/P11_OpenClassrooms_Python_Testing.git
```

```sh
- python -m venv env
```

```sh
- .\env\Scripts\activate
```

```sh
- pip install -r requirements.txt
```

# Launching the Application

Set the Flask app environment variable:

```sh
$env:FLASK_APP = "server.py"
```

Activate virtual env

```sh
- .\env\Scripts\activate
```

Run the application

```sh
flask run
```

# Running Test

## Run integration, unit, and fonctional tests all in one

```sh
pytest test/
```

## Run integration tests

```sh
pytest .\test\test_integrations\
```

## Run unit tests

```sh
pytest .\test\test_unitaires\
```

## Run functionnal tests

Run the application

```sh
pytest .\test\test_functionnels\
```

## Run performance test

```sh
locust -f .\test\test_performance\locustfile.py
```

Open the browser at http://localhost:8089.

Performance Test Notes:
No failures, but response times are very long (3-4s). Why?

## Coverage Testing

```sh
pytest --cov=. test/
```

For detailed coverage, generate an HTML report:

```sh
pytest --cov=. --cov-report html test/
```

Open the index.html file in the htmlcov directory.

# Git

La convention de nommage des branches suit la terminologie suivante :
`<Numéro>/<Type>/<NomDeLaBranche>`

- `<Numéro>` : Un identifiant unique pour le ticket associé.
- `<Type>` : Indique le type de travail effectué. Utilisez `Bug` pour les corrections de bugs et `Feature` pour les nouvelles fonctionnalités.
- `<NomDeLaBranche>` : Un nom descriptif, court et précis, séparé par des tirets si nécessaire.

Exemple :
`123/Feature/amelioration-du-login`

La branche master est la branche principale du projet

La branche QA correspond à la branche de test

Les autres branches sont nommées selon la nomenclagie suivante:

- `<Numéro>` : Un identifiant unique pour la tâche ou le ticket associé.
- `<Type>` : Indique le type de travail effectué. Utilisez `Bug` pour les corrections de bugs et `Feature` pour les nouvelles fonctionnalités.
- `<NomDeLaBranche>` : Un nom descriptif, court et précis, séparé par des tirets si nécessaire.

Exemple :
`05/Feature/AjoutLoginSocial`
