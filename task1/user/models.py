from django.db import models
from datetime import date


class UserDb(models.Model):
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    birth_date = models.DateField()
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.first_name + " " + self.last_name

    @property
    def name(self):
        return self.first_name + " " + self.last_name

    @property
    def age(self):
        today = date.today()
        return (
            today.year
            - self.birth_date.year
            - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        )

    class Meta:
        db_table = "user_db"
        ordering = ["first_name"]
