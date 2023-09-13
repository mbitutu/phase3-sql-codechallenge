from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)

    reviews = relationship('Review', back_populates='customer')

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def favorite_restaurant(self):
        reviews = [review for review in self.reviews if review.restaurant]
        if reviews:
            return max(reviews, key=lambda review: review.star_rating).restaurant

    
    def add_review(self, restaurant, rating):
        review = Review(customer=self, restaurant=restaurant, star_rating=rating)
        session.add(review)
        session.commit()

    def delete_reviews(self, restaurant):
        reviews_to_delete = [review for review in self.reviews if review.restaurant == restaurant]
        for review in reviews_to_delete:
            session.delete(review)
        session.commit()

    def customer_reviews(self):
        return [review.full_review() for review in self.reviews]

    def restaurants(self):
        return [review.restaurant for review in self.reviews]

    def __repr__(self):
        return f'<Customer(name={self.full_name()})>'
