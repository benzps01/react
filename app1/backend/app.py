from flask import Flask, request
from pytz import timezone
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/baby-tracker'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)

class Event(db.Model):
    __tablename__ = 'baby'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone('Asia/Kolkata')))
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
        
    def format(self):
        return {
            'id': self.id,
            'description': self.description,
            'created_at': self.created_at
        }
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def __repr__(self):
        return f'Event: {self.description}'
    
    def update(self):
        db.session.commit()
    
    def __init__(self, description):
        self.description = description
        
with app.app_context():
    db.create_all()
    

@app.route('/')
def hello():
    return 'Hey!'

# create an event and display them
@app.route('/events', methods=['GET','POST'])
def create_or_show_event():
    if request.method == 'POST':
        description = request.get_json().get('description')
        event = Event(description=description)
        event.insert()
        return event.format()
    events = Event.query.order_by(Event.id.asc()).all()
    event_list = [event.format() for event in events]
    return {
        "events": event_list
    }


#get single event
@app.route('/events/<int:id>', methods = ['GET', 'DELETE', 'PUT'])
def get_or_delete_or_update_event(id):
    if request.method == 'DELETE':
        event = Event.query.filter(Event.id==id).one()
        event.delete()
        return f'Event id: {id} Deleted'
    elif request.method == 'PUT':
        event = Event.query.filter(Event.id == id).one_or_none()
        description = request.get_json().get('description')
        created_at = datetime.now(timezone('Asia/Kolkata'))
        event.description = description
        event.created_at = created_at
        event.update()
        return {
            'event': event.format()
        } 
    event = Event.query.filter(Event.id == id).one()
    formatted_event = event.format()
    return {
        'event': formatted_event
    }
    
if __name__ == "__main__":
    app.run()