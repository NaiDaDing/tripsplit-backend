from rest_framework import serializers

from trips.models import Trip


class TripSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Trip
        fields = (
            'id',
            'name',
            'base_currency',
            'created_by',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'created_by', 'created_at', 'updated_at')

    def validate_base_currency(self, value):
        normalized = value.upper()
        if len(normalized) != 3 or not normalized.isalpha():
            raise serializers.ValidationError('Currency code must be a 3-letter ISO code.')
        return normalized
