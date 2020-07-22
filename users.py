from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlalchemy as sa
from datetime import datetime

DB_PATH = "sqlite:///sochi_athletes_copy.sqlite3"
Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = sa.Column(sa.Integer, primary_key=True)
    first_name = sa.Column(sa.Text)
    last_name = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    email = sa.Column(sa.Text)
    birthdate = sa.Column(sa.DATE)
    height = sa.Column(sa.REAL)


def get_user_data_from_input():
    print("Please enter some information below.")
    first_name = input("First name: ")
    last_name = input("Last name: ")
    gender = input("Gender (Female or Male): ")
    email = input("Email: ")
    birthdate = input("Birthdate (YYYY-MM-DD): ")
    birthdate = datetime.strptime(birthdate, "%Y-%m-%d").date()
    height = input("Height (in meters, only number without units, e.g. 1.73): ")
    print("Thank you!")

    user = User(
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        email=email,
        birthdate=birthdate,
        height=height
    )
    return user


def append_user_to_db(user):
    session = connect_to_db()
    session.add(user)
    session.commit()
    print(f"The user has been added. ID = {user.id}.")


def connect_to_db():
    engine = sa.create_engine(DB_PATH)
    Session = sessionmaker(engine)
    return Session()


def main():
    print(f"Hello! You are going to add a new user to the '{User.__tablename__}' table.")
    new_user = get_user_data_from_input()
    append_user_to_db(new_user)


if __name__ == "__main__":
    main()
