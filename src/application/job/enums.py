from enum import Enum


class WorkType(Enum):
    REMOTE = "remote"
    ONSITE = "on-site"
    HYBRID = "hybrid"
    
class EmploymentType(Enum):
    FULL_TIME = "Full-time"
    PART_TIME = "Part-time"
    CONTRACT = "Contract"
    FLEXIBLE = "Flexible"
