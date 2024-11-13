from flask import Flask, render_template, request, jsonify

# Create an instance of the Flask class
app = Flask(__name__)

# Define a basic route
@app.route('/')
def home():
    return render_template('index.html')

# Define another route with dynamic content
@app.route('/greet/<name>')
def greet(name):
    return f"Hello, {name}!"

# Define an API endpoint that returns JSON
@app.route('/api/data')
def get_data():
    data = {"message": "Hello from Flask API!", "status": "success"}
    return jsonify(data)

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80,debug=True)
