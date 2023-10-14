import random
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from management.models import Country, State, City
from restaurants.models import Restaurant, RestaurantStatus
from users.models import CustomUser


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

    # TODO: Test creating new restaurant if user is authenticated.

    def test_create_restaurant_with_authenticated_client(self):
        restaurants_count_before = Restaurant.objects.count()
        data = {
            'name': 'rustii',
            'address': 'shohadaa Talaat Harb st',
            'city': self.cities[0].id,
            'status': self.status.id,
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


# Restaurant admin tests
    # TODO: Test updating an existing restaurant data.
    # TODO: Test deleting an existing restaurant.
    # TODO: Test deleting a not existing restaurant.
