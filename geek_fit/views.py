from rest_framework.response import Response
from rest_framework import status
from geek_fit.models import Training, Category, Review
from geek_fit.serializers import TrainingSerializer, TrainingValidateSerializer, CategorySerializer, ReviewSerializer, ReviewValidateSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

class TrainingModelViewSet(ModelViewSet):
    queryset = Training.objects.all()
    serializer_class = TrainingSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'id'

    def create(self, request, *args, **kwargs):
        serializer = TrainingValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        training = Training.objects.create(**serializer.validated_data)
        training.save()
        return Response(data=TrainingSerializer(training).data,
                        status=status.HTTP_201_CREATED)

class CategoryModelViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'

class ReviewModelViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = 'id'

    def create(self, request, *args, **kwargs):
        serializer = ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        text = serializer.validated_data.get('text')
        training_id = serializer.validated_data.get('training_id')
        stars = serializer.validated_data.get('stars')
        review = Review.objects.create(text=text, training_id=training_id, stars=stars)
        review.save()
        return Response(data=ReviewSerializer(review).data, status=status.HTTP_201_CREATED)

