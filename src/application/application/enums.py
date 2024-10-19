from enum import Enum


class ApplicationStatus(Enum):
    WAITING = "waiting"
    REJECTED = "rejected"
    INVITED = "invited"
    ACCEPTED = "accepted"