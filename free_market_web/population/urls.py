from django.conf.urls import patterns, include, url
from django.contrib import admin
from population.views import (ExistingUniverseView, NewUniverseView,
                              supply_demand_form, delete_population)

urlpatterns = patterns('',
    url(r'^new_universe/$', NewUniverseView.as_view(), name='new_universe'),
    url(r'^universe/(\d+)/$', ExistingUniverseView.as_view(), name='universe'),
    url(r'^delete_population/(\d+)/$', delete_population, name='delete_population'),
    url(r'supply_demand_form/(\d+)$', supply_demand_form,
        name='supply_demand_form'),
)
