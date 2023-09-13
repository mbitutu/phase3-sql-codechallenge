from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Restaurant(Base):
    __tablename__ = 'restaurants'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)

    
    reviews = relationship('Review', back_populates='restaurant')

    
    def all_reviews(self):
        return [review.full_review() for review in self.reviews]

   
    @classmethod
    def fanciest(cls):
        
        return session.query(cls).order_by(cls.price.desc()).first()

    
    def customers(self):
        return [review.customer for review in self.reviews]

    def __repr__(self):
        return f'<Restaurant(name={self.name}, price={self.price})>'
