from rest_framework import serializers
from .models import Products, AddCard, Bought

class SerializersProducts(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ["id", "name", "price", "file", "active", "created_at", "deleted_at", "updated_at",]
        read_only_fields = ["id", "created_at", "deleted_at", "active", "updated_at"]
     

    def validate(self, values):
        if values["name"] == None:
            raise serializers.ValidationError("product name is required")
        else:
            values["name"] = values["name"].capitalize()
        if values["price"] == None:
            raise serializers.ValidationError("product price is required")
        
        return values

    def __init__(self, *args, **kwargs):
        super(SerializersProducts, self).__init__(*args, **kwargs)
        if self.context != {}:
            request = self.context['request']
            if request.method == 'POST':
                self.write_only_fields = {
                    'name': self.fields['name'], 
                    'price': self.fields['price'],
                    'file': self.fields['file'],
                    'active': self.fields['active']
                }


class SerializersAddCard(serializers.ModelSerializer):
    class Meta:
        model = AddCard
        fields = "__all__"
        read_only_fields = ["active", "created_at", "updated_at", "deleted_at"]
    
    def validate(self, values):
        if values["product_name"] is None:
            raise serializers.ValidationError("product name is required")
        if values["product_price"] == None:
            raise serializers.ValidationError("product price is required")
        if values["number_of_items"] == None:
            values["number_of_items"] = 1
        return values



class SerializersBought(serializers.ModelSerializer):
    class Meta:
        model = Bought
        fields = "__all__"
        read_only_fields = ["active", "created_at", "updated_at", "deleted_at"]
    




from django.contrib.auth import authenticate
from django.contrib.auth.models import User as Users


class SerializersUsers(serializers.ModelSerializer):
    
    class Meta:
        model = Users
        fields = "__all__" #("id", "username", "email", "is_active", "password")
        read_only_fields = ["id"]

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                data["user"] = user
            else:
                raise exceptions.ValidationError("wrong credentials")
        else:
            raise exceptions.ValidationError("password & username are required")
        
        return data
    
