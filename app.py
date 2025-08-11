from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, date
import os
import re
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Add upload configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



def validate_username(username):
    """Validate username with comprehensive rules"""
    errors = []
    
    if not username:
        errors.append("Username is required")
        return errors
    
    # Length validation
    if len(username) < 5:
        errors.append("Username must be at least 5 characters long")
    if len(username) > 13:
        errors.append("Username must be no more than 13 characters long")
    
    # Character validation - only alphanumeric and underscores
    if not re.match("^[a-zA-Z0-9_]+$", username):
        errors.append("Username can only contain letters, numbers, and underscores")
    
    # Must start with a letter
    if not username[0].isalpha():
        errors.append("Username must start with a letter")
    
    # Cannot end with underscore
    if username.endswith('_'):
        errors.append("Username cannot end with an underscore")
    
    # Cannot have consecutive underscores
    if '__' in username:
        errors.append("Username cannot have consecutive underscores")
    
    # Reserved usernames
    reserved_usernames = [
        'admin', 'administrator', 'root', 'user', 'test', 'guest', 'api', 'www',
        'mail', 'email', 'support', 'help', 'info', 'contact', 'about', 'login',
        'register', 'signup', 'signin', 'logout', 'dashboard', 'profile', 'settings',
        'moderator', 'mod', 'staff', 'official', 'system', 'null', 'undefined'
    ]
    if username.lower() in reserved_usernames:
        errors.append("This username is reserved and cannot be used")
    
    return errors

def validate_name(name, field_name="Name"):
    """Validate first name and last name"""
    errors = []
    
    if not name or not name.strip():
        errors.append(f"{field_name} is required")
        return errors
    
    name = name.strip()
    
    # Length validation
    if len(name) < 2:
        errors.append(f"{field_name} must be at least 2 characters long")
    if len(name) > 50:
        errors.append(f"{field_name} must be no more than 50 characters long")
    
    # Character validation - only letters, spaces, hyphens, and apostrophes
    if not re.match("^[a-zA-Z\s\-']+$", name):
        errors.append(f"{field_name} can only contain letters, spaces, hyphens, and apostrophes")
    
    # Cannot start or end with space, hyphen, or apostrophe
    if name[0] in [' ', '-', "'"] or name[-1] in [' ', '-', "'"]:
        errors.append(f"{field_name} cannot start or end with spaces, hyphens, or apostrophes")
    
    # Cannot have consecutive special characters
    if re.search(r"[\s\-']{2,}", name):
        errors.append(f"{field_name} cannot have consecutive spaces, hyphens, or apostrophes")
    
    return errors

def validate_group_title(title):
    """Validate group title"""
    errors = []
    
    if not title or not title.strip():
        errors.append("Group title is required")
        return errors
    
    title = title.strip()
    
    # Length validation
    if len(title) < 5:
        errors.append("Group title must be at least 5 characters long")
    if len(title) > 200:
        errors.append("Group title must be no more than 200 characters long")
    
    # Must contain at least one letter
    if not re.search(r'[a-zA-Z]', title):
        errors.append("Group title must contain at least one letter")
    
    # Cannot be all caps (more than 70% uppercase)
    if title.isupper() and len(title) > 10:
        errors.append("Group title cannot be all uppercase")
    
    # Cannot contain excessive special characters
    special_char_count = len(re.findall(r'[!@#$%^&*()+=\[\]{}|\\:";\'<>?,./]', title))
    if special_char_count > len(title) * 0.3:  # More than 30% special characters
        errors.append("Group title contains too many special characters")
    
    # Inappropriate content check (basic)
    inappropriate_words = ['spam', 'fake', 'scam', 'money', 'cash', 'bitcoin', 'crypto']
    title_lower = title.lower()
    for word in inappropriate_words:
        if word in title_lower:
            errors.append("Group title contains inappropriate content")
            break
    
    return errors

def validate_destination(destination):
    """Validate destination name"""
    errors = []
    
    if not destination or not destination.strip():
        errors.append("Destination is required")
        return errors
    
    destination = destination.strip()
    
    # Length validation
    if len(destination) < 2:
        errors.append("Destination must be at least 2 characters long")
    if len(destination) > 100:
        errors.append("Destination must be no more than 100 characters long")
    
    # Must contain at least one letter
    if not re.search(r'[a-zA-Z]', destination):
        errors.append("Destination must contain at least one letter")
    
    # Valid characters: letters, numbers, spaces, commas, periods, hyphens, apostrophes
    if not re.match("^[a-zA-Z0-9\s,.\-']+$", destination):
        errors.append("Destination contains invalid characters")
    
    return errors

def validate_password(password):
    """Validate password strength"""
    errors = []
    
    if not password:
        errors.append("Password is required")
        return errors
    
    # Length validation
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long")
    if len(password) > 128:
        errors.append("Password must be no more than 128 characters long")
    
    # Strength validation
    if not re.search(r'[a-z]', password):
        errors.append("Password must contain at least one lowercase letter")
    if not re.search(r'[A-Z]', password):
        errors.append("Password must contain at least one uppercase letter")
    if not re.search(r'\d', password):
        errors.append("Password must contain at least one number")
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors.append("Password must contain at least one special character")
    
    # Common password check
    common_passwords = [
        'password', '12345678', 'qwerty', 'abc123', 'password123',
        'admin', 'letmein', 'welcome', 'monkey', '1234567890'
    ]
    if password.lower() in common_passwords:
        errors.append("Password is too common, please choose a stronger password")
    
    return errors

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ========================================
# DATABASE MODELS
# ========================================

# Simple User Model (start basic, then enhance later)
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    bio = db.Column(db.Text)
    travel_interests = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class TravelGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    destination = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    max_members = db.Column(db.Integer, default=10)
    budget_min = db.Column(db.Float)
    budget_max = db.Column(db.Float)
    interests = db.Column(db.Text)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

class GroupMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('travel_group.id'), nullable=False)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='approved')
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('travel_group.id'), nullable=True)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_messages')
    recipient = db.relationship('User', foreign_keys=[recipient_id], backref='received_messages')
    group = db.relationship('TravelGroup', backref='messages')

# ========================================
# HELPER FUNCTIONS
# ========================================

def get_group_creator(group):
    """Safely get group creator"""
    try:
        return User.query.get(group.creator_id)
    except:
        return None

def get_group_members(group_id):
    """Safely get group members"""
    try:
        member_records = GroupMember.query.filter_by(group_id=group_id, status='approved').all()
        members = []
        for record in member_records:
            user = User.query.get(record.user_id)
            if user:
                members.append(user)
        return members
    except:
        return []

def get_member_count(group_id):
    """Safely get member count"""
    try:
        return GroupMember.query.filter_by(group_id=group_id, status='approved').count()
    except:
        return 0
    
def get_groups_by_destination(destination, exclude_group_id=None):
    """Get other groups that visited the same destination"""
    try:
        query = TravelGroup.query.filter_by(destination=destination, is_active=True)
        if exclude_group_id:
            query = query.filter(TravelGroup.id != exclude_group_id)
        
        groups = query.order_by(TravelGroup.created_at.desc()).limit(5).all()
        
        # Add member counts and creator info
        for group in groups:
            group.creator = get_group_creator(group)
            group.member_count = get_member_count(group.id)
            
        return groups
    except:
        return []

def get_popular_destinations():
    """Get most popular destinations"""
    try:
        # Query to count groups per destination
        from sqlalchemy import func
        destinations = db.session.query(
            TravelGroup.destination,
            func.count(TravelGroup.id).label('group_count')
        ).filter_by(is_active=True).group_by(TravelGroup.destination).order_by(
            func.count(TravelGroup.id).desc()
        ).limit(10).all()
        
        return destinations
    except:
        return []
    


# ========================================
# API ROUTES FOR VALIDATION
# ========================================

@app.route('/api/validate/username', methods=['POST'])
def validate_username_api():
    """API endpoint to validate username in real-time"""
    data = request.get_json()
    username = data.get('username', '')
    
    errors = validate_username(username)
    
    # Check if username already exists
    if not errors and User.query.filter_by(username=username).first():
        errors.append("Username is already taken")
    
    return jsonify({
        'valid': len(errors) == 0,
        'errors': errors
    })

@app.route('/api/validate/email', methods=['POST'])
def validate_email_api():
    """API endpoint to validate email availability"""
    data = request.get_json()
    email = data.get('email', '')
    
    errors = []
    
    # Basic email format validation
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        errors.append("Please enter a valid email address")
    
    # Check if email already exists
    if not errors and User.query.filter_by(email=email).first():
        errors.append("Email is already registered")
    
    return jsonify({
        'valid': len(errors) == 0,
        'errors': errors
    })

# ========================================
# ROUTES
# ========================================

@app.route('/')
def index():
    try:
        # Get recent groups
        groups = TravelGroup.query.order_by(TravelGroup.created_at.desc()).limit(6).all()
        
        # Add safe data to each group
        for group in groups:
            group.creator = get_group_creator(group)
            group.member_count = get_member_count(group.id)
        
        return render_template('index.html', groups=groups)
    except Exception as e:
        print(f"Error in index route: {e}")
        return render_template('index.html', groups=[])

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            username = request.form['username'].strip()
            email = request.form['email'].strip()
            password = request.form['password']
            confirm_password = request.form['confirm_password']
            first_name = request.form['first_name'].strip()
            last_name = request.form['last_name'].strip()
            
            # Validate all fields
            all_errors = []
            
            # Username validation
            username_errors = validate_username(username)
            if username_errors:
                all_errors.extend([f"Username: {error}" for error in username_errors])
            
            # Check if username exists
            if not username_errors and User.query.filter_by(username=username).first():
                all_errors.append("Username: Username is already taken")
            
            # Email validation
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, email):
                all_errors.append("Email: Please enter a valid email address")
            elif User.query.filter_by(email=email).first():
                all_errors.append("Email: Email is already registered")
            
            # Name validation
            first_name_errors = validate_name(first_name, "First name")
            if first_name_errors:
                all_errors.extend(first_name_errors)
            
            last_name_errors = validate_name(last_name, "Last name")
            if last_name_errors:
                all_errors.extend(last_name_errors)
            
            # Password validation
            password_errors = validate_password(password)
            if password_errors:
                all_errors.extend([f"Password: {error}" for error in password_errors])
            
            # Confirm password
            if password != confirm_password:
                all_errors.append("Passwords do not match")
            
            # If there are validation errors, show them
            if all_errors:
                for error in all_errors:
                    flash(error, 'error')
                return redirect(url_for('register'))
            
            # Create new user with cleaned data
            user = User(
                username=username,
                email=email.lower(),
                first_name=first_name.title(),  # Capitalize first letter
                last_name=last_name.title()     # Capitalize first letter
            )
            user.set_password(password)
            
            db.session.add(user)
            db.session.commit()
            
            flash('Registration successful! Please sign in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            print(f"Error in register: {e}")
            flash('Registration failed. Please try again.', 'error')
            return redirect(url_for('register'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            username = request.form['username'].strip()
            password = request.form['password']
            
            if not username or not password:
                flash('Please enter both username and password', 'error')
                return redirect(url_for('login'))
            
            user = User.query.filter_by(username=username).first()
            
            if user and user.check_password(password):
                login_user(user)
                flash(f'Welcome back, {user.first_name}!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid username or password', 'error')
        except Exception as e:
            print(f"Error in login: {e}")
            flash('Login failed. Please try again.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    try:
        # Get user's created groups - Fixed query
        user_groups = TravelGroup.query.filter_by(creator_id=current_user.id, is_active=True).all()
        
        # Get joined groups safely
        joined_groups = []
        member_records = GroupMember.query.filter_by(user_id=current_user.id, status='approved').all()
        for record in member_records:
            group = TravelGroup.query.filter_by(id=record.group_id, is_active=True).first()
            if group and group.creator_id != current_user.id:  # Don't include own groups
                joined_groups.append(group)
        
        # Add member counts and creator info
        for group in user_groups + joined_groups:
            group.member_count = get_member_count(group.id)
            group.creator = get_group_creator(group)
        
        print(f"DEBUG: User {current_user.id} created groups: {len(user_groups)}")  # Debug line
        print(f"DEBUG: User groups: {[g.title for g in user_groups]}")  # Debug line
        
        return render_template('dashboard.html', user_groups=user_groups, joined_groups=joined_groups)
    except Exception as e:
        print(f"Error in dashboard: {e}")
        return render_template('dashboard.html', user_groups=[], joined_groups=[])
@app.route('/create_group', methods=['GET', 'POST'])
@login_required
def create_group():
    if request.method == 'POST':
        try:
            title = request.form['title'].strip()
            description = request.form['description'].strip()
            destination = request.form['destination'].strip()
            interests = request.form['interests'].strip()
            
            # Validate all fields
            all_errors = []
            
            # Title validation
            title_errors = validate_group_title(title)
            if title_errors:
                all_errors.extend([f"Title: {error}" for error in title_errors])
            
            # Destination validation
            destination_errors = validate_destination(destination)
            if destination_errors:
                all_errors.extend([f"Destination: {error}" for error in destination_errors])
            
            # Description validation
            if not description or len(description.strip()) < 10:
                all_errors.append("Description: Must be at least 10 characters long")
            elif len(description) > 2000:
                all_errors.append("Description: Must be no more than 2000 characters long")
            
            # Date validation
            try:
                start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
                end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d').date()
                
                if start_date < date.today():
                    all_errors.append("Start date cannot be in the past")
                if end_date < start_date:
                    all_errors.append("End date must be after start date")
                if (end_date - start_date).days > 365:
                    all_errors.append("Trip duration cannot exceed 365 days")
            except ValueError:
                all_errors.append("Invalid date format")
                start_date = end_date = None
            
            # Budget validation
            budget_min = request.form.get('budget_min')
            budget_max = request.form.get('budget_max')
            
            if budget_min:
                try:
                    budget_min = float(budget_min)
                    if budget_min < 0:
                        all_errors.append("Minimum budget cannot be negative")
                    elif budget_min > 100000:
                        all_errors.append("Minimum budget seems unreasonably high")
                except ValueError:
                    all_errors.append("Invalid minimum budget format")
                    budget_min = None
            else:
                budget_min = None
            
            if budget_max:
                try:
                    budget_max = float(budget_max)
                    if budget_max < 0:
                        all_errors.append("Maximum budget cannot be negative")
                    elif budget_max > 100000:
                        all_errors.append("Maximum budget seems unreasonably high")
                    elif budget_min and budget_max < budget_min:
                        all_errors.append("Maximum budget must be greater than minimum budget")
                except ValueError:
                    all_errors.append("Invalid maximum budget format")
                    budget_max = None
            else:
                budget_max = None
            
            # Max members validation
            try:
                max_members = int(request.form['max_members'])
                if max_members < 2:
                    all_errors.append("Group must allow at least 2 members")
                elif max_members > 50:
                    all_errors.append("Group cannot have more than 50 members")
            except ValueError:
                all_errors.append("Invalid maximum members value")
                max_members = None
            
            # If there are validation errors, show them
            if all_errors:
                for error in all_errors:
                    flash(error, 'error')
                return redirect(url_for('create_group'))
            
            # Create group with validated data
            group = TravelGroup(
                title=title,
                description=description,
                destination=destination,
                start_date=start_date,
                end_date=end_date,
                max_members=max_members,
                budget_min=budget_min,
                budget_max=budget_max,
                interests=interests if interests else None,
                creator_id=current_user.id
            )
            
            db.session.add(group)
            db.session.commit()
            
            flash('Travel group created successfully!', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            print(f"Error creating group: {e}")
            flash('Failed to create group. Please try again.', 'error')
    
    return render_template('create_group.html')

@app.route('/groups')
def browse_groups():
    try:
        groups = TravelGroup.query.order_by(TravelGroup.created_at.desc()).all()
        
        # Add safe data to each group
        for group in groups:
            group.creator = get_group_creator(group)
            group.member_count = get_member_count(group.id)
        
        return render_template('browse_groups.html', groups=groups)
    except Exception as e:
        print(f"Error in browse_groups: {e}")
        return render_template('browse_groups.html', groups=[])

@app.route('/group/<int:group_id>')
def view_group(group_id):
    try:
        group = TravelGroup.query.get_or_404(group_id)
        
        # Get data safely
        group.creator = get_group_creator(group)
        members = get_group_members(group_id)
        
        # Get other groups that visited same destination
        similar_groups = get_groups_by_destination(group.destination, exclude_group_id=group_id)
        
        is_member = False
        if current_user.is_authenticated:
            is_member = GroupMember.query.filter_by(
                user_id=current_user.id,
                group_id=group_id
            ).first() is not None
        
        return render_template('view_group.html', 
                             group=group, 
                             members=members, 
                             is_member=is_member,
                             similar_groups=similar_groups)
    except Exception as e:
        print(f"Error in view_group: {e}")
        return f"Error loading group: {e}", 500

@app.route('/join_group/<int:group_id>')
@login_required
def join_group(group_id):
    try:
        group = TravelGroup.query.get_or_404(group_id)
        
        # Check if already a member
        existing_member = GroupMember.query.filter_by(
            user_id=current_user.id,
            group_id=group_id
        ).first()
        
        if existing_member:
            flash('You are already a member of this group', 'info')
        else:
            # Check if group is full
            current_member_count = get_member_count(group_id)
            if current_member_count >= group.max_members:
                flash('This group is full and cannot accept new members', 'error')
            else:
                member = GroupMember(
                    user_id=current_user.id,
                    group_id=group_id,
                    status='approved'
                )
                db.session.add(member)
                db.session.commit()
                flash('Successfully joined the group!', 'success')
        
        return redirect(url_for('view_group', group_id=group_id))


    except Exception as e:
        print(f"Error joining group: {e}")
        flash('Failed to join group. Please try again.', 'error')
        return redirect(url_for('browse_groups'))
@app.route('/edit_group/<int:group_id>', methods=['GET', 'POST'])
@login_required
def edit_group(group_id):
    group = TravelGroup.query.get_or_404(group_id)
    
    # Only creator can edit
    if group.creator_id != current_user.id:
        flash('You can only edit groups you created', 'error')
        return redirect(url_for('view_group', group_id=group_id))
    
    if request.method == 'POST':
        try:
            title = request.form['title'].strip()
            description = request.form['description'].strip()
            destination = request.form['destination'].strip()
            interests = request.form['interests'].strip()
            
            # Validate all fields (same as create_group)
            all_errors = []
            
            # Title validation
            title_errors = validate_group_title(title)
            if title_errors:
                all_errors.extend([f"Title: {error}" for error in title_errors])
            
            # Destination validation
            destination_errors = validate_destination(destination)
            if destination_errors:
                all_errors.extend([f"Destination: {error}" for error in destination_errors])
            
            # Description validation
            if not description or len(description.strip()) < 10:
                all_errors.append("Description: Must be at least 10 characters long")
            elif len(description) > 2000:
                all_errors.append("Description: Must be no more than 2000 characters long")
            
            # Date validation
            try:
                start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
                end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d').date()
                
                if start_date < date.today():
                    all_errors.append("Start date cannot be in the past")
                if end_date < start_date:
                    all_errors.append("End date must be after start date")
                if (end_date - start_date).days > 365:
                    all_errors.append("Trip duration cannot exceed 365 days")
            except ValueError:
                all_errors.append("Invalid date format")
                start_date = end_date = None
            
            # Budget validation
            budget_min = request.form.get('budget_min')
            budget_max = request.form.get('budget_max')
            
            if budget_min:
                try:
                    budget_min = float(budget_min)
                    if budget_min < 0:
                        all_errors.append("Minimum budget cannot be negative")
                    elif budget_min > 100000:
                        all_errors.append("Minimum budget seems unreasonably high")
                except ValueError:
                    all_errors.append("Invalid minimum budget format")
                    budget_min = None
            else:
                budget_min = None
            
            if budget_max:
                try:
                    budget_max = float(budget_max)
                    if budget_max < 0:
                        all_errors.append("Maximum budget cannot be negative")
                    elif budget_max > 100000:
                        all_errors.append("Maximum budget seems unreasonably high")
                    elif budget_min and budget_max < budget_min:
                        all_errors.append("Maximum budget must be greater than minimum budget")
                except ValueError:
                    all_errors.append("Invalid maximum budget format")
                    budget_max = None
            else:
                budget_max = None
            
            # Max members validation
            try:
                max_members = int(request.form['max_members'])
                current_member_count = get_member_count(group_id)
                
                if max_members < 2:
                    all_errors.append("Group must allow at least 2 members")
                elif max_members > 50:
                    all_errors.append("Group cannot have more than 50 members")
                elif max_members < current_member_count:
                    all_errors.append(f"Cannot reduce max members below current member count ({current_member_count})")
            except ValueError:
                all_errors.append("Invalid maximum members value")
                max_members = None
            
            # If there are validation errors, show them
            if all_errors:
                for error in all_errors:
                    flash(error, 'error')
                return redirect(url_for('edit_group', group_id=group_id))
            
            # Update group with validated data
            group.title = title
            group.description = description
            group.destination = destination
            group.start_date = start_date
            group.end_date = end_date
            group.max_members = max_members
            group.budget_min = budget_min
            group.budget_max = budget_max
            group.interests = interests if interests else None
            
            db.session.commit()
            flash('Group updated successfully!', 'success')
            return redirect(url_for('view_group', group_id=group_id))
        except Exception as e:
            print(f"Error updating group: {e}")
            flash('Failed to update group. Please try again.', 'error')
    
    return render_template('edit_group.html', group=group)
@app.route('/delete_group/<int:group_id>', methods=['POST'])
@login_required
def delete_group(group_id):
    group = TravelGroup.query.get_or_404(group_id)
    
    # Only creator can delete
    if group.creator_id != current_user.id:
        flash('You can only delete groups you created', 'error')
        return redirect(url_for('view_group', group_id=group_id))
    
    try:
        # Delete all group members first
        GroupMember.query.filter_by(group_id=group_id).delete()
        
        # Delete the group
        db.session.delete(group)
        db.session.commit()
        
        flash('Group deleted successfully', 'success')
        return redirect(url_for('dashboard'))
    except Exception as e:
        print(f"Error deleting group: {e}")
        flash('Failed to delete group. Please try again.', 'error')
        return redirect(url_for('view_group', group_id=group_id))
@app.route('/recommendations')
def recommendations():
    try:
        # Get popular destinations
        popular_destinations = get_popular_destinations()
        
        # Get recent groups
        recent_groups = TravelGroup.query.filter_by(is_active=True).order_by(
            TravelGroup.created_at.desc()
        ).limit(8).all()
        
        # Add member counts
        for group in recent_groups:
            group.creator = get_group_creator(group)
            group.member_count = get_member_count(group.id)
        
        return render_template('recommendations.html', 
                             popular_destinations=popular_destinations,
                             recent_groups=recent_groups)
    except Exception as e:
        print(f"Error in recommendations: {e}")
        return render_template('recommendations.html', 
                             popular_destinations=[],
                             recent_groups=[])
@app.route('/contact_creator/<int:group_id>', methods=['GET', 'POST'])
@login_required
def contact_creator(group_id):
    group = TravelGroup.query.get_or_404(group_id)
    
    # DEBUG: Print user info
    print(f"DEBUG: Current user ID: {current_user.id}")
    print(f"DEBUG: Group creator ID: {group.creator_id}")
    print(f"DEBUG: Group title: {group.title}")
    
    # Can't message yourself
    if group.creator_id == current_user.id:
        print("DEBUG: User trying to message themselves - blocking")
        flash('You cannot message yourself', 'error')
        return redirect(url_for('view_group', group_id=group_id))
    
    print("DEBUG: Different users - allowing message")
    
    if request.method == 'POST':
        try:
            subject = request.form['subject'].strip()
            message_text = request.form['message'].strip()
            
            if not subject or not message_text:
                flash('Please fill in all fields', 'error')
                return redirect(url_for('contact_creator', group_id=group_id))
            
            # Create message
            message = Message(
                sender_id=current_user.id,
                recipient_id=group.creator_id,
                group_id=group_id,
                subject=subject,
                message=message_text
            )
            
            db.session.add(message)
            db.session.commit()
            
            flash('Message sent successfully!', 'success')
            return redirect(url_for('view_group', group_id=group_id))
        except Exception as e:
            print(f"Error sending message: {e}")
            flash('Failed to send message. Please try again.', 'error')
    
    return render_template('contact_creator.html', group=group)

@app.route('/messages')
@login_required
def messages():
    # Get received messages
    received = Message.query.filter_by(recipient_id=current_user.id).order_by(Message.sent_at.desc()).all()
    
    # Get sent messages
    sent = Message.query.filter_by(sender_id=current_user.id).order_by(Message.sent_at.desc()).all()
    
    # Mark as read when viewing
    unread_messages = Message.query.filter_by(recipient_id=current_user.id, is_read=False).all()
    for msg in unread_messages:
        msg.is_read = True
    db.session.commit()
    
    return render_template('messages.html', received_messages=received, sent_messages=sent)
@app.route('/reply_message/<int:message_id>', methods=['GET', 'POST'])
@login_required
def reply_message(message_id):
    # Get the original message
    original_message = Message.query.get_or_404(message_id)
    
    # Only the recipient can reply
    if original_message.recipient_id != current_user.id:
        flash('You can only reply to messages sent to you', 'error')
        return redirect(url_for('messages'))
    
    if request.method == 'POST':
        try:
            subject = request.form['subject'].strip()
            message_text = request.form['message'].strip()
            
            if not subject or not message_text:
                flash('Please fill in all fields', 'error')
                return redirect(url_for('reply_message', message_id=message_id))
            
            # Create reply message
            reply = Message(
                sender_id=current_user.id,
                recipient_id=original_message.sender_id,  # Send back to original sender
                group_id=original_message.group_id,
                subject=subject,
                message=message_text
            )
            
            db.session.add(reply)
            db.session.commit()
            
            flash('Reply sent successfully!', 'success')
            return redirect(url_for('messages'))
        except Exception as e:
            print(f"Error sending reply: {e}")
            flash('Failed to send reply. Please try again.', 'error')
    
    return render_template('reply_message.html', original_message=original_message)

# ========================================
# MAIN APPLICATION
# ========================================

if __name__ == '__main__':
    with app.app_context():
        try:
            print("Creating database tables...")
            db.create_all()
            print("Database tables created successfully!")
        except Exception as e:
            print(f"Database error: {e}")
    

    app.run(debug=True)
