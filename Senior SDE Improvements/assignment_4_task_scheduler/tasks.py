class Task():
    def __init__(self, name: str, priority: int, action: callable):
        self.name = name
        self.priority = priority
        self.action = action
        self.status = "pending"

    def execute(self):
        if self.status != 'pending':
            raise Exception('Invalid status type')

        self.action()
        self.status = 'completed'

    def cancel(self):
        self.status = 'cancelled'


    def __lt__(self, other):
        return self.priority < other.priority
