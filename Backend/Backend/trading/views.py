from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, views, status
from .serializers import UserSerializer, StockDetailSerializer, StockListSerializer, PortfolioSerializer, HoldingSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Stock, Portfolio, Holding
from datetime import timedelta
from django.utils import timezone
from . import get_stock_data

# GET: takes stock symbol, returns the stock data
class StockDetailView(views.APIView):
  permission_classes = [AllowAny]
  def get(self, request, symbol):
    symbol = symbol.upper()
    try:
      stock = Stock.objects.get(symbol=symbol)
    except Stock.DoesNotExist:
      return Response({"error": "Stock not found"}, status=404)
    
    # if it's been over an hour, then refresh
    if timezone.now() - stock.last_updated > timedelta(hours=1):
      stock_data = get_stock_data.get_stock_info(symbol)
      for key, value in stock_data.items():
        if value is not None:
          setattr(stock, key, value)
      stock.save()


    serializer = StockDetailSerializer(stock)
    return Response(serializer.data)

# GET: takes stock symbol, returns the stock data
class StockListView(views.APIView):
  permission_classes = [AllowAny]
  def get(self, request):
    stocks = Stock.objects.all().only("symbol","company")
    serializer = StockListSerializer(stocks, many=True)
    return Response(serializer.data)

# GET: take user id, return their portfolio
class PortfolioView(views.APIView):
  permission_classes = [IsAuthenticated]

  def get(self, request):
    try:
      portfolio = Portfolio.objects.get(user=request.user)
    except Portfolio.DoesNotExist:
      return Response({"error": "Portfolio not found."}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = PortfolioSerializer(portfolio)
    return Response(serializer.data)

# POST: add holding to portfolio
class BuyHoldingView(views.APIView):
  permission_classes = [IsAuthenticated]

  def post(self, request):
    serializer = HoldingSerializer(data=request.data, context={'request': request, 'action': 'buy'})
    if serializer.is_valid():
      holding = serializer.save()
      return Response(HoldingSerializer(holding).data)
    return Response(serializer.errors, status=400)

# PUT: sell holdings, potentially delete (idk if this should be put)
class SellHoldingView(views.APIView):
  permission_classes = [IsAuthenticated]

  def put(self, request):
    user = request.user
    symbol = request.data.get('symbol')
    quantity = int(request.data.get('quantity', 0))

    if not symbol or quantity <= 0:
      return Response({"error":"invalid input"}, status=400)

    try:
      stock = Stock.objects.get(symbol=symbol.upper())
    except Stock.DoesNotExist:
      return Response({"error":"stock not found"}, status=404)
    
    try:
      portfolio = Portfolio.objects.get(user=user)
    except Portfolio.DoesNotExist:
      return Response({"error": "Portfolio not found"}, status=404)
    
    instance = Holding.objects.get(portfolio=portfolio, stock=stock)
    if not instance:
      return Response({"error": "You don't own this stock"}, status=400)

    serializer = HoldingSerializer(data={'quantity':quantity}, instance=instance, context={'request': request, 'action': 'sell'})
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=400)

# creating new user
class CreateUserView(generics.CreateAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  permission_classes = [AllowAny]
  
  def perform_create(self, serializer):
    user = serializer.save()
    Portfolio.objects.create(user=user, balance=10000.00, net_deposited=10000.00)

class StockHistoryView(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request, symbol):
        symbol = symbol.upper()
        try:
            history = get_stock_data.get_history(symbol)
            return Response(history)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        
