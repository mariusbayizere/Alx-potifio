from flask import flash, redirect, url_for, session
from functools import wraps
from flask_mail import Message
from model import mail

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function



def send_login_notification(email):
    try:
        msg = Message('Login Notification',
                      sender='bayizeremarius119@gmail.com',
                      recipients=[email])
        msg.body = 'A login was detected for your account.'
        mail.send(msg)
    except Exception as e:
        print(f"Failed to send email: {e}")
        flash(f'Failed to send login notification email. Error: {e}', 'warning')



# def send_login_notification(email):
#     try:
#         msg = Message('Login Notification',
#                       sender='bayizeremarius119@gmail.com',
#                       recipients=[email])
#         msg.body = 'A login was detected for your account.'
#         mail.send(msg)
#     except Exception as e:
#         print(f"Failed to send email: {e}")
#         flash(f'Failed to send login notification email. Error: {e}', 'warning')






# from flask import flash, redirect, url_for, session
# from functools import wraps
# from model import mail
# from flask_mail import Message

# def login_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if 'user_id' not in session:
#             flash('Please log in to access this page.', 'warning')
#             return redirect(url_for('login'))
#         return f(*args, **kwargs)
#     return decorated_function

# def send_login_notification(email):
#     try:
#         msg = Message('Login Notification',
#                       sender='bayizeremarius119@gmail.com',
#                       recipients=[email])
#         msg.body = 'A login was detected for your account.'
#         mail.send(msg)
#     except Exception as e:
#         print(f"Failed to send email: {e}")
#         flash('Failed to send login notification email.', 'warning')



