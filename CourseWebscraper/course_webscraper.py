import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# importing beautifulsoup
def chooseCourse(user_input : str):
    course_code = re.search('^[A-Za-z]{4}(\s)*[0-9]{3}$', user_input) # need to match exact length of four letters and three digits
    if course_code:
        course = str(course_code.group(0))
        course = course.lower() # converting to lowercase to be able to use url later on

        if ' ' not in course:
            course = course[:4] + '-' + course[4:]
        else:
            course = course.replace(' ', '-')

        link = 'https://www.mcgill.ca/study/2023-2024/courses/' + course
        source = requests.get(link).text
        soup = BeautifulSoup(source, 'lxml')
        exists = soup.find('h1', attrs={"id" : "page-title"}) # course title 
        if exists.text.strip() == 'Page not found':
            print("This class does not exist, please try another course code")
            
        else:
            # if we've reached this point that means that the course exists
            available = soup.find('p', class_='catalog-terms')
            # we now regex query the terms to find if the course is scheduled for the current year or not
            scheduled = re.search('^(\s)*Terms:(\s)+This course is not scheduled for the 2023-2024 academic year.', available.text)
            if not scheduled: # this means that the course is offered in at least one of the semesters over the school year
                paragraphs = list(soup.findAll('p'))
                offered_by = paragraphs[0].text
                course_overview = paragraphs[1].text
                terms = available.text.strip()[12:]
                instructors = soup.find('p', class_="catalog-instructors").text[25:]
                notes = soup.find('ul', class_="catalog-notes")
                print(f"\n{exists.text.strip()}") # course code and num of credits
                print(f"\n{offered_by.strip()}")
                print(f"\nOVERVIEW:\n{course_overview.strip()}") # printing course overview
                print(f"\nTerms: {terms}")
                print(f"\nInstructors: {instructors}")
                if notes:
                    print("\nNOTES")
                    for course_note in notes.findAll('li'):
                        print(f" - {course_note.find('p').text.strip()}\n")

                
                df = pd.read_excel("CourseAverages.xlsx")
                df = df.loc[:, ~df.columns.str.match('^Unnamed')]
                # dropping the "Unnamed" column for better formatting and usability

                row_filt = df.index < 8536
                df = df.loc[row_filt]
                # removing rows filled with missing/empty values that are not course information

                course = course.replace('-','').upper()
                course_df = df.loc[df['Course'] == course]
                if len(course_df) == 0:
                    print("No information currently available for this course within the Crowdsourced database")
                    # this means that the course is offered but does not have any entered information in the file
                else:
                    print("Here is your course information including term, credits, and averages:\n")
                    print((course_df).to_string(index=False)) # ommitting index
                    avg = course_df['% Avg'].mean()
                    letter_to_gpa = {'A' : 4.0, 'A-' : 3.7, 'B+' : 3.3, 'B' : 3.0, 'B-' : 2.7, 'C+' : 2.3, 'C' : 2.0, 'D' : 2.0}
                    gpa_to_letter = {4.0 : 'A', 3.7 : 'A-', 3.3 : 'B+', 3.0 : 'B', 2.7 : 'B-', 2.3 : 'C+', 2.0 : 'C', 1.0 : 'D'}
                    grade_to_percent = {'A' : '85+%', 'A-' : '80-84%', 'B+' : '75-79%', 'B' : '70-74%', 'B-' : '65-69%', 'C+' : '60-64%', 'C' : '55-59%', 'D' : '50-55%'}
                    avg_gpa = None
                    if avg >= 3.7 and avg < 4.0:
                        avg_gpa = 3.7
                    elif avg >= 3.3 and avg < 3.7:
                        avg_gpa = 3.3
                    elif avg >= 3.0 and avg < 3.3:
                        avg_gpa = 3.0
                    elif avg >= 2.7 and avg < 3.0:
                        avg_gpa = 2.7
                    elif avg >= 2.3 and avg < 2.7:
                        avg_gpa = 2.3
                    elif avg >= 2.0 and avg < 2.3:
                        avg_gpa = 2.0
                    elif avg >= 1.0 and avg < 2.0:
                        avg_gpa = 1.0
                    else:
                        avg_gpa = 'A'
                    print(f"Overall average grade: {gpa_to_letter[avg_gpa]} -> {grade_to_percent[gpa_to_letter[avg_gpa]]} -> {letter_to_gpa[gpa_to_letter[avg_gpa]]} GPA")

            else:
                print("This course is not scheduled for the 2023-2024 academic-year") # course not scheduled
        
    else:
        # course was entered in incorrect format
        print("Invalid format, course code must have 4 letters followed by 3 digits, with an optional space in between (e.g. MATH 133, math133)")

if __name__ == '__main__':
    keep_going = True
    while keep_going:
        user_input = input("Please enter course code, or \"Quit\" to quit: ")
        if user_input.lower() == 'quit':
            break
        else:
            chooseCourse(user_input)
            invalid = False
            while not invalid:
                choice = input("Try another course? Yes/No ")
                if choice.lower() == "yes":
                    break
                elif choice.lower() == "no":
                    keep_going = False
                    break
                else:
                    print("Invalid input, try again")