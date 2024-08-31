from djoser.views import UserViewSet
from drf_spectacular.utils import OpenApiResponse, extend_schema, OpenApiExample
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import NotAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .models import *
from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser

class CustomUserCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CustomUserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Используем метод save() вашего сериализатора для создания пользователя с использованием кастомного менеджера
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomMeViewSet(UserViewSet):

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PromotionConfigViewSet(viewsets.ModelViewSet):
    queryset = PromotionConfig.objects.all()
    serializer_class = PromotionConfigSerializer

    @extend_schema(
        responses={
            400: OpenApiResponse(response=ErrorResponseSerializer, description='Bad Request'),
            403: OpenApiResponse(response=ErrorResponseSerializer, description='Forbidden'),
            404: OpenApiResponse(response=ErrorResponseSerializer, description='Not Found'),
        },
        examples=[
            OpenApiExample(
                'Invalid data',
                summary='Invalid data example',
                value={"error": "Bad Request", "status_code": 400, "message": {"field_name": ["error_detail"]}},
                response_only=True,
                status_codes=["400"]
            ),
            OpenApiExample(
                'Forbidden',
                summary='Forbidden example',
                value={"error": "Forbidden", "status_code": 403, "message": "You do not have permission to perform this action."},
                response_only=True,
                status_codes=["403"]
            ),
            OpenApiExample(
                'Not Found',
                summary='Not Found example',
                value={"error": "Not Found", "status_code": 404, "message": "The requested resource was not found."},
                response_only=True,
                status_codes=["404"]
            ),
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        responses={
            400: OpenApiResponse(response=ErrorResponseSerializer, description='Bad Request'),
            403: OpenApiResponse(response=ErrorResponseSerializer, description='Forbidden'),
            404: OpenApiResponse(response=ErrorResponseSerializer, description='Not Found'),
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

# Repeat similarly for other viewsets





class PromotionViewSet(viewsets.ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionConfigSerializer

    @extend_schema(
        responses={
            400: OpenApiResponse(response=ErrorResponseSerializer, description='Bad Request'),
            403: OpenApiResponse(response=ErrorResponseSerializer, description='Forbidden'),
            404: OpenApiResponse(response=ErrorResponseSerializer, description='Not Found'),
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        responses={
            400: OpenApiResponse(response=ErrorResponseSerializer, description='Bad Request'),
            403: OpenApiResponse(response=ErrorResponseSerializer, description='Forbidden'),
            404: OpenApiResponse(response=ErrorResponseSerializer, description='Not Found'),
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)





class CheckEmail(APIView):

    @extend_schema(
        summary='Check if an email is already registered',
        description='Checks if the given email address is already in use and returns corresponding message.',
        request=None,  # This can be omitted if using default request description
        responses={
            200: OpenApiResponse(description='Email exists', examples=[
                OpenApiExample(
                    name='Email Exists',
                    summary='Existing email',
                    description='The response indicates that the email is already in use.',
                    value='Email exists'
                ),
            ]),
            404: OpenApiResponse(response=ErrorResponseSerializer, description='Email not found'),
            400: OpenApiResponse(response=ErrorResponseSerializer, description='Bad Request')
        },
        examples=[
            OpenApiExample(
                name='Request Example',
                summary='Example POST request with email data',
                description='An example POST request showing how to check an email.',
                value={"email": "example@example.com"}
            )
        ]
    )
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        user = CustomUser.objects.filter(email=email)

        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        user_exists = CustomUser.objects.filter(email=email).exists()
        if user:
            return Response('Email exists', status=status.HTTP_200_OK)
        else:
            return Response({"error": "Email does not exist"}, status=status.HTTP_404_NOT_FOUND)


@extend_schema(tags=['Локация'])
class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



    @extend_schema(
        responses={
            400: OpenApiResponse(response=ErrorResponseSerializer, description='Bad Request'),
            403: OpenApiResponse(response=ErrorResponseSerializer, description='Forbidden'),
            404: OpenApiResponse(response=ErrorResponseSerializer, description='Not Found'),
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        responses={
            400: OpenApiResponse(response=ErrorResponseSerializer, description='Bad Request'),
            403: OpenApiResponse(response=ErrorResponseSerializer, description='Forbidden'),
            404: OpenApiResponse(response=ErrorResponseSerializer, description='Not Found'),
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)



class CustomActivateUser(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):

        print("Request User:", request.user)  # Добавлено логирование
        user = request.user
        if not user or not user.is_authenticated:
            return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        user.is_confirm = True
        user.save()

        return Response({"message": "User confirmed successfully."}, status=status.HTTP_200_OK)

class BaseAdvertisementViewSet(viewsets.ModelViewSet):
    """
    Базовый viewset, который реализует общую логику для всех рекламных объявлений.
    """
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    @extend_schema(
        responses={
            400: OpenApiResponse(response=ErrorResponseSerializer, description='Bad Request'),
            403: OpenApiResponse(response=ErrorResponseSerializer, description='Forbidden'),
            404: OpenApiResponse(response=ErrorResponseSerializer, description='Not Found'),
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        responses={
            400: OpenApiResponse(response=ErrorResponseSerializer, description='Bad Request'),
            403: OpenApiResponse(response=ErrorResponseSerializer, description='Forbidden'),
            404: OpenApiResponse(response=ErrorResponseSerializer, description='Not Found'),
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

@extend_schema(tags=['Подача объявления (Жилая продажа)'])
class SaleResidentialViewSet(viewsets.ModelViewSet):
    queryset = SaleResidential.objects.all()
    serializer_class = SaleResidentialSerializer
    permission_classes = [AllowAny]

@extend_schema(tags=['Аренда длительная (Жилая)'])
class RentLongAdvertisementViewSet(viewsets.ModelViewSet):
    queryset = RentLongAdvertisement.objects.all()
    serializer_class = RentLongAdvertisementSerializer
    permission_classes = [AllowAny]




@extend_schema(tags=['Аренда посуточная (Жилая)'])
class RentDayAdvertisementViewSet(viewsets.ModelViewSet):
    queryset = RentDayAdvertisement.objects.all()
    serializer_class = RentDayAdvertisementSerializer
    permission_classes = [AllowAny]


@extend_schema(tags=['Комерческая продажа'])
class SaleCommercialAdvertisementViewSet(viewsets.ModelViewSet):
    queryset = SaleCommercialAdvertisement.objects.all()
    serializer_class = SaleCommercialAdvertisementSerializer
    permission_classes = [AllowAny]


@extend_schema(tags=['Аренда  Недвижимости (Коммерция)'])
class RentCommercialAdvertisementViewSet(viewsets.ModelViewSet):
    queryset = RentCommercialAdvertisement.objects.all()
    serializer_class = RentCommercialAdvertisementSerializer
    permission_classes = [AllowAny]


@extend_schema(tags=['Фото для объявлений'])
class AdvertisementPhotoViewSet(viewsets.ModelViewSet):
    queryset = AdvertisementPhoto.objects.all()
    serializer_class = AdvertisementPhotoSerializer

    def create(self, request, *args, **kwargs):
        photos = request.FILES.getlist('images')
        photo_instances = []
        for photo in photos:
            photo_instance = AdvertisementPhoto.objects.create(user=request.user, image=photo)
            photo_instances.append(photo_instance)

        serializer = self.get_serializer(photo_instances, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        # Возвращаем все фотографии, сгруппированные по batch_id
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


@extend_schema(tags=['Группа для фотографий'])
class PhotoGroupViewSet(viewsets.ModelViewSet):
    queryset = PhotoGroup.objects.all()
    serializer_class = PhotoGroupSerializer

    def create(self, request, *args, **kwargs):
        object_id = request.data.get('object_id')
        photos_data = request.FILES.getlist('images')
        user = request.user



        # Создаем новую группу для фотографий
        photo_group = PhotoGroup.objects.create()

        photos = []
        for photo_data in photos_data:
            photo = AdvertisementPhoto(
                image=photo_data,
                user=user,
                object_id=object_id,
                photo_group=photo_group
            )
            photo.save()
            photos.append(photo)

        serializer = self.get_serializer(photo_group)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=['Мои объявления'])

class UserAdvertisementsViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user = request.user
        rent_long = RentLongAdvertisement.objects.filter(user=user)
        sale_residential = SaleResidential.objects.filter(user=user)
        rent_day = RentDayAdvertisement.objects.filter(user=user)
        sale_commercial = SaleCommercialAdvertisement.objects.filter(user=user)
        rent_commercial = RentCommercialAdvertisement.objects.filter(user=user)

        combined_queryset = list(rent_long) + list(sale_residential) + list(rent_day) + list(sale_commercial) + list(rent_commercial)

        serialized_data = []
        for obj in combined_queryset:
            if isinstance(obj, RentLongAdvertisement):
                serializer = RentLongAdvertisementSerializer(obj)
            elif isinstance(obj, SaleResidential):
                serializer = SaleResidentialSerializer(obj)
            elif isinstance(obj, RentDayAdvertisement):
                serializer = RentDayAdvertisementSerializer(obj)
            elif isinstance(obj, SaleCommercialAdvertisement):
                serializer = SaleCommercialAdvertisementSerializer(obj)
            elif isinstance(obj, RentCommercialAdvertisement):
                serializer = RentCommercialAdvertisementSerializer(obj)
            serialized_data.append(serializer.data)

        return Response(serialized_data)
