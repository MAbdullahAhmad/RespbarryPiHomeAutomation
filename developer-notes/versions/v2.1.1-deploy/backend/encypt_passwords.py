import os
from config.database import db
from models.user_model import User
from werkzeug.security import generate_password_hash
from server import app

def encrypt_passwords():
    with app.app_context():
        users = User.query.all()

        for user in users:
            if len(user.password) < 60:  
                print(f"Encrypting password for user: {user.username}")
                user.set_password(user.password)
                db.session.commit()
        print("All passwords have been encrypted.")

if __name__ == "__main__":
    encrypt_passwords()
