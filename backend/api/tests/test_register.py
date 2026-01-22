from rest_framework.test import APIClient, APITestCase
from json import loads


class TestRegister(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url = '/api/auth/register/'
        cls.credentials = {
            'username': 'us3rn@me',
            'password': 's3cr_tPwdd'
        }

    def setUp(self):
        self.client = APIClient()

    def testCorrectRegister(self):
        data = self.credentials
        expected_data = {
            'username': 'us3rn@me'
        }
        response = self.client.post(self.url, data)
        self.assertEquals(
            response.status_code,
            201,
            'Убедитесь, что запроc на регистрацию нового пользователя, '
            'содержащий корректные данные, возвращает ответ со статус-кодом 201'
        )
        self.assertEquals(
            loads(response.text),
            expected_data
        )

    def testDuplicateRegister(self):
        data = self.credentials
        expected_data = {
            'username': ['Пользователь с таким именем уже существует.']
        }
        self.client.post(self.url, data)
        response = self.client.post(self.url, data)
        self.assertEquals(
            response.status_code,
            400,
            'Запрос на /api/auth/register/ с уже '
            'зарегистрированным юзернеймом должен вернуть 400'
        )
        self.assertEquals(
            loads(response.text),
            expected_data,
            'Ответ в отчете поля пароля должен '
            'содержать строку о необходимости поля'
        )

    def testNoRegisterWithoutPassword(self):
        data = {
            'username': 'us3rn@me',
        }
        expected_data = {
            'password': ['Обязательное поле.']
        }
        response = self.client.post(self.url, data)
        self.assertEquals(
            response.status_code,
            400,
            'Если в запросе на /api/auth/register/ '
            'нет пароля, должен вернуться 400'
        )
        self.assertEquals(
            loads(response.text),
            expected_data,
            'Ответ в отчете поля пароля должен'
            ' содержать строку о необходимости поля'
        )

    def testNoRegisterWithoutUsername(self):
        data = {
            'password': 's3cr_tPwdd'
        }
        expected_data = {
            'username': ['Обязательное поле.']
        }
        response = self.client.post(self.url, data)
        self.assertEquals(
            response.status_code,
            400,
            'Если в запросе на /api/auth/register/ '
            'нет юзернейма, должен вернуться 400'
        )
        self.assertEquals(
            loads(response.text),
            expected_data,
            'Ответ в отчете поля юзернейма должен '
            'содержать строку о необходимости поля'
        )

    def testNoRegisterWithInvalidUsername(self):
        data = {
            'username': ';isinvalid',
            'password': 's3cr_tPwdd'
        }
        expected_data = {
            'username': [
                'Введите правильное имя пользователя. Оно может содержать '
                'только буквы, цифры и знаки @/./+/-/_.'
            ]
        }
        response = self.client.post(self.url, data)
        self.assertEquals(
            response.status_code,
            400,
            'Если в запросе на /api/auth/register/ передан '
            'невалидный юзернейм, то должен вернуться 400'
        )
        self.assertEquals(
            loads(response.text),
            expected_data,
            'Введите правильное имя пользователя. Оно может содержать '
            'только буквы, цифры и знаки @/./+/-/_.'
        )

    def testNoRegisterWithInvalidPassword(self):
        data = {
            'username': 'quite_unique_username',
            'password': 'qwerty'
        }
        response = self.client.post(self.url, data)
        self.assertEquals(
            response.status_code,
            400,
            'Если в запросе на /api/auth/register/ передан невалидный '
            'пароль, то должен вернуться 400'
        )
        self.assertIn(
            'Введённый пароль слишком широко распространён.',
            loads(response.text)['password'],
            'Ответ в отчете поля пароля должен содержать строку об ошибке'
        )
