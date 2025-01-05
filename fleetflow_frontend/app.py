from flask import Flask, render_template, url_for, request, redirect, flash, session as flask_session
import requests, logging

app = Flask(__name__)
API_URL = 'http://127.0.0.1:3000'
app.secret_key = "fleetflow"

@app.route('/')
def landing_page():
    return render_template('landing_page.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        #request the information from the html template
        username = request.form.get('usr')
        email = request.form.get('email')
        password = request.form.get('pwd')

        # store the information in a python dictionary
        signup_data = {
            "username": username,
            "email": email,
            "password": password
        }

        # send the post request to the backend
        try:
            signup_response = requests.post(f"{API_URL}/signup", signup_data)
        except Exception as e:
            logging.error(f"Signup post request fail: {e}")

        if signup_response.status_code == 200:
            return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username_email = request.form.get('usr_email')
        password = request.form.get('pwd')

        login_data = {
            "username": username_email,
            "email": username_email,
            "password": password
        }

        #request session from the backend
        session = requests.Session()
        # use the session to perform the post method
        login_response = session.post(f"{API_URL}/login", data=login_data)

        # login_response = requests.post(f"{API_URL}/login", data=login_data, headers={'Content-Type': 'application/x-www-form-urlencoded'})


        if login_response.status_code == 200:
            #store the session in the cookies
            flask_session['cookies'] = session.cookies.get_dict()
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid Login Details")
            return redirect(url_for('login'))
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    cookies = flask_session.get('cookies', {})
    with requests.Session() as session:
        session.cookies.update(cookies)
        logout_response = session.get(f"{API_URL}/logout")

    if logout_response.status_code == 200:
        flask_session.clear()
        flash("Logged Out Successfully")
        return redirect(url_for('login'))
    else:
        return ("Error occured while logging out")



@app.route('/dashboard')
def dashboard():
    cookies = flask_session.get('cookies', {})
    with requests.Session() as session:
        session.cookies.update(cookies)
        dashboard_request = session.get(f"{API_URL}/dashboard")

    if dashboard_request.status_code == 200:
        return render_template('dashboard.html')
    else:
        flash("You must Login in before Accessing this page")
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=5000, debug=True)