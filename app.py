from flask import Flask, render_template, request, redirect, flash, jsonify, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date as dt
import os

# --- Ensure critical environment variables are set ---
if not os.environ.get('SECRET_KEY') or not os.environ.get('ADMIN_PASSWORD'):
    raise RuntimeError("SECRET_KEY and ADMIN_PASSWORD must be set as environment variables!")

# --- Flask app setup ---
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')  # required for flash messages and sessions

# Absolute path to your project directory
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'bookings.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ----- Models ----- 
class Booking(db.Model):
    __tablename__ = "bookings" # force the table name 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    service = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"<Booking {self.name} - {self.service} on {self.date} at {self.time}>"

# ----- Helper functions -----
def save_booking_to_db(name, service, date, time):
    # Attempt to save a booking to the database and return a success flag and message 
    new_booking = Booking(name=name, service=service, date=date, time=time)
    try:
        db.session.add(new_booking)
        db.session.commit()
        return True, "Cita creada con éxito!" 
    except Exception as e:
        db.session.rollback() # undo pending changes if error occurs
        return False, f"Error al crear la cita: {str(e)}" 
        
# ----- Helper function for form submissions -----
def handle_booking_submission(form):
    # handle form data validation and feedback message 
    name = request.form.get('name')
    service = request.form.get('service')
    date = request.form.get('date')
    time = request.form.get('time')

    # Validation
    if not name or not service or not date or not time:
        flash("Por favor completa todos los campos.", "error")
        return render_template('index.html', name=name, service=service, date=date, time=time) 

    # Prevent past dates 
    try: 
        selected_date = datetime.strptime(date, "%Y-%m-%d").date()
        if selected_date < dt.today():
            flash("No puedes seleccionar una fecha pasada.", "error")
            return render_template('index.html', name=name, service=service, date=date, time=time)

        # Only allow Monday-Friday 
        if selected_date.weekday() > 4: # 5 = Say, 6 = Sun
            flash("Solo se pueden agendar citas de Lunes a Viernes", "error")
            return render_template('index.html', name=name, service=service, date=date, time=time)
    except ValueError:
        flash("Fecha inválida.", "error")
        return render_template('index.html', name=name, service=service, date=date_str, time=time)

    # Double booking check 
    existing_booking = Booking.query.filter_by(date=date, time=time).first()
    if existing_booking:
        flash(f"Lo siento, {date} a las {time} ya está reservado.", "error")
        return render_template('index.html', name=name, service=service, date=date, time=time)

    # Save booking 
    success, message = save_booking_to_db(name, service, date, time)
    flash(message, "success" if success else "error")

    # return redirect or re-render form based on success
    if success:
        return redirect('/#booking') # <- scrolls to the booking section
    else:
        # Keep the form data so user can fix errors
        return render_template('index.html', name=name, service=service, date=date, time=time) 



# ----- Routes -----
@app.route('/', methods=['GET'])
def index():
    selected_date = request.args.get('date') 
    booked_times = []

    # Check if user selected a date (for GET requests w/ ?date=YYYY-MM-DD)
    
    if selected_date:
        booked_times = [b.time for b in Booking.query.filter_by(date=selected_date).all()]

    bookings_list = Booking.query.all()
    # Get request: render form 
    return render_template('index.html', booking=bookings_list, booked_times=booked_times, date=selected_date)

@app.route('/book', methods=['POST'])
def book():
    # Detect if it's a JS fetch request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        name = request.form.get('name')
        service = request.form.get('service')
        date = request.form.get('date')
        time = request.form.get('time')

        # Validation (reuse your existing logic quickly)
        if not name or not service or not date or not time:
            return jsonify({'status': 'error', 'message': 'Por favor completa todos los campos.'})

        selected_date = datetime.strptime(date, "%Y-%m-%d").date()
        if selected_date < dt.today():
            return jsonify({'status': 'error', 'message': 'No puedes seleccionar una fecha pasada.'})
        if selected_date.weekday() > 4:
            return jsonify({'status': 'error', 'message': 'Solo se pueden agendar citas de Lunes a Viernes.'})

        existing_booking = Booking.query.filter_by(date=date, time=time).first()
        if existing_booking:
            return jsonify({'status': 'error', 'message': f'Lo siento, {date} a las {time} ya está reservado.'})

        success, message = save_booking_to_db(name, service, date, time)
        return jsonify({'status': 'success' if success else 'error', 'message': message})

    # Fallback for normal form submission
    return handle_booking_submission(request.form)


# Optional: for admin viewing or debugging later 
@app.route('/bookings') # add table to present the bookings
def bookings():
    # Fetch all bookings for display (optional)
    all_bookings = Booking.query.all()

    # Format each booking's time for display (e.g., "9 AM" instead of "9:00")
    for b in all_bookings:
        try: 
            hour = int(b.time.split(":")[0]) # Extract hour part (e.g., "09" -> 9)
            if hour == 0:
                display = "12 AM"
            elif hour < 12:
                display = f"{hour} AM"
            elif hour == 12:
                display = "12 PM"
            else:
                display = f"{hour - 12} PM"
            b.time_display = display
        except Exception:
            b.time_display = b.time # fallback in case of format error  

    return render_template('bookings.html', bookings=all_bookings)

@app.route('/available-times')
def available_times():
    date = request.args.get('date')
    all_hours = [f"{hour:02d}:00" for hour in range(9,18)] # 9AM-5PM
    booked = [b.time for b in Booking.query.filter_by(date=date).all()]
    available = [t for t in all_hours if t not in booked]
    return jsonify(available)

@app.route('/delete/<int:booking_id>', methods=['POST'])
def delete_booking(booking_id):

    if not session.get('is_admin'):
        abort(403) # Forbidden


    booking = Booking.query.get_or_404(booking_id)

    try:
        db.session.delete(booking)
        db.session.commit()
        flash("Cita eliminada exitosamente.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al eliminar la cita: {str(e)}", "error")

    return redirect(url_for('bookings'))

@app.route('/update/<int:booking_id>', methods=['GET', 'POST'])
def update_booking(booking_id):

    if not session.get('is_admin'):
        abort(403)

    # fetch booking or 404
    booking = Booking.query.get_or_404(booking_id)

    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        service = request.form.get('service')
        date_str = request.form.get('date')
        time = request.form.get('time')

        # Basic validation
        if not name or not service or not date_str or not time:
            flash("Por favor completa todos los campos.", "error")
            return render_template('update_booking.html', booking=booking)

        # Prevent past dates
        try:
            selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            if selected_date < dt.today():
                flash("No puedes seleccionar una fecha pasada.", "error")
                return render_template('update_booking.html', booking=booking)
        except ValueError:
            flash("Fecha inválida.", "error")
            return render_template('update_booking.html', booking=booking)
        
        # Prevent double bookings (ignore current booking)
        existing = Booking.query.filter_by(date=date_str, time=time).filter(Booking.id != booking_id).first()
        if existing:
            flash(f"Lo siento, {date_str} a las {time} ya está reservado.", "error")
            return render_template('update_booking.html', booking=booking)
        
        # Update booking 
        booking.name = name
        booking.service = service
        booking.date = date_str
        booking.time = time 
        db.session.commit()

        return redirect('/bookings')

    # GET request: render pre-filled form 
    return render_template('update_booking.html', booking=booking)

# --- Admin login --- 
@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form.get('password')  # fix typo
        if password == os.environ.get('ADMIN_PASSWORD'):
            session['is_admin'] = True
            return redirect(url_for('bookings'))  # redirect works now
        else:
            flash("Contraseña incorrecta.", "error")
            return render_template('admin_login.html')  # add return

    return render_template('admin_login.html')


@app.route('/admin-logout')
def admin_logout():
    session.pop('is_admin', None)
    flash("Se cerró sesión exitosamente.", "success")
    return redirect(url_for('index'))

# ----- Create tables and run app -----
if __name__ == "__main__":
    # Create tables inside the app context 
    with app.app_context():
        db.create_all()

    # only used if you run `python3 app.py`
    app.run(debug=False) # True for testing / False for deployment  

''' 
TODO: 
- Future: Make a column to table in DB where it shows a booking was completed (Give it green color once completed, perhaps green check mark?)
- Add a products section where customers can see products sold at SPA 
- make a link when you click a service in services section 
- when a successful booking, don't go to top to scroll down
'''