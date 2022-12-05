from sqlalchemy import Column, String, JSON, DateTime, create_engine
from sqlalchemy.dialects.postgresql import psycopg2
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class AgentDBModel(Base):
    __tablename__ = 'agents'
    id = Column(int, primary_key=True, autoincrement=True)
    name = Column(String(255))
    type = Column(JSON)
    address = Column(String(255))
    role = Column(String(255))
    years = Column(String(255))
    phone = Column(JSON)
    email = Column(String(255))
    website = Column(String(255))
    languages = Column(String(255))
    times = Column(JSON)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


def setup_db():
    engine = create_engine("postgresql://wesley:30086477@localhost:5432/wesley")
    Session = sessionmaker(bind=engine)
    session = Session()
    AgentDBModel.metadata.create_all(engine)
    session.close()


def insert_agent(agent: AgentDBModel):
    engine = create_engine("postgresql://wesley:30086477@localhost:5432/wesley")
    Session = sessionmaker(bind=engine)
    session = Session()
    #agent_exists = session.query(AgentDBModel).filter_by(name=agent['name']).first()

    #if not agent_exists or agent_exists == agent:
    session.add(agent)
    session.commit()
    session.close()
