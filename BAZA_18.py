from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, Table, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# создание базы
engine = create_engine('sqlite:///dz18.sqlite')

Base = declarative_base(bind=engine)
Session = sessionmaker()



# wordskills = Table('wordskills', Base.metadata,
#                     Column('id', Integer, primary_key=True),
#                     # связь 1 - много, связь через внешний ключ
#                     Column('id_word' ,Integer, ForeignKey('words.id')),
#                     Column('id_skill', Integer, ForeignKey('skills.id')),
#                     Column('count', Integer),
#                     Column('percent', Integer)
#                    )

class Wordskill(Base):
    __tablename__ = 'wordskills'
    id = Column(Integer, primary_key=True)
    id_word = Column(Integer, ForeignKey('words.id'))
    id_skill = Column(Integer, ForeignKey('skills.id'))
    count = Column(Float, default=0)
    percent = Column(Float, default=0)

    def __str__(self):
        return f'{self.id}) {self.id_word} | {self.id_skill} | {self.count} | {self.percent} |'


class Area(Base):
    __tablename__ = 'area'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    ind = Column(Integer)

    # def __init__(self, name, ind):
    #     self.name = name
    #     self.ind = ind
    #
    # def __str__(self):
    #     return f'{self.id}) {self.name}: {self.ind}'
    def __str__(self):
        return f'{self.id}) {self.name} | {self.ind} |'

    def __repr__(self):
        return f'{self.id} - {self.name} - {self.ind}'

class Skills(Base):
    __tablename__ = 'skills'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f'{self.id}) {self.name}'

class Words(Base):
    __tablename__ = 'words'
    id = Column(Integer, primary_key=True)
    word = Column(String)
    count = Column(Integer)
    up = Column(Integer)
    down = Column(Integer)

    def __init__(self, word, count, up, down):
        self.word = word
        self.count = count
        self.up = up
        self.down = down

    def __str__(self):
        return f'{self.id}) {self.word} {self.count} {self.up} {self.down}'


# создание таблицы
Base.metadata.create_all()
# # заполнение таблиц
# Session = sessionmaker(bind=engine)
# # создание сеанса
# session = Session()

