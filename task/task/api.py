from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.authtoken.models import Token
from serializers import UserSerializer,BrandSerializer, ItemSerializer 
from project.models import Brand, Item


class UserList(APIView):
	"""
	List all users, or create a new user.
	"""
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		users = User.objects.all()
		serializer = UserSerializer(users, many=True)
		return Response(serializer.data)

	def post(self, request, format=None):
		print request.data
		serializer = UserSerializer(data=request.data)
		if serializer.is_valid():
			user = serializer.save()
			if user:
				token = Token.objects.create(user=user)
				json = serializer.data
				json['token'] = token.key
				return Response(json, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk, format=None):
		user = self.get_object(pk)
		user.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)


class UserDetail(APIView):
	"""
	Retrieve, update or delete a user instance.
	"""
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	def get_object(self, pk):
		try:
			return User.objects.get(pk=pk)
		except User.DoesNotExist:
			raise Http404

	def get(self, request, pk, format=None):
		user = self.get_object(pk)
		user = UserSerializer(user)
		return Response(user.data)

	def put(self, request, pk, format=None):
		user = self.get_object(pk)
		serializer = UserSerializer(user, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def patch(self, request, pk, format=None):
		user = self.get_object(pk)
		serializer = UserSerializer(user, data= request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data,status.HTTP_200_OK)
		return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk, format=None):
		user = self.get_object(pk)
		user.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)



class BrandList(APIView):
	permission_classes = (IsAuthenticated,)
	authentication_classes = (TokenAuthentication,)
	parser_classes = (MultiPartParser, FormParser,)

	def get(self, request, format = None):
		brand = Brand.objects.all()
		serializer = BrandSerializer(brand, many = True)
		return Response(data= serializer.data, status = status.HTTP_200_OK)

	def post(self, request, format = None):
		serializer = BrandSerializer(data=request.data, context={'request':request})
		print serializer
		if serializer.is_valid():
			print "valid "
			serializer.save()
			return Response(serializer.data, status = status.HTTP_201_CREATED)
		return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class BrandDetail(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	parser_classes = (MultiPartParser, FormParser,)

	def get_object(self, pk):
		try:
			return Brand.objects.get(pk=pk)
		except:
			return Http404

	def get(self, request, pk,format=None):
		brand = self.get_object(pk)
		print "brand", brand
		serializer = BrandSerializer(brand,context={'request':request})
		return Response(data=serializer.data, status = status.HTTP_200_OK)

	def post(self, request, format = None):
		serializer = ItemSerializer(data=request.data, files = request.FILES)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status = status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

	def put (self, request, pk, format= None):
		brand = self.get_object(pk)
		serializer = BrandSerializer(brand, data= request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

	def patch(self, request, pk, format=None):
		brand = self.get_object(pk)
		serializer = BrandSerializer(brand, data= request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data,status.HTTP_200_OK)
		return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk, format= None):
		brand = self.get_object(pk)
		brand.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)


class ItemList(APIView):
	permission_classes = (IsAuthenticated,)
	authentication_classes = (TokenAuthentication,)
	parser_classes = (MultiPartParser, FormParser,)

	def get(self, request, format = None):
		item = Item.objects.all()
		serializer = ItemSerializer(item, many = True)
		return Response(data= serializer.data, status = status.HTTP_200_OK)

	def post(self, request, format = None):
		serializer = ItemSerializer(data=request.data, context={'request':request})
		print serializer
		if serializer.is_valid():
			print "valid "
			serializer.save()
			return Response(serializer.data, status = status.HTTP_201_CREATED)
		return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class ItemDetail(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	parser_classes = (MultiPartParser, FormParser,)

	def get_object(self, pk):
		try:
			return Item.objects.get(pk=pk)
		except:
			return Http404

	def get(self, request, pk,format=None):
		item = self.get_object(pk)
		print "item", item
		serializer = ItemSerializer(item,context={'request':request})
		return Response(data=serializer.data, status = status.HTTP_200_OK)

	def post(self, request, format = None):
		serializer = ItemSerializer(data=request.data, files = request.FILES)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status = status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

	def put (self, request, pk, format= None):
		item = self.get_object(pk)
		serializer = ItemSerializer(item, data= request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

	def patch(self, request, pk, format=None):
		item = self.get_object(pk)
		serializer = ItemSerializer(item, data= request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data,status.HTTP_200_OK)
		return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk, format= None):
		item = self.get_object(pk)
		item.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)


