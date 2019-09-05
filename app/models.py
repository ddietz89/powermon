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

class ChannelPackets(PaginatedMixin, db.Model):
   id = db.Column(db.Integer, primary_key=True)
   channel_id = db.Column(db.Integer)
   datetime = db.Column(db.DateTime, default=datetime.utcnow)
   voltage = db.Column(db.Integer)
   wattsec = db.Column(db.Integer)
   

   def to_dict(self):
       data = {
           'id': self.id,
	   'channel_id': self.channel_id,
	   'datetime': self.datetime,
	   'voltage': float(self.voltage) / 10.0,
	   'wattsec': self.wattsec
	   }

       return data
