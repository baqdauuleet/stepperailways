from django.db import models
from django.contrib.auth.models import User

class Cities(models.Model):
    cid = models.AutoField(primary_key=True)
    city = models.TextField()

    def __str__(self):
        return str(self.city)

class Trains(models.Model):
    tid = models.AutoField(primary_key=True)
    number = models.TextField()
    route = models.ForeignKey('Route', on_delete=models.CASCADE)
    service_level = models.TextField()

    def __str__(self) -> str:
        return str(self.number)

class Route(models.Model):
    route_name = models.CharField(max_length=100)
    route_stations = models.TextField()

    def __str__(self) -> str:
        return str(self.route_name)

class Schedule(models.Model):
    train = models.ForeignKey(Trains, on_delete=models.CASCADE)
    departure_datetime = models.DateTimeField()

    def __str__(self):
        return str(self.departure_datetime)  # Преобразуйте объект datetime в строку

    # Дополнительно, если хотите более читаемое отображение в админке
    def get_formatted_datetime(self):
        return self.departure_datetime.strftime("%Y-%m-%d %H:%M:%S")

class WagonType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)

class Wagon(models.Model):
    id = models.AutoField(primary_key=True)
    train = models.ForeignKey(Trains, on_delete=models.CASCADE)
    wagon_type = models.ForeignKey(WagonType, on_delete=models.CASCADE)
    seats = models.PositiveIntegerField()

    def __str__(self) -> str:
        return str(self.id)

class TicketPrice(models.Model):
    wagon_type = models.ForeignKey(WagonType, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Reviews(models.Model):
    rid = models.AutoField(primary_key=True)
    rating = models.TextField()
    author = models.TextField()
    text = models.TextField()

class Tickets(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    train = models.ForeignKey(Trains, on_delete=models.CASCADE)
    wagon = models.ForeignKey(Wagon, on_delete=models.CASCADE)
    seat = models.IntegerField()
    purchase_date = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField()

    def __str__(self):
        return str(self.id)
    
class Questions(models.Model):
    id = models.AutoField(primary_key=True)
    firstname = models.TextField()
    lastname = models.TextField()
    email = models.TextField()
    city = models.TextField()
    question = models.TextField()

    def __str__(self):
        return str(self.id)