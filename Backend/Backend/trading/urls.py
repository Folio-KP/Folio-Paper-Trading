from django.urls import path
from . import views

urlpatterns = [
  path('stocks/<str:symbol>/', views.StockDetailView.as_view(),name="stock-detail"),
  path('symbols/', views.StockListView.as_view(),name="stock-list"),
  path('portfolio/',views.PortfolioView.as_view(),name='portfolio'),
  path('holdings/buy/',views.BuyHoldingView.as_view(),name='buy-holding'),
  path('holdings/sell/',views.SellHoldingView.as_view(),name='sell-holding'),
  path('historical/<str:symbol>/', views.StockHistoryView.as_view(), name='stock-history'),
  ]