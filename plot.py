import os
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

def create_scatter_plot():

    base_path = os.path.abspath(os.path.dirname(__file__))
    full_path = os.path.join(base_path, "rec_count.csv")
    with open(full_path) as fileref:
        lines = fileref.readlines()
        rec_count_lst = []
        avg_lst = []
        for line in lines[1:]:
            row = line.split(',')
            rec_count = int(row[1])
            qol_avg = float(row[2])
            rounded = round(qol_avg,2)
            if rec_count < 25:
                rec_count_lst.append(rec_count)
                avg_lst.append(rounded)
            else:
                continue

        plt.scatter(rec_count_lst, avg_lst)
        plt.xlabel('Count of Recreation Areas')
        plt.ylabel('Average Quality of Life Rating (Out of 10)')
        plt.title('Average Quality of Life vs Count of Recreation Areas')
        plt.show()

def create_bar_chart():
    base_path = os.path.abspath(os.path.dirname(__file__))
    full_path = os.path.join(base_path, "rec_count.csv")
    with open(full_path) as fileref:
        lines = fileref.readlines()
        rec_count_lst = []
        avg_lst = []
        for line in lines[1:]:
            row = line.split(',')
            rec_count = int(row[1])
            qol_avg = float(row[2])
            rounded = round(qol_avg,2)
            if rec_count < 25:
                rec_count_lst.append(rec_count)
                avg_lst.append(rounded)
            else:
                continue
    plt.bar(rec_count_lst, avg_lst, color = 'g')
    plt.xlabel('Count of Recreation Areas')
    plt.ylabel('Average Quality of Life Ratings (Out Of 10)')
    plt.title('Average Quality of Life Ratings vs Recreation Areas')
    plt.show()


def correlationCalc(): 
    base_path = os.path.abspath(os.path.dirname(__file__))
    full_path = os.path.join(base_path, "rec_count.csv")
    with open(full_path) as fileref:
        lines = fileref.readlines()
        rec_count_lst = []
        avg_lst = []
        for line in lines[1:]:
            row = line.split(',')
            rec_count = int(row[1])
            qol_avg = float(row[2])
            rounded = round(qol_avg,2)
            rec_count_lst.append(rec_count)
            avg_lst.append(rounded)

    corr = pearsonr(rec_count_lst, avg_lst)
    print(corr[0])
    return corr[0]

def createPieChart1():
    base_path = os.path.abspath(os.path.dirname(__file__))
    full_path = os.path.join(base_path, "rec_count.csv")
    with open(full_path) as fileref:
        lines = fileref.readlines()
        rec_count_lst = {}
        rec_count_lst["0-4"] = 0
        rec_count_lst["5-9"] = 0
        rec_count_lst["10-14"] = 0
        rec_count_lst["15-19"] = 0
        rec_count_lst["20+"] = 0
        for line in lines[1:]:
            row = line.split(',')
            rec_count = int(row[1])
            qol_avg = float(row[2])
            if qol_avg > 6:
                if rec_count <= 4 and rec_count >= 0:
                    rec_count_lst["0-4"] += 1
                elif rec_count <= 9 and rec_count >= 4:
                    rec_count_lst["5-9"] += 1
                elif rec_count <= 14 and rec_count >= 9:
                    rec_count_lst["10-14"] += 1
                elif rec_count <= 19 and rec_count >= 15:
                    rec_count_lst["15-19"] += 1
                else:
                    rec_count_lst["20+"] += 1
    plt.pie(list(rec_count_lst.values()), labels = list(rec_count_lst.keys()))
    plt.axis('equal')
    plt.title('Number of Rec Areas for QoL Ratings above 6')
    plt.show()


def createPieChart2():
    base_path = os.path.abspath(os.path.dirname(__file__))
    full_path = os.path.join(base_path, "rec_count.csv")
    with open(full_path) as fileref:
        lines = fileref.readlines()
        rec_count_lst = {}
        rec_count_lst = {}
        rec_count_lst["0-2"] = 0
        rec_count_lst["3-5"] = 0
        rec_count_lst["6-8"] = 0
        rec_count_lst["9-11"] = 0
        rec_count_lst["12+"] = 0
        for line in lines[1:]:
            row = line.split(',')
            rec_count = int(row[1])
            qol_avg = float(row[2])
            if qol_avg < 5:
                if rec_count <= 2 and rec_count >= 0:
                    rec_count_lst["0-2"] += 1
                elif rec_count <= 5 and rec_count >= 3:
                    rec_count_lst["3-5"] += 1
                elif rec_count <= 8 and rec_count >= 6:
                    rec_count_lst["6-8"] += 1
                elif rec_count <= 11 and rec_count >= 9:
                    rec_count_lst["9-11"] += 1
                else:
                    rec_count_lst["12+"] += 1
    plt.pie(list(rec_count_lst.values()), labels = list(rec_count_lst.keys()))
    plt.axis('equal')
    plt.title('Number of Rec Areas for QoL Ratings below 5')
    plt.show()




def main():
    create_scatter_plot()
    create_bar_chart()
    correlationCalc()
    createPieChart1()
    createPieChart2()

if __name__ == "__main__":
    main()