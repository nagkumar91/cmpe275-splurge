>Project name: Splurge
>Team 13
>Team members:
<p> Nagkumar Arkalgud 010095345
<p> Namratha Ramalinge Gowda 010096268
<p> Harmit Patel 010124634

##Steps to run the project (on a ubuntu or *nix based machine)

0. Create a virtual environment if you do not want to mess up with the current version of python
1. Install the requirements:
    `pip install -r requirements.txt`
2. Create a settings file with the correct details about the database running in your local machine [django settings](https://docs.djangoproject.com/en/1.8/ref/settings/#databases)
    `cp splurge/splurge/settings/nagkumar.py splurge/splurge/settings/<your_name>.py`
    make sure you use the proper database name and password. You can use any database mysql/postgres
    you have to edit the ngrok URL later on. I have explained this in the following steps
3. Install [ngrok](https://ngrok.com/#download)
4. SyncDB - Run the following command to create all the tables in your database
    > `cd splurge`
    > `export DJANGO_SETTINGS_MODULE=splurge.settings.<your_name>.py`
    > `python manage.py syncdb`
   Make sure you fill up all the details for creating an "admin"
5. Running the migrations - Run the following command to create the migrations in your database
    > `python manage.py migrate`
6. Run the server - the following command will start the server if you have followed all the previous steps
    > `python manage.py runserver`
    Ignore all the warnings as this was developed for Django 1.8 and 1.9 was released on December 1st
7. Setting up queuing - In a new terminal, install rabbitmq and create a setting if your credentails are different
    > `vim splurge/settings/<your_name>.py`
    Paste `BROKER_URL = "amqp://admin:admin@localhost:5672/default"` If
    admin is the username and password and there is a virtual host named `default`. If not, the format of the setting is:
    `BROKER_URL = "amqp://username:pasword@localhost:5672/virtual_host_name"`
8. Run celery to process the queue
    >`celery -A core worker -B -l info`
    This command will run the celery beat and spawn workers to complete the tasks in the queue
9. In a new terminal tunnel the traffic through ngrok to obtain proper links in email
    > `ngrok http 8000`
    Copy the URL that you get and change the `SITE_URL` in your settings file accordingly

Following these steps should get the whole project up and running. Visit [http://localhost:8000/](http://localhost:8000/) on any browser to see the web app live.
  
##Note on email listener
As the project relies on email callback to complete the redeeming, we have to set up a context.io callback to your current server so that you can see the process being completed.
As I cannot share the context.io credentials. If you want to see the complete working app, you can send the ngrok URL to nagkumar.arkalgud@sjsu.edu and I will update the context.io callback.
    

    
