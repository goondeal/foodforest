import random
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from faker import Faker
from faker_food import FoodProvider
from users.models import CustomUser
from restaurants.models import *
from restaurants.serializers import *
from orders.models import *
from management.models import *


class OrderViewSetTests(TestCase):
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
            'email': cls.user_data['email'],
            'password': cls.user_data['password']
        }
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
        cls.statuses = [
            RestaurantStatus.objects.create(
                title='open', title_ar='open', color='#0f0'),
            RestaurantStatus.objects.create(
                title='closed', title_ar='closed', color='#f00'),
            RestaurantStatus.objects.create(
                title='Getting ready', title_ar='Getting ready', color='#ccc'),
        ]
        # create restaurants
        data = {
            'address': 'shohadaa Talaat Harb st',
            'owner': cls.user,
            
        }
        cls.restaurants = [
            Restaurant.objects.create(
                **data,
                name=random.choice(
                    ['rustii', 'Nest', 'Bazoka', 'KFC', 'Sobhy Kaber', 'Hosny']),
                city=random.choice(cls.cities),
                active=True,
                status=random.choice(cls.statuses),
                rating=random.choice([1, 2, 3, 4, 5]),
                num_of_reviewers=random.randint(1, 100)
            ) for i in range(15)
        ] + [
            Restaurant.objects.create(
                **data,
                name=random.choice(
                    ['rustii', 'Nest', 'Bazoka', 'KFC', 'Sobhy Kaber', 'Hosny']),
                city=random.choice(cls.cities),
                active=False,
                status=random.choice(cls.statuses),
                rating=random.choice([1, 2, 3, 4, 5]),
                num_of_reviewers=random.randint(1, 100)
            ) for i in range(10)
        ]
        cls.menu_categories = [
            MenuCategory.objects.create
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
        for restaurant in cls.restaurants:
            for i in range(random.choice([2, 3])):
                mc = MenuCategory.objects.create(
                    restaurant=restaurant,
                    ordering=i,
                    **random.choice(menu_categories)
                )
                for j in range(10):
                    mi = MenuItem.objects.create(
                        name=faker.dish(),
                        name_ar='لا يوجد',
                        description=faker.dish_description(),
                        price=random.randint(5, 500),
                        active=True,
                        menu_category=mc,
                        ordering=j,
                        rating=random.randint(0, 5),
                        num_of_reviews=random.randint(1, 10000)
                    )
                    mi.features.add(random.choice(features))
                    mi.save()
        cls.order_types = [
            OrderType.objects.create(title='H', description='Hall'),
            OrderType.objects.create(title='D', description='Delivery'),
            OrderType.objects.create(title='T', description='Takeaway'),
        ]
        cls.order_statuses = [
            OrderStatus.objects.create(title='sent', color='#ccc'),
            OrderStatus.objects.create(title='seen', color='#00f'),
            OrderStatus.objects.create(title='being prepared', color='#ccc'),
            OrderStatus.objects.create(title='delivered', color='#0f0'),
        ]

    def _get_restaurant_items(self, restaurant):
        result = []
        for c in restaurant.menu_categories.prefetch_related('items'):
            result += [item for item in c.items.all()]
        return result

    def test_make_a_valid_order_with_authenticated_user(self):
        r = random.choice(
            [r for r in self.restaurants if r.active and r.status.is_open])
        items = random.sample(self._get_restaurant_items(r), k=5)
        # print('items =', items)
        data = {
            'restaurant': r.slug,
            'type': random.choice(self.order_types).id,
            'note': '',
            'items': [
                {
                    'item': item.id,
                    'name': item.name,
                    'description': item.description,
                    'price': float(item.price),
                    'features': MenuItemSerializer(item).data.get('features'),
                    'quantity': random.choice(range(1, 6))
                }
                for item in items
            ],
            'phone': '+201066133855',
        }
        orders_count = Order.objects.count()
        response = self.authenticated_client.post(
            reverse('orders-list'), data=data)
        # print('response = ', response.json())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Order.objects.count(), orders_count+1)
        self.assertEqual(data['restaurant'],
                         response.json().get('restaurant').get('slug'))
        self.assertEqual(
            set([(item.get('item'), item.get('quantity'))
                for item in data['items']]),
            set([(item.get('item'), item.get('quantity'))
                for item in response.json()['items']])
        )

    def test_make_a_valid_order_with_unauthenticated_user(self):
        r = random.choice(
            [r for r in self.restaurants if r.active and r.status.is_open])
        items = random.sample(self._get_restaurant_items(r), k=5)
        # print('items =', items)
        data = {
            'restaurant': r.slug,
            'type': random.choice(self.order_types).id,
            'note': '',
            'items': [
                {
                    'item': item.id,
                    'name': item.name,
                    'description': item.description,
                    'price': float(item.price),
                    'features': MenuItemSerializer(item).data.get('features'),
                    'quantity': random.choice(range(1, 6))
                }
                for item in items
            ],
            'phone': '+201066133855',
        }
        orders_count = Order.objects.count()
        response = self.unauthenticated_client.post(
            reverse('orders-list'), data=data)
        print('response = ', response.json())
        self.assertEqual(response.status_code, 401)
        self.assertEqual(Order.objects.count(), orders_count)

    def test_make_a_valid_order_to_a_not_active_restaurant(self):
        r = random.choice(
            [r for r in self.restaurants if not r.active and r.status.is_open])
        items = random.sample(self._get_restaurant_items(r), k=5)
        # print('items =', items)
        data = {
            'restaurant': r.slug,
            'type': random.choice(self.order_types).id,
            'note': '',
            'items': [
                {
                    'item': item.id,
                    'name': item.name,
                    'description': item.description,
                    'price': float(item.price),
                    'features': MenuItemSerializer(item).data.get('features'),
                    'quantity': random.choice(range(1, 6))
                }
                for item in items
            ],
            'phone': '+201066133855',
        }
        orders_count = Order.objects.count()
        response = self.authenticated_client.post(
            reverse('orders-list'), data=data)
        print('\nresponse = ', response.json())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Order.objects.count(), orders_count)

    def test_make_a_valid_order_to_a_not_open_restaurant(self):
        r = random.choice(
            [r for r in self.restaurants if r.active and not r.status.is_open])
        items = random.sample(self._get_restaurant_items(r), k=5)
        # print('items =', items)
        data = {
            'restaurant': r.slug,
            'type': random.choice(self.order_types).id,
            'note': '',
            'items': [
                {
                    'item': item.id,
                    'name': item.name,
                    'description': item.description,
                    'price': float(item.price),
                    'features': MenuItemSerializer(item).data.get('features'),
                    'quantity': random.choice(range(1, 6))
                }
                for item in items
            ],
            'phone': '+201066133855',
        }
        orders_count = Order.objects.count()
        response = self.authenticated_client.post(
            reverse('orders-list'), data=data)
        print('\nresponse = ', response.json())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Order.objects.count(), orders_count)


    def test_make_an_order_with_items_from_multiple_restaurants(self):
        rs = random.sample(
            [r for r in self.restaurants if r.active and r.status.is_open], k=2)
        items = random.sample(self._get_restaurant_items(rs[0]), k=3) + \
            random.sample(self._get_restaurant_items(rs[-1]), k=3)
        # print('items =', items)
        data = {
            'restaurant': rs[0].slug,
            'type': random.choice(self.order_types).id,
            'note': '',
            'items': [
                {
                    'item': item.id,
                    'name': item.name,
                    'description': item.description,
                    'price': float(item.price),
                    'features': MenuItemSerializer(item).data.get('features'),
                    'quantity': random.choice(range(1, 6))
                }
                for item in items
            ],
            'phone': '+201066133855',
        }
        orders_count = Order.objects.count()
        response = self.authenticated_client.post(
            reverse('orders-list'), data=data)
        print('response = ', response.json())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Order.objects.count(), orders_count)

    def test_make_an_empty_order(self):
        r = random.choice(
            [r for r in self.restaurants if r.active and r.status.is_open])
        data = {
            'restaurant': r.slug,
            'type': random.choice(self.order_types).id,
            'note': '',
            'items': [],
            'phone': '+201066133855',
        }
        orders_count = Order.objects.count()
        response = self.authenticated_client.post(
            reverse('orders-list'), data=data)
        print('response = ', response.json())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Order.objects.count(), orders_count)


    def test_make_an_order_with_invalid_phone(self):
        r = random.choice([r for r in self.restaurants if r.active and r.status.is_open])
        items = random.sample(self._get_restaurant_items(r), k=5)
        # print('items =', items)
        data = {
            'restaurant': r.slug,
            'type': random.choice(self.order_types).id,
            'note': '',
            'items': [
                {
                    'item': item.id,
                    'name': item.name,
                    'description': item.description,
                    'price': float(item.price),
                    'features': MenuItemSerializer(item).data.get('features'),
                    'quantity': random.choice(range(1, 6))
                }
                for item in items
            ],
            'phone': '01066133855',
        }
        orders_count = Order.objects.count()
        response = self.authenticated_client.post(
            reverse('orders-list'), data=data)
        print('response = ', response.json())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Order.objects.count(), orders_count)


    def test_make_an_order_with_wrong_items_prices(self):
        r = random.choice([r for r in self.restaurants if r.active and r.status.is_open])
        items = random.sample(self._get_restaurant_items(r), k=5)
        # print('items =', items)
        data = {
            'restaurant': r.slug,
            'type': random.choice(self.order_types).id,
            'note': '',
            'items': [
                {
                    'item': item.id,
                    'name': item.name,
                    'description': item.description,
                    'price': float(item.price) + 2,
                    'features': MenuItemSerializer(item).data.get('features'),
                    'quantity': random.choice(range(1, 6))
                }
                for item in items
            ],
            'phone': '+201066133855',
        }
        orders_count = Order.objects.count()
        response = self.authenticated_client.post(
            reverse('orders-list'), data=data)
        print('response = ', response.json())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Order.objects.count(), orders_count)

    def test_make_an_order_with_wrong_items_names(self):
        r = random.choice([r for r in self.restaurants if r.active and r.status.is_open])
        items = random.sample(self._get_restaurant_items(r), k=5)
        # print('items =', items)
        data = {
            'restaurant': r.slug,
            'type': random.choice(self.order_types).id,
            'note': '',
            'items': [
                {
                    'item': item.id,
                    'name': item.name + 'edited',
                    'description': item.description,
                    'price': float(item.price) + 2,
                    'features': MenuItemSerializer(item).data.get('features'),
                    'quantity': random.choice(range(1, 6))
                }
                for item in items
            ],
            'phone': '+201066133855',
        }
        orders_count = Order.objects.count()
        response = self.authenticated_client.post(
            reverse('orders-list'), data=data)
        print('response = ', response.json())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Order.objects.count(), orders_count)

    def test_make_an_order_with_wrong_items_ids(self):
        r = random.choice([r for r in self.restaurants if r.active and r.status.is_open])
        items = random.sample(self._get_restaurant_items(r), k=5)
        # print('items =', items)
        data = {
            'restaurant': r.slug,
            'type': random.choice(self.order_types).id,
            'note': '',
            'items': [
                {
                    'item': item.id + 1,
                    'name': item.name,
                    'description': item.description,
                    'price': float(item.price) + 2,
                    'features': MenuItemSerializer(item).data.get('features'),
                    'quantity': random.choice(range(1, 6))
                }
                for item in items
            ],
            'phone': '+201066133855',
        }
        orders_count = Order.objects.count()
        response = self.authenticated_client.post(
            reverse('orders-list'), data=data)
        print('response = ', response.json())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Order.objects.count(), orders_count)

    def test_make_an_order_with_wrong_items_description(self):
        r = random.choice([r for r in self.restaurants if r.active and r.status.is_open])
        items = random.sample(self._get_restaurant_items(r), k=5)
        # print('items =', items)
        data = {
            'restaurant': r.slug,
            'type': random.choice(self.order_types).id,
            'note': '',
            'items': [
                {
                    'item': item.id,
                    'name': item.name,
                    'description': item.description + 'edited',
                    'price': float(item.price) + 2,
                    'features': MenuItemSerializer(item).data.get('features'),
                    'quantity': random.choice(range(1, 6))
                }
                for item in items
            ],
            'phone': '+201066133855',
        }
        orders_count = Order.objects.count()
        response = self.authenticated_client.post(
            reverse('orders-list'), data=data)
        print('response = ', response.json())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Order.objects.count(), orders_count)

    def test_make_an_order_with_zero_quantities(self):
        r = random.choice([r for r in self.restaurants if r.active and r.status.is_open])
        items = random.sample(self._get_restaurant_items(r), k=5)
        # print('items =', items)
        data = {
            'restaurant': r.slug,
            'type': random.choice(self.order_types).id,
            'note': '',
            'items': [
                {
                    'item': item.id,
                    'name': item.name,
                    'description': item.description,
                    'price': float(item.price) + 2,
                    'features': MenuItemSerializer(item).data.get('features'),
                    'quantity': 0
                }
                for item in items
            ],
            'phone': '+201066133855',
        }
        orders_count = Order.objects.count()
        response = self.authenticated_client.post(
            reverse('orders-list'), data=data)
        print('response = ', response.json())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Order.objects.count(), orders_count)

    def test_make_an_order_with_negative_quantities(self):
        r = random.choice([r for r in self.restaurants if r.active and r.status.is_open])
        items = random.sample(self._get_restaurant_items(r), k=5)
        # print('items =', items)
        data = {
            'restaurant': r.slug,
            'type': random.choice(self.order_types).id,
            'note': '',
            'items': [
                {
                    'item': item.id,
                    'name': item.name,
                    'description': item.description,
                    'price': float(item.price) + 2,
                    'features': MenuItemSerializer(item).data.get('features'),
                    'quantity': -3
                }
                for item in items
            ],
            'phone': '+201066133855',
        }
        orders_count = Order.objects.count()
        response = self.authenticated_client.post(
            reverse('orders-list'), data=data)
        print('response = ', response.json())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Order.objects.count(), orders_count)


    def test_make_an_order_with_float_quantities(self):
        r = random.choice([r for r in self.restaurants if r.active and r.status.is_open])
        items = random.sample(self._get_restaurant_items(r), k=5)
        # print('items =', items)
        data = {
            'restaurant': r.slug,
            'type': random.choice(self.order_types).id,
            'note': '',
            'items': [
                {
                    'item': item.id,
                    'name': item.name,
                    'description': item.description,
                    'price': float(item.price) + 2,
                    'features': MenuItemSerializer(item).data.get('features'),
                    'quantity': 3.5
                }
                for item in items
            ],
            'phone': '+201066133855',
        }
        orders_count = Order.objects.count()
        response = self.authenticated_client.post(
            reverse('orders-list'), data=data)
        print('response = ', response.json())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Order.objects.count(), orders_count)
