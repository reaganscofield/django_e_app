import datetime
from django.http import Http404
from rest_framework import status
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import logout as Logout
from django.contrib.auth.models import update_last_login
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import Products, Users, AddCard, Bought, Users
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .permissions import  IsOwner
from .serializers import ( 
    SerializersProducts, SerializersUsers, UpdateSerializersUsers,
    SerializersAddCard, SerializersBought 
)


class ProductSerializer(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser]
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
    permission_classes = [IsAuthenticated]

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




class UsersRetrieveUpdate(generics.RetrieveUpdateAPIView):
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

class LougoutView(APIView):
    def post(self, request):
        Logout(request)

        return Response({"success": "logout"}, status=200)
