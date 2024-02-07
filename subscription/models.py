from django.db import models


class Subscription(models.Model):
    amount = models.CharField(max_length=10,)

    def __str__(self):
        return self.amount
