from django.test import TestCase
from django.utils.text import slugify
from management.models import Country, State, City
from restaurants.models import Restaurant, RestaurantStatus
from users.models import CustomUser


class RestaurantModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
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
        cls.down_town = City.objects.create(
            name='Down Town',
            state=cairo,
            ordering=1,
            active=True
        )
        # create restaurant status
        cls.status = RestaurantStatus.objects.create(
            title='open',
            title_ar='open',
            color='#ccc'
        )


    def test_create_restaurants_with_the_same_name(self):
        data = {
            'name': 'rustii',
            'address': 'shohadaa Talaat Harb st',
            'city': self.down_town,
            'status': self.status,
            'owner': self.user,
        }
        r1 = Restaurant.objects.create(**data)
        self.assertEqual(r1.id, 1)
        self.assertEqual(r1.name, data['name'])
        self.assertEqual(r1.slug, data['name'])

        r2 = Restaurant.objects.create(**data)
        self.assertEqual(r2.id, 2)
        self.assertEqual(r2.name, data['name'])
        slug = slugify(f'{data["name"]} {self.down_town}')
        self.assertEqual(r2.slug, slug)

        r3 = Restaurant.objects.create(**data)
        self.assertEqual(r3.id, 3)
        self.assertEqual(r3.name, data['name'])
        slug_parts = r3.slug.split('-')
        self.assertGreaterEqual(len(slug_parts), 3)
        self.assertEqual(slug_parts[0], data['name'])
        self.assertEqual(' '.join(slug_parts[1:-1]), self.down_town.name.lower())
        self.assertTrue(slug_parts[-1].isnumeric())
        

        r4 = Restaurant.objects.create(**data)
        self.assertEqual(r4.id, 4)
        self.assertEqual(r4.name, data['name'])
        self.assertEqual(r1.slug, data['name'])
        slug_parts = r3.slug.split('-')
        self.assertGreaterEqual(len(slug_parts), 3)
        self.assertEqual(slug_parts[0], data['name'])
        self.assertEqual(' '.join(slug_parts[1:-1]), self.down_town.name.lower())
        self.assertTrue(slug_parts[-1].isnumeric())
