# Import necessary modules
from flask import Flask, request, jsonify, render_template_string
import os
import psycopg2

# Initialize Flask app
app = Flask(__name__)

# Database connection setup
DATABASE_URL = (
    f"dbname='{os.getenv('DB_NAME', 'ravuladb')}' "
    f"user='{os.getenv('DB_USER', 'ravula')}' "
    f"password='{os.getenv('DB_PASSWORD', 'ravula1')}' "
    f"host='{os.getenv('DB_HOST', '34.16.22.103')}'"
)

# Function to establish database connection
def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn


# Create a new record in the database
@app.route('/create-record', methods=['POST'])
def create_record():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Get data from request
    data = request.form
    # Insert data into database
    cursor.execute("INSERT INTO users (id, username, email) VALUES (%s, %s, %s)", (data['id'], data['username'], data['email']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Record created successfully'})

# Read records from the database
@app.route('/read-records', methods=['GET'])
def read_records():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    # Format records as JSON
    result = [{'id': record[0], 'username': record[1], 'email': record[2]} for record in records]
    return jsonify(result)

# Update a record in the database
@app.route('/update-record/<int:id>', methods=['PUT'])
def update_record(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Get data from request
    data = request.form
    # Update record in database
    cursor.execute("UPDATE users SET username = %s, email = %s WHERE id = %s", (data['username'], data['email'], id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Record updated successfully'})

# Delete a record from the database
@app.route('/delete-record/<int:id>', methods=['DELETE'])
def delete_record(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Delete record from database
    cursor.execute("DELETE FROM users WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Record deleted successfully'})

# Define a route to display the HTML form
@app.route('/')
def index():
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Simple CRUD App</title>
    </head>
    <body>
        <h1>Simple CRUD App</h1>
        
        <!-- Form to create a new record -->
        <h2>Create Record</h2>
        <form action="/create-record" method="POST">
            <label for="id">ID:</label><br>
            <input type="text" id="id" name="id" required><br>
            <label for="username">Username:</label><br>
            <input type="text" id="username" name="username" required><br>
            <label for="email">Email:</label><br>
            <input type="email" id="email" name="email" required><br><br>
            <input type="submit" value="Submit">
        </form>
        
        <!-- Display existing records -->
        <h2>Existing Records</h2>
        <ul id="records">
            <!-- Records will be displayed here dynamically -->
        </ul>
        
        <!-- Script to fetch and display existing records -->
        <script>
            fetch('/read-records')
                .then(response => response.json())
                .then(records => {
                    const recordsList = document.getElementById('records');
                    records.forEach(record => {
                        const listItem = document.createElement('li');
                        listItem.textContent = ID: ${record.id}, Username: ${record.username}, Email: ${record.email};
                        recordsList.appendChild(listItem);
                    });
                })
                .catch(error => console.error('Error fetching records:', error));
        </script>
    </body>
    </html>
    """
    return render_template_string(html)


# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)