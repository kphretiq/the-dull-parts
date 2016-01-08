# The Dull Parts
The dull parts of writing a web app:
- Database Init
- Authentication
- Profile
- Password Recovery

## environment

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
