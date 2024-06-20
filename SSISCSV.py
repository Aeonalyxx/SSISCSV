import sys
import os
import csv
from PyQt5 import QtCore, QtGui, QtWidgets
from functools import partial

#CHRIS ADRIAN GUMISAD               CCC-151

#ADD STUDENT DIALOG ======================================================================================

class AddStudentDialog(QtWidgets.QDialog):
    def __init__(self, course_codes, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Student")
        self.setFixedSize(500, 210)
        self.course_codes = course_codes

        self.student_id_label = QtWidgets.QLabel("Student ID:")
        self.name_label = QtWidgets.QLabel("Student Name:")
        self.gender_label = QtWidgets.QLabel("Student Gender:")
        self.course_label = QtWidgets.QLabel("Course Code:")
        self.year_label = QtWidgets.QLabel("Student Year:")

        self.student_id_edit = QtWidgets.QLineEdit(self)
        self.name_edit = QtWidgets.QLineEdit(self)
        
        self.gender_combobox = QtWidgets.QComboBox(self)
        self.gender_combobox.addItems(["Male", "Female"])

        self.course_combobox = QtWidgets.QComboBox(self)
        self.course_combobox.addItems(self.course_codes)  

        self.year_combobox = QtWidgets.QComboBox(self)
        self.year_combobox.addItems(["1", "2", "3", "4"])

        self.ok_button = QtWidgets.QPushButton("Ok", self)
        self.ok_button.clicked.connect(self.save_and_close)
        self.cancel_button = QtWidgets.QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.reject)

        # Create layouts
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow(self.student_id_label, self.student_id_edit)
        form_layout.addRow(self.name_label, self.name_edit)
        form_layout.addRow(self.gender_label, self.gender_combobox)
        form_layout.addRow(self.course_label, self.course_combobox)
        form_layout.addRow(self.year_label, self.year_combobox)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.ok_button)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addItem(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
        main_layout.addLayout(button_layout)
        
    def save_and_close(self):
        if not all((field.text() if isinstance(field, QtWidgets.QLineEdit) else field.currentText()) for field in [self.student_id_edit, self.name_edit, self.gender_combobox, self.course_combobox, self.year_combobox]):
            QtWidgets.QMessageBox.critical(self, "Error", "Please fill in all fields.")
        else:
            student_data = [
                self.student_id_edit.text(),
                self.name_edit.text(),
                self.gender_combobox.currentText(),
                self.course_combobox.currentText(), 
                self.year_combobox.currentText()
            ]
            if self.check_student_id_unique(student_data[0]):
                self.save_to_csv(student_data)
                self.accept()
            else:
                QtWidgets.QMessageBox.warning(self, "Warning", "Student ID already exists. Please enter a unique ID.")

    def check_student_id_unique(self, new_student_id):
        directory = os.path.dirname(os.path.abspath(__file__))
        csv_file_path = os.path.join(directory, 'studentlist.csv')
        
        existing_data = []
        if os.path.exists(csv_file_path):
            with open(csv_file_path, mode='r', newline='') as file:
                reader = csv.reader(file)
                existing_data = list(reader)

        for row in existing_data:
            if row[0] == new_student_id:
                return False
        return True

    def save_to_csv(self, student_data):
        directory = os.path.dirname(os.path.abspath(__file__))
        csv_file_path = os.path.join(directory, 'studentlist.csv')

        with open(csv_file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(student_data)

#EDIT STUDENT DIALOG ======================================================================================

class EditStudentDialog(QtWidgets.QDialog):
    data_changed = QtCore.pyqtSignal(list)

    def __init__(self, student_data, course_codes, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Student")
        self.setFixedSize(500, 210)
        self.course_codes = ['Not Enrolled'] + course_codes 

        self.student_id_label = QtWidgets.QLabel("Student ID:")
        self.name_label = QtWidgets.QLabel("Student Name:")
        self.gender_label = QtWidgets.QLabel("Student Gender:")
        self.course_label = QtWidgets.QLabel("Course Code:")
        self.year_label = QtWidgets.QLabel("Student Year:")

        self.student_id_edit = QtWidgets.QLineEdit(self)
        self.name_edit = QtWidgets.QLineEdit(self)
        
        self.gender_combobox = QtWidgets.QComboBox(self)
        self.gender_combobox.addItems(["Male", "Female"])

        self.course_combobox = QtWidgets.QComboBox(self)
        self.course_combobox.addItems(self.course_codes)
        self.course_combobox.setCurrentIndex(0)

        self.year_combobox = QtWidgets.QComboBox(self)
        self.year_combobox.addItems(["1", "2", "3", "4"])

        self.ok_button = QtWidgets.QPushButton("Ok", self)
        self.ok_button.clicked.connect(self.save_and_close)
        self.cancel_button = QtWidgets.QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.reject)

        # Create layouts
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow(self.student_id_label, self.student_id_edit)
        form_layout.addRow(self.name_label, self.name_edit)
        form_layout.addRow(self.gender_label, self.gender_combobox)
        form_layout.addRow(self.course_label, self.course_combobox)
        form_layout.addRow(self.year_label, self.year_combobox)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.ok_button)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addItem(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
        main_layout.addLayout(button_layout)

        self.set_student_data(student_data)
        self.original_student_data = student_data
        
    def set_student_data(self, student_data):
        self.student_id_edit.setText(student_data[0])
        self.name_edit.setText(student_data[1])
        self.gender_combobox.setCurrentText(student_data[2])
        if student_data[3] is None or student_data[3] == '':
            self.course_combobox.setCurrentIndex(0)  
        else:
            self.course_combobox.setCurrentText(student_data[3])
        
        self.year_combobox.setCurrentText(student_data[4])
        
    def save_and_close(self):
        if not all((field.text() if isinstance(field, QtWidgets.QLineEdit) else field.currentText()) 
               for field in [self.student_id_edit, self.name_edit, self.gender_combobox, self.year_combobox]):
            QtWidgets.QMessageBox.critical(self, "Error", "Please fill in all fields.")
        else:
            edited_student_data = [
                self.student_id_edit.text(),
                self.name_edit.text(),
                self.gender_combobox.currentText(),
                self.course_combobox.currentText() if self.course_combobox.currentText() != '' else None,
                self.year_combobox.currentText()
            ]
            if edited_student_data[0] != self.original_student_data[0]:
                if not self.check_student_id_unique(edited_student_data[0]):
                    QtWidgets.QMessageBox.warning(self, "Warning", "Student ID already exists. Please enter a unique ID.")
                    return
              
            self.update_student_data(edited_student_data)
            self.data_changed.emit(edited_student_data)
            self.accept()
    
    def check_student_id_unique(self, new_student_id):
        directory = os.path.dirname(os.path.abspath(__file__))
        csv_file_path = os.path.join(directory, 'studentlist.csv')

        existing_data = []
        if os.path.exists(csv_file_path):
            with open(csv_file_path, mode='r', newline='') as file:
                reader = csv.reader(file)
                existing_data = list(reader)

        for row in existing_data:
            if row[0] == new_student_id:
                return False
        return True

    def update_student_data(self, edited_student_data):
        directory = os.path.dirname(os.path.abspath(__file__))
        csv_file_path = os.path.join(directory, 'studentlist.csv')

        updated_data = []
        with open(csv_file_path, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row == self.original_student_data:
                    updated_data.append(edited_student_data)
                else:
                    updated_data.append(row)

        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(updated_data)

#ADD COURSE DIALOG ======================================================================================

class AddCourseDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Course")
        self.setFixedSize(500, 210)

        self.course_id_label = QtWidgets.QLabel("Course Code:")
        self.name_label = QtWidgets.QLabel("Course Name:")
        self.department_label = QtWidgets.QLabel("Course Bldg. :")

        self.course_id_edit = QtWidgets.QLineEdit(self)
        
        self.name_edit = QtWidgets.QLineEdit(self)
        
        self.department_combobox = QtWidgets.QComboBox(self)
        self.department_combobox.addItems(["CCS", "CASS", "COE", "CBAA", "CON", "CSM", "CED"])

        self.ok_button = QtWidgets.QPushButton("Ok", self)
        self.ok_button.clicked.connect(self.save_and_close)
        self.cancel_button = QtWidgets.QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.reject)

        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow(self.course_id_label, self.course_id_edit)
        form_layout.addRow(self.name_label, self.name_edit)
        form_layout.addRow(self.department_label, self.department_combobox)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.ok_button)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addItem(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
        main_layout.addLayout(button_layout)
        
    def save_and_close(self):
        if not all((field.text() if isinstance(field, QtWidgets.QLineEdit) else field.currentText()) for field in [self.course_id_edit, self.name_edit, self.department_combobox]):
            QtWidgets.QMessageBox.critical(self, "Error", "Please fill in all fields.")
        else:
            course_data = [
                self.course_id_edit.text(),
                self.name_edit.text(),
                self.department_combobox.currentText()
            ]
            if self.check_course_id_unique(course_data[0]):
                self.save_to_csv(course_data)
                self.accept()
            else:
                QtWidgets.QMessageBox.warning(self, "Warning", "Course Code already exists. Please enter a unique ID.")

    def check_course_id_unique(self, new_course_id):
        directory = os.path.dirname(os.path.abspath(__file__))
        csv_file_path = os.path.join(directory, 'courselist.csv')

        existing_data = []
        if os.path.exists(csv_file_path):
            with open(csv_file_path, mode='r', newline='') as file:
                reader = csv.reader(file)
                existing_data = list(reader)

        for row in existing_data:
            if row[0] == new_course_id:
                return False
        return True

    def save_to_csv(self, course_data):
        directory = os.path.dirname(os.path.abspath(__file__))
        csv_file_path = os.path.join(directory, 'courselist.csv')

        with open(csv_file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(course_data)

#EDIT COURSE DIALOG ======================================================================================

class EditCourseDialog(QtWidgets.QDialog):
    data_changed = QtCore.pyqtSignal(list)

    def __init__(self, course_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Course")
        self.setFixedSize(500, 210)

        self.course_ID_label = QtWidgets.QLabel("Course Code:")
        self.course_name_label = QtWidgets.QLabel("Course Name:")
        self.department_label = QtWidgets.QLabel("Course Bldg. :")

        self.course_ID_edit = QtWidgets.QLineEdit(self)
        
        self.course_name_edit = QtWidgets.QLineEdit(self)
        
        self.department_combobox = QtWidgets.QComboBox(self)
        self.department_combobox.addItems(["CCS", "CASS", "COE", "CBAA", "CON", "CSM", "CED"])

        self.ok_button = QtWidgets.QPushButton("Ok", self)
        self.ok_button.clicked.connect(self.save_and_close)
        self.cancel_button = QtWidgets.QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.reject)

        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow(self.course_ID_label, self.course_ID_edit)
        form_layout.addRow(self.course_name_label, self.course_name_edit)
        form_layout.addRow(self.department_label, self.department_combobox)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.ok_button)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addItem(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
        main_layout.addLayout(button_layout)
        
        self.setCourseData(course_data)
        self.original_course_data = course_data
        
    def setCourseData(self, course_data):
        self.course_ID_edit.setText(course_data[0])
        self.course_name_edit.setText(course_data[1])
        self.department_combobox.setCurrentText(course_data[2])
        
    def get_course_data(self):
        new_course_code = self.course_ID_edit.text()
        new_course_name = self.course_name_edit.text()
        new_building = self.department_combobox.currentText()
        return [new_course_code, new_course_name, new_building]

    def save_and_close(self):
        if not all((field.text() if isinstance(field, QtWidgets.QLineEdit) else field.currentText()) for field in [self.course_ID_edit, self.course_name_edit, self.department_combobox]):
            QtWidgets.QMessageBox.critical(self, "Error", "Please fill in all fields.")
        else:
            edited_course_data = [
                self.course_ID_edit.text(),
                self.course_name_edit.text(),
                self.department_combobox.currentText()
            ]
            if edited_course_data[0] != self.original_course_data[0]:
                if not self.check_course_code_unique(edited_course_data[0]):
                    QtWidgets.QMessageBox.warning(self, "Warning", "Course Code already exists. Please enter a unique code.")
                    return

            self.update_course_data(edited_course_data)
            self.data_changed.emit(edited_course_data)
            self.accept()

    def check_course_code_unique(self, new_course_code):
        directory = os.path.dirname(os.path.abspath(__file__))
        csv_file_path = os.path.join(directory, 'courselist.csv')

        existing_data = []
        if os.path.exists(csv_file_path):
            with open(csv_file_path, mode='r', newline='') as file:
                reader = csv.reader(file)
                existing_data = list(reader)

        for row in existing_data:
            if row[0] == new_course_code:
                return Falses
        return True

    def update_course_data(self, edited_course_data):
        directory = os.path.dirname(os.path.abspath(__file__))
        csv_file_path = os.path.join(directory, 'courselist.csv')

        existing_data = []
        if os.path.exists(csv_file_path):
            with open(csv_file_path, mode='r', newline='') as file:
                reader = csv.reader(file)
                existing_data = list(reader)

        for i, row in enumerate(existing_data):
            if row == self.original_course_data:
                existing_data[i] = edited_course_data

        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(existing_data)

#UI MAIN WINDOW===============================================================================================

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1176, 705)
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("background-color: lightsteelblue;")
        self.centralwidget.setObjectName("centralwidget")
        
        self.SSIS = QtWidgets.QLabel(self.centralwidget)
        self.SSIS.setGeometry(QtCore.QRect(320, 10, 691, 51))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.SSIS.setFont(font)
        self.SSIS.setObjectName("SSIS")
        
    #TAB BUTTONS
        self.TabButtons = QtWidgets.QTabWidget(self.centralwidget)
        self.TabButtons.setGeometry(QtCore.QRect(30, 60, 1121, 591))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.TabButtons.setFont(font)
        self.TabButtons.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.TabButtons.setStyleSheet("background-color: white;")

        self.TabButtons.setObjectName("TabButtons")
        
#STUDENTS TAB =================================================================================================

        self.Students = QtWidgets.QWidget()
        font = QtGui.QFont()
        font.setPointSize(14)
        self.Students.setFont(font)
        
    #STUDENT SEARCH BAR
        self.StudentIDLineEdit = QtWidgets.QLineEdit(self.Students)
        self.StudentIDLineEdit.setGeometry(QtCore.QRect(150, 510, 210, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.StudentIDLineEdit.setFont(font)
        self.StudentIDLineEdit.setMaxLength(50) 
        self.StudentIDLineEdit.setPlaceholderText("Search...")
        self.StudentIDLineEdit.setObjectName("StudentIDLineEdit")
        self.StudentIDLineEdit.returnPressed.connect(self.search_students)
        
    #SEARCH STUDENT BUTTON
        self.SearchStudentIDButton = QtWidgets.QPushButton(self.Students)
        self.SearchStudentIDButton.setGeometry(QtCore.QRect(360, 510, 93, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.SearchStudentIDButton.setFont(font)
        self.SearchStudentIDButton.setObjectName("SearchStudent")
        self.SearchStudentIDButton.setStyleSheet("""QPushButton {background-color: lightsteelblue; color: black;} QPushButton:hover {background-color: darkblue; color: white; }""")
        self.SearchStudentIDButton.clicked.connect(self.search_students)
        
    #STUDENT FILTER BOX
        self.StudentfilterComboBox = QtWidgets.QComboBox(self.Students)
        self.StudentfilterComboBox.setGeometry(QtCore.QRect(10, 510, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.StudentfilterComboBox.setFont(font)
        self.StudentfilterComboBox.setObjectName("filterComboBox")
        self.StudentfilterComboBox.addItems(["Student ID", "Name", "Gender", "Course Code", "Year"])
        
    #STUDENT TABLE
        self.StudentTable = QtWidgets.QTableWidget(self.Students)
        self.StudentTable.setGeometry(QtCore.QRect(120, 10, 981, 491))
        self.StudentTable.setColumnCount(5)
        self.StudentTable.setHorizontalHeaderLabels(["Student ID", "Name", "Gender", "Course Code", "Year"])
        self.StudentTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.StudentTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        
        # Adjust column widths
        self.StudentTable.setColumnWidth(0, 170)  
        self.StudentTable.setColumnWidth(1, 360)  
        self.StudentTable.setColumnWidth(2, 100)   
        self.StudentTable.setColumnWidth(3, 200) 
        self.StudentTable.setColumnWidth(4, 70)  

    #ADD STUDENT BUTTON 
        self.AddStudentButton = QtWidgets.QPushButton(self.Students)
        self.AddStudentButton.setGeometry(QtCore.QRect(10, 120, 93, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.AddStudentButton.setFont(font)
        self.AddStudentButton.setStyleSheet("""QPushButton {background-color: lightsteelblue; color: black;} QPushButton:hover {background-color: green; color: white; }""")
        self.AddStudentButton.clicked.connect(self.open_add_student_dialog)
        
    #EDIT STUDENT BUTTON   
        self.EditStudentButton = QtWidgets.QPushButton(self.Students)
        self.EditStudentButton.setGeometry(QtCore.QRect(10, 210, 93, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.EditStudentButton.setFont(font)
        self.EditStudentButton.setStyleSheet("""QPushButton {background-color: lightsteelblue; color: black;} QPushButton:hover {background-color: yellow; color: black; }""")
        self.EditStudentButton.clicked.connect(self.open_edit_student_dialog)
        
    #DELETE STUDENT BUTTON    
        self.DeleteStudentButton = QtWidgets.QPushButton(self.Students)
        self.DeleteStudentButton.setGeometry(QtCore.QRect(10, 300, 93, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.DeleteStudentButton.setFont(font)
        self.DeleteStudentButton.setStyleSheet("""QPushButton {background-color: lightsteelblue; color: black;} QPushButton:hover {background-color: darkred; color: white; }""")
        self.DeleteStudentButton.clicked.connect(self.delete_student)
        self.TabButtons.addTab(self.Students, "")
        
#COURSE TAB =================================================================================================

        self.Courses = QtWidgets.QWidget()
        font = QtGui.QFont()
        font.setPointSize(14)
        self.Courses.setFont(font)
        
    #SEARCH COURSE ID BUTTON
        self.SearchCourseIDButton = QtWidgets.QPushButton(self.Courses)
        self.SearchCourseIDButton.setGeometry(QtCore.QRect(360, 510, 93, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.SearchCourseIDButton.setFont(font)
        self.SearchCourseIDButton.setStyleSheet("""QPushButton {background-color: lightsteelblue;} QPushButton:hover {background-color: darkblue; color: white; }""")
        self.SearchCourseIDButton.clicked.connect(self.search_courses)
        
    #COURSE SEARCH BAR
        self.CourseIDLineEdit = QtWidgets.QLineEdit(self.Courses)
        self.CourseIDLineEdit.setGeometry(QtCore.QRect(150, 510, 210, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.CourseIDLineEdit.setFont(font)
        self.CourseIDLineEdit.setMaxLength(80) 
        self.CourseIDLineEdit.setPlaceholderText("Search...")
        self.CourseIDLineEdit.returnPressed.connect(self.search_courses)
        
    #FILTER BOX
        self.CoursefilterComboBox = QtWidgets.QComboBox(self.Courses)
        self.CoursefilterComboBox.setGeometry(QtCore.QRect(10, 510, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.CoursefilterComboBox.setFont(font)
        self.CoursefilterComboBox.setObjectName("filterComboBox")
        self.CoursefilterComboBox.addItems(["Course Code", "Course Name", "Bldg."])
        
    #COURSE TABLE   
        font.setPointSize(11)
        self.CourseTable = QtWidgets.QTableWidget(self.Courses)
        self.CourseTable.setGeometry(QtCore.QRect(120, 10, 981, 491))
        self.CourseTable.setColumnCount(3)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.CourseTable.setHorizontalHeaderLabels(["Course Code", "Course Name", "Bldg."])
        self.CourseTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.CourseTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        self.CourseTable.setColumnWidth(0, 155) 
        self.CourseTable.setColumnWidth(1, 680) 
        self.CourseTable.setColumnWidth(2, 80) 
    
    #ADD COURSE BUTTON 
        self.AddCourseButton = QtWidgets.QPushButton(self.Courses)
        self.AddCourseButton.setGeometry(QtCore.QRect(10, 120, 93, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.AddCourseButton.setFont(font)
        self.AddCourseButton.setStyleSheet("""QPushButton {background-color: lightsteelblue;} QPushButton:hover {background-color: green; color: white; }""")
        self.AddCourseButton.clicked.connect(self.open_add_course_dialog)

    #EDIT COURSE BUTTON   
        self.EditCourseButton = QtWidgets.QPushButton(self.Courses)
        self.EditCourseButton.setGeometry(QtCore.QRect(10, 210, 93, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.EditCourseButton.setFont(font)
        self.EditCourseButton.setStyleSheet("""QPushButton {background-color: lightsteelblue;} QPushButton:hover {background-color: yellow; }""")
        self.EditCourseButton.clicked.connect(self.open_edit_course_dialog)

    #DELETE COURSE BUTTON  
        self.DeleteCourseButton = QtWidgets.QPushButton(self.Courses)
        self.DeleteCourseButton.setGeometry(QtCore.QRect(10, 300, 93, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.DeleteCourseButton.setFont(font)
        self.DeleteCourseButton.setStyleSheet("""QPushButton {background-color: lightsteelblue; color: black;} QPushButton:hover {background-color: darkred; color: white; }""")
        self.DeleteCourseButton.clicked.connect(self.delete_course)
        self.TabButtons.addTab(self.Courses, "")

#MAIN WINDOW =================================================================================================

        MainWindow.setCentralWidget(self.centralwidget)
        self.translateUi(MainWindow)
        self.TabButtons.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

#RETRANSLATE UI =================================================================================================

    def translateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SSIS"))
        self.SSIS.setText(_translate("MainWindow", "Simple Student Information System"))
        self.SSIS.setStyleSheet(" font-weight: bold;")
        
        self.SearchStudentIDButton.setText(_translate("MainWindow", "Search"))
        self.AddStudentButton.setText(_translate("MainWindow", "Add"))
        self.EditStudentButton.setText(_translate("MainWindow", "Edit"))
        self.DeleteStudentButton.setText(_translate("MainWindow", "Delete"))
        self.TabButtons.setTabText(self.TabButtons.indexOf(self.Students), _translate("MainWindow", "Students"))
        
        self.SearchCourseIDButton.setText(_translate("MainWindow", "Search"))
        self.AddCourseButton.setText(_translate("MainWindow", "Add"))
        self.EditCourseButton.setText(_translate("MainWindow", "Edit"))
        self.DeleteCourseButton.setText(_translate("MainWindow", "Delete"))
        self.TabButtons.setTabText(self.TabButtons.indexOf(self.Courses), _translate("MainWindow", "Programs"))
        

#Implementations =================================================================================================
# FOR STUDENT ====================================================================================================
                    
    #GET ALL STUDENT DATA
    def get_all_student_data(self):

        directory = os.path.dirname(os.path.abspath(__file__))
        csv_file_path = os.path.join(directory, 'studentlist.csv')

        all_student_data = []

        with open(csv_file_path, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                all_student_data.append(row)

        return all_student_data
    
    # SEARCH STUDENTS
    def search_students(self):
        filter_option = self.StudentfilterComboBox.currentText()
        search_query = self.StudentIDLineEdit.text().strip().lower()
        directory = os.path.dirname(os.path.abspath(__file__))
        csv_file_path = os.path.join(directory, 'studentlist.csv')
        self.StudentTable.setRowCount(0)
        matches_found = False
        
        with open(csv_file_path, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row_data in reader:
                if filter_option == "Student ID" and search_query in row_data[0].lower():
                    self.add_row_to_student_table(row_data)
                    matches_found = True
                elif filter_option == "Name" and search_query in row_data[1].lower():
                    self.add_row_to_student_table(row_data)
                    matches_found = True
                elif filter_option == "Gender" and search_query == row_data[2].lower():
                    self.add_row_to_student_table(row_data)
                    matches_found = True
                elif filter_option == "Course Code" and search_query in row_data[3].lower():
                    self.add_row_to_student_table(row_data)
                    matches_found = True
                elif filter_option == "Year" and search_query in row_data[4].lower():
                    self.add_row_to_student_table(row_data)
                    matches_found = True

        if not matches_found: 
            QtWidgets.QMessageBox.warning(self.StudentIDLineEdit, "No Match", f"No student found with the given {filter_option}.")


    def add_row_to_student_table(self, student_data):
        row_position = self.StudentTable.rowCount()
        self.StudentTable.insertRow(row_position)
        for column, value in enumerate(student_data):
            item = QtWidgets.QTableWidgetItem(value)
            font = QtGui.QFont()
            font.setPointSize(14)  
            item.setFont(font)
            self.StudentTable.setItem(row_position, column, item)

    
    # OPEN ADD STUDENT DIALOG
    def open_add_student_dialog(self):
        course_codes = [self.CourseTable.item(row, 0).text() for row in range(self.CourseTable.rowCount())]
        dialog = AddStudentDialog(course_codes)
        if dialog.exec_():
            self.update_student_table()

    #OPEN EDIT STUDENT DIALOG
    def open_edit_student_dialog(self):
        course_codes = [self.CourseTable.item(row, 0).text() for row in range(self.CourseTable.rowCount())]
        selected_row = self.StudentTable.currentRow()
        if selected_row >= 0:
            student_data = []
            for column in range(self.StudentTable.columnCount()):
                item = self.StudentTable.item(selected_row, column)
                student_data.append(item.text() if item else "")

            dialog = EditStudentDialog(student_data, course_codes)
            dialog.data_changed.connect(self.update_student_table)
            if dialog.exec_():
                self.update_student_table()
        else:
            QtWidgets.QMessageBox.information(self.centralwidget, "Information", "Please select a row to edit.")

    # DELETE STUDENT
    def delete_student(self):
        selected_row = self.StudentTable.currentRow()
        if selected_row >= 0:
            confirmation = QtWidgets.QMessageBox.question(self.centralwidget, "Confirmation", "Are you sure you want to delete this student?",
                                                        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if confirmation == QtWidgets.QMessageBox.Yes:
                student_id_item = self.StudentTable.item(selected_row, 0)
                if student_id_item is not None:
                    student_id = student_id_item.text()
                    self.StudentTable.removeRow(selected_row)
                    self.update_csv_file_for_students(student_id)
        else:
            QtWidgets.QMessageBox.information(self.centralwidget, "Information", "Please select a row to delete.")
            
    # UPDATE CSV FOR STUDENTS
    def update_csv_file_for_students(self, deleted_student_id):
        directory = os.path.dirname(os.path.abspath(__file__))
        csv_file_path = os.path.join(directory, 'studentlist.csv')

        existing_data = []
        if os.path.exists(csv_file_path):
            with open(csv_file_path, mode='r', newline='') as file:
                reader = csv.reader(file)
                existing_data = list(reader)

        updated_data = [row for row in existing_data if row[0] != deleted_student_id] 

        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(updated_data)

        if len(updated_data) == 0:
            with open(csv_file_path, mode='w', newline='') as file:
                pass
   
            
    #UPDATE STUDENT TABLE
    def update_student_table(self):
        directory = os.path.dirname(os.path.abspath(__file__))
        csv_file_path = os.path.join(directory, 'studentlist.csv')
        with open(csv_file_path, mode='r') as file:
            reader = csv.reader(file)
            self.StudentTable.setRowCount(0)
            for row_number, row_data in enumerate(reader):
                self.StudentTable.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    item = QtWidgets.QTableWidgetItem(data)
                    font = QtGui.QFont()
                    font.setPointSize(14)  
                    item.setFont(font)
                    self.StudentTable.setItem(row_number, column_number, item)
                    
    # SAVE STUDENT DATA
    def save_student_data(self):
        directory = os.path.dirname(os.path.abspath(__file__))
        csv_file_path = os.path.join(directory, 'studentlist.csv')

        student_data = []
        for row in range(self.StudentTable.rowCount()):
            row_data = []
            for column in range(self.StudentTable.columnCount()):
                item = self.StudentTable.item(row, column)
                row_data.append(item.text() if item else "")
            student_data.append(row_data)

        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(student_data)
    

    #GET STUDENT DATA IN CSV
    def get_student_data_by_id(self, student_id):

        directory = os.path.dirname(os.path.abspath(__file__))
        csv_file_path = os.path.join(directory, 'studentlist.csv')

        with open(csv_file_path, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == student_id:
                    return row

        return None

# FOR COURSE =================================================================================================
                    
    #GET ALL CUORSE DATA
    def get_all_course_data(self):

        directory = os.path.dirname(os.path.abspath(__file__))
        csv_file_path = os.path.join(directory, 'courselist.csv')

        all_course_data = []

        with open(csv_file_path, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                all_course_data.append(row)

        return all_course_data
    
    # OPEN COURSE DIALOG
    def open_add_course_dialog(self):
        dialog = AddCourseDialog()
        if dialog.exec_():
            self.update_course_table()
            
    # OPEN EDIT COURSE DIALOG
    def open_edit_course_dialog(self):
        selected_row = self.CourseTable.currentRow()
        if selected_row >= 0:
            course_data = []
            for column in range(self.CourseTable.columnCount()):
                item = self.CourseTable.item(selected_row, column)
                course_data.append(item.text() if item else "")
        
            dialog = EditCourseDialog(course_data)
            if dialog.exec_():
                new_course_data = dialog.get_course_data()
                self.update_course_table()
                
                old_course_code = course_data[0]
                new_course_code = new_course_data[0]
                
                if old_course_code != new_course_code:
                  self.update_student_course_code(old_course_code, new_course_code)
                  ui.update_student_table()
        else:
            QtWidgets.QMessageBox.information(self.centralwidget, "Information", "Please select a row to edit.")
            
    #UPDATE COURSE CODE STUDENT/COURSE
    def update_student_course_code(self, old_course_code, new_course_code):
        directory = os.path.dirname(os.path.abspath(__file__))
        csv_file_path = os.path.join(directory, 'studentlist.csv')

        updated_rows = []
        with open(csv_file_path, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[3] == old_course_code:
                    row[3] = new_course_code
                updated_rows.append(row)

        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(updated_rows)

    # DELETE COURSE
    def delete_course(self):
        selected_row = self.CourseTable.currentRow()

        if selected_row >= 0:
            course_id_item = self.CourseTable.item(selected_row, 0)
            course_id = course_id_item.text()

            confirmation = QtWidgets.QMessageBox.question(self.centralwidget, "Confirmation", 
                                                          "Are you sure you want to delete this course?",
                                                          QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if confirmation == QtWidgets.QMessageBox.Yes:
                updated_rows = []

                with open('courselist.csv', 'r', newline='') as courses_file:
                    reader = csv.reader(courses_file)
                    courses_data = list(reader)
                
                with open('courselist.csv', 'w', newline='') as courses_file:
                    writer = csv.writer(courses_file)
                    for row in courses_data:
                        if row[0] == course_id:
                            continue
                        else:
                            writer.writerow(row)
                            updated_rows.append(row)

                with open('studentlist.csv', 'r', newline='') as students_file:
                    reader = csv.reader(students_file)
                    students_data = list(reader)
                
                with open('studentlist.csv', 'w', newline='') as students_file:
                    writer = csv.writer(students_file)
                    for row in students_data:
                        if len(row) >= 4 and row[3] == course_id:  # Check if row has enough columns
                            row[3] = 'Not Enrolled'
                        writer.writerow(row)
                
                if updated_rows:
                    with open('courselist.csv', 'w', newline='') as courses_file:
                        writer = csv.writer(courses_file)
                        writer.writerows(updated_rows)

                self.update_student_table()
                self.update_course_table()
                
                QtWidgets.QMessageBox.information(self.centralwidget, "Information", "Course deleted and students associated are marked as 'Not Enrolled'.")
            else:
                QtWidgets.QMessageBox.information(self.centralwidget, "Information", "Deletion canceled.")
        else:
            QtWidgets.QMessageBox.information(self.centralwidget, "Information", "Please select a row to delete.")

    #UPDATE CSV FOR COURSES
    def update_csv_file_for_courses(self, delete_course):
        directory = os.path.dirname(os.path.abspath(__file__))
        csv_file_path = os.path.join(directory, 'courselist.csv')

        existing_data = []
        if os.path.exists(csv_file_path):
            with open(csv_file_path, mode='r', newline='') as file:
                reader = csv.reader(file)
                existing_data = list(reader)

        existing_data = [row for row in existing_data if row[0] != delete_course]
        
        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(existing_data)

        if len(existing_data) == 0:
            with open(csv_file_path, mode='w', newline='') as file:
                pass  

    #UPDATE COURSE TABLE       
    def update_course_table(self):
        directory = os.path.dirname(os.path.abspath(__file__))
        csv_file_path = os.path.join(directory, 'courselist.csv')
        with open(csv_file_path, mode='r') as file:
            reader = csv.reader(file)
            self.CourseTable.setRowCount(0)
            for row_number, row_data in enumerate(reader):
                self.CourseTable.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    item = QtWidgets.QTableWidgetItem(data)
                    font = QtGui.QFont()
                    font.setPointSize(14)  
                    item.setFont(font)
                    self.CourseTable.setItem(row_number, column_number, item)
    
    # SAVE COURSE DATA
    def save_course_data(self):
        directory = os.path.dirname(os.path.abspath(__file__))
        csv_file_path = os.path.join(directory, 'courselist.csv')

        course_data = []
        for row in range(self.CourseTable.rowCount()):
            row_data = []
            for column in range(self.CourseTable.columnCount()):
                item = self.CourseTable.item(row, column)
                row_data.append(item.text() if item else "")
            course_data.append(row_data)

        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(course_data)
            
    #SEARCH COURSE FILTER
    def search_courses(self):
        filter_option = self.CoursefilterComboBox.currentText()
        search_query = self.CourseIDLineEdit.text().strip().lower()
        directory = os.path.dirname(os.path.abspath(__file__))
        csv_file_path = os.path.join(directory, 'courselist.csv')
        self.CourseTable.setRowCount(0)
        matches_found = False
        
        with open(csv_file_path, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row_data in reader:
                if filter_option == "Course Code" and search_query in row_data[0].lower():
                    self.add_row_to_course_table(row_data)
                    matches_found = True
                elif filter_option == "Course Name" and search_query in row_data[1].lower():
                    self.add_row_to_course_table(row_data)
                    matches_found = True
                elif filter_option == "Bldg." and search_query in row_data[2].lower():
                    self.add_row_to_course_table(row_data)
                    matches_found = True

        if not matches_found:
            if filter_option == "Course Code":
                QtWidgets.QMessageBox.warning(self.CourseIDLineEdit, "No Match", "No course found with the given Course Code.")
            elif filter_option == "Course Name":
                QtWidgets.QMessageBox.warning(self.CourseIDLineEdit, "No Match", "No course found with the given Course Name.")
            elif filter_option == "Bldg.":
                QtWidgets.QMessageBox.warning(self.CourseIDLineEdit, "No Match", "No course found with the given Bldg.")

    def add_row_to_course_table(self, course_data):
        row_position = self.CourseTable.rowCount()
        self.CourseTable.insertRow(row_position)
        for column, value in enumerate(course_data):
            item = QtWidgets.QTableWidgetItem(value)
            font = QtGui.QFont()
            font.setPointSize(14)  
            item.setFont(font)
            self.CourseTable.setItem(row_position, column, item)
            
#==================================================================================================================

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    
    # Check if the student CSV file exists
    student_csv_file_path = os.path.join(os.path.dirname(__file__), 'studentlist.csv')
    if os.path.exists(student_csv_file_path):
        ui.update_student_table()
    else:
        # If not found, create a new CSV file
        with open(student_csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
        ui.update_student_table()
        
    # Check if the course CSV file exists
    course_csv_file_path = os.path.join(os.path.dirname(__file__), 'courselist.csv')
    if os.path.exists(course_csv_file_path):
        ui.update_course_table()
    else:
        # If not found, create a new CSV file
        with open(course_csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
        ui.update_course_table()
    
    sys.exit(app.exec_())
