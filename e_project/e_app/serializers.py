from rest_framework import serializers
from .models import Products, AddCard, Bought, Users
from rest_framework.authtoken.models import Token

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
    


class SerializersUsers(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ('id', 'username', 'email', 'password', 'last_name', 'first_name', 'is_active', 'date_joined')
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ["id", "is_active", "date_joined"]

    def validate(self, data):
        if data["email"] == "" or data["email"] == None:
            raise serializers.ValidationError("email is required")
        if data["username"] == "" or data["username"] == None:
            raise serializers.ValidationError("username is required")
        if data["password"] == "" or data["password"] == None:
            raise serializers.ValidationError("email is required")
        return data

    def create(self, validated_data):
        user = Users(
            email=validated_data['email'],
            username=validated_data['username'],
            is_active=False
        )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user
    
    
class UpdateSerializersUsers(serializers.ModelSerializer):
    
    class Meta:
        model = Users
        fields = ('id', 'username', 'email', 'last_name', 'first_name', 'is_active', 'date_joined')
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ["id", "is_active", "date_joined", 'email', 'username']

    
    def validate(self, data):
        if data["first_name"] == None or data["first_name"] == "":
            raise serializers.ValidationError("first name is required")
        else:
            data["first_name"] = data["first_name"].capitalize()
        if data["last_name"] == None or data["last_name"] == "":
            raise serializers.ValidationError("last name is required")
        else:
            data["last_name"] = data["last_name"].capitalize()
        
        return data

