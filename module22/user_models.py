from pydantic import BaseModel , conint , constr
from typing import Optional

# class User (BaseModel):
#     id: int
#     name: str
#     age: int
#     email: str
#
# user = User(id=1 , name="Amant" , age="16" , email= "test@gmail.com")
#
# print(user)

class User(BaseModel):
    id: int
    name: str
    age: int = 0
    email: str = "test@gmail.com"

user1 = user(id=2, name="Amant")

print(user1)