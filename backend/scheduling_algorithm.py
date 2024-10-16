import pandas as pd

# Step 1: Define the input structures
def parse_file1(file1_content):
    rooms = {}
    courses = []
    times = []

    # Parsing File 1 content (rooms, courses, times)
    lines = file1_content.strip().split('\n')
    current_section = None
    for line in lines:
        line = line.strip()
        if line == 'rooms':
            current_section = 'rooms'
        elif line == 'courses':
            current_section = 'courses'
        elif line == 'times':
            current_section = 'times'
        elif current_section == 'rooms':
            room, capacity = line.split(':')
            rooms[room.strip()] = int(capacity.strip())
        elif current_section == 'courses':
            courses = line.split(',')
        elif current_section == 'times':
            times = line.split(',')
    
    return rooms, courses, times


def parse_file2(file2_content):
    course_preferences = {}

    # Parsing File 2 content (course, enrollment, preferences)
    lines = file2_content.strip().split('\n')
    for line in lines:
        parts = line.split()
        course = parts[0]
        enrollment = int(parts[1])
        preferences = parts[2:]
        course_preferences[course] = {
            'enrollment': enrollment,
            'preferences': preferences
        }
    
    return course_preferences


# Step 2: Validate the input data
def validate_inputs(rooms, courses, times, course_preferences):
    errors = []
    
    # Validate room capacities
    for room, capacity in rooms.items():
        if capacity < 10 or capacity > 300:
            errors.append(f"Room {room} has an invalid capacity: {capacity}")
    
    # Validate course numbers and enrollment
    for course, details in course_preferences.items():
        if not course.startswith("cs") or not course[2:].isdigit():
            errors.append(f"Invalid course number: {course}")
        if details['enrollment'] > 300 or details['enrollment'] < 10:
            errors.append(f"Invalid enrollment for course {course}: {details['enrollment']}")
    
    # Validate time slots
    valid_time_format = ['MWF9', 'MWF10', 'MWF11', 'MWF2', 'TT9', 'TT10:30', 'TT2', 'TT3:30']
    for time in times:
        if time not in valid_time_format:
            errors.append(f"Invalid time slot: {time}")
    
    return errors


# Step 3: Scheduling algorithm
def schedule_courses(rooms, courses, times, course_preferences):
    schedule = {}
    conflicts = []

    available_times = {time: [] for time in times}  # Keep track of time availability per room
    post_grad_courses = [course for course in courses if course.startswith("cs6")]

    for course in courses:
        course_details = course_preferences.get(course)
        if not course_details:
            continue
        
        enrollment = course_details['enrollment']
        preferences = course_details['preferences']
        
        # Assign room based on availability and capacity
        assigned = False
        for time in preferences:
            if time not in available_times:
                continue

            for room, capacity in rooms.items():
                if capacity >= enrollment and room not in available_times[time]:
                    # Assign course to room at this time
                    available_times[time].append(room)
                    schedule[course] = {'room': room, 'time': time}
                    assigned = True
                    break

            if assigned:
                break

        if not assigned:
            conflicts.append({
                'course': course,
                'reason': 'Room capacity issues or time clashes'
            })
    
    return schedule, conflicts


# Step 4: Generate conflict report
def generate_conflict_report(conflicts):
    report = []
    for conflict in conflicts:
        report.append(f"Course {conflict['course']} could not be scheduled: {conflict['reason']}")
    return '\n'.join(report)


# Step 5: Main function to integrate everything
def main(file1_content, file2_content):
    rooms, courses, times = parse_file1(file1_content)
    course_preferences = parse_file2(file2_content)

    # Validate inputs
    errors = validate_inputs(rooms, courses, times, course_preferences)
    if errors:
        return "Errors found in input files:\n" + "\n".join(errors)

    # Schedule courses
    schedule, conflicts = schedule_courses(rooms, courses, times, course_preferences)

    # Output results
    schedule_output = pd.DataFrame.from_dict(schedule, orient='index')
    conflict_report = generate_conflict_report(conflicts)

    return schedule_output, conflict_report
