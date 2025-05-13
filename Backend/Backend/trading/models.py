from django.db import models
from django.contrib.auth.models import User

# orm - write model definition in Python and django will convert to db code
class Stock(models.Model):
  symbol = models.CharField(max_length=10, unique=True)
  
  # optional fields
  company = models.CharField(max_length=100, blank=True, null=True)
  country = models.CharField(max_length=100, blank=True, null=True)
  industry = models.CharField(max_length=100, blank=True, null=True)
  sector = models.CharField(max_length=100, blank=True, null=True)
  
  last_sale = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
  high = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
  low = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
  open = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
  pe_ratio = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
  dividend_yield = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
  
  volume = models.PositiveBigIntegerField(blank=True, null=True)
  market_cap = models.PositiveBigIntegerField(blank=True, null=True)
  revenue = models.PositiveBigIntegerField(blank=True, null=True)
  debt = models.PositiveBigIntegerField(blank=True, null=True)
  ipo_year = models.PositiveSmallIntegerField(blank=True, null=True)

  last_updated = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.symbol

class Portfolio(models.Model):
  # user can only have 1 portfolio
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  balance = models.DecimalField(max_digits=15, decimal_places=2)
  net_deposited = models.DecimalField(max_digits=12, decimal_places=2)

  def __str__(self):
    return self.user.username
  
class Holding(models.Model):
  portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
  stock = models.ForeignKey(Stock, on_delete=models.CASCADE) 
  quantity = models.PositiveIntegerField()

  class Meta:
    unique_together = ('portfolio', 'stock')
  
  def __str__(self):
    return f"user: {self.portfolio.user.username} stock: {self.stock.symbol} {self.quantity}"