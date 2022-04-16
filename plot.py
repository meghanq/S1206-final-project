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
        sorted_rec_count = sorted(rec_count_lst)
        sorted_avg = sorted(avg_lst)

        plt.scatter(sorted_rec_count, sorted_avg)
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
        sorted_rec_count = sorted(rec_count_lst)
        sorted_avg = sorted(avg_lst)
    plt.bar(sorted_rec_count, sorted_avg)
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
    return corr

def createPieChart1():
    base_path = os.path.abspath(os.path.dirname(__file__))
    full_path = os.path.join(base_path, "rec_count.csv")
    with open(full_path) as fileref:
        lines = fileref.readlines()
        rec_count_lst = []
        for line in lines[1:]:
            row = line.split(',')
            rec_count = int(row[1])
            qol_avg = float(row[2])
            if qol_avg > 6:
                rec_count_lst.append(rec_count)
    plt.pie(rec_count_lst, labels = rec_count_lst)
    plt.axis('equal')
    plt.title('Number of Rec Areas for QoL Ratings above 6')
    plt.show()


def createPieChart2():
    base_path = os.path.abspath(os.path.dirname(__file__))
    full_path = os.path.join(base_path, "rec_count.csv")
    with open(full_path) as fileref:
        lines = fileref.readlines()
        rec_count_lst = []
        for line in lines[1:]:
            row = line.split(',')
            rec_count = int(row[1])
            qol_avg = float(row[2])
            if qol_avg < 5:
                rec_count_lst.append(rec_count)
    plt.pie(rec_count_lst, labels = rec_count_lst)
    plt.axis('equal')
    plt.title('Number of Rec Areas for QoL Ratings below 5')
    plt.show()




def main():
    create_scatter_plot()
    create_bar_chart()
    # correlationCalc()
    # createPieChart()
    # createPieChart2()

if __name__ == "__main__":
    main()