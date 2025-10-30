from app import create_app, db
from app.models.service_category import ServiceCategory

app = create_app()

with app.app_context():
    # Sample service categories
    services = [
        {'name': 'Plumbing', 'description': 'Water pipe repairs, installations, and maintenance'},
        {'name': 'Cleaning', 'description': 'House cleaning, office cleaning, and deep cleaning services'},
        {'name': 'Electrical', 'description': 'Electrical installations, repairs, and maintenance'},
        {'name': 'Tutoring', 'description': 'Academic tutoring and educational support'},
        {'name': 'Cooking', 'description': 'Personal chef services and meal preparation'},
        {'name': 'Gardening', 'description': 'Garden maintenance, landscaping, and plant care'}
    ]
    
    for service_data in services:
        # Check if service already exists
        existing = ServiceCategory.query.filter_by(name=service_data['name']).first()
        if not existing:
            service = ServiceCategory(
                name=service_data['name'],
                description=service_data['description']
            )
            db.session.add(service)
    
    db.session.commit()
    print("Sample services added successfully!")
    
    # List all services
    all_services = ServiceCategory.query.all()
    print(f"Total services: {len(all_services)}")
    for service in all_services:
        print(f"- {service.name}: {service.description}")