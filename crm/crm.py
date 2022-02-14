import re
import string
from tinydb import TinyDB, where
from pathlib import Path

class User:

    DB = TinyDB(Path(__file__).resolve().parent / 'db.json', indent=4) #récupérer le chemin absolu vers db.json

    def __init__(self, first_name:str, last_name:str, phone_number: str="", address: str=""):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.address = address

    def __repr__(self):
        return f"User({self.first_name}, {self.last_name})"

    def __str__(self):
        return f"{self.full_name}\n{self.phone_number}\n{self.address}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


    @property
    def db_instance(self):
        return User.DB.get((where('first_name') == self.first_name) & (where('last_name') == self.last_name))

    def _check_phone_number(self):
        phone_number = re.sub(r"[+()\s]*", "", self.phone_number)
        print(phone_number, 'hello')
        if len(phone_number)<10 or not phone_number.isdigit():
            raise ValueError(f"Numéro {self.phone_number} invalide ")

    def _check_names(self):
        if not (self.first_name and self.last_name):
            raise ValueError("prenom et nom ne peuvent pas être vide")
        special_characters = string.punctuation + string.digits
        for character in self.first_name + self.last_name:
            if character in special_characters:
                raise ValueError(f"Nom invalide {self.full_name}")

    def _checks(self):
        self._check_names()
        self._check_phone_number()

    def exists(self):
        return bool(self.db_instance)

    def delete(self):
        if self.exists():
            return User.DB.remove(doc_ids=[self.db_instance.doc_id])
        return []

    def save(self, validate_data: bool=False) -> int:
        if validate_data == True:
            self._checks()
        
        return User.DB.insert(self.__dict__)
def get_all_users():
    # print(User.DB.all())
    # for user in User.DB.all():
        # print(user)
        # u = User(**user)
        # print(u.first_name)
    return [User(**user)for user in User.DB.all()]

if __name__ == "__main__":
    daniel = User("Daniel", "Garcia")
    tartampion = User("Tar", "Tampion")
    print(daniel.delete())
    # print("daniel = " , daniel.exists(), "tartampion = ", tartampion.exists())
    # print(daniel.db_instance)
    # print(type(daniel.db_instance))
    # print("tous ", get_all_users())
    # from faker import Faker
    # fake = Faker(locale="fr_FR")
    # for _ in range(5):
    #     user = User(first_name = fake.first_name(), 
    #                 last_name = fake.last_name(), 
    #                 phone_number = fake.phone_number(), 
    #                 address = fake.address())
    #     print(user.__dict__ , "dict")
    #     print(user.save)
    #     # user.save(validate_data=True)

    #     # print(user)
    #     print("-" * 5, "fake user")
    # User.DB