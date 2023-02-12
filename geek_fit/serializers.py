from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from geek_fit.models import Training, Category, Review

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'text stars'.split()

class TrainingSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    reviews = ReviewSerializer(many=True)
    class Meta:
        model = Training
        fields = 'title duration category video reviews'.split()

class TrainingValidateSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField(required=False)
    duration = serializers.CharField()
    category_id = serializers.IntegerField()
    video = serializers.FileField()

    def validate_category_id(self, category_id):
        categories = Category.objects.filter(id=category_id)
        if len(categories) == 0:
            raise ValidationError(f'Category with id({category_id}) does not exist')
        return category_id

class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField()
    training_id = serializers.IntegerField()
    stars = serializers.IntegerField()

    def validate_training_id(self, training_id):
        trainings = Training.objects.filter(id=training_id)
        if len(trainings) == 0:
            raise ValidationError(f'Movie with id({training_id}) does not exist')
        return training_id
