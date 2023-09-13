from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

# Create the SQLAlchemy engine and session
engine = create_engine('sqlite:///restaurant_reviews.db')
Session = sessionmaker(bind=engine)
session = Session()

# Define the base class for declarative models
Base = declarative_base()

# Define the Restaurant class
class Restaurant(Base):
    __tablename__ = 'restaurants'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)

    # Define the relationship with Review
    reviews = relationship('Review', back_populates='restaurant')

    # Define a method to get all reviews for this restaurant
    def all_reviews(self):
        return [review.full_review() for review in self.reviews]

    # Define a class method to get the fanciest restaurant
    @classmethod
    def fanciest(cls):
        return session.query(cls).order_by(cls.price.desc()).first()

# Define the Customer class
class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)

    # Define the relationship with Review
    reviews = relationship('Review', back_populates='customer')

    # Define a method to get the full name of the customer
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    # Define a method to get the favorite restaurant for this customer
    def favorite_restaurant(self):
        reviews = [review for review in self.reviews if review.restaurant]
        if reviews:
            return max(reviews, key=lambda review: review.star_rating).restaurant

    # Define a method to add a new review
    def add_review(self, restaurant, rating):
        review = Review(customer=self, restaurant=restaurant, star_rating=rating)
        session.add(review)
        session.commit()

    # Define a method to delete all reviews for a specific restaurant
    def delete_reviews(self, restaurant):
        reviews_to_delete = [review for review in self.reviews if review.restaurant == restaurant]
        for review in reviews_to_delete:
            session.delete(review)
        session.commit()

    # Define a method to get all reviews left by this customer
    def reviews(self):
        return [review.full_review() for review in self.reviews]

# Define the Review class
class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    star_rating = Column(Integer)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    customer_id = Column(Integer, ForeignKey('customers.id'))

    # Define the relationships with Restaurant and Customer
    restaurant = relationship('Restaurant', back_populates='reviews')
    customer = relationship('Customer', back_populates='reviews')

    # Define a method to get the customer instance for this review
    def customer(self):
        return self.customer

    # Define a method to get the restaurant instance for this review
    def restaurant(self):
        return self.restaurant

    # Define a method to get the full review text
    def full_review(self):
        return f"Review for {self.restaurant.name} by {self.customer.full_name()}: {self.star_rating} stars."

# Create the database tables
Base.metadata.create_all(engine)
