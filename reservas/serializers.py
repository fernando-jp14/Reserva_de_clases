from rest_framework import serializers
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
	user = serializers.PrimaryKeyRelatedField(read_only=True)

	class Meta:
		model = Booking
		fields = '__all__'
