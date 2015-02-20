from django.http.request import HttpRequest
from django.test import TestCase
from population.views import ExistingUniverseView
from unittest.mock import patch


class TestUniverseView(TestCase):

    def setUp(self):
        self.request = HttpRequest()
        self.universe_view = ExistingUniverseView()

    @patch('population.views.NewPopulationForm')
    @patch('population.views.Universe')
    @patch('population.views.render')
    def test_get_request_renderes_universe_template_with_universe_and_form(
        self, render, universe_cls, population_form_cls
    ):
        universe_obj = universe_cls.objects.get.return_value
        form_obj = population_form_cls.return_value

        self.universe_view.get(self.request, 1)

        universe_cls.objects.get.assert_called_once_with(id=1)
        render.assert_called_once_with(self.request, 'universe.html', {
            'universe': universe_obj, 'form': form_obj
        })

    @patch('population.views.NewPopulationForm')
    def test_post_passes_POST_data_to_form(self, form_cls):
        self.universe_view.post(self.request, 1)

        form_cls.assert_called_once_with(data=self.request.POST)

    @patch('population.views.NewPopulationForm')
    def test_saves_form_if_valid(self, form_cls):
        form_obj = form_cls.return_value
        form_obj.is_valid.return_value = True

        self.universe_view.post(self.request, 1)

        form_obj.save.assert_called_once_with(for_universe=1)

    @patch('population.views.redirect')
    @patch('population.views.NewPopulationForm')
    def test_redirects_to_form_return_value_if_form_valid(self, form_cls, redirect_mock):
        form_obj = form_cls.return_value
        form_obj.is_valid.return_value = True

        self.universe_view.post(self.request, 1)

        redirect_mock.assert_called_once_with(form_obj.save.return_value)

    @patch('population.views.Universe')
    @patch('population.views.render')
    @patch('population.views.NewPopulationForm')
    def test_does_not_save_if_form_is_invalid(self, form_cls, render_mock, universe_mock):
        form_obj = form_cls.return_value
        form_obj.is_valid.return_value = False

        self.universe_view.post(self.request, 1)

        self.assertFalse(form_obj.save.called)

    @patch('population.views.Universe')
    @patch('population.views.NewPopulationForm')
    @patch('population.views.render')
    def test_passes_form_to_template_if_form_invalid(self, render_mock, form_class_mock, universe_cls_mock):
        form_object_mock = form_class_mock.return_value
        form_object_mock.is_valid.return_value = False
        universe_obj_mock = universe_cls_mock.objects.get.return_value

        self.universe_view.post(self.request, 2)

        universe_cls_mock.objects.get.assert_called_once_with(id=2)
        form_class_mock.assert_called_once_with(data=self.request.POST)
        render_mock.assert_called_once_with(self.request, 'universe.html',
                                            {'form': form_object_mock,
                                             'universe': universe_obj_mock})
