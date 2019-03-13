import random
from math import floor
from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from cockroachdb.sqlalchemy import run_transaction
import os

Base = declarative_base()

DB_URL = os.getenv('DB_URL', "localhost")
DB_PORT = os.getenv('DB_PORT', "26257")
DB_USER = os.getenv('DB_USER', "maxroach")
DB_TABLE = os.getenv('DB_TABLE', "bank")

# The Account class corresponds to the "accounts" database table.
class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    balance = Column(Integer)

    def to_dict(self):
        return {"id": self.id, "balance": self.balance}



# Create an engine to communicate with the database. The
# "cockroachdb://" prefix for the engine URL indicates that we are
# connecting to CockroachDB using the 'cockroachdb' dialect.
# For more information, see
# https://github.com/cockroachdb/cockroachdb-python.

secure_cluster = False # Set to False for insecure clusters

connect_args = {'sslmode': 'disable'}

engine = create_engine(
    f'cockroachdb://{DB_USER}@{DB_URL}:{DB_PORT}/{DB_TABLE}',
    connect_args=connect_args,
    echo=True                   # Log SQL queries to stdout
)

# Automatically create the "accounts" table based on the Account class.
Base.metadata.create_all(engine)


# Store the account IDs we create for later use.

seen_account_ids = set()


# The code below generates random IDs for new accounts.

def create_random_accounts(sess, n):
    """Create N new accounts with random IDs and random account balances.

    Note that since this is a demo, we don't do any work to ensure the
    new IDs don't collide with existing IDs.
    """
    new_accounts = []
    elems = iter(range(n))
    for i in elems:
        billion = 1000000000
        new_id = floor(random.random()*billion)
        seen_account_ids.add(new_id)
        new_accounts.append(
            Account(
                id=new_id,
                balance=floor(random.random()*1000000)
            )
        )
    sess.add_all(new_accounts)

def create_accounts():
    run_transaction(sessionmaker(bind=engine),
                    lambda s: create_random_accounts(s, 10))


# Helper for getting random existing account IDs.

def get_random_account_id():
    id = random.choice(tuple(sessionmaker(bind=engine, expire_on_commit=False)().query(Account.id).distinct()))
    return id


def transfer_funds_randomly(session):
    """Transfer money randomly between accounts (during SESSION).

    Cuts a randomly selected account's balance in half, and gives the
    other half to some other randomly selected account.
    """
    source_id = get_random_account_id()
    sink_id = get_random_account_id()

    source = session.query(Account).filter_by(id=source_id).one()
    amount = floor(source.balance/2)

    # Check balance of the first account.
    if source.balance < amount:
        raise "Insufficient funds"

    source.balance -= amount
    session.query(Account).filter_by(id=sink_id).update(
        {"balance": (Account.balance + amount)}
    )


# Run the transfer inside a transaction.
def randomize_accounts():
    run_transaction(sessionmaker(bind=engine), transfer_funds_randomly)


def get_all_accounts(session):
    f = session.query(Account).all()
    return f

def delete_all_accoutns(session):
    return session.query(Account).delete()

def get_accounts():
    return run_transaction(sessionmaker(bind=engine, expire_on_commit=False), get_all_accounts)

def delete_all():
    return run_transaction(sessionmaker(bind=engine), delete_all_accoutns)
