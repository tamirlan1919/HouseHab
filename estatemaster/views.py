from djoser.views import UserViewSet
from drf_spectacular.utils import OpenApiResponse, extend_schema, OpenApiExample
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
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

@extend_schema(tags=['Аренда длительная (Жилая)'])
class RentLongAdvertisementViewSet(BaseAdvertisementViewSet):
    queryset = RentLongAdvertisement.objects.all()
    serializer_class = RentLongAdvertisementSerializer

@extend_schema(tags=['Аренда посуточная (Жилая)'])
class RentDayAdvertisementViewSet(BaseAdvertisementViewSet):
    queryset = RentDayAdvertisement.objects.all()
    serializer_class = RentDayAdvertisementSerializer

class SaleCommercialAdvertisementViewSet(BaseAdvertisementViewSet):
    queryset = SaleCommercialAdvertisement.objects.all()
    serializer_class = SaleCommercialAdvertisementSerializer

class RentCommercialAdvertisementViewSet(BaseAdvertisementViewSet):
    queryset = RentCommercialAdvertisement.objects.all()
    serializer_class = RentCommercialAdvertisementSerializer