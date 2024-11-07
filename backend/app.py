from flask import Flask, request, jsonify
from flask_cors import CORS
from scheduling_data_structures import parse_input_file1, parse_input_file2, validate_input_data
from scheduling_algorithm import basic_scheduling
import logging
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

@app.route('/read_files', methods=['POST'])
def read_files():
    if 'file1' not in request.files or 'file2' not in request.files:
        logging.error("Missing files: Both file1 and file2 are required")
        return jsonify({'error': 'Both files are required'}), 400

    file1 = request.files['file1']
    file2 = request.files['file2']
    logging.info(f"Received File 1: {file1.filename}")
    logging.info(f"Received File 2: {file2.filename}")

    try:
        # Ensure files are not empty
        if file1.filename == '' or file2.filename == '':
            logging.error("Input files are empty.")
            return jsonify({'error': 'Input files cannot be empty'}), 400
        
        file1_content = file1.read().decode('utf-8')
        file2_content = file2.read().decode('utf-8')

        # Parse the input files
        file1_data = parse_input_file1(file1_content)
        file2_data = parse_input_file2(file2_content)

        # Validate the input data
        errors = validate_input_data(file1_data, file2_data)

        if errors:
            logging.error(f"Validation errors: {errors}")
            return jsonify({
                'error': 'Validation errors',
                'details': errors
            }), 400

        # Schedule the courses with preferences
        schedule, unscheduled_courses = basic_scheduling(file1_data, file2_data)

        # If successful, return the schedule and unscheduled courses (conflicts)
        return jsonify({
            'schedule': schedule,
            'unscheduled_courses': unscheduled_courses,
            "message": "Files processed and schedule created successfully"
        }), 200

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
