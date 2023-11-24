import os
import django
from django.db.models import Q, Count, F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
# Create and run your queries within functions
from main_app.models import Profile, Order, Product


# Django Queries I
def get_profiles(search_string=None) -> str:
    if search_string is None:
        return ''

    query = Q(full_name__icontains=search_string) | \
            Q(email__icontains=search_string) | \
            Q(phone_number__icontains=search_string)

    profiles = Profile.objects.filter(query).order_by('full_name')

    if not profiles:
        return ''

    return '\n'.join([
        f"Profile: {p.full_name}, email: {p.email}, "
        f"phone number: {p.phone_number}, orders: {p.profile_orders.count()}"
        for p in profiles
    ])


def get_loyal_profiles() -> str:
    profiles = Profile.objects.get_regular_customers()

    if not profiles:
        return ''

    return '\n'.join([
        f"Profile: {p.full_name}, orders: {p.num_orders}" for p in profiles
    ])


def get_last_sold_products() -> str:
    last_order = Order.objects.prefetch_related('products').last()

    if not last_order or not last_order.products.exists():
        return ''

    sold_products = ', '.join([p.name for p in last_order.products.all()])

    return f"Last sold products: {sold_products}"


# Django Queries II
def get_top_products() -> str:
    top_products = Product.objects.annotate(
        num_orders=Count('products_orders')
    ).filter(
        num_orders__gt=0
    ).order_by(
        '-num_orders',
        'name'
    )[:5]

    if not top_products:
        return ''

    product_sales = '\n'.join([f"{p.name}, sold {p.num_orders} times" for p in top_products])

    return f"Top products:\n{product_sales}"


def apply_discounts() -> str:
    orders = Order.objects.annotate(
        num_products=Count('products')
    ).filter(
        num_products__gt=2,
        is_completed=False,
    )

    updated_orders = orders.update(F('total_price') * 0.9)

    return f"Discount applied to {updated_orders} orders."


def complete_order() -> str:
    order = Order.objects.prefetch_related('products').filter(
        is_completed=False
    ).order_by(
        'creation_date'
    ).first()

    if not order:
        return ''

    for product in order.products.all():
        product.in_stock -= 1

        if product.in_stock <= 0:
            product.is_available = False

        product.save()

    order.is_completed = True
    order.save()

    return "Order has been completed!"
