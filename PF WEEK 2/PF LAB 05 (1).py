# GPA Calculator using User Defined Function

def calculate_gpa(subjects):
    total_grade_points = 0
    total_credit_hours = 0

    for i in range(subjects):
        grade_point = float(input(f"Enter Grade Point for subject {i+1}: "))
        credit_hours = int(input(f"Enter Credit Hours for subject {i+1}: "))

        total_grade_points += grade_point * credit_hours
        total_credit_hours += credit_hours

    gpa = total_grade_points / total_credit_hours
    return gpa

num_subjects = int(input("Enter number of subjects: "))

result = calculate_gpa(num_subjects)

print("Semester GPA =", round(result, 2))