# Student Details Hash Map
# This program creates a hash map to store student details such as name, age, and average grade.


# Define a hash map (dictionary) to store student details
student_details = {
    "student_001": {"name": "Alice", "age": 20, "average_grade": 88.5},
    "student_002": {"name": "Bob", "age": 22, "average_grade": 92.0},
    "student_003": {"name": "Charlie", "age": 19, "average_grade": 85.0},
    "student_004": {"name": "Diana", "age": 21, "average_grade": 90.5},
    "student_005": {"name": "Ethan", "age": 23, "average_grade": 87.0},
    "student_006": {"name": "Fiona", "age": 20, "average_grade": 91.5},
    "student_007": {"name": "George", "age": 22, "average_grade": 84.0},
    "student_008": {"name": "Hannah", "age": 19, "average_grade": 89.0},
    "student_009": {"name": "Ian", "age": 21, "average_grade": 93.5},
    "student_010": {"name": "Jane", "age": 20, "average_grade": 86.0},
}


# Function to display student details
def display_student_details():
    input_id = ""
    while input_id != "0":
        input_id = input('Enter student ID (e.g., student_001) or "0" to exit: ')
        if input_id == "0":
            print("Exiting the program.")
            break
        elif input_id in student_details:
            print(student_details.get(input_id))
        else:
            print("Student ID not found. Please try again.")
    return


student_details.setdefault()
print(student_details.get("student_001"))
display_student_details()
