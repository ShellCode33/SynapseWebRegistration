WEB_ROOT = "/var/www/html/ejabberd-web-registration/"
WEBSITE_NAME = "YourWebsite"

ASK_EMAIL_ADDRESS = True
EMAIL_ADDRESS_MENDATORY = False
SMTP_HOST = "localhost"

ADMIN_PASSWORD = ""
SECRET_KEY = ""
XMPP_HOST = "your_domain.fr"
EJABBERD_CONFIG_FILE = "/etc/ejabberd/ejabberd.yml"

# MySQL database configuration
# By default, the web server will try to parse EJABBERD_CONFIG_FILE in order to retreive DB parameters 
#MYSQL_HOST = ""
#MYSQL_USER = "root"
#MYSQL_PASSWORD = ""
#MYSQL_DB = ""
#MYSQL_PORT = 3306

# ReCaptcha configuration
RECAPTCHA_ENABLED = False # True highly recommanded
RECAPTCHA_SITE_KEY = "YOUR_KEY"
RECAPTCHA_SECRET_KEY = "YOUR_SECRET_KEY"
RECAPTCHA_THEME = "dark" # light or dark
