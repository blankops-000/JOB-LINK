from marshmallow import Schema, fields, validate

class ProviderProfileSchema(Schema):
    id = fields.UUID(dump_only=True)
    user_id = fields.UUID(required=True)
    category_id = fields.UUID(required=True)
    service_area_id = fields.UUID(required=True)
    bio = fields.Str(validate=validate.Length(max=500))
    location = fields.Str()
    is_verified = fields.Bool()
    average_rating = fields.Float(dump_only=True)

class BookingSchema(Schema):
    id = fields.UUID(dump_only=True)
    customer_id = fields.UUID(required=True)
    provider_id = fields.UUID(required=True)
    service_date = fields.DateTime(required=True)
    notes = fields.Str()
    status = fields.Str(validate=validate.OneOf(["pending", "confirmed", "completed", "cancelled"]))

class ReviewSchema(Schema):
    id = fields.UUID(dump_only=True)
    booking_id = fields.UUID(required=True)
    customer_id = fields.UUID(required=True)
    provider_id = fields.UUID(required=True)
    rating = fields.Int(required=True, validate=validate.Range(min=1, max=5))
    comment = fields.Str()

class PaymentSchema(Schema):
    id = fields.UUID(dump_only=True)
    booking_id = fields.UUID(required=True)
    amount = fields.Decimal(required=True)
    status = fields.Str(validate=validate.OneOf(["pending", "paid", "failed"]))
    transaction_ref = fields.Str()

class ServiceCategorySchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str()
