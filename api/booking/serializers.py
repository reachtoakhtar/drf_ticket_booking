import logging
from rest_framework import serializers

__author__ = "akhtar"

from booking.models import Screen, Row

logger = logging.getLogger(__name__)


class RowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Row
        fields = ["name", "no_of_seats", "aisle_seats", ]


class ScreenCreateSerializer(serializers.ModelSerializer):
    seatInfo = serializers.JSONField()

    class Meta:
        model = Screen
        fields = ["name", "seatInfo", ]

    def validate(self, attrs):
        # Validate data here
        return attrs

    def create(self, validated_data):
        rows = []
        seat_info = validated_data.get("seatInfo")
        for name, value in seat_info.items():
            row = Row.objects.create(
                name=name,
                no_of_seats=value["numberOfSeats"],
                aisle_seats=value["aisleSeats"],
            )
            rows.append(row.id)

        # pop out 'seatInfo' since it is not a valid model field
        validated_data.pop("seatInfo")
        validated_data["rows"] = rows
        return super().create(validated_data)


class ScreenResponseSerializer(serializers.ModelSerializer):
    rows = serializers.SerializerMethodField()

    class Meta:
        model = Screen
        fields = ["name", "rows", ]

    def get_rows(self, value):
        rows = value.rows.all()
        return RowSerializer(rows, many=True).data
