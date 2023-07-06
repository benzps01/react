from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/baby-tracker'
db = SQLAlchemy(app)

class Event(db.Model):
    __tablename__ = 'baby'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f'Event: {self.description}'
    
    def __init__(self, description):
        self.description = description
        
    

@app.route('/')
def hello():
    return 'Hey!'

if __name__ == "__main__":
    app.run()