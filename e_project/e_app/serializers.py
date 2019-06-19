from .models import Products, Users, AddCard, Bought

class SerializersUsers():
    class Meta:
        model = Users
        fields = ()
    pass

class SerializersProducts():
    class Meta:
        model = Products
        fields = ()
    pass

class SerializersAddCard():
    class Meta:
        model = AddCard
        fields = ()
    pass

class SerializersBought():
    class Meta:
        model = Bought
        fields = ()
    pass