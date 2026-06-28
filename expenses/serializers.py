from rest_framework import serializers

from expenses.models import Expense


class ExpenseSerializer(serializers.ModelSerializer):
    paid_by = serializers.StringRelatedField(read_only=True)
    trip = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Expense
        fields = (
            'id',
            'trip',
            'title',
            'amount',
            'paid_by',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'trip', 'paid_by', 'created_at', 'updated_at')

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError('Amount must be greater than zero.')
        return value
