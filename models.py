from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from slugify import slugify
import bcrypt

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # One-to-one relationship with graduate profile
    profile = db.relationship('GraduateProfile', backref='user', uselist=False, cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def __repr__(self):
        return f'<User {self.email}>'


class GraduateProfile(db.Model):
    __tablename__ = 'graduate_profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)

    # Personal info
    first_name = db.Column(db.String(100), nullable=False, default='')
    last_name = db.Column(db.String(100), nullable=False, default='')
    photo_url = db.Column(db.String(500), nullable=True)
    personal_message = db.Column(db.Text, nullable=True)

    # Academic info
    school_name = db.Column(db.String(200), nullable=True)
    degree = db.Column(db.String(200), nullable=True)
    graduation_date = db.Column(db.Date, nullable=True)
    graduation_year = db.Column(db.Integer, nullable=True)

    # Public URL slug
    slug = db.Column(db.String(200), unique=True, nullable=True)

    # Visibility
    is_public = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    party_details = db.relationship('PartyDetails', backref='profile', uselist=False, cascade='all, delete-orphan')
    registry_items = db.relationship('RegistryItem', backref='profile', lazy='dynamic', cascade='all, delete-orphan', order_by='RegistryItem.created_at')
    external_registries = db.relationship('ExternalRegistry', backref='profile', lazy='dynamic', cascade='all, delete-orphan')

    def generate_slug(self):
        base = f"{self.first_name} {self.last_name}"
        candidate = slugify(base)
        if not candidate:
            candidate = f"graduate-{self.user_id}"
        # Ensure uniqueness
        existing = GraduateProfile.query.filter(
            GraduateProfile.slug == candidate,
            GraduateProfile.id != self.id
        ).first()
        if existing:
            candidate = f"{candidate}-{self.user_id}"
        self.slug = candidate
        return candidate

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def __repr__(self):
        return f'<GraduateProfile {self.full_name}>'


class PartyDetails(db.Model):
    __tablename__ = 'party_details'

    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('graduate_profiles.id'), nullable=False, unique=True)

    event_title = db.Column(db.String(200), nullable=True)
    event_date = db.Column(db.Date, nullable=True)
    event_time = db.Column(db.String(50), nullable=True)
    location_name = db.Column(db.String(200), nullable=True)
    location_address = db.Column(db.String(400), nullable=True)
    rsvp_instructions = db.Column(db.Text, nullable=True)
    additional_notes = db.Column(db.Text, nullable=True)
    rsvp_deadline = db.Column(db.Date, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<PartyDetails for profile {self.profile_id}>'


class RegistryItem(db.Model):
    __tablename__ = 'registry_items'

    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('graduate_profiles.id'), nullable=False)

    title = db.Column(db.String(300), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=True)
    quantity_needed = db.Column(db.Integer, default=1)
    quantity_purchased = db.Column(db.Integer, default=0)
    external_url = db.Column(db.String(1000), nullable=True)
    image_url = db.Column(db.String(1000), nullable=True)
    category = db.Column(db.String(100), nullable=True)
    priority = db.Column(db.String(20), default='medium')  # high, medium, low

    is_purchased = db.Column(db.Boolean, default=False)
    purchased_by_note = db.Column(db.String(200), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @property
    def remaining_quantity(self):
        return max(0, self.quantity_needed - self.quantity_purchased)

    @property
    def is_fully_claimed(self):
        return self.quantity_purchased >= self.quantity_needed

    def __repr__(self):
        return f'<RegistryItem {self.title}>'


class ExternalRegistry(db.Model):
    __tablename__ = 'external_registries'

    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('graduate_profiles.id'), nullable=False)

    name = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(1000), nullable=False)
    description = db.Column(db.String(400), nullable=True)
    icon_url = db.Column(db.String(500), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ExternalRegistry {self.name}>'
