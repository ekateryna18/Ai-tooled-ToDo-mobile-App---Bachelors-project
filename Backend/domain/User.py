class User:
    def __init__(self, username,  password):
        self.__username__ = username
        self.__password__ = password

    @property
    def username(self):
        return self.__username__

    @username.setter
    def username(self,other):
        self.__username__ = other

    @property
    def password(self):
        return self.__password__

    @password.setter
    def password(self, other):
        self.__password__ = other

    def __str__(self):
        return self.username + " hashed_pw: " + self.password
