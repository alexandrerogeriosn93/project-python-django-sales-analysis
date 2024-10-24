import random
from django.core.management.base import BaseCommand
from faker import Faker
from sales.models import Sale


class Command(BaseCommand):
    help = 'Popula o banco de dados com vendas fictícias'

    def handle(self, *args, **kwargs):
        faker = Faker()

        products = [
            "Smart TV", "Caneca", "Mouse", "Teclado", "Headset",
            "Air fryer", "Monitor", "IPhone", "Desktop", "PC Gamer"
        ]

        sales = []

        for _ in range(300):
            sale = Sale(
                date=faker.date_this_year(),
                product=random.choice(products),
                quantity=random.randint(1, 100),
                price=round(random.uniform(10.0, 500.0), 2)
            )

            sales.append(sale)

        Sale.objects.bulk_create(sales)
        self.stdout.write(self.style.SUCCESS('Banco de dados populado com 300 vendas.'))
