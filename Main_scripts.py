from sqlalchemy import create_engine, ForeignKey, Column, String, CHAR, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base() #Создание базового класса
class Users_dns(Base):
    __tablename__ = 'Users_dns'
    # Create columns
    user_id = Column("id", Integer, primary_key=True, nullable=False, autoincrement=True)
    username = Column("username", String(50), nullable=False)
    gender = Column("gender", String(1), nullable=False)
    country = Column("country", String(50), nullable=False)
    city = Column("city", String(100), nullable=False)

    # Table initializing
    def __init__(self, username, gender, country, city):
        self.username = username
        self.gender = gender
        self.country = country
        self.city = city


    def __repr__(self):
        return f"({self.user_id} {self.username} {self.gender} {self.country} {self.city})"

engine = create_engine('sqlite:///users_dns.db', echo=True)
Base.metadata.create_all(bind=engine)

def insert_user(username, gender, country, city):
    """
    :param username: название пользователя
    :param gender: его пол
    :param country: страна пользователя
    :param city: город пользователя
    :return: возвращает успешный/неуспешный ответ о добавлении пользователя
    """
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        user = Users_dns(username, gender, country, city)
        session.add(user)
        session.commit()
        return 1
    except:
        return 0

def get_all_users():
    """
    Получение всех пользователей списком
    """
    Session = sessionmaker(bind=engine)
    session = Session()
    results = session.query(Users_dns).all()
    return results

def get_usa_users():
    """
        Получение всех пользователей списком из США
        """
    Session = sessionmaker(bind=engine)
    session = Session()
    results = session.query(Users_dns)\
        .filter(Users_dns.country == 'USA')\
        .filter(Users_dns.city == 'Atlanta')
    usa_users = []
    for user in results:
        usa_users.append(user)
    return usa_users

def delete_rus_users():
    """
    Удаление всех пользователей из Russia
    """
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        session.query(Users_dns).filter_by(country='Russia').delete()
        session.commit()
        return 1
    except:
        return 0

def specify_russia_name():
    """
    Изменяет Russia -> Russian Federation
    """
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        session.query(Users_dns).filter_by(country='Russia').update({Users_dns.country: 'Russian Federation'})
        session.commit()
        return 1
    except:
        return 0

# insert_user('Roman', 'm', 'Russia', 'Moscow')
# specify_russia_name()
# print(get_all_users())


