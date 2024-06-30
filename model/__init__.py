from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

# Initialize extensions
db = SQLAlchemy()
mail = Mail()

def create_app():
    app = Flask(__name__, static_folder='static')
    app.config.from_object('model.configuration.config.Config')

#     # Initialize extensions with the app
    db.init_app(app)
    mail.init_app(app)

    with app.app_context():
        # Import models here to ensure they are registered properly
        from model import Customer, employee, payment, Car, rental, maintenance, location, insurance, user
        db.create_all()  # Create tables

        # Test email sending (optional, you might want to remove it later)
        try:
            msg = Message('Test Email',
                          sender='bayizeremarius119@gmail.com',
                          recipients=['mariusbayizere119@gmail.com'])
            msg.body = 'This is a test email.'
            mail.send(msg)
            print("Email sent successfully!")
        except Exception as e:
            print(f"Failed to send email: {e}")

    return app





# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_mail import Mail, Message

# app = Flask(__name__)
# app.config.from_object('model.configuration.config.Config')
# # app.config.from_object('configuration.config.Config') 

# db = SQLAlchemy(app)
# mail = Mail(app)
# with app.app_context():
#     try:
#         msg = Message('Test Email',
#                       sender='bayizeremarius119@gmail.com',
#                       recipients=['mariusbayizere119@gmail.com'])
#         msg.body = 'This is a test email.'
#         mail.send(msg)
#         print("Email sent successfully!")
#     except Exception as e:
#         print(f"Failed to send email: {e}")

# # Import models after initializing db to avoid circular import
# from model import Customer, employee, payment, Car, rental, maintenance, location, insurance, user

















# from flask_sqlalchemy import SQLAlchemy  # type: ignore
# from flask_mail import Mail, Message

# db = SQLAlchemy()
# mail = Mail(app)