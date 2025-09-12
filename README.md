# ✈️ Travel Together

A social travel platform that connects like-minded travelers with shared interests, making solo travel safer and more enjoyable by finding compatible travel companions.

## 🌟 Features

- **👥 Find Travel Companions** - Connect with travelers who share your interests and travel style
- **🗺️ Group Travel Planning** - Create and join travel groups for specific destinations
- **💬 Real-time Messaging** - Chat with potential travel buddies before your trip
- **📍 Destination Discovery** - Browse and recommend amazing travel destinations
- **👤 Personal Profiles** - Showcase your travel preferences, interests, and experience
- **🔐 Safe & Secure** - Verified user profiles and secure messaging system
- **📱 Responsive Design** - Works seamlessly on desktop, tablet, and mobile devices
- **🎯 Interest Matching** - Advanced algorithm to match travelers based on preferences

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- pip (Python package manager)
- Web browser (Chrome, Firefox, Safari, Edge)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/martyns254/travel_together.git
   cd travel_together
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Create .env file
   cp .env.example .env
   
   # Edit .env with your configuration
   SECRET_KEY=your_secret_key_here
   DATABASE_URL=sqlite:///travel_together.db
   ```

5. **Initialize database**
   ```bash
   python config.py
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Open in browser**
   Navigate to `http://localhost:5000`

## 📁 Project Structure

```
travel_together/
├── __pycache__/               # Python cache files
├── static/                    # Static assets (CSS, JS, images)
├── templates/
│   ├── base.html              # Base template
│   ├── index.html             # Landing page
│   ├── login.html             # User authentication
│   ├── register.html          # User registration
│   ├── dashboard.html         # User dashboard
│   ├── profile.html           # User profiles
│   ├── edit_profile.html      # Profile editing
│   ├── create_group.html      # Create travel groups
│   ├── edit_group.html        # Edit travel groups
│   ├── browse_groups.html     # Browse available groups
│   ├── view_group.html        # View group details
│   ├── messages.html          # Messaging system
│   ├── reply_message.html     # Message replies
│   ├── contact_creator.html   # Contact group creators
│   └── recommendations.html   # Travel recommendations
├── .env                       # Environment variables
├── app.py                     # Main Flask application
├── config.py                  # Database configuration
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```

## 🎮 How It Works

### For Travelers

1. **Create Your Profile**
   - Sign up and complete your travel profile
   - Add your interests, travel style, and preferences
   - Upload photos and write about yourself

2. **Discover Travel Groups**
   - Browse existing travel groups by destination
   - Filter by dates, interests, and group size
   - Read group descriptions and member profiles

3. **Connect & Chat**
   - Join groups that match your interests
   - Message other travelers directly
   - Plan activities and coordinate travel details

4. **Create Your Own Group**
   - Start a new travel group for your dream destination
   - Set group preferences and requirements
   - Invite like-minded travelers to join

### For Group Creators

- **Manage Groups** - Edit group details, manage members
- **Screen Members** - Review and approve join requests
- **Coordinate Plans** - Organize activities and logistics
- **Share Recommendations** - Suggest places and experiences

## 🛠️ Key Features Deep Dive

### Smart Matching Algorithm
Our platform uses intelligent matching based on:
- Travel interests and hobbies
- Preferred travel style (adventure, relaxation, culture)
- Budget range and accommodation preferences
- Age group and travel experience level

### Safety Features
- **Profile Verification** - Email verification required
- **Secure Messaging** - End-to-end encrypted communications
- **User Reporting** - Report inappropriate behavior
- **Privacy Controls** - Control who can see your information

### Group Management
- **Flexible Group Sizes** - From 2 to 20+ travelers
- **Date Coordination** - Built-in calendar integration
- **Expense Sharing** - Track and split group expenses
- **Itinerary Planning** - Collaborative trip planning tools

## 🔧 Technical Details

- **Backend**: Python 3.7+ with Flask framework
- **Frontend**: HTML5 (73.1%), CSS (2.9%), JavaScript (5.1%)
- **Database**: SQLAlchemy with SQLite/PostgreSQL support
- **Authentication**: Flask-Login with session management
- **Forms**: Flask-WTF for secure form handling
- **Messaging**: Real-time chat system
- **File Upload**: Profile photos and group images
- **Responsive Design**: Mobile-first approach
- **Security**: CSRF protection, secure password hashing

## 🌍 Use Cases

- **Solo Travelers** seeking companions for safety and shared experiences
- **Adventure Seekers** looking for thrill-seeking travel buddies
- **Cultural Enthusiasts** wanting to explore heritage sites together
- **Budget Travelers** sharing costs and accommodations
- **Digital Nomads** coordinating workations and co-living
- **Students** organizing affordable group trips
- **Seniors** finding age-appropriate travel companions

## 🤝 Contributing

I welcome contributions from travel enthusiasts and developers!

### Development Setup

1. **Fork the repository**
2. **Set up development environment**
   ```bash
   git clone https://github.com/yourusername/travel_together.git
   cd travel_together
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

3. **Create feature branch**
   ```bash
   git checkout -b feature/amazing-new-feature
   ```

4. **Make your changes**
5. **Test thoroughly**
   ```bash
   python -m pytest tests/
   ```

6. **Submit pull request**

### Development Guidelines
- Follow PEP 8 for Python code style
- Use semantic HTML and accessible design
- Write comprehensive tests for new features
- Follow Flask best practices
- Ensure mobile responsiveness
- Maintain user privacy and security standards

## 📱 API Endpoints

```
Authentication:
POST /register        - User registration
POST /login          - User login
GET  /logout         - User logout

User Management:
GET  /profile        - View user profile
POST /edit_profile   - Update profile
GET  /dashboard      - User dashboard

Groups:
GET  /browse_groups  - Browse all groups
POST /create_group   - Create new group
GET  /view_group/<id> - View group details
POST /join_group     - Join a group
POST /edit_group     - Edit group (creator only)

Messaging:
GET  /messages       - View messages
POST /reply_message  - Send message reply
POST /contact_creator - Contact group creator

Recommendations:
GET  /recommendations - Get travel recommendations
```

## 🔒 Privacy & Security

- **Data Protection** - GDPR compliant data handling
- **Secure Authentication** - Bcrypt password hashing
- **Session Security** - Secure session management
- **Input Validation** - Comprehensive form validation
- **XSS Protection** - Cross-site scripting prevention
- **CSRF Protection** - Cross-site request forgery prevention

## 🚀 Roadmap

### Phase 1 (Current)
- [x] User registration and profiles
- [x] Group creation and browsing
- [x] Basic messaging system
- [x] Responsive design

### Phase 2 (Coming Soon)
- [ ] Advanced matching algorithms
- [ ] Video chat integration
- [ ] Mobile app (React Native)
- [ ] Payment integration for group expenses
- [ ] Travel insurance partnerships

### Phase 3 (Future)
- [ ] AI-powered trip recommendations
- [ ] Integration with booking platforms
- [ ] Multi-language support
- [ ] Social media integration
- [ ] Travel journal features

## 📊 Technologies Used

- **Flask** - Lightweight Python web framework
- **SQLAlchemy** - Database ORM
- **Jinja2** - Template engine
- **WTForms** - Form handling and validation
- **Bootstrap** - Responsive CSS framework
- **jQuery** - JavaScript functionality
- **SQLite/PostgreSQL** - Database options



## 🆘 Support

Need help or have questions?

- **Documentation**: Check this README and inline code comments
- **Issues**: Report bugs on GitHub Issues
- **Feature Requests**: Use GitHub Discussions
- **Security**: Email martinmaraba5@gmail.com for security concerns

## 🙏 Acknowledgments

- Thanks to all travelers who believe in the power of shared adventures
- Inspired by the need for safer, more connected travel experiences
- Built with passion for the global travel community

---

**Start your next adventure with Travel Together - Because the best journeys are shared! ✈️🌍**

For more information, visit my [GitHub repository](https://github.com/martyns254/travel_together)
