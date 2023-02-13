from rest_framework import serializers
from .models import product
class prod_serail(serializers.ModelSerializer):
    class Meta:
        model=product()
        fields=['name','price']