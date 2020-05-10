from django.shortcuts import render
from django.views import View
from .data import departures, tours
import random


class MainView(View):
    """Класс, отвечающий за наполнение главной странички"""

    def get(self, request, *args, **kwargs):
        # Массив из 6 чисел для отображения случайных отелей на главной стр
        arr_random = random.sample(list(tours.keys()), 6)
        tours_on_page = {tour_id: tours[tour_id] for tour_id in arr_random}
        return render(request, 'index.html', context={
            'departures': departures,
            'tours': tours_on_page
        }
                      )


class DepartureView(View):
    """Класс, отвечающий за наполнение departure/<str:departure>"""

    def departure_nights(self, departure, tours=tours):
        """Функция для определения минимального и максимального количество ночей по выбранному направлению"""
        arr_night = [tours[i]['nights'] for i in tours if tours[i]['departure'] == departure]
        return (min(arr_night), max(arr_night))

    def departure_price(self, departure, tours=tours):
        """Функция для определения минимальной и максимальной сумм по выбранному направлению"""
        arr_price = [tours[i]['price'] for i in tours if tours[i]['departure'] == departure]
        return (min(arr_price), max(arr_price))

    def departure_id(self, departure, tours=tours):
        """Функция для формирования словаря с данными по выбранному направлению"""
        arr_departure_id = {tour_id: tours[tour_id] for tour_id in tours if tours[tour_id]['departure'] == departure}
        return arr_departure_id

    def get(self, request, *args, **kwargs):
        departure = kwargs['departure']
        min_nights, max_nights = self.departure_nights(departure)
        min_price, max_price = self.departure_price(departure)
        tours_on_page = self.departure_id(departure)
        info = {'departure': departures[departure],
                'max_price': max_price,
                'min_price': min_price,
                'max_nights': max_nights,
                'min_nights': min_nights,
                'quantity_tours': len(tours_on_page)
                }

        return render(
            request, 'departure.html', context={
                'departures': departures,
                'tours': tours_on_page,
                'info': info
            }
        )


class TourView(View):
    """Класс, отвечающий за наполнение tour/<int:id>/"""

    def get(self, request, *args, **kwargs):
        tour_id = kwargs['id']
        return render(request, 'tour.html', context={
            'departures': departures,
            'tour': tours[tour_id],
        }
                      )
