from datetime import datetime
from typing import Any

from sqlalchemy import (
    DECIMAL,
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import _RelationshipDeclared
from sqlalchemy.sql import expression

from app.db.base_class import Base


class Category(Base):
    id = Column(Integer, primary_key=True, index=True)
    category_name: Column[str] = Column(String, index=True)
    category_code: Column[str] = Column(String)
    active: Column[bool] = Column(
        Boolean, default=True, server_default=expression.true()
    )
    created_at: Column[datetime] = Column(DateTime, default=datetime.now)
    updated_at: Column[datetime] = Column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )

    client_account: _RelationshipDeclared[Any] = relationship(
        "ClientAccount", back_populates="category"
    )


class Strategy(Base):
    id = Column(Integer, primary_key=True, index=True)
    strategy_name: Column[str] = Column(String, index=True)
    strategy_shortname: Column[str] = Column(String, default=None)
    strategy_clubcode: Column[str] = Column(String)
    active: Column[bool] = Column(
        Boolean, default=True, server_default=expression.true()
    )
    created_at: Column[datetime] = Column(DateTime, default=datetime.now)
    updated_at: Column[datetime] = Column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )

    broker: _RelationshipDeclared[Any] = relationship(
        "Broker", back_populates="strategy"
    )
    client_account: _RelationshipDeclared[Any] = relationship(
        "ClientAccount", back_populates="strategy"
    )


class Custodian(Base):
    id = Column(Integer, primary_key=True, index=True)
    custody_name: Column[str] = Column(String, index=True)
    deal_file: Column[bool] = Column(
        Boolean,
        nullable=False,
        default=True,
        server_default=expression.true(),
    )
    trade_file: Column[bool] = Column(
        Boolean,
        nullable=False,
        default=False,
        server_default=expression.false(),
    )
    active = Column(Boolean, default=True, server_default=expression.true())
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    client_account = relationship("ClientAccount", back_populates="custodian")
    dealfile = relationship("DealFile", back_populates="custodian")


class Family(Base):
    id = Column(Integer, primary_key=True, index=True)
    family_name = Column(String, index=True)
    family_shortname = Column(String, default=None)
    external_code = Column(String)
    active = Column(Boolean, default=True, server_default=expression.true())
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class ClientAccount(Base):
    id = Column(Integer, primary_key=True, index=True)
    bo_code = Column(String)
    client_code = Column(String, index=True)
    client_pan = Column(String, index=True)
    client_name = Column(String)
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)
    pool = Column(Boolean, default=True, server_default=expression.true())
    strategy_id = Column(Integer, ForeignKey("strategy.id"), nullable=False)
    custodian_id = Column(Integer, ForeignKey("custodian.id"), nullable=False)
    cp_code = Column(String)
    cpbo_code = Column(String)
    country = Column(String)
    nri_type = Column(String)
    active = Column(Boolean, default=True, server_default=expression.true())
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    category = relationship("Category", back_populates="client_account")
    strategy = relationship("Strategy", back_populates="client_account")
    custodian = relationship("Custodian", back_populates="client_account")


class Broker(Base):
    id = Column(Integer, primary_key=True, index=True)
    broker_name = Column(String, index=True)
    sebi_no = Column(String)
    strategy_id = Column(Integer, ForeignKey("strategy.id"), nullable=True)
    buy_ucc = Column(String, nullable=True)
    sell_ucc = Column(String, nullable=True)
    buy_brok_per = Column(DECIMAL(precision=8, scale=4), nullable=True)
    sell_brok_per = Column(DECIMAL(precision=8, scale=4), nullable=True)
    stt = Column(DECIMAL(precision=8, scale=4), nullable=True)
    hdfc_nse = Column(String, index=True)
    hdfc_bse = Column(String, index=True)
    kotak_broker = Column(String, index=True)
    applicable_on_nri = Column(
        Boolean,
        default=False,
        server_default=expression.false(),
        name="applicable_on_NRI",
        nullable=False,
    )
    active = Column(Boolean, default=True, server_default=expression.true())
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    strategy = relationship("Strategy", back_populates="broker")


class DealFile(Base):
    id = Column(Integer, primary_key=True, index=True)
    bo_code = Column(String, index=True)
    deal_date = Column(Date)
    buy_sell = Column(String, nullable=False)
    isin = Column(String, nullable=False)
    symbol = Column(String, nullable=False)
    exchange = Column(String, nullable=False)
    quantity = Column(DECIMAL(precision=26, scale=5), nullable=False)
    market_rate = Column(DECIMAL(precision=16, scale=5), nullable=False)
    trade_settlement_val = Column(DECIMAL(precision=26, scale=5), nullable=False)
    brok_seb = Column(String, nullable=False)
    total_val = Column(DECIMAL(precision=26, scale=5), nullable=False)
    buy_sell_brokerage = Column(DECIMAL(precision=16, scale=5), nullable=False)
    stt_val = Column(DECIMAL(precision=16, scale=5), nullable=False)
    net_rate = Column(DECIMAL(precision=16, scale=5), nullable=False)
    deal_settlement_val = Column(DECIMAL(precision=26, scale=5), nullable=False)
    total_deal_settlement_val = Column(DECIMAL(precision=26, scale=5), nullable=False)
    settlement_diff = Column(DECIMAL(precision=26, scale=5), nullable=False)
    cpbo_code = Column(String, nullable=False)
    trade_bo_code = Column(String, nullable=False)
    custodian_id = Column(Integer, ForeignKey("custodian.id"), nullable=False)
    cont_no = Column(Integer, nullable=False)
    segment = Column(String, nullable=False)
    settlement_no = Column(Integer, nullable=False)
    trade_year = Column(String, nullable=False)
    bse_code = Column(String)
    series = Column(String, nullable=False)
    scrip_name = Column(String)
    active = Column(Boolean, default=True, server_default=expression.true())
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    custodian = relationship("Custodian", back_populates="dealfile")


class TradeFile(Base):
    id = Column(Integer, primary_key=True, index=True)
    brok_seb = Column(String, nullable=False)
    cont_no = Column(Integer, nullable=False)
    exchange = Column(String, nullable=False)
    trade_date = Column(Date)
    segment = Column(String, nullable=False)
    settlement_no = Column(Integer, nullable=False)
    bo_code = Column(String, nullable=False)
    nse_symbol = Column(String, nullable=False)
    series = Column(String, nullable=False)
    scrip_isin = Column(String, nullable=False)
    bs = Column(String, nullable=False)
    trade_qty = Column(DECIMAL(precision=26, scale=5), nullable=False)
    market_rate = Column(DECIMAL(precision=16, scale=5), nullable=False)
    net_rate = Column(DECIMAL(precision=16, scale=5), nullable=False)
    transaction_tax = Column(DECIMAL(precision=16, scale=5), nullable=False)
    settlement_val = Column(DECIMAL(precision=26, scale=5), nullable=False)
    active = Column(Boolean, default=True, server_default=expression.true())
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class ScripIsin(Base):
    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, nullable=False)
    scrip_name = Column(String, nullable=False)
    scrip_isin = Column(String, nullable=False, index=True, unique=True)
    bse_code = Column(String, nullable=False)
    nse_code = Column(String, nullable=False)
    symbol = Column(String, nullable=False, index=True)
    active = Column(Boolean, default=True, server_default=expression.true())
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    scripisin_brokeruniquebrokerage = relationship(
        "ScripIsinBrokerUniqueBrokerage",
        back_populates="scripisin",
    )


class BrokerUniqueBrokerage(Base):
    id = Column(Integer, primary_key=True, index=True)
    sebi_no = Column(String, nullable=False)
    buy_brok_per = Column(DECIMAL(precision=8, scale=4), nullable=False)
    sell_brok_per = Column(DECIMAL(precision=8, scale=4), nullable=False)
    active = Column(Boolean, default=True, server_default=expression.true())
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    scripisin_brokeruniquebrokerage = relationship(
        "ScripIsinBrokerUniqueBrokerage",
        back_populates="broker_unique_brokerage",
    )


class ScripIsinBrokerUniqueBrokerage(Base):
    id = Column(Integer, primary_key=True, index=True)
    scripisin_id = Column(Integer, ForeignKey("scripisin.id"), nullable=False)
    brokeruniquebrokerage_id = Column(
        Integer,
        ForeignKey("brokeruniquebrokerage.id"),
        nullable=False,
    )
    active = Column(Boolean, default=True, server_default=expression.true())
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    scripisin = relationship(
        "ScripIsin",
        back_populates="scripisin_brokeruniquebrokerage",
    )
    broker_unique_brokerage = relationship(
        "BrokerUniqueBrokerage", back_populates="scripisin_brokeruniquebrokerage"
    )
