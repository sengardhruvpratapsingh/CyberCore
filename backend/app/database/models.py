from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base


class Case(Base):
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, nullable=False, default="active")
    report_generated = Column(Boolean, nullable=False, default=False)
    terminated_at = Column(DateTime, nullable=True)
    deletion_at = Column(DateTime, nullable=True)

    evidence = relationship(
        "Evidence",
        back_populates="case",
        cascade="all, delete"
    )

    transactions = relationship(
        "Transaction",
        back_populates="case",
        cascade="all, delete"
    )

    device_records = relationship(
        "DeviceRecord",
        back_populates="case",
        cascade="all, delete"
    )

    email_artifacts = relationship(
        "EmailArtifact",
        back_populates="case",
        cascade="all, delete"
    )


class Evidence(Base):
    __tablename__ = "evidence"

    id = Column(Integer, primary_key=True, index=True)

    case_id = Column(
        Integer,
        ForeignKey("cases.id"),
        nullable=False
    )

    filename = Column(String, nullable=False)

    sha256 = Column(String, nullable=False)

    kind = Column(String, nullable=False, default="case_document")
    file_path = Column(String, nullable=True)

    uploaded_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    case = relationship(
        "Case",
        back_populates="evidence"
    )


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    case_id = Column(
        Integer,
        ForeignKey("cases.id"),
        nullable=False
    )

    transaction_id = Column(
        String,
        nullable=False,
        index=True
    )

    sender = Column(
        String,
        nullable=False
    )

    receiver = Column(
        String,
        nullable=False
    )

    amount = Column(
        Float,
        nullable=False
    )

    timestamp = Column(
        DateTime,
        nullable=False
    )

    case = relationship(
        "Case",
        back_populates="transactions"
    )


class DeviceRecord(Base):
    __tablename__ = "device_records"

    id = Column(Integer, primary_key=True, index=True)

    case_id = Column(
        Integer,
        ForeignKey("cases.id"),
        nullable=False
    )

    record_id = Column(
        String,
        nullable=False,
        index=True
    )

    phone_number = Column(
        String,
        nullable=False,
        index=True
    )

    imei = Column(
        String,
        nullable=False,
        index=True
    )

    timestamp = Column(
        DateTime,
        nullable=False
    )

    case = relationship(
        "Case",
        back_populates="device_records"
    )


class EmailArtifact(Base):
    __tablename__ = "email_artifacts"

    id = Column(Integer, primary_key=True, index=True)

    case_id = Column(
        Integer,
        ForeignKey("cases.id"),
        nullable=False
    )

    message_id = Column(
        String,
        nullable=True,
        index=True
    )

    from_address = Column(
        String,
        nullable=True
    )

    to_address = Column(
        String,
        nullable=True
    )

    reply_to = Column(
        String,
        nullable=True
    )

    date_header = Column(
        String,
        nullable=True
    )

    source_ip = Column(
        String,
        nullable=True
    )

    case = relationship(
        "Case",
        back_populates="email_artifacts"
    )