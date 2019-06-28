from rest_framework import serializers
from .models import Products, Users, AddCard, Bought

class SerializersProducts(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ["id", "name", "price", "file", "active", "created_at", "deleted_at", "updated_at",]
        read_only_fields = ["id", "created_at", "deleted_at", "active", "updated_at"]
     
    def validate_name(self, value):
        if value is not None:
            return value.capitalize()
        raise serializers.ValidationError("product name is required please provide your product name")

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

    def validate_product_name(self, value):
        if value is not None:
            return value
        raise serializers.ValidationError("Product id required")

    class Meta:
        model = AddCard
        fields = "__all__"
        read_only_fields = ["active", "created_at", "updated_at", "deleted_at"]
    


     


        # if value["product_name"] is None:
        #     serializers.ValidationError("Product name is required")
        # if value["product_price"] is None:
        #     serializers.ValidationError("Product price is required")
        # if value["number_of_item"] is None:
        #     serializers.ValidationError("Number of items is required")
        # return value

class SerializersBought(serializers.ModelSerializer):
    class Meta:
        model = Bought
        fields = ()
    pass


class SerializersUsers(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ()
    pass