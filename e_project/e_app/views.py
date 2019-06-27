import datetime
from django.http import Http404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import SerializersProducts, SerializersUsers, SerializersAddCard
from .models import Products, Users, AddCard, Bought

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

