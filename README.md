# PIA Toolkit

WebApp for Django Project 

### Prerequisites

Django2.0 runs on Python 3.6, I suggest the use of virtualenv to avoid problems with the dependencies while deploying the app in your local host. The approach would be:

```
pip install virtualenv
```
And then ```create``` and ```activate``` your virtual environment to install all the dependencies in it.

If it's the first time you've heard about virtualenv visit  [virtualenv documentation](https://virtualenv.pypa.io/en/stable/installation/)

Django filetransfers needs to be installed from the ```wkornewald-django-filetransfers-b2df8b4fbf2e``` directory included in the root folder of the project.
This package comes from  [Django-filetransfers](https://bitbucket.org/wkornewald/django-filetransfers)
Then go into the downloaded folder and install with:

```
python setup.py install
```

You can use [pip](https://pypi.org/project/pip/) for the installation of the rest of the packages and dependences included on the ```requirements.txt``` file,
  
```
pip install -r requirements.txt
```

### Running the webApp

Once installed all the dependencies navigate to the root folder of the project, apply the migrations to generate the local database:

```
python manage.py migrate
```

and run the Django Application with:

```
python manage.py runserver
```

And the PIA Toolkit App will be running in the specified port of your local host.

You may want to add a super user to have acces to the admin panel,

```
python manage.py createsuperuser
```

Bear in mind that the project is using django-admin-honeypot, so the real admin panel by default will be on ```/secret``` instead.

## DB structure

![alt text](https://raw.githubusercontent.com/m3d14n0/PIA-Toolkit/edit/master/README.md/DB.png)

## Deploying

The live version of this project was deployed using [AWS elasticbeanstalk](https://aws.amazon.com/es/elasticbeanstalk/) that is the reason why some dependencies as boto3 or django-ses are included. Same with AWS-related environment variables as ```RDS_DB_NAME ```.

Feel free to grab your own choice of Deployment platform!

## Authors

**m3d14n0** - [GitHub account](https://github.com/m3d14n0)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

