from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Stock, Portfolio, Holding

class UserSerializer(serializers.ModelSerializer):
  # look at model and all the fields in the model to see if valid
  class Meta:
    model = User # user obj is builtin to django
    fields = ['id', 'username', 'password']
    # want to write the password when creating, but don't want to return the password
    extra_kwargs = {'password': {'write_only': True}}

  # overwriting the default create
  def create(self, validated_data):
    # ** splits up the stuff in the dictionary
    user = User.objects.create_user(**validated_data)
    return user

# stocks will only be read by the client
class StockDetailSerializer(serializers.Serializer):

  symbol = serializers.CharField(max_length=10)
  company = serializers.CharField(max_length=100)
  country = serializers.CharField(max_length=100)
  industry = serializers.CharField(max_length=100)
  sector = serializers.CharField(max_length=100)
  
  last_sale = serializers.DecimalField(max_digits=12, decimal_places=2)
  high = serializers.DecimalField(max_digits=12, decimal_places=2)
  low = serializers.DecimalField(max_digits=12, decimal_places=2)
  open = serializers.DecimalField(max_digits=12, decimal_places=2)
  pe_ratio = serializers.DecimalField(max_digits=8, decimal_places=2)
  dividend_yield = serializers.DecimalField(max_digits=4, decimal_places=2)
  
  volume = serializers.IntegerField()
  market_cap = serializers.IntegerField()
  revenue = serializers.IntegerField()
  debt = serializers.IntegerField()
  ipo_year = serializers.IntegerField()

class StockListSerializer(serializers.Serializer):
  symbol = serializers.CharField(max_length=10,read_only=True)
  company = serializers.CharField(max_length=100,read_only=True)

class HoldingSerializer(serializers.ModelSerializer):
  stock = StockDetailSerializer(read_only=True)
  # assigns the existing 'stock' field to the stock object it finds using the symbol.
  # But on the outgoing side, 'stock' refers to the serializer data.
  stock_symbol = serializers.SlugRelatedField(
    slug_field='symbol',
    queryset=Stock.objects.all(),
    write_only=True,
    source='stock'
  )

  class Meta:
    model = Holding
    fields = ['id', 'stock', 'stock_symbol', 'quantity']

  def validate_quantity(self, value):
    if value <= 0:
      raise serializers.ValidationError('Quantity must be greater than 0')
    return value

  def validate(self, data):
    # access to context is specified in view 
    action = self.context.get('action')
    request = self.context['request']

    if action == 'buy':
      portfolio = Portfolio.objects.get(user=request.user)
      stock = data['stock']
      quantity = data['quantity']
      cost = stock.last_sale * quantity

      if cost > portfolio.balance:
        raise serializers.ValidationError('Not enough balance to purchase')

    elif action == 'sell':
      if quantity > self.instance.quantity:
        raise serializers.ValidationError('Not enough shares to sell')

    return data
  
  # this handles adding holdings to a portfolio
  def create(self, validated_data):
    action = self.context.get('action')
    if action == 'buy':
      request = self.context['request']
      portfolio = Portfolio.objects.get(user=request.user)
      stock = validated_data['stock']
      quantity = validated_data['quantity']
      cost = stock.last_sale * quantity

      # Deduct from balance
      portfolio.balance -= cost
      portfolio.save()

      # Add to holding (or create new)
      holding, created = Holding.objects.get_or_create(
        portfolio=portfolio, stock=stock,
        defaults={'quantity': quantity}
      )
      if not created:
        holding.quantity += quantity
        holding.save()

    return holding
  
  # this is used for selling holdings
  def update(self, instance, validated_data):
    action = self.context.get('action')
    request = self.context['request']
    if action == 'sell':
      portfolio = Portfolio.objects.get(user=request.user)
      stock = instance.stock
      quantity = validated_data['quantity']

      instance.quantity -= quantity
      if instance.quantity == 0:
        instance.delete()
      else:
        instance.save()
      
      portfolio.balance += stock.last_sale * quantity
      portfolio.save()
    
    return instance

# this is read only
class PortfolioSerializer(serializers.ModelSerializer):
  user = serializers.ReadOnlyField(source='user.username')
  holdings = HoldingSerializer(many=True, read_only=True)

  class Meta:
    model = Portfolio
    # return user in case want feature to view other profiles
    fields = ['id', 'user', 'balance', 'net_deposited', 'holdings']
