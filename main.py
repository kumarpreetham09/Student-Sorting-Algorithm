all_deviations = []
all_genders = []
all_schools = []

def main():
    # Load all students into a list
    all_students = load_data()

    # Create a clean csv file with relavant headings
    with open("FCE2_Team1.csv", "w") as file:
        file.write("Tutorial Group,Student ID,School,Name,Gender,CGPA,Team Assigned\n")

    # Loop for 120 tutorial groups
    for i in range(120):
        # Initialise dictionary containing student data in current tutorial group
        students_dict = init_new_dict(all_students)

        # Initialise list of student ids for easy reference
        id_list = init_id_list(all_students)

        # Remove the first 50 entries from all_students list
        all_students = all_students[50:]

        # Initialise sorted_CGPA which contains student ids in order of ascending GPAs
        sorted_CGPA = CGPAmergesort(id_list, students_dict)

        # Initialise dictionary for assigned groups
        group_dict = initialise_groups()

        # Separate top and bottom 10 students from sorted_CGPA
        high_GPA, low_GPA = init_high_low_GPA(sorted_CGPA)

        # Initialise dictionary to compare popularity of schools within remaining students in sorted_CGPA
        school_dict = init_school_dict(sorted_CGPA, students_dict)

        # Place popular schools into a list
        popular_schools = find_popular_schools(school_dict)

        # Distribute first ten students to assigned groups and delete these ten from sorted_CGPA
        distribute_schools(sorted_CGPA, popular_schools, students_dict, group_dict)

        # Assign second student opposite to the gender of the first student and delete these ten from sorted_CGPA
        distribute_gender(sorted_CGPA,students_dict, group_dict)

        # Exhaust high_GPA and low_GPA lists for third and fourth students for each group respectively
        distribute_high_GPA(high_GPA, students_dict, group_dict)
        distribute_low_GPA(low_GPA,students_dict,group_dict)

        # Find groups that have three out of existing four, of the same gender
        flagged_groups = evaluate_priority(group_dict)

        distribute_to_flagged(flagged_groups, sorted_CGPA,students_dict,group_dict)

        # Distribute remaining in sorted_CGPA to remaining assigned groups
        distribute_remaining(sorted_CGPA,students_dict, group_dict)

        # # CASE FOR USING evaluate_priority() INSTEAD
        # lazy_distribute_remaining(sorted_CGPA, students_dict, group_dict)

        # Formatting for export into FCE2_Team1.csv
        results = formatting_for_export(group_dict)

        # Exports into new FCE2_Team1.csv
        export(results)

        # Analyse distribution
        tut_grp = students_dict[high_GPA[0]][0]
        analysis(tut_grp,students_dict, group_dict,id_list)

    # Analysis compared to all 120 tutorial groups
    total_analysis()


def load_data():
    all_students_list = []
    with open("FCE2_Team1.csv", "r") as myfile:
        p = myfile.readlines()[1:]
        for i in p:
            x = i.split(",")
            all_students_list.append(x)
    return all_students_list


def init_new_dict(students_list):
    students_dict = {}
    for i in range(50):
        x = students_list[i]
        students_dict.update({int(x[1]) : [x[0] , int(x[1]) , x[2] , x[3] , x[4] , float(x[5].split("\n")[0])]})
    return students_dict


def init_id_list(all_students_list):
    id_list = []
    for i in range(50):
        id_list.append(int(all_students_list[i][1]))
    return id_list


def CGPAmergesort(theIDs, mydict):
    dictlen = len(theIDs)

    if dictlen < 2:
        return theIDs

    leftID = theIDs[:dictlen // 2]
    rightID = theIDs[dictlen // 2:]

    leftID = CGPAmergesort(leftID, mydict)
    rightID = CGPAmergesort(rightID, mydict)

    return CGPAmerge(leftID , rightID, mydict)

def CGPAmerge(leftID , rightID, mydict):
    resultIDlist = []

    while leftID and rightID:
        L = leftID[0]
        R = rightID[0]

        if float(mydict[L][5]) >= float(mydict[R][5]):
            resultIDlist.append(L)
            leftID.pop(0)
        else:
            resultIDlist.append(R)
            rightID.pop(0)

    if leftID:
        resultIDlist.extend(leftID)
    else:
        resultIDlist.extend(rightID)

    return resultIDlist


def initialise_groups():
    group_dict = {}
    for i in range(10):
        group_dict[f"Group{i}"] = []
    return group_dict


def init_high_low_GPA(sorted_CGPA):
    high_GPA = []
    low_GPA = []
    for i in range(10):
        high_student = sorted_CGPA[0]
        high_GPA.append(high_student)
        sorted_CGPA.remove(high_student)

        low_student = sorted_CGPA[-1]
        low_GPA.append(low_student)
        sorted_CGPA.remove(low_student)
    return high_GPA, low_GPA


def init_school_dict(sorted_CGPA, students_dict):
    school_dict = {}
    for i in range(30):
        school = students_dict.get(sorted_CGPA[i])[2]
        if school not in school_dict:
            school_dict[school] = 1
        else:
            school_dict[school] += 1
    return school_dict


def find_popular_schools(school_dict):
    popular_schools = []
    count = 0

    while count < 10:
        school = max(school_dict,key=school_dict.get)
        no_of_students = school_dict[school]
        count += no_of_students
        popular_schools.append(school)
        school_dict.pop(school)

    return popular_schools


def distribute_schools(sorted_CGPA, popular_schools, students_dict, group_dict):
    delete_list = []
    counter = 0
    for i in range(len(sorted_CGPA)):
        if students_dict[sorted_CGPA[i]][2] in popular_schools:
            if counter == 10:
                break
            group_dict[f"Group{counter}"].append(students_dict[sorted_CGPA[i]])
            delete_list.append(sorted_CGPA[i])
            counter+=1

    for i in delete_list:
        sorted_CGPA.remove(i)


def distribute_gender(sorted_CGPA, students_dict, group_dict):
    male_list = []
    female_list = []

    for i in sorted_CGPA:
        if students_dict[i][4] == "Male":
            male_list.append(i)
        else:
            female_list.append(i)

    for i in group_dict:
        if group_dict[i][0][4] == "Male":
            if len(female_list) > 0:
                group_dict[i].append(students_dict[female_list[0]])
                sorted_CGPA.remove(female_list[0])
                female_list.remove(female_list[0])
            else:
                group_dict[i].append(students_dict[male_list[0]])
                sorted_CGPA.remove(male_list[0])
                male_list.remove(male_list[0])

        else:
            if len(male_list) > 0:
                group_dict[i].append(students_dict[male_list[0]])
                sorted_CGPA.remove(male_list[0])
                male_list.remove(male_list[0])
            else:
                group_dict[i].append(students_dict[female_list[0]])
                sorted_CGPA.remove(female_list[0])
                female_list.remove(female_list[0])


def distribute_high_GPA(high_GPA, students_dict, group_dict):
    for i in range(len(high_GPA)):
        group_dict[f"Group{9-i}"].append(students_dict[high_GPA[i]])


def distribute_low_GPA(low_GPA, students_dict, group_dict):
    for i in range(len(low_GPA)):
        group_dict[f"Group{i}"].append(students_dict[low_GPA[i]])


def evaluate_priority(group_dict):
    flagged_groups = []

    for i in group_dict:
        male = 0
        female = 0
        for j in group_dict[i]:
            if j[4] == "Male":
                male += 1
            else:
                female += 1

        if male >= 3 or female >= 3:
            str = ""
            if male > female:
                str = "Male"
            else:
                str = "Female"
            flagged_groups.append([i, str])
    return flagged_groups


def distribute_to_flagged(flagged_groups, sorted_CGPA, students_dict, group_dict):
    delete_list = []
    for i in sorted_CGPA:
        for j in flagged_groups:
            if len(group_dict[j[0]]) != 5:
                if students_dict[i][4] != j[1]:
                    delete_list.append(i)
                    group_dict[j[0]].append(students_dict[i])
                    break

    for i in delete_list:
        sorted_CGPA.remove(i)

def distribute_remaining(sorted_CGPA, students_dict, group_dict):
    index = 0
    for i in range(10):
        if len(group_dict[f"Group{i}"]) < 5:
            group_dict[f"Group{i}"].append(students_dict[sorted_CGPA[index]])
            index += 1

def lazy_distribute_remaining(sorted_CGPA, students_dict, group_dict):
    index = 0
    for i in group_dict:
        group_dict[i].append(students_dict[sorted_CGPA[index]])
        index+=1


def formatting_for_export(group_dict):
    result_list = []
    string = ""
    for i in group_dict:
            for k in group_dict[i]:
                k.append(i)

    for i in group_dict:
        for j in group_dict[i]:
            for k in j:
                string += str(k)
                string += ","
            string = string[:-1]
            string += "\n"
            result_list.append(string)
            string = ""
    return result_list

def export(results):
    with open("FCE2_Team1.csv", "a",newline="") as results_file:
        for i in results:
            results_file.write(i)

def analysis(tut_grp, students_dict, group_dict, id_list):
    # ANALYSIS
    group_gpa = []
    group_gender = []
    group_school = []

    for i in group_dict:
        temp_gpa = 0
        for j in group_dict[i]:
            temp_gpa += j[5]

        # GPA ANALYSIS
        group_gpa.append(round(temp_gpa/5, 2))

        # GENDER ANALYSIS
        male = 0
        female = 0
        for j in group_dict[i]:
            if j[4] == "Male":
                male += 1
            else:
                female += 1

        if male >= 4 or female >= 4:
            str = ""
            if male > female:
                str = "Male"
            else:
                str = "Female"
            group_gender.append([i, str])

        # SCHOOL ANALYSIS
        schools = []
        for j in group_dict[i]:
            schools.append(j[2])
        if len(set(schools)) <= 2:
            group_school.append([i])

    # TOTAL STATISTICS OF ONE TUTORIAL GROUP
    total_gpa = 0
    male = 0
    female = 0
    for i in id_list:
        total_gpa += students_dict[i][5]
        if students_dict[i][4] == "Male":
            male += 1
        else:
            female += 1
    ave_gpa = round(total_gpa/50, 2)
    max_dev = round(max(abs(gpa - ave_gpa) for gpa in group_gpa), 2)


    all_deviations.append(max_dev)
    if group_gender:
        all_genders.append([tut_grp, group_gender])

    if group_school:
        for i in group_school:
            all_schools.append(group_dict[i[0]])


def total_analysis():
    count = 0
    for i in all_genders:
        count += len(i[1])
    print()
    print("EFFECTIVENESS")
    print(f"GENDER: {100-round(count*100/1200, 2)}% PASSES")
    print(f"SCHOOLS: {100-round(len(all_schools)*100/1200 ,2)}% PASSES")
    print(f"MAXIMUM DEVIATION: {max(all_deviations)} POINTS")
    print()


if __name__ == "__main__":
    main()