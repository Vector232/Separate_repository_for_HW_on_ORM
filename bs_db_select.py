import sqlalchemy
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from bs_db_models import create_tables, insert_test_data, Publisher, Book, Shop, Stock, Sale

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

DSN = f'{dialect}+{driver}://{login}:{password}@{server_name}:{port}/{db_name}'
#print(DSN)

engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

insert_test_data(session)

input = 'O\u2019Reilly'
# название книги | название магазина, в котором была куплена эта книга | стоимость покупки | дата покупки
subq = session.query(Publisher.id).filter(Publisher.name == input).subquery()
subq2 = session.query(Book.id, Book.title).filter(subq.c.id == Book.id_publisher).subquery()
subq3 = session.query(Stock.id_shop).filter(Stock.id_book == subq2.c.id).subquery()
subq4 = session.query(Shop.name).filter(Shop.id == subq3.c.id_shop).subquery()
ans = session.query(subq2.c.title, subq4.c.name, Sale.price, Sale.date_sale).distinct()

ans = session.query(subq2.c.title, subq4.c.name, Sale.price, Sale.date_sale).distinct()

str_len_title = max([len(title[0]) for title in ans])
str_len_name = max([len(name[1]) for name in ans])

for c in ans:
    print(f'{str(c[0]).center(str_len_title)}|{str(c[1]).center(str_len_name)}|{str(c[2]).center(10)}|{str(c[3]).center(15)}')

session.close()