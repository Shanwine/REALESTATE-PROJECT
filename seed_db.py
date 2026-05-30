import os
import django
import random
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realestate.settings')
django.setup()

from accounts.models import CustomUser
from properties.models import Property
from inquiries.models import Inquiry
from transactions.models import Transaction
from favorites.models import Favorite

def seed():
    print("Seeding database...")
    
    # Create agents / admins
    admin_user = CustomUser.objects.filter(role='admin').first()
    if not admin_user:
        admin_user = CustomUser.objects.create_superuser(
            username='admin',
            email='admin@estatehub.com',
            password='admin123',
            first_name='System',
            last_name='Administrator',
            role='admin'
        )
        print("Admin user created")
        
    # Create customers
    customers = []
    customer_data = [
        ('john_doe', 'John', 'Doe', 'john@gmail.com'),
        ('mary_jane', 'Mary', 'Jane', 'mary@gmail.com'),
        ('alex_smith', 'Alex', 'Smith', 'alex@gmail.com'),
    ]
    
    for username, first, last, email in customer_data:
        user, created = CustomUser.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'first_name': first,
                'last_name': last,
                'role': 'customer'
            }
        )
        if created:
            user.set_password('customer123')
            user.save()
        customers.append(user)
    print(f"Created {len(customers)} customers")

    # Clear existing properties to prevent duplicates on multiple runs
    Property.objects.all().delete()

    # Create properties
    properties_data = [
        {
            'title': 'Modern Minimalist Villa',
            'description': 'A stunning modern minimalist villa located in the heart of Tagaytay. Featuring breathtaking views, high ceilings, spacious living areas, and an infinity pool. Perfect for weekend getaways or permanent luxury living.',
            'price': Decimal('15500000.00'),
            'location': 'Tagaytay City',
            'address': '123 Ridge View Road, Tagaytay City, Cavite',
            'bedrooms': 4,
            'bathrooms': 4,
            'area_sqft': Decimal('3500.00'),
            'property_type': 'house',
            'status': 'available',
            'is_featured': True
        },
        {
            'title': 'Skyline View Condominium',
            'description': 'Luxurious high-rise condominium unit in Bonifacio Global City. Offers panoramic views of the city skyline, state-of-the-art kitchen appliances, and access to premium building amenities including a gym, pool, and 24/7 security.',
            'price': Decimal('8500000.00'),
            'location': 'Taguig City',
            'address': 'Unit 24B, Horizon Tower, Bonifacio Global City, Taguig',
            'bedrooms': 2,
            'bathrooms': 2,
            'area_sqft': Decimal('1100.00'),
            'property_type': 'condo',
            'status': 'available',
            'is_featured': True
        },
        {
            'title': 'Spacious Townhouse in Quezon City',
            'description': 'A beautiful 3-story townhouse situated in a quiet, gated subdivision in Quezon City. Close to top universities and shopping malls. Features a 2-car garage, modern design, and a rooftop pocket garden.',
            'price': Decimal('12000000.00'),
            'location': 'Quezon City',
            'address': 'Block 5 Lot 12, Greenhills East, Quezon City',
            'bedrooms': 3,
            'bathrooms': 3,
            'area_sqft': Decimal('2200.00'),
            'property_type': 'townhouse',
            'status': 'available',
            'is_featured': False
        },
        {
            'title': 'Cozy Suburban Family Home',
            'description': 'Charming single-family home located in a peaceful neighborhood in Nuvali, Santa Rosa. Very family-friendly environment with parks, schools, and biking trails nearby. Features a spacious backyard and a wrap-around porch.',
            'price': Decimal('7200000.00'),
            'location': 'Santa Rosa',
            'address': '45 Solenad Subd, Nuvali, Santa Rosa, Laguna',
            'bedrooms': 3,
            'bathrooms': 2,
            'area_sqft': Decimal('1800.00'),
            'property_type': 'house',
            'status': 'reserved',
            'is_featured': False
        },
        {
            'title': 'Premium Vacant Lot in Batangas',
            'description': 'Build your dream vacation home on this premium vacant lot overlooking the sea in Nasugbu, Batangas. Located within a high-end seaside resort community with complete membership privileges.',
            'price': Decimal('4500000.00'),
            'location': 'Nasugbu, Batangas',
            'address': 'Lot 15 Phase 3, Terrazas de Punta Fuego, Nasugbu, Batangas',
            'bedrooms': 0,
            'bathrooms': 0,
            'area_sqft': Decimal('5000.00'),
            'property_type': 'lot',
            'status': 'available',
            'is_featured': True
        },
        {
            'title': 'Studio Apartment near Makati CBD',
            'description': 'Fully furnished studio apartment just minutes away from Makati Central Business District. Highly profitable rental property, currently tenanted. Perfect for property investors or young professionals.',
            'price': Decimal('3200000.00'),
            'location': 'Makati City',
            'address': '10F Linear Condominium, Mayapis St, Makati City',
            'bedrooms': 1,
            'bathrooms': 1,
            'area_sqft': Decimal('350.00'),
            'property_type': 'apartment',
            'status': 'sold',
            'is_featured': False
        }
    ]

    properties = []
    for p_data in properties_data:
        prop = Property.objects.create(
            title=p_data['title'],
            description=p_data['description'],
            price=p_data['price'],
            location=p_data['location'],
            address=p_data['address'],
            bedrooms=p_data['bedrooms'],
            bathrooms=p_data['bathrooms'],
            area_sqft=p_data['area_sqft'],
            property_type=p_data['property_type'],
            status=p_data['status'],
            is_featured=p_data['is_featured'],
            agent=admin_user
        )
        properties.append(prop)
    print(f"Created {len(properties)} properties")

    # Create favorites
    Favorite.objects.all().delete()
    for customer in customers:
        # Choose 2 random properties to favorite
        favs = random.sample(properties, 2)
        for prop in favs:
            Favorite.objects.create(customer=customer, property=prop)
    print("Created favorites")

    # Create inquiries
    Inquiry.objects.all().delete()
    inquiries_data = [
        {
            'customer': customers[0],
            'property': properties[0],
            'subject': 'Inquiry about Modern Minimalist Villa financing options',
            'message': 'Hi, I am interested in the Modern Minimalist Villa in Tagaytay. Are there bank financing options available, and what is the required downpayment percentage?',
            'status': 'replied',
            'admin_reply': 'Hello John! Yes, bank financing is available up to 80% of the total price. The minimum downpayment is 20% (₱3,100,000.00). Let us know if you want to schedule a viewing!'
        },
        {
            'customer': customers[1],
            'property': properties[1],
            'subject': 'Inquiry about Skyline View Condominium parking slot',
            'message': 'Hello, does the unit come with a dedicated parking slot? Or is it sold separately? Thank you.',
            'status': 'new',
            'admin_reply': ''
        },
        {
            'customer': customers[2],
            'property': properties[4],
            'subject': 'Lot location plan request',
            'message': 'Good day, can you email me the lot plan and map coordinates for the Nasugbu lot? Thanks.',
            'status': 'read',
            'admin_reply': ''
        }
    ]
    for inq in inquiries_data:
        Inquiry.objects.create(
            customer=inq['customer'],
            property=inq['property'],
            subject=inq['subject'],
            message=inq['message'],
            status=inq['status'],
            admin_reply=inq['admin_reply']
        )
    print("Created inquiries")

    # Create transactions
    Transaction.objects.all().delete()
    # Transaction for cozy family home (reserved)
    Transaction.objects.create(
        listing=properties[3],
        customer=customers[0],
        amount=properties[3].price,
        status='approved',
        payment_method='bank_transfer',
        notes='Reservation deposit paid. Bank financing documents in progress.'
    )
    # Transaction for studio apartment (sold)
    Transaction.objects.create(
        listing=properties[5],
        customer=customers[1],
        amount=properties[5].price,
        status='completed',
        payment_method='cash',
        notes='Full cash payment completed. Title transfer initiated.'
    )
    print("Created transactions")
    print("Database seeding completed successfully!")

if __name__ == '__main__':
    seed()
