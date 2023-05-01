import re

USER_FSM = {}


class IsTask:
    def __call__(self, message):
        if message.from_user.id in USER_FSM and USER_FSM[message.from_user.id]['task']:
            return True
        else:
            return False

class IsDate:
    def __call__(self, message):
        return bool(re.search('\d{2}/\d{2}', message.text ) or re.search('\d{2}/\d{2}', message.text))
1
class IsNote:
    def __call__(self, message):
        if message.from_user.id in USER_FSM and USER_FSM[message.from_user.id]['note']:
            return True
        else:
            return False
