WEB_ROOT = "/var/www/html/ejabberd-web-registration/"
WEBSITE_NAME = "WitchDoctors"

ASK_EMAIL_ADDRESS = True
EMAIL_ADDRESS_MENDATORY = False
SMTP_HOST = "localhost"

ADMIN_PASSWORD = "db58b154e05efec29a3162b5924d3a3e40c7045b0cef4ced21a7a31f8c16583527be98971cf6bf794ddcb052799e816ff4b12b90d76d902df2aee09f7c4c892d"
SECRET_KEY = "OgynKQyJly4xMX6Bqe8Zcfz2"
XMPP_HOST = "witchdoctors.fr"
EJABBERD_CONFIG_FILE = "/etc/ejabberd/ejabberd.yml"

# MySQL database configuration
# By default, the web server will try to parse EJABBERD_CONFIG_FILE in order to retreive DB parameters 
#MYSQL_HOST = ""
#MYSQL_USER = "root"
#MYSQL_PASSWORD = ""
#MYSQL_DB = ""
#MYSQL_PORT = 3306

# ReCaptcha configuration
RECAPTCHA_ENABLED = False
RECAPTCHA_SITE_KEY = "6LfLcz0UAAAAAHKxX0CTf-4unFWW2OwGiJ5zR1D4"
RECAPTCHA_SECRET_KEY = "6LfLcz0UAAAAALS-2R7se9iLGButcMU7ytGCocoR"
RECAPTCHA_THEME = "dark" # light or dark
