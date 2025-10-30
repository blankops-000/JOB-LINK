from app import create_app, db
from app.models import User, ServiceCategory, ProviderProfile
from datetime import datetime, timezone

app = create_app()

with app.app_context():
    try:
        # Check if user exists, if not create one
        user = User.query.filter_by(email='testprovider@example.com').first()
        if not user:
            user = User(
                email='testprovider@example.com',
                password_hash='testpassword',
                first_name='Test',
                last_name='Provider',
                phone='1234567890',
                role='PROVIDER',
                is_verified=True
            )
            db.session.add(user)
            db.session.commit()  # Commit user creation immediately
            print("✅ Created test user")
        else:
            print(f"ℹ️  Using existing user: {user.email} (ID: {user.id})")

        # Get or create a service category
        category = ServiceCategory.query.first()
        if not category:
            category = ServiceCategory(
                name="General Services",
                description="General service provider"
            )
            db.session.add(category)
            db.session.commit()  # Commit category creation
            print("✅ Created service category")
        else:
            print(f"ℹ️  Using existing service category: {category.name}")

        # Create provider profile
        profile = ProviderProfile.query.filter_by(user_id=user.id).first()
        if not profile:
            profile = ProviderProfile(
                user_id=user.id,
                business_name=f"{user.first_name}'s Services",
                description="Professional service provider",
                hourly_rate=50.00,
                service_category_id=category.id,
                is_available=True,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            )
            db.session.add(profile)
            db.session.commit()  # Commit profile creation
            print("✅ Created provider profile")
        else:
            print("ℹ️  Provider profile already exists")

        # Verify the data
        print("\n📊 Verification:")
        print(f"Users: {User.query.count()}")
        print(f"Service Categories: {ServiceCategory.query.count()}")
        print(f"Provider Profiles: {ProviderProfile.query.count()}")

        # List all providers
        print("\n👥 All Provider Profiles:")
        for p in ProviderProfile.query.all():
            print(f"- {p.business_name} (ID: {p.id}, User ID: {p.user_id})")

        # Explicitly commit any remaining changes
        db.session.commit()

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        db.session.rollback()
    finally:
        # Don't rollback at the end
        pass