# The Dull Parts
The dull parts of writing a web app:
- Database Init
- Authentication
- Admin
- Profile Editing
- Password Change/Recovery

This rubber-stamp project is basically everything surrounding an actual app.
## Quick Start

## Database Init

### Tables
Tables are defined in App/Models.py. You are supplied with three tables:

- User: The user authentication table supplied by Flask-Auth
- Profile: User profile table which has a relation to User.
- TempAuth: A temporary table used to supply keys for initiializing user and updating passwords.

### Initialize a New Database and Create Root User

1. find the ADMIN_SECRET_KEY value in config.py or your environment variable. 
1. browse to http://your.domain/admin/init/<ADMIN_SECRET_KEY>
1. create your root user
1. log in
1. complete root profile

Note that attempts to re-initialize the database or create a new root user will be thwarted. See App/Routes/Admin.py.

## Authentication
- Flask-Auth handles authentication and assignment of roles.
- sqlite with a SESSION_TYPE of "sqlalchemy" is fine for development
- redis handles session in production. Use SESSION_TYPE "redis".

see App/Routes/Auth.py and App/Roles.py

## Environments

### local
I use virtualenv and autoenv for development.

.env file
```bash
APP_SECRET_KEY="backinnagasakiwherethefellowschewtobaccy";
ADMIN_SECRET_KEY="andthewomenwickywackywoo";
SQLALCHEMY_DATABASE_URI="sqlite:////$(pwd)/dullparts.db";
SQLALCHEMY_DATABASE_NAME="dullparts";
SESSION_TYPE="sqlalchemy"
MAIL_USERNAME="someuser@gmail.com";
MAIL_PASSWORD="secretpassword";
SIGN_UP_SENDER="someuser@gmail.com";
SIGN_UP_MESSAGE="Exiting App! It Excites One!"
```

#### postgresql+psycopg2
You'll need to run redis, as the session key is too large for sqlalchemy session to handle
```bash
SQLALCHEMY_DATABASE_URI="postgresql+psycopg2://dullparts:password@localhost/dullparts";
SESSION_TYPE="redis"
```
#### mysql
You'll need to run redis, as the session key is too large for sqlalchemy session to handle
```bash
SQLALCHEMY_DATABASE_URI="mysql+pymysql://dullparts:password@localhost/dullparts";
SESSION_TYPE="redis"
```


### heroku
heroku configuration here

### deploy with gunicorn
