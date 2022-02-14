import pytest
from tinydb import TinyDB, table
from tinydb.storages import MemoryStorage
from crm import User
import re


@pytest.fixture
def setup_db():
    User.DB = TinyDB(storage=MemoryStorage)


@pytest.fixture
def user(setup_db):
    u = User(first_name="Tar", last_name="Tampion", address="rue du soleil 21212 Nuage", phone_number="0101010101")
    u.save()
    return u

def test_full_name(user):
    assert user.full_name == "Tar Tampion"

def test_first_name(user):
    assert user.first_name == "Tar"

def test_last_name(user):
    assert user.last_name == "Tampion"

# def test_address(user):
#     assert user.test_address == "rue du soleil 21212 Nuage"

def test_phone_number(user):
    assert user.phone_number == "0101010101"

def test_exists(user):
    assert user.exists() is True

def test_not_exists():
    u = User(first_name="Sophie",
             last_name="Lagirafe",
             address="1 rue du chemin, 00789 Dodo",
             phone_number="0123456789")
    assert u.exists() is False

def test_db_instance(user):
    assert isinstance(user.db_instance, table.Document)
    assert user.db_instance["first_name"] == "Tar"
    assert user.db_instance["last_name"] == "Tampion"
    assert user.db_instance["address"] == "rue du soleil 21212 Nuage"
    assert user.db_instance["phone_number"] == "0101010101"

def test__check_phone_number():
    user_good = User(first_name="Jean",
                     last_name="Smith",
                     address="1 rue du chemin, 75015, Paris",
                     phone_number="0123456789")
    user_bad = User(first_name="Jean",
                    last_name="Smith",
                    address="1 rue du chemin, 75015, Paris",
                    phone_number="abcd")
    with pytest.raises(ValueError) as err:
        user_bad._check_phone_number()

    assert "invalide" in str(err.value)

    user_good.save(validate_data=True)
    assert user_good.exists() is True

def test__check_names_empty(setup_db):
    user_bad = User(first_name="",
                    last_name="",
                    address="1 rue du chemin, 75000 Paris",
                    phone_number="0123456789")

    with pytest.raises(ValueError) as err:
        user_bad._check_names()

    assert "prenom et nom ne peuvent pas être vide" in str(err.value)

def test__check_names_whith_special_character(setup_db):
    user_bad = User(first_name="Jean%*",
                    last_name="Smith",
                    address="1 rue du chemin, 75000 Paris",
                    phone_number="0123456789")

    with pytest.raises(ValueError) as err:
        user_bad._check_names()

    assert "Nom invalide" in str(err.value)


def test_delete():
    user_test = User(first_name="John",
                     last_name="Smith",
                     address="1 rue du chemin, 75015, Paris",
                     phone_number="0123456789")
    user_test.save()
    first = user_test.delete()
    second = user_test.delete()
    assert len(first) > 0
    assert isinstance(first, list)
    assert len(second) == 0
    assert isinstance(second, list)