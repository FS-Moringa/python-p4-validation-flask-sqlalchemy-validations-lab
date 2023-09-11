from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy.exc import IntegrityError, CompileError


db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validate_name(cls, key, name):
        existing_name = Author.query.filter_by(name=name).first()
        if not name:
            raise ValueError("Name must be added")
        if existing_name:
            raise IntegrityError("Name already exists in the Database")
        return name
    
    @validates('phone_number')
    def validate_phone(cls, key, phone_number):
        if 10 < len(phone_number) > 10:
            raise ValueError("Phone number must be 10 digits")
        return phone_number
    

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('title')
    def validate_title(cls, key, title):
        if not title:
            raise ValueError("Title must be added")
        if "Won't Believe" not in title or "Secret" not in title or "Top" not in title or "Guess" not in title:
            raise ValueError("Not ClickBaitable")
        return title
    
    @validates('content')
    def validate_content(cls, key, content):
        if len(content) < 250 :
            raise ValueError("The content Length Must be greater than 250 characters")
        return content
    
    @validates('summary')
    def validate_summary(cls, key, summary):
        if len(summary) > 250:
            raise ValueError("The content Length Should be Less than 250 characters")
        return summary

    @validates('category')
    def validate_category(cls, key, category):
        if category!='Fiction' and category!='Non-Fiction':
            raise ValueError('The Values are not Valid')
        return category



    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
