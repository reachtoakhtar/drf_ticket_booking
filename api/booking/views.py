from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response

from booking.models import Screen, Reserve, Row
from booking.serializers import ScreenCreateSerializer, ScreenResponseSerializer


class ScreenView(CreateAPIView):
    model_class = Screen
    serializer_class = ScreenCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ser_data = self.perform_create(serializer)
        data = ScreenResponseSerializer(ser_data).data
        headers = self.get_success_headers(data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()


class ReserveView(CreateAPIView):
    """ Could use serializer here. """
    model_class = Reserve

    def create(self, request, *args, **kwargs):
        try:
            screen = Screen.objects.get(name=self.kwargs["screen_name"])
            seats = self.request.data.get("seats")
            for name, values in seats.items():
                try:
                    row = screen.rows.get(name=name)
                    reserve_obj = Reserve.objects.get(screen=screen, row=row)
                    reserved_seats = list(reserve_obj.seats_reserved)
                    for s in values:
                        if s in reserved_seats:
                            return Response(
                                {"message": "Seat {name}: {row} is not available."
                                        .format(name=name, row=str(s))},
                                    status=status.HTTP_400_BAD_REQUEST)
                except Reserve.DoesNotExist as e:
                    pass

            for name, values in seats.items():
                row = screen.rows.get(name=name)
                Reserve.objects.create(
                    screen=screen, row=row, seats_reserved=values)

            return Response(
                {"message": "Successfully booked tickets."},
                status=status.HTTP_201_CREATED)
        except Screen.DoesNotExist as e:
            return Response(
                {"message": "Given screen does not exist."},
                status=status.HTTP_404_NOT_FOUND)
        except Row.DoesNotExist as e:
            return Response(
                {"message": "Given row does not exist."},
                status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                {"message": "Internal Server Error."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SeatView(RetrieveAPIView):
    """ Could use serializer here. """
    def retrieve(self, request, *args, **kwargs):
        try:
            booking_status = self.request.query_params.get("status")
            screen = Screen.objects.get(name=self.kwargs["screen_name"])

            available_seats = {}
            for row in screen.rows.all():
                total_seats = set(list(range(row.no_of_seats)))
                try:
                    reserve_obj = Reserve.objects.get(screen=screen, row=row)
                    booked_seats = set(reserve_obj.seats_reserved)
                except Reserve.DoesNotExist as e:
                    booked_seats = set()

                available_seats[row.name] = list(total_seats - booked_seats)

            return Response({"seats": available_seats})
        except Screen.DoesNotExist as e:
            return Response(
                {"message": "Given screen does not exist."},
                status=status.HTTP_404_NOT_FOUND)
        except Row.DoesNotExist as e:
            return Response(
                {"message": "Given row does not exist."},
                status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                {"message": "Internal Server Error."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
