import datetime
from builtins import int

from django.http import Http404
from rest_framework import status
from rest_framework import viewsets
from rest_framework import generics
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import logout as Logout
from django.contrib.auth.models import update_last_login
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import Products, Users, AddCard, Bought, Users
from .customer_permissions import  IsOwner, IsAdminUserOrReadOnly, IsOwnerUser
from rest_framework.permissions import (
    IsAuthenticated, 
    IsAdminUser, 
    AllowAny, 
    IsAuthenticatedOrReadOnly
)
from .serializers import ( 
    SerializersProducts, 
    SerializersUsers, 
    UpdateSerializersUsers,
    SerializersAddCard, 
    SerializersBought 
)


####
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Message                                            
from .serializers import MessageSerializer


def update(request, pk=None):
    getObj = Products.objects.get(id=pk)
    if getObj:
        getObj.name = request.data["name"]
        getObj.price = request.data["price"]
        getObj.file = request.data["file"]
        getObj.updated_at = datetime.datetime.now()
        getObj.save()
        return Response({"success": getObj}, status=status.HTTP_200_OK)

    raise Http404


def create(request):
    serializer = SerializersProducts(data = request.data, context = {'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductSerializer(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminUserOrReadOnly]
    queryset = Products.objects.all()
    serializer_class = SerializersProducts

    def get_queryset(self):
         return Products.objects.all()

    def destroy(self, info, **kwargs):
        try:
            if kwargs["pk"]:
                getObj = Products.objects.get(id=kwargs["pk"])
                if getObj:
                    getObj.delete()
                    return Response({"success": "success deleted product"}, status=status.HTTP_200_OK)
        except Products.DoesNotExist:
            raise Http404


class ProductsSearch(generics.ListAPIView):
    serializer_class = SerializersProducts

    def get_queryset(self):
        qs = Products.objects.all()

        name = self.request.query_params.get('name', None)
        price = self.request.query_params.get('price', "0")
        created_at = self.request.query_params.get('created_at', None)
        active = self.request.query_params.get("active", None)

   
        qs = qs.filter(
            Q(name=name) |
            Q(price=int(price)) |
            Q(created_at=created_at) |
            Q(active=active)
        )

        return qs



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


def list(request):
    queryset = Bought.objects.filter(customer_id=request.user)
    serializer = SerializersBought(queryset, many=True)
    return Response(serializer.data)


class BoughtView(generics.ListAPIView):
    queryset = Bought.objects.all()
    serializer_class  = SerializersBought
    permission_classes = [IsAuthenticated]


class BoughtCreate(generics.CreateAPIView):
    queryset = Bought.objects.all()
    serializer_class  = SerializersBought
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated, IsAdminUserOrReadOnly]


class BoughtDetails(generics.RetrieveAPIView):
    lookup_field = 'id'
    queryset = Bought.objects.all()
    serializer_class  = SerializersBought
    permission_classes = [IsAuthenticated, IsOwner]

class BoughtDestroy(generics.RetrieveDestroyAPIView):
    lookup_field = 'id'
    queryset = Bought.objects.all()
    serializer_class  = SerializersBought
    permission_classes = [IsAuthenticated, IsAdminUserOrReadOnly]
    


class UsersView(generics.ListCreateAPIView):
    queryset = Users.objects.all()
    serializer_class = SerializersUsers
    permission_classes = [IsAuthenticated, IsAdminUser]


class UsersRetrieveUpdate(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, IsOwnerUser]
    lookup_field = 'id'
    queryset = Users.objects.all()
    serializer_class = UpdateSerializersUsers


class UsersRetrieveDestroy(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    lookup_field = 'id'
    queryset = Users.objects.all()
    serializer_class = UpdateSerializersUsers


class UserCreate(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = SerializersUsers


class LoginView(APIView):
    permission_classes = ()

    def post(self, request,):
        username = request.data.get("username")
        password = request.data.get("password")
        if username == "" and password == "":
            return Response({
                "error": "username and password is required"
            })
        user = authenticate(
            username=username, 
            password=password
        )
        if user:
            token, created = Token.objects.get_or_create(user=user)
            update_last_login(None, token.user)
            return Response({"token": token.key})
        else:
            return Response({
                "error": "Wrong Credentials"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

class IfLoggedIn(generics.ListAPIView):
    queryset = Users.objects.all()
    serializer_class = SerializersUsers
    permission_classes = [IsAuthenticated, IsOwner]

    def get(self, request):
        queryset = Users.objects.get(username=request.user)
        serializer = SerializersUsers(queryset)
        return Response(serializer.data)

class LougoutView(APIView):
    def post(self, request):
        Logout(request)

        return Response({"success": "logout"}, status=200)



@csrf_exempt                                                    
def user_list(request, id=None):
    if request.method == 'GET':
        if id:                                                              
            users = Users.objects.filter(id=id)        
        else:
            users = Users.objects.all()    
        serializer = SerializersUsers(users, many=True, context={'request': request}) 
        return JsonResponse(serializer.data, safe=False)    
    elif request.method == 'POST':
        data = JSONParser().parse(request)         
        serializer = UserSerializer(data=data)      
        if serializer.is_valid():
            serializer.save()     
            return JsonResponse(serializer.data, status=201)    
        return JsonResponse(serializer.errors, status=400)  


@csrf_exempt
def message_list(request, sender=None, receiver=None):
    if request.method == 'GET':
        messages = ( Message.objects.filter(sender_id=sender).filter(receiver_id=receiver) | 
                     Message.objects.filter(sender_id=receiver).filter(receiver_id=sender)
                    )
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

