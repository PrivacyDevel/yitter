import time

class AuthManager:
    def __init__(self, auth_list, fallback=None):
        self.auth_list = auth_list
        self.blocked_until = [0 for auth in auth_list]
        self.cur = 0

    def _next(self):
        self.cur = (self.cur + 1) % len(self.auth_list)

    def get(self):
        for i in range(len(self.auth_list)):
            if self.blocked_until[self.cur] < time.time():
                auth = self.auth_list[self.cur]
                self._next()
                return auth
            self._next()
        if fallback is not None:
            return fallback()

    def block_last(self):
        self.blocked_until[(self.cur - 1) % len(self.auth_list)] = time.time() + 15

