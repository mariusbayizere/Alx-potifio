import datetime
import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:auca%402023@127.0.0.1:3306/car_rent_management_alx'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # PERMANENT_SESSION_LIFETIME = datetime.timedelta(seconds=60)
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(seconds=180)
    SECRET_KEY = 'auca@2023'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'bayizeremarius119@gmail.com')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'xgkf wwve strh vvyq')









# class Config:
#     SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:auca%402023@127.0.0.1:3306/car_rent_management_alx'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     PERMANENT_SESSION_LIFETIME = datetime.timedelta(seconds=60)
#     MAIL_SERVER = 'smtp.gmail.com'
#     MAIL_PORT = 587
#     MAIL_USE_TLS = True
#     MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'bayizeremarius119@gmail.com'
#     MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'prin zrxh zkvy ieex'






# import os

# class Config:
#     SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:auca%402023@127.0.0.1:3306/car_rent_management_alx'

#     SQLALCHEMY_TRACK_MODIFICATIONS = False
    
