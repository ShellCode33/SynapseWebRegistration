WEBSITE_NAME = "YourWebsite"

# Web Config
ASK_EMAIL_ADDRESS = True
EMAIL_ADDRESS_MENDATORY = False
SMTP_HOST = "localhost"
EMAIL_FROM = "noreply@domain.fr"

# Web Admin
ADMIN_PASSWORD = "" # Please define it
SECRET_KEY = "" # Will be randomly generated

# Database Connection
DB_TYPE = "sqlite" # sqlite or postgres

#SQLITE
DB_FILE_SQLITE = "homeserver.db"

#POSTGRES
DB_HOST = ""
DB_NAME = ""
DB_USER= ""
DB_PASS = ""

MATRIX_DOMAIN = "domain.fr" # server_name in homeserver.yaml
FEDERATION_PORT = 8448
SYNAPSE_CONFIG_FILE = "/PATH/TO/homeserver.yaml" # Parse synapse config coming soon


# ReCaptcha configuration
RECAPTCHA_ENABLED = False # True highly recommanded
RECAPTCHA_SITE_KEY = "YOUR_KEY"
RECAPTCHA_SECRET_KEY = "YOUR_SECRET_KEY"
RECAPTCHA_THEME = "dark" # light or dark
