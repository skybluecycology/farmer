# my_classes.py

from dataclasses import dataclass

@dataclass
class User:
    name: str
    email: str
    age: int

class Bob:
    def processUser(self, user: User):
        print(f"Bob is processing user: {user.name}, Email: {user.email}, Age: {user.age}")

class Carol:
    def notifyUser(self, user: User):
        print(f"Carol is notifying user: {user.name}, Email: {user.email}")

class Dave:
    def logUserActivity(self, user: User):
        print(f"Dave is logging activity for user: {user.name}, Age: {user.age}")