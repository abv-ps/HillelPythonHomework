import inspect


class Person:
    """Class for """

    def __init__(self, name : str, age: int, email="abv@gmail.com"):

        self.name = name
        self.age = age
        self.email = email


class Human(Person):
    pass

own = Person("Ivan", 18,)
owned = Person("Sara", 33,)
print (type(Person))
print (type(Human))
print(isinstance(own, Person))
print(issubclass(Human, Person))
print(Person.__base__)
print(Person.__dict__)
for attribute in ['name', 'age', 'email']:
    print(f'{attribute}: {getattr(own, attribute)}')
for attribute, value in vars(owned).items():
    print(f'{attribute}: {value}')
print(own.email)
setattr(own, 'email', 'ivan@gmail.com')
print(own.email)



