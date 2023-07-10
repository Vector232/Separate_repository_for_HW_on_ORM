import sqlalchemy
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from bsdbmodels import create_tables, insert_test_data, Publisher, Book, Shop, Stock, Sale


def load_dsn():
    # подключаемся к окружению
    load_dotenv()
    # достаем переменные из окружения
    dialect = os.getenv('dialect')
    driver = os.getenv('driver')
    login = os.getenv('login')
    password = os.getenv('password')
    server_name = os.getenv('server_name')
    port = os.getenv('port') 
    db_name = os.getenv('db_name_2')

    return f'{dialect}+{driver}://{login}:{password}@{server_name}:{port}/{db_name}'



DSN = load_dsn()
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

insert_test_data(session)

#second try
def get_sales(input):
    mainq = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).select_from(Shop).\
        join(Stock).\
        join(Book).\
        join(Publisher).\
        join(Sale)
    
    if input.isdigit():
        ans = mainq.filter(input == Publisher.id).all()
    else:
        ans = mainq.filter(input == Publisher.name).all()
    
    for title, name, price, date in ans:
         print(f"{title: <40} | {name: <10} | {price: <8} | {date.strftime('%d-%m-%Y')}")

name = 'O\u2019Reilly'
id = '1'
get_sales(input=name)
print()
get_sales(input=id)
session.close()