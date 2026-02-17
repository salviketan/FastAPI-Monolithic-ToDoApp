from datetime import datetime

from pydantic import BaseModel


##### Category Table Schema #####
# Shared properties
class CategoryBase(BaseModel):
    category_name: str
    category_code: str


# Properties to receive on Category creation
class CategoryCreate(CategoryBase):
    pass


# Properties to receive on Category update
class CategoryUpdate(CategoryBase):
    active: bool | None = True


# Properties shared by models stored in DB
class CategoryInDBBase(CategoryBase):
    id: int

    class Config:
        orm_mode = True


# ---------------------------------------------


##### Strategy Table Schema #####
# Shared properties
class StrategyBase(BaseModel):
    strategy_name: str
    strategy_shortname: str | None = None
    strategy_clubcode: str


# Properties to receive on Strategy creation
class StrategyCreate(StrategyBase):
    pass


# Properties to receive on Strategy update
class StrategyUpdate(StrategyBase):
    active: bool | None = True


# Properties shared by models stored in DB
class StrategyInDBBase(StrategyBase):
    id: int

    class Config:
        orm_mode = True


# ---------------------------------------------


##### Custodian Table Schema #####
# Shared properties
class CustodianBase(BaseModel):
    custody_name: str
    deal_file: bool = True
    trade_file: bool = False


# Properties to receive on Custodian creation
class CustodianCreate(CustodianBase):
    pass


# Properties to receive on Custodian update
class CustodianUpdate(CustodianBase):
    active: bool | None = True


# Properties shared by models stored in DB
class CustodianInDBBase(CustodianBase):
    id: int

    class Config:
        orm_mode = True


# ---------------------------------------------


##### Family Table Schema #####
# Shared properties
class FamilyBase(BaseModel):
    family_name: str
    family_shortname: str | None = None
    external_code: str


# Properties to receive on Family creation
class FamilyCreate(FamilyBase):
    pass


# Properties to receive on Family update
class FamilyUpdate(FamilyBase):
    active: bool | None = True


# Properties shared by models stored in DB
class FamilyInDBBase(FamilyBase):
    id: int

    class Config:
        orm_mode = True


# ---------------------------------------------


##### Client Account Table Schema #####
# Shared properties
class ClientAccountBase(BaseModel):
    bo_code: str
    client_code: str
    client_pan: str
    client_name: str
    pool: bool | None = True
    cp_code: str
    cpbo_code: str
    country: str
    nri_type: str


# Properties to receive on Client Account creation
class ClientAccountCreate(ClientAccountBase):
    category_id: int
    strategy_id: int
    custodian_id: int


# Properties to receive on Client Account update
class ClientAccountUpdate(ClientAccountCreate):
    active: bool | None = True


# Properties shared by models stored in DB
class ClientAccountInDBBase(ClientAccountBase):
    id: int
    category: CategoryInDBBase
    strategy: StrategyInDBBase
    custodian: CustodianInDBBase

    class Config:
        orm_mode = True


# ---------------------------------------------


##### Broker Table Schema #####
# Shared properties
class BrokerBase(BaseModel):
    broker_name: str
    sebi_no: str
    buy_ucc: str | None = None
    sell_ucc: str | None = None
    buy_brok_per: str | None = None
    sell_brok_per: str | None = None
    stt: str | None = None
    hdfc_nse: str
    hdfc_bse: str
    kotak_broker: str
    applicable_on_nri: bool | None = False


# Properties to receive on Broker creation
class BrokerCreate(BrokerBase):
    strategy_id: int


# Properties to receive on Broker update
class BrokerUpdate(BrokerBase):
    active: bool | None = True


# Properties shared by models stored in DB
class BrokerInDBBase(BrokerBase):
    id: int
    strategy: StrategyInDBBase | None = None

    class Config:
        orm_mode = True


# ---------------------------------------------


##### DealFile Table Schema #####
# Shared properties
class DealFileBase(BaseModel):
    bo_code: str
    deal_date: datetime
    buy_sell: str
    isin: str
    symbol: str
    exchange: str
    quantity: float
    market_rate: float
    trade_settlement_val: float
    brok_seb: str
    total_val: float
    buy_sell_brokerage: float
    stt_val: float
    net_rate: float
    deal_settlement_val: float
    total_deal_settlement_val: float
    settlement_diff: float
    cpbo_code: str
    trade_bo_code: str
    cont_no: int
    segment: str
    settlement_no: int
    trade_year: str
    bse_code: str | None = None
    series: str
    scrip_name: str | None = None


# Properties to receive on Broker creation
class DealFileCreate(DealFileBase):
    custodian_id: int


# Properties to receive on Broker update
class DealFileUpdate(DealFileBase):
    active: bool | None = True


# Properties shared by models stored in DB
class DealFileInDBBase(DealFileBase):
    id: int
    custodian: CustodianInDBBase

    class Config:
        orm_mode = True


# ---------------------------------------------


##### TradeFile Table Schema #####
# Shared properties
class TradeFileBase(BaseModel):
    brok_seb: str
    cont_no: int
    exchange: str
    trade_date: datetime
    segment: str
    settlement_no: int
    bo_code: str
    nse_symbol: str
    series: str
    scrip_isin: str
    bs: str
    trade_qty: float
    mark_rate: float
    net_rate: float
    transaction_tax: float
    settlement_val: float


# Properties to receive on Broker creation
class TradeFileCreate(TradeFileBase):
    pass


# Properties to receive on Broker update
class TradeFileUpdate(TradeFileBase):
    active: bool | None = True


# Properties shared by models stored in DB
class TradeFileInDBBase(TradeFileBase):
    id: int

    class Config:
        orm_mode = True


# ---------------------------------------------


##### ScripIsin Table Schema #####
# Shared properties
class ScripIsinBase(BaseModel):
    company_name: str
    scrip_name: str
    scrip_isin: str
    bse_code: str
    nse_code: str
    symbol: str


# Properties to receive on Broker creation
class ScripIsinCreate(ScripIsinBase):
    pass


# Properties to receive on Broker update
class ScripIsinUpdate(ScripIsinBase):
    active: bool | None = True


# Properties shared by models stored in DB
class ScripIsinInDBBase(ScripIsinBase):
    id: int

    class Config:
        orm_mode = True


# ---------------------------------------------


##### BrokerUniqueBrokerage Table Schema #####
# Shared properties
class BrokerUniqueBrokerageBase(BaseModel):
    sebi_no: str
    buy_brok_per: str
    sell_brok_per: str


# Properties to receive on Broker creation
class BrokerUniqueBrokerageCreate(BrokerUniqueBrokerageBase):
    pass


# Properties to receive on Broker update
class BrokerUniqueBrokerageUpdate(BrokerUniqueBrokerageBase):
    active: bool | None = True


# Properties shared by models stored in DB
class BrokerUniqueBrokerageInDBBase(BrokerUniqueBrokerageBase):
    id: int

    class Config:
        orm_mode = True


# ---------------------------------------------


##### ScripIsinBrokerUniqueBrokerage Table Schema #####
# Shared properties
class ScripIsinBrokerUniqueBrokerageBase(BaseModel):
    pass


# Properties to receive on Broker creation
class ScripIsinBrokerUniqueBrokerageCreate(ScripIsinBrokerUniqueBrokerageBase):
    scripisin_id: int
    brokeruniquebrokerage_id: int


# Properties to receive on Broker update
class ScripIsinBrokerUniqueBrokerageUpdate(ScripIsinBrokerUniqueBrokerageBase):
    active: bool | None = True


# Properties shared by models stored in DB
class ScripIsinBrokerUniqueBrokerageInDBBase(ScripIsinBrokerUniqueBrokerageBase):
    id: int
    scripisin: ScripIsinInDBBase
    broker_unique_brokerage: BrokerUniqueBrokerageInDBBase

    class Config:
        orm_mode = True


# ---------------------------------------------


# Properties to return to client
class Category(CategoryInDBBase):
    active: bool
    created_at: datetime
    updated_at: datetime


class Strategy(StrategyInDBBase):
    active: bool
    created_at: datetime
    updated_at: datetime


class Custodian(CustodianInDBBase):
    active: bool
    created_at: datetime
    updated_at: datetime


class Family(FamilyInDBBase):
    active: bool
    created_at: datetime
    updated_at: datetime


class ClientAccount(ClientAccountInDBBase):
    active: bool
    created_at: datetime
    updated_at: datetime


class Broker(BrokerInDBBase):
    active: bool
    created_at: datetime
    updated_at: datetime


class DealFile(DealFileInDBBase):
    active: bool
    created_at: datetime
    updated_at: datetime


class TradeFile(TradeFileInDBBase):
    active: bool
    created_at: datetime
    updated_at: datetime


class ScripIsin(ScripIsinInDBBase):
    active: bool
    created_at: datetime
    updated_at: datetime


class BrokerUniqueBrokerage(BrokerUniqueBrokerageInDBBase):
    active: bool
    created_at: datetime
    updated_at: datetime


class ScripIsinBrokerUniqueBrokerage(ScripIsinBrokerUniqueBrokerageInDBBase):
    active: bool
    created_at: datetime
    updated_at: datetime


# Properties stored in DB
class CategoryInDB(CategoryInDBBase):
    pass


class StrategyInDB(StrategyInDBBase):
    pass


class CustodianInDB(CustodianInDBBase):
    pass


class FamilyInDB(FamilyInDBBase):
    pass


class ClientAccountInDB(ClientAccountInDBBase):
    pass


class BrokerInDB(BrokerInDBBase):
    pass


class DealFileInDB(DealFileInDBBase):
    pass


class TradeFileInDB(TradeFileInDBBase):
    pass


class ScripIsinInDB(ScripIsinInDBBase):
    pass


class BrokerUniqueBrokerageInDB(BrokerUniqueBrokerageInDBBase):
    pass


class ScripIsinBrokerUniqueBrokerageInDB(ScripIsinBrokerUniqueBrokerageInDBBase):
    pass
