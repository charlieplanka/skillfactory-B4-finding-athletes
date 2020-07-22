from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlalchemy as sa
from users import User
import datetime

DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()


class Athlete(Base):
    __tablename__ = "athelete"
    id = sa.Column(sa.Integer, primary_key=True)
    birthdate = sa.Column(sa.Text)
    height = sa.Column(sa.REAL)
    name = sa.Column(sa.Text)


def main():
    print("Hello! We are going to find athletes similar to the current user. I hope it makes you happy.")
    user_id = input("Please enter a user ID (integer number): ")
    session = connect_to_db()
    user = find_user_in_db(session, user_id)
    if not user:
        print("Sorry, there are no user with such ID.")
    else:
        print(f"User's height is {user.height}. User was born at {user.birthdate}.")
        print("Searching for athletes...")
        nearest_athlete_by_height = find_nearest_athlete(session, user.height, "height")
        nearest_athlete_by_birthdate = find_nearest_athlete(session, user.birthdate, "birthdate")
        print(f"The nearest athlete by height is {nearest_athlete_by_height.name} — {nearest_athlete_by_height.height}.")
        print(f"The nearest athlete by birthdate is {nearest_athlete_by_birthdate.name} — {nearest_athlete_by_birthdate.birthdate}.")
    print("I hope you're a happy person now. Bye!")


def connect_to_db():
    engine = sa.create_engine(DB_PATH)
    Session = sessionmaker(engine)
    return Session()


def find_user_in_db(session, user_id):
    user = session.query(User).filter(User.id == user_id).first()
    return user


def find_nearest_athlete(session, user_value, column_name):
    athletes = get_althletes_data(session)
    nearest_athlete = compare_user_data_to_athletes(user_value, athletes, column_name)
    return nearest_athlete


def get_althletes_data(session):
    athletes = session.query(Athlete).all()
    athletes = convert_birhdates_to_datetime(athletes)
    return athletes


def convert_birhdates_to_datetime(athletes):
    for athlete in athletes:
        birthdate = athlete.birthdate
        if isinstance(birthdate, datetime.date):
            continue
        birthdate = datetime.datetime.strptime(birthdate, "%Y-%m-%d").date()
        athlete.birthdate = birthdate
    return athletes


def compare_user_data_to_athletes(user_value, athletes, column_name):
    min_delta = None
    nearest_athlete = None
    for athlete in athletes:
        athlete_value = getattr(athlete, column_name)
        if not athlete_value:
            continue
        delta = abs(user_value - athlete_value)
        if min_delta is None or delta < min_delta:
            min_delta = delta
            nearest_athlete = athlete
    return nearest_athlete


if __name__ == "__main__":
    main()
