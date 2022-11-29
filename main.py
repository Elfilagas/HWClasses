from settings import logger


class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def __average_grade(self):
        return sum(sum(self.grades.values(), [])) / len(self.grades) if self.grades else 0

    def __str__(self):
        s = f'Имя: {self.name}\n' \
            f'Фамилия: {self.surname}\n' \
            f'Средняя оценка за домашние задания: {self.__average_grade()}\n' \
            f'Курсы в процессе изучения: {", ".join(self.courses_in_progress)}\n' \
            f'Завершенные курсы: {", ".join(self.finished_courses)}\n'
        return s

    def __lt__(self, other_student):
        if not isinstance(other_student, Student):
            print(f'{other_student} не является представителем класса Student.')
            return
        return self.__average_grade() < other_student.__average_grade()

    def rate_lector(self, lector, course, grade):
        if isinstance(lector, Lecturer) and course in self.courses_in_progress and course in lector.courses_attached:
            if course in lector.grades:
                lector.grades[course] += [grade]
            else:
                lector.grades[course] = [grade]
        else:
            logger.debug(f'Check params in rate_lector of Student class'
                         f'{isinstance(lector, Lecturer)}, '
                         f'{course in self.courses_in_progress}, '
                         f'{course in lector.courses_attached}')
            print(f'Ошибка, оценка к курсу {course} не добавлена лектору {lector.name} {lector.surname}!')


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def __average_grade(self):
        return sum(sum(self.grades.values(), [])) / len(self.grades) if self.grades else 0

    def __str__(self):
        return f'Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за лекции: {self.__average_grade()}\n'

    def __lt__(self, other_lecturer):
        if not isinstance(other_lecturer, Lecturer):
            print(f'{other_lecturer} не является представителем класса Lecturer.')
            return
        return self.__average_grade() < other_lecturer.__average_grade()


class Reviewer(Mentor):
    def __str__(self):
        return f'Имя: {self.name}\nФамилия: {self.surname}\n'

    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            logger.debug(f'Check params in rate_hw of Review class'
                         f'{isinstance(student, Student)}, '
                         f'{course in self.courses_attached}, '
                         f'{course in student.courses_in_progress}')
            print(f'Ошибка, оценка к курсу {course} не добавлена лектору {student.name} {student.surname}!')


def average_grade_of_course(classes_list, course):
    """Return average value of grades of course for instances of classes Student or Lecturer or None if not
    all instances in list of same class or another class"""
    logger.debug(f'Input for all() in func average_grade_of_course '
                 f'{list(map(lambda x: isinstance(x, Student), classes_list))}')
    if all(map(lambda x: isinstance(x, Student), classes_list)) or \
            all(map(lambda x: isinstance(x, Lecturer), classes_list)):
        marks = sum([person.grades[course] for person in classes_list], [])
        return sum(marks) / len(marks)


def main():
    first_reviewer = Reviewer('Mark', 'Twen')
    first_reviewer.courses_attached += ['Python', 'C#']
    second_reviewer = Reviewer('Benedict', 'Vigor')
    second_reviewer.courses_attached += ['Java', 'Python']

    first_student = Student('Ruoy', 'Eman', 'male')
    first_student.courses_in_progress += ['Python', 'Java', 'C#']
    first_student.finished_courses += ['Введение в программирование']
    second_student = Student('Mary', 'McFly', 'female')
    second_student.courses_in_progress += ['Python']
    second_student.finished_courses += ['Введение в программирование']

    first_lecturer = Lecturer('Kanibal', 'Lector')
    first_lecturer.courses_attached += ['Python', 'C#']
    second_lecturer = Lecturer('Tom', 'Hanks')
    second_lecturer.courses_attached += ['Python', 'Java']

    first_reviewer.rate_hw(first_student, 'Python', 10)
    first_reviewer.rate_hw(first_student, 'C#', 9)
    second_reviewer.rate_hw(second_student, 'Python', 4)

    first_student.rate_lector(first_lecturer, 'Python', 10)
    first_student.rate_lector(first_lecturer, 'C#', 8)

    second_student.rate_lector(second_lecturer, 'Python', 9)
    first_student.rate_lector(second_lecturer, 'Java', 4)

    print(first_reviewer)
    print(second_reviewer)
    print(first_lecturer)
    print(second_lecturer)
    print(first_student)
    print(second_student)

    if first_lecturer > second_lecturer:
        print(f"{first_lecturer.name} {first_lecturer.surname} имеет более высокую среднюю оценку, чем"
              f" {second_lecturer.name} {second_lecturer.surname}")
    else:
        print(f"{second_lecturer.name} {second_lecturer.surname} имеет более высокую среднюю оценку, чем"
              f" {first_lecturer.name} {first_lecturer.surname}")

    if first_student > second_student:
        print(f"{first_student.name} {first_student.surname} имеет более высокую среднюю оценку, чем"
              f" {second_student.name} {second_student.surname}")
    else:
        print(f"{second_student.name} {second_student.surname} имеет более высокую среднюю оценку, чем"
              f" {first_student.name} {first_student.surname}")

    student_list = [first_student, second_student]
    print("Средняя оценка всех студентов по курсу 'Python' составляет: "
          f"{average_grade_of_course(student_list, course='Python')}")

    lecturers_list = [first_lecturer, second_lecturer]
    print("Средняя оценка всех лекторов по курсу 'Python' составляет: "
          f"{average_grade_of_course(lecturers_list, course='Python')}")


if __name__ == '__main__':
    logger.disabled = True
    main()
