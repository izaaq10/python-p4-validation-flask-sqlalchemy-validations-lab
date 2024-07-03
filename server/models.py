from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database_name.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    @validates('name')
    def validate_name(self, key, name):
        if not name.strip():
            raise ValueError("Name cannot be empty.")
        return name.strip()

    def validate_unique_name(self, key, name):
        existing_author = Author.query.filter(Author.name == name).first()
        if existing_author:
            if existing_author.id != self.id:
                raise ValueError("Another author with this name already exists.")
        return name
    
    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if phone_number and len(phone_number) != 10:
            raise ValueError("Phone number must be exactly 10 digits.")
        return phone_number
    
    def __repr__(self):
        return f'Author(id={self.id}, name={self.name}, phone_number={self.phone_number})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    summary = db.Column(db.String(250), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    @validates('content')
    def validate_content(self, key, content):
        if len(content.strip()) < 250:
            raise ValueError("Content must be at least 250 characters long.")
        return content

    @validates('category')
    def validate_category(self, key, category):
        if category not in ['Fiction', 'Non-Fiction']:
            raise ValueError("Category must be either 'Fiction' or 'Non-Fiction'.")
        return category

    @validates('summary')
    def validate_summary(self, key, summary):
        if len(summary.strip()) > 250:
            raise ValueError("Summary must not exceed 250 characters.")
        return summary

      
    @validates('title')
    def validate_title(self, key, title):
        clickbait_phrases = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(phrase in title for phrase in clickbait_phrases):
            raise ValueError("Title must contain one of the following: 'Won't Believe', 'Secret', 'Top', 'Guess'.")
        return title

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title}, content={self.content}, category={self.category}, summary={self.summary})'
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
