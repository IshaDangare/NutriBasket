from django.test import TestCase, Client
from django.urls import reverse
from .utils import load_nutrition_data


class NutritionUtilsTests(TestCase):
    def test_load_returns_expected_items(self):
        data = load_nutrition_data()
        # we know product.text contains at least pizza and banana
        self.assertIn('pizza', data)
        self.assertIn('banana', data)
        self.assertEqual(data['pizza']['calories'], 266)
        # also verify newly-added categories are read
        self.assertIn('milk', data)
        self.assertIn('chicken', data)


class CaloriesViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_calories_success(self):
        response = self.client.get(reverse('get_calories'), {'name': 'Pizza'})
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertEqual(json.get('calories'), 266)

    def test_get_calories_not_found(self):
        response = self.client.get(reverse('get_calories'), {'name': 'Nonexistent'})
        self.assertEqual(response.status_code, 404)
