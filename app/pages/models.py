from app.app_and_db import Base, db
from sqlalchemy import Column, Integer, String, TIMESTAMP, Text

class Trade(Base):
  __tablename__ = 'trades'
  name = Column(Text, primary_key=True)
  from_team = Column(Text, primary_key=True)
  to_team = Column(Text)
  year = Column(Text, primary_key=True)
  note = Column(Text)
  player_id = Column(Text)
  transaction_id = Column(Text)

  def __str__(self):
    return self.note

  def serialize(self):
    return {
      'name' : self.name,
      'from_team' : self.from_team,
      'to_team' : self.to_team,
      'year' : self.year,
      'note' : self.note,
      'player_id' : self.player_id,
      'transaction_id' : self.transaction_id
    }