import datetime
from django.http import Http404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import generics

from .serializers import ( 
    SerializersProducts, SerializersUsers, 
    SerializersAddCard, SerializersBought 
)

from .models import Products, Users, AddCard, Bought, Users

class ProductSerializer(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = SerializersProducts

    def get_queryset(self):
         return Products.objects.all()

    def create(self, request):
        serializer = SerializersProducts(data = request.data, context = {'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 
    def update(self, request, pk=None):
        getObj = Products.objects.get(id=pk)
        if getObj:
            getObj.name = request.data["name"]
            getObj.price = request.data["price"]
            getObj.file = request.data["file"]
            getObj.created_at = datetime.datetime.now()
            getObj.save()
            return Response({"success": getObj}, status=status.HTTP_200_OK)

        raise Http404
  
    def destroy(self, info, **kwargs):
        try:
            if kwargs["pk"]:
                getObj = Products.objects.get(id=kwargs["pk"])
                if getObj:
                    getObj.delete()
                    return Response({"success": "success deleted product"}, status=status.HTTP_200_OK)
        except Products.DoesNotExist:
            raise Http404


class AddCardView(viewsets.ModelViewSet):
    queryset = AddCard.objects.all()
    serializer_class = SerializersAddCard

    def create(self, request):
        product_name = request.data["product_name"]
        serializer = SerializersAddCard(data = request.data)
        if AddCard.objects.filter(product_name=product_name).exists():
            addCardObj = AddCard.objects.get(product_name=product_name)
            if serializer.is_valid(raise_exception=True):
                product_name = serializer["product_name"].value 
                num_of_items = serializer["number_of_items"].value
                if addCardObj:
                    total_items = addCardObj.number_of_items + int(num_of_items)
                    addCardObj.number_of_items = total_items
                    addCardObj.save()
                    return Response({"success": serializer.data}, status=status.HTTP_200_OK)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class BoughtView(generics.ListAPIView):
    queryset = Bought.objects.all()
    serializer_class  = SerializersBought

    def list(self, request):
        queryset = Bought.objects.all()
        serializer = SerializersBought(queryset, many=True)
        return Response(serializer.data)

class BoughtCreate(generics.CreateAPIView):
    queryset = Bought.objects.all()
    serializer_class  = SerializersBought

    def post(self, request, format=None):
        serializer = SerializersBought(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BoughtUpdate(generics.RetrieveUpdateAPIView):
    lookup_field = 'id'
    queryset = Bought.objects.all()
    serializer_class  = SerializersBought

class BoughtDetails(generics.RetrieveAPIView):
    lookup_field = 'id'
    queryset = Bought.objects.all()
    serializer_class  = SerializersBought

class BoughtDestroy(generics.RetrieveDestroyAPIView):
    lookup_field = 'id'
    queryset = Bought.objects.all()
    serializer_class  = SerializersBought


class UsersView(generics.ListCreateAPIView):
    queryset = Users.objects.all()
    serializer_class = SerializersUsers




from rest_framework.views import APIView
from django.contrib.auth import login as Login, logout as Logout
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication

class LoginView(APIView):
    
    def post(self, request):
        serializer = SerializersUsers(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validate_data["user"]
        Login(request, user)
        token, created = Token.objects.get_or_create(user=user)

        return Response({"token": token.key}, status=200)


class LougoutView(APIView):
    authentication_classes = (TokenAuthentication)

    def post(self, request):
        Logout(request)

        return Response({"success": "logout"}, status=200)

