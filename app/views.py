from django.shortcuts import render, redirect  # добавьте redirect
from django.utils import timezone
from datetime import datetime
from django.db.models import Q
from .models import Trains, Route, Schedule, Wagon, WagonType, TicketPrice, Reviews, Cities, Questions

from django.views.generic import View, FormView, ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.auth import logout, login
from .forms import *
from django.urls import reverse_lazy

from .forms import LoginUserForm, RegisterUserForm
from django.contrib.auth.decorators import login_required

from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def index(request):
    to_city = Cities.objects.all()
    from_city = Cities.objects.all()
    return render(request, 'index.html', {'from_city': from_city, 'to_city': to_city})

def about(request):
    return render(request, "about.html")

def contacts(request):
    return render(request, "contacts.html")

def success_form(request):
    return render(request, 'success_form.html')

def reviews(request):
    reviews = Reviews.objects.all()
    return render(request, 'reviews.html', {'reviews': reviews})

def find_trains(request):
    if request.method == 'POST':
        from_city = request.POST.get('from_city', '')  # Получаем значение поля "Откуда"
        to_city = request.POST.get('to_city', '')      # Получаем значение поля "Куда"
        date_str = request.POST.get('date', '')        # Получаем значение поля "Дата"

        print(f"Город отправления: {from_city}")
        print(f"Город прибытия: {to_city}")
        print(f"Выбранная дата: {date_str}")
        print(request.POST)

        if date_str:
            selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            
            matching_trains = []  # Создаем пустой список для хранения найденных поездов

            routes = Route.objects.all()  # Получаем все маршруты из базы данных
            for route in routes:
                stations = route.route_stations.split(', ')  # Разбиваем станции маршрута на список

                # Проверяем, есть ли указанные города в этом маршруте и в правильном ли порядке они указаны
                if from_city in stations and to_city in stations:
                    from_city_index = stations.index(from_city)
                    to_city_index = stations.index(to_city)

                    if from_city_index < to_city_index:  # Если порядок городов правильный
                        # Получаем расписание для данного маршрута и выбранной даты
                        schedules = Schedule.objects.filter(train__route=route, departure_datetime__date=selected_date)
                        matching_trains.extend([schedule.train for schedule in schedules])  # Добавляем поезда в список найденных

            return render(request, 'list.html', {'trains': matching_trains})  # Возвращаем список найденных поездов на страницу
        else:
            return render(request, 'date_error.html')

    # Возвращаем пустой список поездов, если не найдено или если запрос был GET
    return render(request, 'list.html', {'trains': []})

from django.shortcuts import get_object_or_404

def buy_ticket(request, train_id):
    try:
        train = get_object_or_404(Trains, tid=train_id)
        wagons = Wagon.objects.filter(train=train)
        wagon_info = []
        stations = train.route.route_stations

        for wagon in wagons:
            wagon_id = wagon.id
            wagon_type = wagon.wagon_type
            seats = wagon.seats
            ticket_price = int(TicketPrice.objects.get(wagon_type=wagon_type).price)
            wagon_info.append({'id': wagon_id, 'type': wagon_type.name, 'seats': seats, 'ticket_price': ticket_price})

        return render(
            request,
            'ticket_details.html',
            {'train': train, 'wagon_info': wagon_info, 'stations': stations}
        )
    except Trains.DoesNotExist:
        return render(request, 'train_not_found.html')
    
def select_wagon(request):
    if request.method == 'POST':
        id = request.POST.get('wagon', '')
        wagon = Wagon.objects.get(id=id)
        train = Wagon.objects.get(id=id).train
        wagon_type = Wagon.objects.get(id=id).wagon_type
        seats = Wagon.objects.get(id=id).seats
        ticket_price = int(TicketPrice.objects.get(wagon_type=wagon_type).price)
        tickets = Tickets.objects.filter(train=train, wagon=wagon).values_list('seat', flat=True)
        stations = train.route.route_stations

        seat = range(1, seats + 1)

        wagon = {
            'id': id, 
            'wagon_type': wagon_type, 
            'seats': seats, 
            'ticket_price': ticket_price
            }
        

    return render(
            request, 'select_seat.html', 
            {'train': train, 'tickets': tickets, 'wagon': wagon, 'stations': stations, 'seats': seat}
            )


def payment_test(request):
    if request.method == 'POST':
        train_id = request.POST.get('train_id')
        wagon_id = request.POST.get('wagon_id')
        wagon_type = request.POST.get('wagon_type')
        ticket_price = request.POST.get('ticket_price')
        seat = request.POST.get('seat')

    return render(request, 'payment_test.html', {'ticket_price': ticket_price, 'wagon_id': wagon_id, 'wagon_type': wagon_type, 'seat': seat, 'train_id': train_id})

def payment_success(request):
    # Логика для страницы успешной оплаты
    if request.method == 'POST':
        train_id = request.POST.get('train_id')
        wagon_id = request.POST.get('wagon_id')
        wagon_type = request.POST.get('wagon_type')
        ticket_price = request.POST.get('ticket_price')
        seat = request.POST.get('seat')

        ticket = Tickets()
        ticket.user = request.user
        ticket.train = Trains.objects.get(number=train_id)
        ticket.wagon = Wagon.objects.get(id=wagon_id)
        ticket.seat = seat
        ticket.price = ticket_price

        ticket.save()

        latest = Tickets.objects.filter(user=request.user).order_by('-purchase_date').first()

        train = Trains.objects.get(number=train_id)


        email = request.user.email

        ticket_text = f'Ваш билет №{latest.id}!\n\nПоезд №{train_id}.\nМаршрут {train.route}.\nВагон: {wagon_id}.\nКласс обслуживания: {wagon_type}.\nМесто: {seat}.\nСтоимость билета: {ticket_price}₸.\n\nСпасибо что выбираете нас!'
        title = f'Билет №{latest.id}'

        send_email(ticket_text, title, email)
    

    return render(request, 'payment_success.html')

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = "registration.html"
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("index")

class LoginUser(LoginView):
    template_name = 'login.html'
    form_class = LoginUserForm
    success_url = reverse_lazy('index')
    def get_success_url(self):
        return self.success_url

def logout_user(request):
    logout(request)
    return redirect("index")

@login_required
def create(request):
    if request.method == "POST":
        reviews = Reviews()
        reviews.author = request.user.username
        reviews.text = request.POST.get("review")
        reviews.rating = request.POST.get("rating")
        reviews.save()
    return redirect("reviews")

def delete(request, rid):
    try:
        reviews = Reviews.objects.get(rid=rid)
        reviews.delete()
        return redirect("reviews")
    except:
        return redirect("reviews")
    
def send_email(text, title, *emails):
    email_sender = "stepperailways@inbox.ru"
    email_getters = emails

    smtp_server = SMTP("smtp.mail.ru", 587)
    smtp_server.starttls()

    smtp_server.login(email_sender, 'apAUJGnQ57TNUvgmdckA')

    subject = title
    body = text
    message = MIMEMultipart()
    message["From"] = email_sender
    message["To"] = ', '.join(email_getters)
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    smtp_server.sendmail(email_sender, email_getters, message.as_string())

def question_save(request):
    if request.method == "POST":
        questions = Questions()
        questions.firstname = request.POST.get("firstname")
        questions.lastname = request.POST.get("lastname")
        questions.email = request.POST.get("email")
        questions.city = request.POST.get("city")
        questions.question = request.POST.get("question")
        questions.save()
    return redirect("success_form")