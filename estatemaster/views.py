from uuid import UUID

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from drf_spectacular.utils import OpenApiResponse, extend_schema, OpenApiExample
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action, permission_classes
from rest_framework.exceptions import NotAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .models import *
from .filters import *
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
    filter_backends = [DjangoFilterBackend]  # Подключаем backend для фильтрации
    filterset_class = SaleResidentialFilter  # Указываем класс фильтра
    permission_classes = [AllowAny]

@extend_schema(tags=['Аренда длительная (Жилая)'])
class RentLongAdvertisementViewSet(viewsets.ModelViewSet):
    queryset = RentLongAdvertisement.objects.all()
    serializer_class = RentLongAdvertisementSerializer
    filter_backends = [DjangoFilterBackend]  # Подключаем backend для фильтрации
    filterset_class = RentLongFilter  # Указываем класс фильтра
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
    filter_backends = [DjangoFilterBackend]  # Подключаем backend для фильтрации
    filterset_class = SaleCommercialFilter  # Указываем класс фильтра
    permission_classes = [AllowAny]


@extend_schema(tags=['Аренда  Недвижимости (Коммерция)'])
class RentCommercialAdvertisementViewSet(viewsets.ModelViewSet):
    queryset = RentCommercialAdvertisement.objects.all()
    serializer_class = RentCommercialAdvertisementSerializer
    filter_backends = [DjangoFilterBackend]  # Подключаем backend для фильтрации
    filterset_class = RentCommercialFilter  # Указываем класс фильтра
    permission_classes = [AllowAny]


@extend_schema(tags=['Фото для объявлений'])
class AdvertisementPhotoViewSet(viewsets.ModelViewSet):
    queryset = AdvertisementPhoto.objects.all()
    serializer_class = AdvertisementPhotoSerializer

    def create(self, request, *args, **kwargs):
        photos = request.FILES.getlist('images')
        is_main_flags = request.data.getlist('isMain')  # Получаем значения isMain из запроса
        photo_instances = []

        # Установить первое фото как главное по умолчанию, если не указано другое
        main_photo_set = False

        for index, photo in enumerate(photos):
            # Проверка переданного значения isMain или установка главного по умолчанию
            if index < len(is_main_flags):
                is_main = is_main_flags[index].lower() == 'true'
            else:
                is_main = not main_photo_set  # Ставим True только для первого, если еще не было главного

            # Обновление флага, если главное фото установлено
            if is_main:
                main_photo_set = True

            # Создание экземпляра фото
            photo_instance = AdvertisementPhoto.objects.create(
                user=request.user,
                image=photo,
                isMain=is_main
            )

            # Если фото установлено как главное, сбрасываем остальные
            if is_main:
                AdvertisementPhoto.objects.filter(
                    photo_group=photo_instance.photo_group, isMain=True
                ).exclude(id=photo_instance.id).update(isMain=False)

            photo_instances.append(photo_instance)

        serializer = self.get_serializer(photo_instances, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

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




@extend_schema(tags=['Избранное'])
class FavoritesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Получаем список избранных
        favorites = request.user.favorites.all()
        result = []

        # Проходим по каждому избранному объекту и добавляем его в результат
        for favorite in favorites:
            instance = favorite.content_object
            model_name = instance.__class__.__name__
            serializer_class = globals().get(f'{model_name}Serializer')

            if serializer_class:
                serializer = serializer_class(instance)
                result.append(serializer.data)

        return Response(result, status=200)

    def post(self, request, uuid=None):
        # Validate UUID format
        try:
            advertisement_uuid = UUID(uuid, version=4)
        except ValueError:
            return Response({'error': 'Invalid UUID format'}, status=400)

        # Retrieve the advertisement
        advertisement = self.get_advertisement_by_uuid(advertisement_uuid)
        if not advertisement:
            return Response({'error': 'Advertisement not found'}, status=404)

        # Add to favorites
        request.user.add_to_favorites(advertisement)
        return Response({'status': 'added'})

    def delete(self, request, uuid=None):
        # Validate UUID format
        try:
            advertisement_uuid = UUID(uuid)
        except ValueError:
            return Response({'error': 'Invalid UUID'}, status=400)

        # Retrieve the advertisement
        advertisement = self.get_advertisement_by_uuid(advertisement_uuid)
        if not advertisement:
            return Response({'error': 'Advertisement not found'}, status=404)

        content_type = ContentType.objects.get_for_model(advertisement.__class__)
        favorite = Favorite.objects.filter(
            user=request.user,
            advertisement_type=content_type,
            object_id=advertisement_uuid
        ).first()

        if not favorite:
            return Response({'error': 'Favorite not found'}, status=404)

        # Удаление из избранного
        favorite.delete()
        return Response({'status': 'removed'})

    def get_advertisement_by_uuid(self, advertisement_uuid):
        # Ищем объект среди всех моделей объявлений
        models = [SaleResidential, RentLongAdvertisement, RentDayAdvertisement, SaleCommercialAdvertisement, RentCommercialAdvertisement]
        for model in models:
            try:
                advertisement = model.objects.get(id=advertisement_uuid)
                return advertisement
            except model.DoesNotExist:
                continue
        return None

    # Удаление всех избранных объектов
    def delete_all(self, request):
        request.user.favorites.all().delete()
        return Response({'status': 'all favorites removed'}, status=204)


@extend_schema(tags=['Избранное удаление всех'])
class RemoveAllFavoritesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        # Логика для удаления всех избранных
        request.user.favorites.all().delete()
        return Response({'status': 'all favorites removed'}, status=204)

@permission_classes([AllowAny])
class PublicUserDetailView(APIView):

    def get(self, request, id, *args, **kwargs):
        user = get_object_or_404(CustomUser, id=id)
        serializer = CustomUserProfileSerializer(user)
        return Response(serializer.data)


