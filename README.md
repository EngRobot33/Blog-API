# Blog
**This is a simple blog app with Django REST Framework.**

## Installation

* First of all clone the project:
```
git clone https://github.com/EngRobot33/Quiz.git
```
* Then, we need a virtual environment you can create like this:
```
virtualenv venv
```
* Activate it with the command below:
```
source venv/bin/activate
```
* After that, you must install all of the packages in `requirements.txt` file in project directory:
```
pip install -r requirements.txt
```
* Then you should have a superuser for accessing to admin panel:
```
python3 manage.py createsuperuser
```
* After that, migration:
```
python3 manage.py migrate
```
* That's finished now you can run the project:
```
python3 manage.py runserver
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
