from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os
import uuid
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cmk-construction-secret-2026'

# ============================================
# SERVICES - UPDATED COLORS
# ============================================
SERVICES = [
    {
        'id': 'kitchen_remodeling',
        'name': 'Kitchen Remodeling',
        'icon': 'fa-kitchen-set',
        'description': 'Transform your kitchen into a beautiful, functional space with custom cabinetry, countertops, and modern appliances.',
        'image': 'https://images.unsplash.com/photo-1556911220-bff31c812dba?w=600&h=400&fit=crop',
        'features': ['Custom Cabinetry', 'Granite Countertops', 'Modern Appliances', 'Lighting Design']
    },
    {
        'id': 'bathroom_remodeling',
        'name': 'Bathroom Remodeling',
        'icon': 'fa-bath',
        'description': 'Create a spa-like retreat with luxurious fixtures, custom tile work, and elegant vanities.',
        'image': 'https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=600&h=400&fit=crop',
        'features': ['Custom Tile Work', 'Luxury Fixtures', 'Walk-in Showers', 'Heated Floors']
    },
    {
        'id': 'home_additions',
        'name': 'Home Additions',
        'icon': 'fa-house-circle-check',
        'description': 'Expand your living space with custom room additions, second stories, and garage conversions.',
        'image': 'https://images.unsplash.com/photo-1570129477492-45c003edd2be?w=600&h=400&fit=crop',
        'features': ['Room Additions', 'Second Stories', 'Garage Conversions', 'Sunrooms']
    },
    {
        'id': 'flooring',
        'name': 'Flooring Installation',
        'icon': 'fa-layer-group',
        'description': 'Expert flooring installation with hardwood, tile, carpet, and luxury vinyl options.',
        'image': 'https://images.unsplash.com/photo-1581858726788-75bc0f6a952d?w=600&h=400&fit=crop',
        'features': ['Hardwood Flooring', 'Tile Installation', 'Carpet', 'Luxury Vinyl']
    },
    {
        'id': 'painting',
        'name': 'Interior & Exterior Painting',
        'icon': 'fa-paint-roller',
        'description': 'Professional painting services to refresh your home\'s interior and exterior.',
        'image': 'https://images.unsplash.com/photo-1589939705384-5185137a7f0f?w=600&h=400&fit=crop',
        'features': ['Interior Painting', 'Exterior Painting', 'Cabinet Refinishing', 'Wallpaper Removal']
    },
    {
        'id': 'deck_building',
        'name': 'Deck & Patio Building',
        'icon': 'fa-tree',
        'description': 'Create stunning outdoor living spaces with custom decks, patios, and outdoor kitchens.',
        'image': 'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=600&h=400&fit=crop',
        'features': ['Custom Decks', 'Patio Design', 'Outdoor Kitchens', 'Fire Pits']
    }
]

# ============================================
# PROJECTS - ROOFING REMOVED
# ============================================
PROJECTS = [
    {
        'id': 'project1',
        'title': 'Modern Kitchen Remodel',
        'category': 'Kitchen',
        'image': 'https://images.unsplash.com/photo-1556911220-bff31c812dba?w=600&h=400&fit=crop',
        'description': 'Complete kitchen transformation with custom cabinetry and granite countertops.'
    },
    {
        'id': 'project2',
        'title': 'Luxury Bathroom Renovation',
        'category': 'Bathroom',
        'image': 'https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=600&h=400&fit=crop',
        'description': 'Spa-inspired bathroom with walk-in shower and freestanding tub.'
    },
    {
        'id': 'project3',
        'title': 'Two-Story Home Addition',
        'category': 'Addition',
        'image': 'https://images.unsplash.com/photo-1570129477492-45c003edd2be?w=600&h=400&fit=crop',
        'description': 'Full second-story addition with master suite and home office.'
    },
    {
        'id': 'project4',
        'title': 'Outdoor Living & Deck',
        'category': 'Outdoor',
        'image': 'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=600&h=400&fit=crop',
        'description': 'Custom deck and outdoor kitchen for entertaining.'
    },
    {
        'id': 'project5',
        'title': 'Full Home Renovation',
        'category': 'Renovation',
        'image': 'https://images.unsplash.com/photo-1580587771525-78b9dba3b914?w=600&h=400&fit=crop',
        'description': 'Complete home renovation with modern finishes and open floor plan.'
    },
    {
        'id': 'project6',
        'title': 'Hardwood Flooring Installation',
        'category': 'Flooring',
        'image': 'https://images.unsplash.com/photo-1581858726788-75bc0f6a952d?w=600&h=400&fit=crop',
        'description': 'Premium hardwood flooring installation throughout the home.'
    }
]

# ============================================
# TESTIMONIALS
# ============================================
TESTIMONIALS = [
    {
        'name': 'Sarah Johnson',
        'location': 'Sarasota, FL',
        'rating': 5,
        'text': 'CMK Construction completely transformed our kitchen! The team was professional, on time, and the quality of work exceeded our expectations.',
        'project': 'Kitchen Remodel'
    },
    {
        'name': 'Michael Roberts',
        'location': 'Bradenton, FL',
        'rating': 5,
        'text': 'We hired CMK for a bathroom renovation and couldn\'t be happier. They listened to our vision and brought it to life beautifully.',
        'project': 'Bathroom Remodel'
    },
    {
        'name': 'Jennifer Williams',
        'location': 'Lakewood Ranch, FL',
        'rating': 5,
        'text': 'The team at CMK Construction did an amazing job on our home addition. Professional, reliable, and the craftsmanship is top-notch.',
        'project': 'Home Addition'
    }
]

# ============================================
# ROUTES
# ============================================

@app.route('/')
def index():
    return render_template('construction.html', 
        services=SERVICES, 
        projects=PROJECTS,
        testimonials=TESTIMONIALS
    )

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name', '')
        email = request.form.get('email', '')
        phone = request.form.get('phone', '')
        message = request.form.get('message', '')
        
        return render_template('contact.html', 
            success=True, 
            name=name,
            message='Thank you for contacting CMK Construction! We will respond within 24 hours.'
        )
    
    return render_template('contact.html', success=False)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
