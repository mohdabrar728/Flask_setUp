from app import db,ma
class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, nullable=False)
    description = db.Column(db.String(120), index=True, nullable=False)
    status = db.Column(db.Boolean, default=False)

class EntrySearilzer(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Entry()

class User(db.Model):
    username = db.Column(db.String(64), primary_key=True)
    password = db.Column(db.String(64),nullable=False)