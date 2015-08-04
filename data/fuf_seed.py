"""Utility file to seed unprocessed tree database from Friends of the Urban Forest"""

from model import User, Rating, Movie, connect_to_db, db
from server import app
from datetime import datetime

def load_ratings():
    """Load ratings from u.data into database."""
    
    f = open("seed_data/u.data")

    for line in f:
        split_line = line.rstrip().split()
        new_rating = Rating(user_id=split_line[0], movie_id=split_line[1], score=split_line[2])
        db.session.add(new_rating)

    db.session.commit()



if __name__ == "__main__":
    connect_to_db(app)