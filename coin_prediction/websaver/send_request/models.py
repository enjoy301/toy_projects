from django.db import models
import datetime
class orderbook(models.Model):
    amount_ask_bid = models.DecimalField(max_digits=7, decimal_places=5, blank=True)
    time = models.DateTimeField(default=0, blank=True)
