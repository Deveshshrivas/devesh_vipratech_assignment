from django.core.management.base import BaseCommand
from payments.models import Product


class Command(BaseCommand):
    help = 'Setup 3 fixed products for the shop'

    def handle(self, *args, **options):
        products = [
            {
                'name': 'Premium Laptop',
                'description': 'High-performance laptop with 16GB RAM and 512GB SSD',
                'price': 1299.99,
            },
            {
                'name': 'Wireless Headphones',
                'description': 'Noise-cancelling Bluetooth headphones with 30-hour battery',
                'price': 249.99,
            },
            {
                'name': 'Smart Watch',
                'description': 'Fitness tracker with heart rate monitor and GPS',
                'price': 399.99,
            },
        ]

        for product_data in products:
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults={
                    'description': product_data['description'],
                    'price': product_data['price'],
                    'is_active': True,
                }
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created product: {product.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Product already exists: {product.name}')
                )

        self.stdout.write(
            self.style.SUCCESS('\nSuccessfully setup products!')
        )
