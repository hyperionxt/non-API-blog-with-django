import dj_database_url

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST="smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT=587
EMAIL_FROM = 'alt4ccount082@gmail.com'
EMAIL_HOST_USER="alt4ccount082@gmail.com"
EMAIL_HOST_PASSWORD="qubljcqmphwbjqtx"
PASSWORD_RESET_TIMEOUT = 1800 #30 minutes timeout



#DB CONFIG

ENGINE= 'django.db.backends.postgresql'
NAME= 'db1' 
USER= 'postgres' 
PASSWORD= 'arroz'
HOST= 'localhost'
PORT= '5432'

# RENDER.COM
DEFAULT = dj_database_url.config(
    default='postgres://postgres:arroz@localhost:5432/db1',
        conn_max_age=600)



# IMPLEMENTATION DJANGO CAPTCHA

RECAPTCHA_PUBLIC_KEY = '6LfNIKsjAAAAAJIzb6A05RSgoumpR1yEfa1GJJRG'
RECAPTCHA_PRIVATE_KEY = '6LfNIKsjAAAAANQDH9QG4z5MHyBlF3C9L3vKfMUr'
SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']