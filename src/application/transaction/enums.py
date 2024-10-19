from enum import Enum


class TransactionType(Enum):
    OUTCOME = "outcome"
    INCOME = "income"

class TransactionIncomeType(Enum):
    PURCHASE = "purchase"
    TASK = "task"
    REFERRAL = "referral"
    REFERRAL_EARNINGS = "referral_earnings"

class TransactionOutcomeType(Enum):
    ANALYTICS = "analytics"
    DM_ADS = "dm_ads"
    BOOST = "boost"

