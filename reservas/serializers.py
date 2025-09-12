from rest_framework import serializers
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
	user = serializers.PrimaryKeyRelatedField(read_only=True)
	user_name = serializers.CharField(source='user.username', read_only=True)
	class_session_id = serializers.IntegerField(source='class_session.id', read_only=True)
	class_session_title = serializers.CharField(source='class_session.title', read_only=True)
	class_session_start = serializers.DateTimeField(source='class_session.start', read_only=True)
	class_session_end = serializers.DateTimeField(source='class_session.end', read_only=True)

	class Meta:
		model = Booking
		fields = [
			'id',
			'user',
			'user_name',
			'class_session_id',
			'class_session_title',
			'class_session_start',
			'class_session_end',
			'status',
		]
