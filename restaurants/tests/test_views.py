import random
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from faker import Faker
from faker_food import FoodProvider
from management.models import Country, State, City
from restaurants.models import *
from users.models import CustomUser
from restaurants.serializers import *


# End user tests
class RestaurantViewSetTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.unauthenticated_client = APIClient()
        # credentials
        cls.user_data = {
            'email': 'ahmed.salamony497@gmail.com',
            'password': 'ghanx154',
            'phone': '+201066133855',
            'first_name': 'Ahmed',
            'last_name': 'Salamouny'
        }

        # create user
        cls.user = CustomUser.objects.create(**cls.user_data)
        cls.user.set_password(cls.user_data['password'])
        cls.user.save()
        # create client and login
        cls.authenticated_client = APIClient()
        credentials = {
            'email': cls.user_data['email'], 'password': cls.user_data['password']}
        response = cls.authenticated_client.post(
            reverse('login'), data=credentials)

        auth_token = response.json().get('auth_token')
        cls.authenticated_client.credentials(
            HTTP_AUTHORIZATION=f'Token {auth_token}')

        # create places
        eg = Country.objects.create(
            name='Egypt',
            name_ar='مصر',
            code='eg',
            currency='EGP',
            currency_ar='جم',
            active=True
        )
        cairo = State.objects.create(
            name='Cairo',
            name_ar='القاهرة',
            country=eg,
            ordering=1,
            active=True,
        )
        cls.cities = [
            City.objects.create(name='Down Town', state=cairo,
                                ordering=1, active=True),
            City.objects.create(name='Maadi', state=cairo,
                                ordering=2, active=True),
            City.objects.create(name='Nasr City', state=cairo,
                                ordering=3, active=True),
            City.objects.create(name='New Cairo', state=cairo,
                                ordering=4, active=True),
            City.objects.create(name='Cheraton', state=cairo,
                                ordering=5, active=True)
        ]
        # create restaurant status
        cls.status = RestaurantStatus.objects.create(
            title='open',
            title_ar='open',
            color='#ccc'
        )
        cls.food_categories = [
            FoodCategory.objects.create(name='Grills', name_ar='Grills'),
            FoodCategory.objects.create(
                name='Fried chicken', name_ar='Grills'),
            FoodCategory.objects.create(name='Burger', name_ar='Grills'),
            FoodCategory.objects.create(name='Pizza', name_ar='Grills'),
            FoodCategory.objects.create(name='Pasta', name_ar='Grills'),
            FoodCategory.objects.create(name='Koshari', name_ar='Grills'),
        ]
        # create restaurants
        data = {
            'address': 'shohadaa Talaat Harb st',
            'owner': cls.user,
            'status': cls.status,
        }
        cls.restaurants = [
            Restaurant.objects.create(
                **data,
                name=random.choice(
                    ['rustii', 'Nest', 'Bazoka', 'KFC', 'Sobhy Kaber', 'Hosny']),
                city=random.choice(cls.cities),
                active=random.choice([True, False, True]),
                rating=random.choice([1, 2, 3, 4, 5]),
                num_of_reviewers=random.randint(1, 100)
            ) for i in range(200)
        ]
        menu_categories = [
            {'title': 'meals', 'title_ar': 'الوجبات'},
            {'title': 'sandwiches', 'title_ar': 'السندوتشات'},
            {'title': 'salads', 'title_ar': 'السلطات'},
            {'title': 'main dishes', 'title_ar': 'الأطباق الرئيسية'},
            {'title': 'deserts', 'title_ar': 'الحلا'},
            {'title': 'drinks', 'title_ar': 'المشروبات'},
            {'title': 'addons', 'title_ar': 'الإضافات'},
            {'title': 'pizza', 'title_ar': 'بيتزا'},
            {'title': 'pasta', 'title_ar': 'باستا'},
            {'title': 'spicial dishes', 'title_ar': 'أطباق خاصة'},
        ]
        feature_categories = [
            {
                'title': 'size',
                'title_ar': 'الحجم',
                'features': [
                    {
                        'title': 'S',
                        'title_ar': 'ص',
                    },
                    {
                        'title': 'M',
                        'title_ar': 'و',
                    },
                    {
                        'title': 'L',
                        'title_ar': 'ك',
                    },
                ],

            },
            {
                'title': 'taste',
                'title_ar': 'الطعم',
                'features': [
                    {
                        'title': 'normal',
                        'title_ar': 'عادي',
                    },
                    {
                        'title': 'spicy',
                        'title_ar': 'حار',
                    }
                ],

            }
        ]
        for fc in feature_categories:
            new_fc = MenuItemFeatureCategory.objects.create(
                title=fc.get('title'),
                title_ar=fc.get('title_ar'),
            )
            for f in fc.get('features'):
                MenuItemFeature.objects.create(
                    title=f.get('title'),
                    title_ar=f.get('title_ar'),
                    category=new_fc
                )

        faker = Faker()
        faker.add_provider(FoodProvider)
        features = MenuItemFeature.objects.all()
        cls.active_restaurants = [r for r in cls.restaurants if r.active]
        for restaurant in cls.active_restaurants[:10]:
            categories = random.sample(
                cls.food_categories, k=random.choice([2, 3]))
            for c in categories:
                restaurant.categories.add(c)
            restaurant.save()
            for i in range(10):
                mc = MenuCategory.objects.create(
                    restaurant=restaurant,
                    active=random.choice([True, False]),
                    ordering=i,
                    **random.choice(menu_categories)
                )
                for j in range(30):
                    mi = MenuItem.objects.create(
                        name=faker.dish(),
                        name_ar='لا يوجد',
                        description=faker.dish_description(),
                        price=random.randint(5, 500),
                        active=random.choice([True, False]),
                        menu_category=mc,
                        ordering=j,
                        rating=random.randint(0, 5),
                        num_of_reviews=random.randint(1, 10000)
                    )
                    mi.features.add(random.choice(features))
                    mi.save()

    # TODO: Test creating new restaurant if user is authenticated.

    def test_create_restaurant_with_authenticated_client(self):
        restaurants_count_before = Restaurant.objects.count()
        data = {
            'name': 'rustii',
            'address': 'shohadaa Talaat Harb st',
            'city': self.cities[0].id,
            'status': self.status.id,
            'categories': random.sample([c.id for c in self.food_categories], k=2)
        }
        response = self.authenticated_client.post(
            reverse('restaurant-list'),
            data=data,
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            Restaurant.objects.count(),
            restaurants_count_before+1
        )
        r = Restaurant.objects.get(slug=response.json().get('slug'))
        self.assertEqual(r.city.id, data['city'])
        self.assertEqual(r.status.id, data['status'])
        self.assertEqual(
            set([c.id for c in r.categories.all()]), set(data['categories']))

    # TODO: Test creating new restaurant if user is NOT authenticated.

    def test_create_restaurant_with_unauthenticated_client(self):
        restaurants_count_before = Restaurant.objects.count()
        data = {
            'name': 'rustii',
            'address': 'Talaat Harb st',
            'city': self.cities[0].id,
            'status': self.status.id,
        }
        response = self.unauthenticated_client.post(
            reverse('restaurant-list'),
            data=data,
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(Restaurant.objects.count(),
                         restaurants_count_before)

    # TODO: Test read an existing restaurant.

    def test_get_a_city_restaurants_list(self):
        city = random.choice(self.cities)
        city_restaurants = [
            r for r in self.restaurants if r.active and r.city == city]
        response = self.unauthenticated_client.get(
            f"{reverse('restaurant-list')}?city={city.id}"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], len(city_restaurants))
        # assert that all returned restaurants belong to this city
        self.assertTrue(
            all([r.get('city') == city.id for r in response.json()['results']]))

    def test_get_different_cities_restaurants_list(self):
        cities = random.choices(self.cities, k=3)
        cities_ids = [c.id for c in cities]
        cities_restaurants = [
            r for r in self.restaurants if r.active and r.city.id in set(cities_ids)]
        response = self.unauthenticated_client.get(
            f"{reverse('restaurant-list')}?city={'&city='.join([str(id) for id in cities_ids])}"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], len(cities_restaurants))
        # assert that all returned restaurants belong to one of those city
        self.assertTrue(all([r.get('city') in set(cities_ids)
                        for r in response.json()['results']]))

    # TODO: test order_by default modes

    def test_get_different_cities_restaurants_list_ordered_by_name(self):
        '''
        default mode = accending
        '''
        cities = random.choices(self.cities, k=3)
        cities_ids = [c.id for c in cities]
        cities_restaurants = [
            r for r in self.restaurants if r.active and r.city.id in set(cities_ids)]
        url = f"{reverse('restaurant-list')}?city={'&city='.join([str(id) for id in cities_ids])}&order_by=name"
        print(url)
        response = self.unauthenticated_client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], len(cities_restaurants))
        # assert that all returned restaurants belong to one of those city
        self.assertTrue(all([r.get('city') in set(cities_ids)
                        for r in response.json()['results']]))
        # assert that returned restaurants are ordered by name
        result = response.json()['results']
        self.assertTrue(all([result[i].get(
            'name') >= result[i-1].get('name') for i in range(1, len(result))]))

    def test_get_different_cities_restaurants_list_ordered_by_rating(self):
        '''
        default mode = descending
        '''
        cities = random.choices(self.cities, k=3)
        cities_ids = [c.id for c in cities]
        cities_restaurants = [
            r for r in self.restaurants if r.active and r.city.id in set(cities_ids)]
        url = f"{reverse('restaurant-list')}?city={'&city='.join([str(id) for id in cities_ids])}&order_by=rating"
        print(url)
        response = self.unauthenticated_client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], len(cities_restaurants))
        # assert that all returned restaurants belong to one of those city
        self.assertTrue(all([r.get('city') in set(cities_ids)
                        for r in response.json()['results']]))
        # assert that returned restaurants are ordered by name
        result = response.json()['results']
        self.assertTrue(all([result[i].get(
            'rating') <= result[i-1].get('rating') for i in range(1, len(result))]))

    def test_get_different_cities_restaurants_list_ordered_by_num_reviews(self):
        '''
        default mode = descending
        '''
        cities = random.choices(self.cities, k=3)
        cities_ids = [c.id for c in cities]
        cities_restaurants = [
            r for r in self.restaurants if r.active and r.city.id in set(cities_ids)]
        url = f"{reverse('restaurant-list')}?city={'&city='.join([str(id) for id in cities_ids])}&order_by=num_reviews"
        print(url)
        response = self.unauthenticated_client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], len(cities_restaurants))
        # assert that all returned restaurants belong to one of those city
        self.assertTrue(all([r.get('city') in set(cities_ids)
                        for r in response.json()['results']]))
        # assert that returned restaurants are ordered by name
        result = response.json()['results']
        self.assertTrue(all([result[i].get('num_of_reviewers') <=
                        result[i-1].get('num_of_reviewers') for i in range(1, len(result))]))

    def test_get_different_cities_restaurants_list_ordered_by_newest(self):
        '''
        default mode = descending
        '''
        cities = random.choices(self.cities, k=3)
        cities_ids = [c.id for c in cities]
        cities_restaurants = [
            r for r in self.restaurants if r.active and r.city.id in set(cities_ids)]
        url = f"{reverse('restaurant-list')}?city={'&city='.join([str(id) for id in cities_ids])}&order_by=newest"
        print(url)
        response = self.unauthenticated_client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], len(cities_restaurants))
        # assert that all returned restaurants belong to one of those city
        self.assertTrue(all([r.get('city') in set(cities_ids)
                        for r in response.json()['results']]))
        # assert that returned restaurants are ordered by name
        result = response.json()['results']
        for i in range(1, len(result)):
            r1 = Restaurant.objects.get(slug=result[i-1].get('slug'))
            r2 = Restaurant.objects.get(slug=result[i].get('slug'))
            self.assertTrue(r2.created_at <= r1.created_at)

    # test order_by specified modes
    def test_get_different_cities_restaurants_list_ordered_by_name_descending(self):
        print('hi name desc')
        cities = random.choices(self.cities, k=3)
        cities_ids = [c.id for c in cities]
        cities_restaurants = [
            r for r in self.restaurants if r.active and r.city.id in set(cities_ids)]
        url = f"{reverse('restaurant-list')}?city={'&city='.join([str(id) for id in cities_ids])}&order_by=name&mode=desc"
        print(url)
        response = self.unauthenticated_client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], len(cities_restaurants))
        # assert that all returned restaurants belong to one of those city
        self.assertTrue(all([
            r.get('city') in set(cities_ids) for r in response.json()['results']
        ]))
        # assert that returned restaurants are ordered by name
        result = response.json()['results']
        # for i in range(1, len(result)):
        #     name_prev = result[i-1].get('name').lower()
        #     name = result[i].get('name').lower()
        #     if not name <= name_prev:
        #         print('i =', i)
        #         print('names =', name_prev, name)
        #     self.assertTrue(name <= name_prev)

        self.assertTrue(all([
            result[i].get('name').lower() <= result[i-1].get('name').lower() for i in range(1, len(result))
        ]))

    def test_get_different_cities_restaurants_list_ordered_by_name_accending(self):
        cities = random.choices(self.cities, k=3)
        cities_ids = [c.id for c in cities]
        cities_restaurants = [
            r for r in self.restaurants if r.active and r.city.id in set(cities_ids)]
        url = f"{reverse('restaurant-list')}?city={'&city='.join([str(id) for id in cities_ids])}&order_by=name&mode=acc"
        print(url)
        response = self.unauthenticated_client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], len(cities_restaurants))
        # assert that all returned restaurants belong to one of those city
        self.assertTrue(all([
            r.get('city') in set(cities_ids) for r in response.json()['results']
        ]))
        # assert that returned restaurants are ordered by name
        result = response.json()['results']
        self.assertTrue(all([
            result[i].get('name').lower() >= result[i-1].get('name').lower() for i in range(1, len(result))
        ]))

    def test_get_different_cities_restaurants_list_ordered_by_rating_accending(self):
        cities = random.choices(self.cities, k=3)
        cities_ids = [c.id for c in cities]
        cities_restaurants = [
            r for r in self.restaurants if r.active and r.city.id in set(cities_ids)]
        url = f"{reverse('restaurant-list')}?city={'&city='.join([str(id) for id in cities_ids])}&order_by=rating&mode=acc"
        print(url)
        response = self.unauthenticated_client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], len(cities_restaurants))
        # assert that all returned restaurants belong to one of those city
        self.assertTrue(all([r.get('city') in set(cities_ids)
                        for r in response.json()['results']]))
        # assert that returned restaurants are ordered by name
        result = response.json()['results']
        self.assertTrue(all([result[i].get(
            'rating') >= result[i-1].get('rating') for i in range(1, len(result))]))

    def test_get_different_cities_restaurants_list_ordered_by_rating_descending(self):
        cities = random.choices(self.cities, k=3)
        cities_ids = [c.id for c in cities]
        cities_restaurants = [
            r for r in self.restaurants if r.active and r.city.id in set(cities_ids)]
        url = f"{reverse('restaurant-list')}?city={'&city='.join([str(id) for id in cities_ids])}&order_by=rating&mode=desc"
        print(url)
        response = self.unauthenticated_client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], len(cities_restaurants))
        # assert that all returned restaurants belong to one of those city
        self.assertTrue(all([r.get('city') in set(cities_ids)
                        for r in response.json()['results']]))
        # assert that returned restaurants are ordered by name
        result = response.json()['results']
        self.assertTrue(all([result[i].get(
            'rating') <= result[i-1].get('rating') for i in range(1, len(result))]))

    def test_get_different_cities_restaurants_list_ordered_by_num_reviews_acc(self):
        cities = random.choices(self.cities, k=3)
        cities_ids = [c.id for c in cities]
        cities_restaurants = [
            r for r in self.restaurants if r.active and r.city.id in set(cities_ids)]
        url = f"{reverse('restaurant-list')}?city={'&city='.join([str(id) for id in cities_ids])}&order_by=num_reviews&mode=acc"
        print(url)
        response = self.unauthenticated_client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], len(cities_restaurants))
        # assert that all returned restaurants belong to one of those city
        self.assertTrue(all([r.get('city') in set(cities_ids)
                        for r in response.json()['results']]))
        # assert that returned restaurants are ordered by name
        result = response.json()['results']
        self.assertTrue(all([result[i].get('num_of_reviewers') >=
                        result[i-1].get('num_of_reviewers') for i in range(1, len(result))]))

    def test_get_different_cities_restaurants_list_ordered_by_num_reviews_desc(self):
        cities = random.choices(self.cities, k=3)
        cities_ids = [c.id for c in cities]
        cities_restaurants = [
            r for r in self.restaurants if r.active and r.city.id in set(cities_ids)]
        url = f"{reverse('restaurant-list')}?city={'&city='.join([str(id) for id in cities_ids])}&order_by=num_reviews&mode=desc"
        print(url)
        response = self.unauthenticated_client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], len(cities_restaurants))
        # assert that all returned restaurants belong to one of those city
        self.assertTrue(all([r.get('city') in set(cities_ids)
                        for r in response.json()['results']]))
        # assert that returned restaurants are ordered by name
        result = response.json()['results']
        self.assertTrue(all([result[i].get('num_of_reviewers') <=
                        result[i-1].get('num_of_reviewers') for i in range(1, len(result))]))

    def test_get_different_cities_restaurants_list_ordered_by_newest_acc(self):
        cities = random.choices(self.cities, k=3)
        cities_ids = [c.id for c in cities]
        cities_restaurants = [
            r for r in self.restaurants if r.active and r.city.id in set(cities_ids)]
        url = f"{reverse('restaurant-list')}?city={'&city='.join([str(id) for id in cities_ids])}&order_by=newest&mode=acc"
        print(url)
        response = self.unauthenticated_client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], len(cities_restaurants))
        # assert that all returned restaurants belong to one of those city
        self.assertTrue(all([r.get('city') in set(cities_ids)
                        for r in response.json()['results']]))
        # assert that returned restaurants are ordered by name
        result = response.json()['results']
        for i in range(1, len(result)):
            r1 = Restaurant.objects.get(slug=result[i-1].get('slug'))
            r2 = Restaurant.objects.get(slug=result[i].get('slug'))
            self.assertTrue(r2.created_at >= r1.created_at)

    def test_get_different_cities_restaurants_list_ordered_by_newest_desc(self):
        cities = random.choices(self.cities, k=3)
        cities_ids = [c.id for c in cities]
        cities_restaurants = [
            r for r in self.restaurants if r.active and r.city.id in set(cities_ids)]
        url = f"{reverse('restaurant-list')}?city={'&city='.join([str(id) for id in cities_ids])}&order_by=newest&mode=desc"
        print(url)
        response = self.unauthenticated_client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], len(cities_restaurants))
        # assert that all returned restaurants belong to one of those city
        self.assertTrue(all([r.get('city') in set(cities_ids)
                        for r in response.json()['results']]))
        # assert that returned restaurants are ordered by name
        result = response.json()['results']
        for i in range(1, len(result)):
            r1 = Restaurant.objects.get(slug=result[i-1].get('slug'))
            r2 = Restaurant.objects.get(slug=result[i].get('slug'))
            self.assertTrue(r2.created_at <= r1.created_at)

    # TODO: Test read an existing restaurant.
    def test_read_an_existing_restaurant(self):
        r = random.choice([r for r in self.restaurants if r.active])
        url = f"{reverse('restaurant-detail', kwargs={'slug': r.slug})}"
        print(url)
        response = self.unauthenticated_client.get(url)
        print('response =', response.json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('slug'), r.slug)

    # TODO: Test read an existing non active restaurant.

    def test_read_an_existing_not_active_restaurant(self):
        r = random.choice([r for r in self.restaurants if not r.active])
        url = f"{reverse('restaurant-detail', kwargs={'slug': r.slug})}"
        print(url)
        response = self.unauthenticated_client.get(url)
        print('response =', response.json())
        self.assertEqual(response.status_code, 404)

    # TODO: Test read a non existing restaurant.
    def test_read_a_non_existing_restaurant(self):
        url = f"{reverse('restaurant-detail', kwargs={'slug': 'non-existing-restaurant-slug'})}"
        print(url)
        response = self.unauthenticated_client.get(url)
        print('response =', response.json())
        self.assertEqual(response.status_code, 404)

    # Restaurant menu user tests
    # TODO: Test all returned menu categories and items are active

    def test_all_returned_menu_categories_and_items_are_active(self):
        for r in random.sample(self.active_restaurants[:10], k=4):
            url = f"{reverse('restaurant-detail', kwargs={'slug': r.slug})}"
            print(url)
            response = self.unauthenticated_client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json().get('slug'), r.slug)
            menu = response.json().get('menu')
            self.assertNotEqual(menu, None)
            for c in menu:
                self.assertEqual(MenuCategory.objects.get(
                    pk=c.get('id')).active, True)
                items = c.get('items')
                for item in items:
                    self.assertEqual(MenuItem.objects.get(
                        pk=item.get('id')).active, True)

# Restaurant admin tests
    # TODO: Test updating an existing restaurant data.
    # TODO: Test deleting an existing restaurant.
    # TODO: Test deleting a not existing restaurant.


class RestaurantAdminTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.unauthenticated_client = APIClient()
        # credentials
        cls.users_data = [{
            'email': 'ahmed.salamony497@gmail.com',
            'password': 'ghanx154',
            'phone': '+201066133855',
            'first_name': 'Ahmed',
            'last_name': 'Salamouny'
        }, {
            'email': 'ali.wega@gmail.com',
            'password': 'ghanx154',
            'phone': '+201066133800',
            'first_name': 'Ali',
            'last_name': 'Wega'
        }
        ]

        # create users
        cls.users = []
        for user_data in cls.users_data:
            user = CustomUser.objects.create(**user_data)
            user.set_password(user_data['password'])
            user.save()
            cls.users.append(user)

        # create client and login
        cls.authenticated_client = APIClient()
        credentials = {
            'email': cls.users_data[0]['email'], 'password': cls.users_data[0]['password']}
        response = cls.authenticated_client.post(
            reverse('login'), data=credentials)

        auth_token = response.json().get('auth_token')
        cls.authenticated_client.credentials(
            HTTP_AUTHORIZATION=f'Token {auth_token}')

        # create places
        eg = Country.objects.create(
            name='Egypt',
            name_ar='مصر',
            code='eg',
            currency='EGP',
            currency_ar='جم',
            active=True
        )
        cairo = State.objects.create(
            name='Cairo',
            name_ar='القاهرة',
            country=eg,
            ordering=1,
            active=True,
        )
        cls.cities = [
            City.objects.create(name='Down Town', state=cairo,
                                ordering=1, active=True),
            City.objects.create(name='Maadi', state=cairo,
                                ordering=2, active=True),
            City.objects.create(name='Nasr City', state=cairo,
                                ordering=3, active=True),
            City.objects.create(name='New Cairo', state=cairo,
                                ordering=4, active=True),
            City.objects.create(name='Cheraton', state=cairo,
                                ordering=5, active=True)
        ]
        # create restaurant status
        cls.status = RestaurantStatus.objects.create(
            title='open',
            title_ar='open',
            color='#ccc'
        )
        cls.food_categories = [
            FoodCategory.objects.create(name='Grills', name_ar='Grills'),
            FoodCategory.objects.create(
                name='Fried chicken', name_ar='Grills'),
            FoodCategory.objects.create(name='Burger', name_ar='Grills'),
            FoodCategory.objects.create(name='Pizza', name_ar='Grills'),
            FoodCategory.objects.create(name='Pasta', name_ar='Grills'),
            FoodCategory.objects.create(name='Koshari', name_ar='Grills'),
        ]
        # create restaurants
        data = {
            'address': 'shohadaa Talaat Harb st',
            'status': cls.status,
        }
        cls.restaurants = [
            Restaurant.objects.create(
                **data,
                owner=random.choice(cls.users),
                name=random.choice(
                    ['rustii', 'Nest', 'Bazoka', 'KFC', 'Sobhy Kaber', 'Hosny']),
                city=random.choice(cls.cities),
                active=random.choice([True, False, True]),
                rating=random.choice([1, 2, 3, 4, 5]),
                num_of_reviewers=random.randint(1, 100)
            ) for i in range(20)
        ]
        menu_categories = [
            {'title': 'meals', 'title_ar': 'الوجبات'},
            {'title': 'sandwiches', 'title_ar': 'السندوتشات'},
            {'title': 'salads', 'title_ar': 'السلطات'},
            {'title': 'main dishes', 'title_ar': 'الأطباق الرئيسية'},
            {'title': 'deserts', 'title_ar': 'الحلا'},
            {'title': 'drinks', 'title_ar': 'المشروبات'},
            {'title': 'addons', 'title_ar': 'الإضافات'},
            {'title': 'pizza', 'title_ar': 'بيتزا'},
            {'title': 'pasta', 'title_ar': 'باستا'},
            {'title': 'spicial dishes', 'title_ar': 'أطباق خاصة'},
        ]
        feature_categories = [
            {
                'title': 'size',
                'title_ar': 'الحجم',
                'features': [
                    {
                        'title': 'S',
                        'title_ar': 'ص',
                    },
                    {
                        'title': 'M',
                        'title_ar': 'و',
                    },
                    {
                        'title': 'L',
                        'title_ar': 'ك',
                    },
                ],

            },
            {
                'title': 'taste',
                'title_ar': 'الطعم',
                'features': [
                    {
                        'title': 'normal',
                        'title_ar': 'عادي',
                    },
                    {
                        'title': 'spicy',
                        'title_ar': 'حار',
                    }
                ],

            }
        ]
        for fc in feature_categories:
            new_fc = MenuItemFeatureCategory.objects.create(
                title=fc.get('title'),
                title_ar=fc.get('title_ar'),
            )
            for f in fc.get('features'):
                MenuItemFeature.objects.create(
                    title=f.get('title'),
                    title_ar=f.get('title_ar'),
                    category=new_fc
                )

        cls.faker = Faker()
        cls.faker.add_provider(FoodProvider)
        features = MenuItemFeature.objects.all()
        for restaurant in cls.restaurants:
            categories = random.sample(
                cls.food_categories, k=random.choice([2, 3]))
            for c in categories:
                restaurant.categories.add(c)
            restaurant.save()
            for i in range(random.randint(2, 6)):
                mc = MenuCategory.objects.create(
                    restaurant=restaurant,
                    active=random.choice([True, False]),
                    ordering=i,
                    **random.choice(menu_categories)
                )
                for j in range(35):
                    mi = MenuItem.objects.create(
                        name=cls.faker.dish(),
                        name_ar='لا يوجد',
                        description=cls.faker.dish_description(),
                        price=random.randint(5, 500),
                        active=random.choice([True, False]),
                        menu_category=mc,
                        ordering=j,
                        rating=random.randint(0, 5),
                        num_of_reviews=random.randint(1, 10000)
                    )
                    mi.features.add(random.choice(features))
                    mi.save()

    # TODO: Test create new restaurant branch

    def test_create_new_restaurant_branch(self):
        restaurants_count_before = Restaurant.objects.count()
        data = {
            'name': 'rustii',
            'address': 'shohadaa Talaat Harb st',
            'city': self.cities[0].id,
            'status': self.status.id,
            'categories': random.sample([c.id for c in self.food_categories], k=2)
        }
        response = self.authenticated_client.post(
            reverse('restaurant-list'),
            data=data,
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            Restaurant.objects.count(),
            restaurants_count_before+1
        )
        r = Restaurant.objects.get(slug=response.json().get('slug'))
        self.assertEqual(r.city.id, data['city'])
        self.assertEqual(r.status.id, data['status'])
        self.assertEqual(
            set([c.id for c in r.categories.all()]), set(data['categories']))
        self.assertEqual(set([c.get('id') for c in response.json().get(
            'categories')]), set(data['categories']))

    # TODO: Test read user owned restaurants

    def test_read_user_owned_restaurants(self):
        response = self.authenticated_client.get(
            reverse('restaurant-admin-list'))
        print('response =', response.json())
        self.assertEqual(
            Restaurant.objects.filter(owner=self.users[0]).count(),
            self.users[0].owned_restaurants.count()
        )
        rs = response.json().get('results')
        for r in rs:
            self.assertEqual(Restaurant.objects.get(
                slug=r.get('slug')).owner, self.users[0])

    def _get_random_owned_restaurant(self):
        rs = [r for r in self.users[0].owned_restaurants.all()]
        return random.choice(rs)

    # TODO: Test update user owned restaurant
    def test_update_owned_restaurant_name(self):
        r = self._get_random_owned_restaurant()
        old_name = r.name
        edited_name = old_name + 'edited!!'
        response = self.authenticated_client.patch(
            reverse('restaurant-admin-detail', kwargs={'slug': r.slug}),
            data={'name': edited_name}
        )
        print('response =', response.json())
        r = Restaurant.objects.get(slug=r.slug)
        self.assertEqual(r.name, edited_name)

    def test_update_owned_restaurant_city(self):
        r = self._get_random_owned_restaurant()
        old_city = r.city
        cities_sample = random.sample(self.cities, k=2)
        new_city = cities_sample[0] if cities_sample[0] != old_city else cities_sample[1]

        response = self.authenticated_client.patch(
            reverse('restaurant-admin-detail', kwargs={'slug': r.slug}),
            data={'city': new_city.id}
        )
        print('response =', response.json())
        r = Restaurant.objects.get(slug=r.slug)
        self.assertEqual(r.city, new_city)

    def test_update_owned_restaurant_slogan(self):
        r = self._get_random_owned_restaurant()
        old_slogan = r.slogan or ''
        new_slogan = old_slogan + 'edited!!'

        response = self.authenticated_client.patch(
            reverse('restaurant-admin-detail', kwargs={'slug': r.slug}),
            data={'slogan': new_slogan}
        )
        print('response =', response.json())
        r = Restaurant.objects.get(slug=r.slug)
        self.assertEqual(r.slogan, new_slogan)

    def test_update_owned_restaurant_description(self):
        r = self._get_random_owned_restaurant()
        old_description = r.description or ''
        edited_description = old_description + 'edited!!'
        response = self.authenticated_client.patch(
            reverse('restaurant-admin-detail', kwargs={'slug': r.slug}),
            data={'description': edited_description}
        )
        print('response =', response.json())
        r = Restaurant.objects.get(slug=r.slug)
        self.assertEqual(r.description, edited_description)

    def test_update_owned_restaurant_address(self):
        r = self._get_random_owned_restaurant()
        old_address = r.address or ''
        edited_address = old_address + 'edited!!'
        response = self.authenticated_client.patch(
            reverse('restaurant-admin-detail', kwargs={'slug': r.slug}),
            data={'address': edited_address}
        )
        print('response =', response.json())
        r = Restaurant.objects.get(slug=r.slug)
        self.assertEqual(r.address, edited_address)

    def test_update_owned_restaurant_active(self):
        r = self._get_random_owned_restaurant()
        old_status = r.active
        new_status = not old_status
        response = self.authenticated_client.patch(
            reverse('restaurant-admin-detail', kwargs={'slug': r.slug}),
            data={'active': new_status}
        )
        print('response =', response.json())
        r = Restaurant.objects.get(slug=r.slug)
        self.assertEqual(r.active, new_status)

    def test_update_owned_restaurant_status(self):
        r = self._get_random_owned_restaurant()
        new_status = RestaurantStatus.objects.create(
            title='closed',
            title_ar='closed',
            color='#000'
        )
        response = self.authenticated_client.patch(
            reverse('restaurant-admin-detail', kwargs={'slug': r.slug}),
            data={'status': new_status.id}
        )
        print('response =', response.json())
        r = Restaurant.objects.get(slug=r.slug)
        self.assertEqual(r.status, new_status)

    def test_update_owned_restaurant_categories(self):
        r = self._get_random_owned_restaurant()
        old_categories = set([c.id for c in r.categories.all()])
        new_categories = random.sample(
            set([c.id for c in self.food_categories]).difference(old_categories), k=2)
        new_categories.append(old_categories.pop())
        response = self.authenticated_client.patch(
            reverse('restaurant-admin-detail', kwargs={'slug': r.slug}),
            data={'categories': new_categories}
        )
        print('response =', response.json())
        r = Restaurant.objects.get(slug=r.slug)
        self.assertEqual(
            set([c.id for c in r.categories.all()]),
            set([c.get('id') for c in response.json().get('categories')])
        )

    def test_update_owned_restaurant_multiple_fields(self):
        r = self._get_random_owned_restaurant()
        data = {
            'name': r.name + 'edited',
            'slogan': (r.slogan or '') + 'edited',
            'description': (r.description or '') + 'edited',
            'categories': [c.id for c in random.sample(self.food_categories, k=2)]
        }
        response = self.authenticated_client.patch(
            reverse('restaurant-admin-detail', kwargs={'slug': r.slug}),
            data=data
        )
        print('response =', response.json())
        r = Restaurant.objects.get(slug=r.slug)
        categories = data.pop('categories')
        self.assertEqual(
            set(categories),
            set([c.get('id') for c in response.json().get('categories')])
        )
        for key in data:
            self.assertEqual(response.json().get(key), data.get(key))

    # TODO: Test delete a user owned restaurant

    # TODO: Test create a restaurant menu category

    def test_create_new_menu_category(self):
        restaurants_count_before = Restaurant.objects.count()
        data = {
            'name': 'rustii',
            'address': 'shohadaa Talaat Harb st',
            'city': self.cities[0],
            'status': self.status,
        }
        r = Restaurant.objects.create(**data, owner=self.users[0])
        self.assertEqual(
            Restaurant.objects.count(),
            restaurants_count_before+1
        )
        self.assertEqual(r.menu_categories.count(), 0)
        active = random.choice([True, False])
        menu_category_data = {
            'title': 'Menu Category #1',
            'active': active
        }
        response = self.authenticated_client.post(
            reverse('menu-list', kwargs={'restaurant_slug': r.slug}),
            data=menu_category_data
        )

        self.assertEqual(response.status_code, 201)
        r = Restaurant.objects.get(slug=r.slug)
        self.assertEqual(r.menu_categories.count(), 1)
        self.assertEqual(r.menu_categories.all()[
                         0].title, menu_category_data.get('title'))
        self.assertEqual(r.menu_categories.all()[
                         0].active, menu_category_data.get('active'))

    # TODO: Test read restaurant menu categories

    def test_read_restaurant_menu_categories(self):
        r = random.choice(self.users[0].owned_restaurants.filter(active=True))
        self.assertGreater(r.menu_categories.count(), 0)
        response = self.authenticated_client.get(
            reverse('menu-list', kwargs={'restaurant_slug': r.slug}),
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(r.menu_categories.count(),
                         response.json().get('count'))
        self.assertEqual(
            MenuCategoryAdminSerializer(
                r.menu_categories.all(), many=True).data,
            response.json().get('results')
        )

    # TODO: Test update a restaurant menu category
    def test_update_restaurant_menu_category(self):
        r = random.choice(self.users[0].owned_restaurants.filter(active=True))
        self.assertGreater(r.menu_categories.count(), 0)
        data = {
            'ordering': 2,
            'title_ar': 'جديد'
        }
        mc = random.choice(r.menu_categories.all())
        response = self.authenticated_client.patch(
            reverse('menu-detail',
                    kwargs={'restaurant_slug': r.slug, 'pk': mc.pk}),
            data=data
        )

        self.assertEqual(response.status_code, 200)
        mc = MenuCategoryAdminSerializer(
            MenuCategory.objects.get(pk=mc.pk)).data
        for key in data:
            self.assertEqual(data[key], mc.get(key))

    # TODO: Test delete a restaurant menu category
    def test_delete_restaurant_menu_category(self):
        r = random.choice(self.users[0].owned_restaurants.filter(active=True))
        count_before = r.menu_categories.count()
        self.assertGreater(count_before, 0)
        mc = random.choice(r.menu_categories.all())
        self.assertTrue(MenuItem.objects.filter(menu_category=mc).exists())

        response = self.authenticated_client.delete(
            reverse('menu-detail',
                    kwargs={'restaurant_slug': r.slug, 'pk': mc.pk}),
        )

        self.assertEqual(response.status_code, 204)
        self.assertEqual(r.menu_categories.count(), count_before-1)
        self.assertFalse(r.menu_categories.filter(pk=mc.pk).exists())
        self.assertFalse(MenuItem.objects.filter(menu_category=mc).exists())

    # TODO: Test add a menu item to restaurant menu category

    def test_create_new_menu_item(self):
        r = self._get_random_owned_restaurant()
        self.assertGreater(r.menu_categories.count(), 0)
        mc = random.choice(r.menu_categories.all())
        count_before = mc.items.count()
        self.assertGreater(count_before, 0)

        name = self.faker.dish()
        name_ar = 'لا يوجد'
        description = self.faker.dish_description()
        price = random.randint(5, 500)
        active = random.choice([True, False])

        item_data = {
            'name': name,
            'name_ar': name_ar,
            'description': description,
            'price': price,
            'active': active,
            'ordering': 1
        }
        response = self.authenticated_client.post(
            reverse(
                'items-list', kwargs={'restaurant_slug': r.slug, 'menu_category_pk': mc.pk}),
            data=item_data
        )

        self.assertEqual(response.status_code, 201)
        mc = MenuCategory.objects.get(pk=mc.pk)
        self.assertEqual(mc.items.count(), count_before+1)
        item = MenuItem.objects.get(pk=response.json().get('id'))
        self.assertEqual(item.menu_category, mc)
        for key in item_data:
            self.assertEqual(response.json().get(key), item_data[key])

    # TODO: Test read menu items of a restaurant menu category
    def test_read_menu_items(self):
        r = self._get_random_owned_restaurant()
        self.assertGreater(r.menu_categories.count(), 0)
        mc = random.choice(r.menu_categories.all())
        count_before = mc.items.count()
        self.assertGreater(count_before, 0)
        url = reverse(
            'items-list', kwargs={'restaurant_slug': r.slug, 'menu_category_pk': mc.pk})
        print('url = ', url)
        response = self.authenticated_client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('count'), count_before)

    # TODO: Test update a menu item to restaurant menu category
    def test_update_a_menu_item(self):
        r = self._get_random_owned_restaurant()
        self.assertGreater(r.menu_categories.count(), 0)
        mc = random.choice(r.menu_categories.all())
        count_before = mc.items.count()
        self.assertGreater(count_before, 0)

        item = random.choice(mc.items.all())
        data = {
            # 'name': 'edited',
            'active': False,
            'price': 50
        }
        response = self.authenticated_client.patch(
            reverse('items-detail', kwargs={'restaurant_slug': r.slug,
                    'menu_category_pk': mc.pk, 'pk': item.pk}),
            data=data
        )

        self.assertEqual(response.status_code, 200)
        item = MenuItem.objects.get(pk=item.pk)
        item_data = MenuItemAdminSerializer(item).data
        for key in data:
            self.assertEqual(data[key], item_data[key])

    # TODO: Test delete a menu item to restaurant menu category
    def test_delete_a_menu_item(self):
        r = self._get_random_owned_restaurant()
        self.assertGreater(r.menu_categories.count(), 0)
        mc = random.choice(r.menu_categories.all())
        count_before = mc.items.count()
        self.assertGreater(count_before, 0)

        item = random.choice(mc.items.all())
        response = self.authenticated_client.delete(
            reverse('items-detail', kwargs={'restaurant_slug': r.slug,
                    'menu_category_pk': mc.pk, 'pk': item.pk})
        )

        self.assertEqual(response.status_code, 204)
        self.assertEqual(mc.items.count(), count_before-1)
        self.assertFalse(mc.items.filter(pk=item.pk).exists())
        self.assertFalse(MenuItem.objects.filter(pk=item.pk).exists())
