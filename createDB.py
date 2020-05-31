from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pymysql

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@127.0.0.1:3306/m_blog"


db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    pwd = db.Column(db.String(100))
    addtime = db.Column(db.DateTime,default=datetime.now)

class Blog(db.Model):
    __tablename__ = 'blog'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100))
    author = db.Column(db.String(100))
    content = db.Column(db.Text)
    addtime = db.Column(db.DateTime,default=datetime.now)


if __name__ == "__main__":
    user =User(
        name="test",
        pwd="test",
    )
    blog = Blog(
        title= "test",
        author="test",
        content="test"
    )
    db.session.add(user)
    db.session.add(blog)
    db.session.commit()