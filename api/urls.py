from django.urls import path
from .views import RunSimulationView

urlpatterns = [
    path('run-simulation/', RunSimulationView.as_view(), name='run_simulation'),
]
