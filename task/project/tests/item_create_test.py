import os
import io
from PIL import Image
from django.core.urlresolvers import reverse
from django.conf import settings
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework.renderers import JSONRenderer
from django.contrib.auth.models import User
from project.models import Brand, Item


class ItemTests(APITestCase):

    fixtures = []
    maxDiff = None
    def setUp(self):
        # Normal user
        self.normal_user = User.objects.create(first_name="siddu",username="siddu",email="revansbiradar@gmail.com",
            is_active=True,is_staff=False)
        self.normal_user.set_password('password1234')
        self.normal_user.save()
        self.url = reverse('itemList')
        self.normal_token, created = Token.objects.get_or_create(user=self.normal_user)

    def generate_photo_file(self):
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file


    def test_upload_photo(self):
        """
        Test if we can upload a photo
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.normal_token.key)
        # url = reverse('itemList')
        b1 = Brand.objects.create(name='test brand', title='brand title testing', description='brand desrciption')
        photo_file = self.generate_photo_file()
        data = {
                'name':'test',
                'title': 'test title',
                'brand':  b1.pk,
                'image':photo_file,
                'description':'images files description'
            }
        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_upload_image(self):
        """ unit tests for testing image uploads using DRF"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.normal_token.key)
        b1 = Brand.objects.create(name='test brand', title='brand title testing', description='brand desrciption')

        path_to_image = os.path.join('/home/mypc/Downloads','image.jpg')

        data = {    
            'name':'testImage',
            'title':'tesging',
            'brand':b1.pk,
            'image': open(path_to_image, 'rb'),
            'description':'images files description'
        }
        response = self.client.post(self.url, data ,format='multipart')
        self.assertEquals(response.status_code,201)

    def test_item_add_invalid(self):
        """ unit tests for testing image uploads using DRF"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.normal_token.key)
        b1 = Brand.objects.create(name='test brand', title='brand title testing', description='brand desrciption')
        path_to_image = os.path.join('/home/mypc/Downloads','image.jpg')

        data = {    
            'name':'testImage',
            'title':'tesging',
            'image': open(path_to_image, 'rb'),
            'description':'images files description'
        }

        response = self.client.post(self.url, data ,format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_items_add_put(self):
        """ unit tests for testing image uploads using DRF"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.normal_token.key)
        b1 = Brand.objects.create(name='test brand', title='brand title testing', description='brand desrciption')

        path_to_image = os.path.join('/home/mypc/Downloads','image.jpg')
        item = Item.objects.create(name='asdfg', title="asdf", brand=b1)

        data = {    
            'name':'mage',
            'title':'ing',
            'brand':b1.pk,
            'image': open(path_to_image, 'rb'),
            'description':'images files description'
        }

        response = self.client.put(self.url+ str(item.id), data ,format='multipart')
        self.assertEquals(response.status_code,200)

    def test_items_add_patch(self):
        """ unit tests for testing image uploads using DRF"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.normal_token.key)
        b1 = Brand.objects.create(name='test brand', title='brand title testing', description='brand desrciption')
        item = Item.objects.create(name='asdfg', title="asdf", brand=b1)

        data = {    
            'name':'testing',
            'brand': b1.pk
        }

        response = self.client.patch(self.url+ str(item.id), data ,format='multipart')
        self.assertEquals(response.status_code,200)

    def test_items_delete(self):
        """ unit tests for testing image uploads using DRF"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.normal_token.key)
        b1 = Brand.objects.create(name='test brand', title='brand title testing', description='brand desrciption')
        item = Item.objects.create(name='asdfg', title="asdf", brand=b1)
        item.delete()
        data = {    
            'id':item.id,
            'name':'asdfg',
            'brand': b1.pk
        }

        response = self.client.delete(self.url+ str(item.id), data ,format='multipart')
        self.assertEquals(response.status_code,404)
        

