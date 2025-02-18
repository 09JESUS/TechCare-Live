import cohere
from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os

# Load environment variables from .env file


app = Flask(__name__)

# Initialize Cohere API client
co = cohere.Client('YNqxUzM0HSZSeuUojyV70RkbQPpneGGLJ2eQkFPU')  # Directly pass your API key
# Replace with your actual Cohere API key

# Load tickets from JSON
def load_tickets():
    try:
        with open('data/tickets.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Save tickets to JSON
def save_tickets(tickets):
    with open('data/tickets.json', 'w') as f:
        json.dump(tickets, f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        ticket = {
            "name": request.form['name'],
            "email": request.form['email'],
            "issue": request.form['issue']
        }
        tickets = load_tickets()
        tickets.append(ticket)
        save_tickets(tickets)
        return redirect(url_for('index'))
    return render_template('contact.html')

@app.route('/admin')
def admin():
    tickets = load_tickets()
    return render_template('admin.html', tickets=tickets)

@app.route('/generate', methods=['POST'])
def generate():
    user_input = request.form.get('user_input', '').strip()

    if not user_input:
        return jsonify({"response": "Please provide a message."})
    
    try:
        response = co.generate(
            model='command',  # Choose appropriate model
            prompt=user_input,
            max_tokens=200
        )
        bot_reply = response.generations[0].text.strip()
        
        if not bot_reply:
            return jsonify({"response": "Sorry, I couldn't generate a response. Please try again."})
        
    except Exception as e:
        bot_reply = f"Error fetching response: {str(e)}"

    return jsonify({"response": bot_reply})

#Add the testimonials 
# Simulated database
testimonials = []

@app.route("/submit-ticket", methods=["POST"])
def submit_ticket():
    data = request.json
    testimonials.append({
        "name": data["name"],
        "message": data["message"],
        "rating": int(data["rating"])
    })
    return jsonify({"message": "Feedback saved"}), 201

@app.route("/get-testimonials", methods=["GET"])
def get_testimonials():
    return jsonify(testimonials)

if __name__ == '__main__':
    app.run(debug=True)