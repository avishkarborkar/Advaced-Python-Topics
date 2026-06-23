from enum import Enum
from dataclasses import dataclass

class Priority(Enum):
    LOW = "Low"
    NORMAL = "Normal"
    HIGH = "High"
    URGENT = "Urgent"


class Channel(Enum):
    EMAIL = "Email"
    SMS = "SMS"
    SLACK = "Slack"

@dataclass
class Notification:
    user_id: str
    channel: Channel
    subject: str
    body: str
    priority: Priority
    metadata : dict

@dataclass
class DeliveryResult:
    delivered: bool
    channel: Channel
    error: str
    attempts: int
