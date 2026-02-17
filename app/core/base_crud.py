from crud import CRUDBase
from models import (
    Broker,
    BrokerUniqueBrokerage,
    Category,
    ClientAccount,
    Custodian,
    DealFile,
    Family,
    ScripIsin,
    ScripIsinBrokerUniqueBrokerage,
    Strategy,
    TradeFile,
)
from schemas import (
    BrokerCreate,
    BrokerUniqueBrokerageCreate,
    BrokerUniqueBrokerageUpdate,
    BrokerUpdate,
    CategoryCreate,
    CategoryUpdate,
    ClientAccountCreate,
    ClientAccountUpdate,
    CustodianCreate,
    CustodianUpdate,
    DealFileCreate,
    DealFileUpdate,
    FamilyCreate,
    FamilyUpdate,
    ScripIsinBrokerUniqueBrokerageCreate,
    ScripIsinBrokerUniqueBrokerageUpdate,
    ScripIsinCreate,
    ScripIsinUpdate,
    StrategyCreate,
    StrategyUpdate,
    TradeFileCreate,
    TradeFileUpdate,
)


class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]):
    pass


class CRUDStrategy(CRUDBase[Strategy, StrategyCreate, StrategyUpdate]):
    pass


class CRUDCustodian(CRUDBase[Custodian, CustodianCreate, CustodianUpdate]):
    pass


class CRUDFamily(CRUDBase[Family, FamilyCreate, FamilyUpdate]):
    pass


class CRUDClientAccount(
    CRUDBase[ClientAccount, ClientAccountCreate, ClientAccountUpdate],
):
    pass


class CRUDBroker(CRUDBase[Broker, BrokerCreate, BrokerUpdate]):
    pass


class CRUDDealFile(CRUDBase[DealFile, DealFileCreate, DealFileUpdate]):
    pass


class CRUDTradeFile(CRUDBase[TradeFile, TradeFileCreate, TradeFileUpdate]):
    pass


class CRUDScripIsin(CRUDBase[ScripIsin, ScripIsinCreate, ScripIsinUpdate]):
    pass


class CRUDBrokerUniqueBrokerage(
    CRUDBase[
        BrokerUniqueBrokerage,
        BrokerUniqueBrokerageCreate,
        BrokerUniqueBrokerageUpdate,
    ],
):
    pass


class CRUDScripIsinBrokerUniqueBrokerage(
    CRUDBase[
        ScripIsinBrokerUniqueBrokerage,
        ScripIsinBrokerUniqueBrokerageCreate,
        ScripIsinBrokerUniqueBrokerageUpdate,
    ],
):
    pass


category = CRUDCategory(Category)
strategy = CRUDStrategy(Strategy)
custodian = CRUDCustodian(Custodian)
family = CRUDFamily(Family)
client_account = CRUDClientAccount(ClientAccount)
broker = CRUDBroker(Broker)
deal_file = CRUDDealFile(DealFile)
trade_file = CRUDTradeFile(TradeFile)
scripisin = CRUDScripIsin(ScripIsin)
brokeruniquebrokerage = CRUDBrokerUniqueBrokerage(BrokerUniqueBrokerage)
scripisinbrokeruniquebrokerage = CRUDScripIsinBrokerUniqueBrokerage(
    ScripIsinBrokerUniqueBrokerage,
)
