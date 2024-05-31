from djoser.views import UserViewSet
from drf_spectacular.utils import OpenApiResponse, extend_schema, OpenApiExample
from rest_framework import status
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

class BuilderViewSet(viewsets.ModelViewSet):
    queryset = Builder.objects.all()
    serializer_class = BuilderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return SaleResidential.objects.filter(user=self.request.user)

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

# Similarly for other viewsets
class SaleResidentialViewSet(viewsets.ModelViewSet):
    queryset = SaleResidential.objects.all()
    serializer_class = SaleResidentialSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return SaleResidential.objects.filter(user=self.request.user)


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


class RentLongAdvertisementViewSet(viewsets.ModelViewSet):
    queryset = RentLongAdvertisement.objects.all()
    serializer_class = RentLongAdvertisementSerializer

    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return SaleResidential.objects.filter(user=self.request.user)
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


class RentDayAdvertisementViewSet(viewsets.ModelViewSet):
    queryset = RentDayAdvertisement.objects.all()
    serializer_class = RentDayAdvertisementSerializer

    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return SaleResidential.objects.filter(user=self.request.user)
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


class SaleCommercialAdvertisementViewSet(viewsets.ModelViewSet):
    queryset = SaleCommercialAdvertisement.objects.all()
    serializer_class = SaleCommercialAdvertisementSerializer

    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return SaleResidential.objects.filter(user=self.request.user)

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


class RentCommercialAdvertisementViewSet(viewsets.ModelViewSet):
    queryset = RentCommercialAdvertisement.objects.all()
    serializer_class = RentCommercialAdvertisementSerializer

    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return SaleResidential.objects.filter(user=self.request.user)

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