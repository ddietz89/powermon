from datetime import datetime
from app import db

class PaginatedMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            'meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
        }
        return data
'''
ChannelPacket
'''
class ChannelPacket(PaginatedMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.Integer)
    datetime = db.Column(db.DateTime, default=datetime.utcnow)
    voltage = db.Column(db.Integer)
    wattsec = db.Column(db.Integer)
    seconds = db.Column(db.Integer)
   

    def to_dict(self):
        data = {
           'id': self.id,
	   'channel_id': self.channel_id,
	   'datetime': self.datetime,
	   'voltage': float(self.voltage) / 10.0,
	   'wattsec': self.wattsec,
	   'seconds': self.seconds
        }
        return data

    def from_dict(self, data):
        for field in ['channel_id', 'voltage', 'wattsec', 'seconds']:
	    if field in data:
	        setattr(self, field, data[field])

'''
Channels
'''

class Channel(PaginatedMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer)
    channel_num = db.Column(db.Integer)
    name = db.Column(db.String)
    
    def to_dict(self):
        data = {
            'id': self.id,
            'device_id': self.device_id,
            'channel_num': self.channel_num,
            'name': self.name
        }
        
        return data
    
    def from_dict(self, data):
        for field in ['device_id', 'channel_num', 'name']:
            if field in data:
                setattr(self, field, data[field])
