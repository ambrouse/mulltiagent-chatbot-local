from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database.setup_postgres import Base

class type_contract(Base):
    __tablename__ = "type_contract"

    id = Column(String, primary_key=True, index=True)
    path = Column(String)
    required_fields = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    contracts = relationship("contract", back_populates="type_info")


class session(Base):
    __tablename__ = "session"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    id_user = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    contract_his_info = relationship("contract_history_mess", back_populates="session_info")
    contract_info = relationship("contract", back_populates="session_info")


class contract(Base):
    __tablename__ = "contract"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    id_type = Column(String, ForeignKey("type_contract.id"), index = True)
    id_user = Column(String)
    session = Column(Integer, ForeignKey("session.id"), index = True)
    status = Column(String)
    missing_fields = Column(JSON, nullable=True)
    json_data = Column(JSON, nullable=True)
    file_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    type_info = relationship("type_contract", back_populates="contracts")
    session_info = relationship("session", back_populates="contract_info")


class contract_history_mess(Base):
    __tablename__ = "contract_history_mess"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    id_user = Column(String)
    session = Column(Integer, ForeignKey("session.id"), index=True)
    role = Column(String)
    mess = Column(Text)
    session_info = relationship("session", back_populates="contract_his_info")

    
    