from dataclasses import dataclass
from typing import List, Dict
import re

@dataclass
class Room:
    number: str
    capacity: int

@dataclass
class Course:
    number: str
    enrollment: int
    preferences: List[str]

@dataclass
class TimeSlot:
    time: str

def parse_input_file1(content: str) -> Dict[str, List]:
    sections = content.split(';')
    data = {}
    
    for section in sections:
        section = section.strip()
        if not section:
            continue  # Skip empty sections

        if 'rooms' in section:
            rooms = []
            for line in section.split('\n')[1:]:
                line = line.strip()
                if line:  # Check if the line is not empty
                    number, capacity = line.split(':')
                    rooms.append(Room(number.strip(), int(capacity.strip())))
            data['rooms'] = rooms
        elif 'courses' in section:
            courses = [course.strip().rstrip(',') for course in section.split('\n')[1].split(',') if course.strip()]
            data['courses'] = courses
        elif 'times' in section:
            times = [TimeSlot(time.strip().rstrip(',')) for time in section.split('\n')[1].split(',') if time.strip()]
            data['times'] = times
    
    return data

def parse_input_file2(content: str) -> List[Course]:
    lines = content.strip().split('\n')[1:]  # Skip the header
    courses = []
    
    for line in lines:
        parts = line.split()
        if len(parts) < 2:  # Skip lines that don't have enough data
            continue
        course_number = parts[0]
        enrollment = int(parts[1])
        # Extract preferences while stripping trailing commas and split by comma
        preferences = [pref.strip().rstrip(',') for pref in ' '.join(parts[2:]).split(',')] if len(parts) > 2 else []
        courses.append(Course(course_number, enrollment, preferences))
    
    return courses

def validate_input_data(file1_data: Dict[str, List], file2_data: List[Course]) -> List[str]:
    errors = []
    
    # Check if all required sections are present in file1
    required_sections = ['rooms', 'courses', 'times']
    for section in required_sections:
        if section not in file1_data:
            errors.append(f"Missing {section} section in input file 1")
    
    # Check room capacity ranges and formats
    for room in file1_data.get('rooms', []):
        if room.capacity < 1 or room.capacity > 300:  # Define your range
            errors.append(f"Classroom capacity out of range for room {room.number}: {room.capacity}")
        if not re.match(r'^\d+$', room.number):  # Check if the room number is valid (only digits)
            errors.append(f"Classroom number has wrong format: {room.number}")

    # Check if all courses in file2 are present in file1
    file1_courses = set(file1_data.get('courses', []))
    for course in file2_data:
        if course.number not in file1_courses:
            errors.append(f"Course {course.number} in input file 2 not found in input file 1")
    
    # Check if all time preferences in file2 are valid
    valid_times = set(slot.time for slot in file1_data.get('times', []))
    for course in file2_data:
        for pref in course.preferences:
            if pref not in valid_times:
                errors.append(f"Invalid time preference {pref} for course {course.number}")
    
    return errors

# Usage example (if needed for testing)
if __name__ == "__main__":
    # Add your testing logic here if needed
    pass
