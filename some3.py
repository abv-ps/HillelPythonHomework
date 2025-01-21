class NameDescriptor:
    def __set__(self, instance, value):
        instance.__dict__['name'] = value.strip()
    def __get__(self, instance, value):
        return instance.__dict__['name']
    def __delete__(self, instance):
        delattr(self, instance.__dict__['name'])


class EmailDescriptor:
    def __set__(self, instance, value):
        instance.__dict__['email'] = value.strip()
    def __get__(self, instance, value):
        return instance.__dict__['email']
    def __delete__(self, instance):
        delattr(self, instance.__dict__['email'])


class AddressDescriptor:
    def __set__(self, instance, value):
        instance.__dict__['address'] = value.strip()
    def __get__(self, instance, value):
        return instance.__dict__['address']
    def __delete__(self, instance):
        delattr(self, instance.__dict__['address'])


class Person:
    name = NameDescriptor()
    email = EmailDescriptor()
    address = AddressDescriptor()

    def __init__(self, name, email, address):
        self.name = name
        self.email = email
        self.address = address

    def __str__(self):
        return f'name: {self.name} email: {self.email} address: {self.address}'


human = Person ('Stepan' , 'abv@gmail.com', 'kilimangaro')
humans = Person ('Stella' , 'zet@gmail.com', 'maintain')
print(human)
print(humans)
