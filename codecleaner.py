# Team 1 LendingClub primary notebook
# import dependencies
from matplotlib.ticker import FormatStrFormatter
import pandas as pd
import numpy as np  # needed for replace nan code below
import glob
import matplotlib.pyplot as plt
# from datetime import datetime

# pull in all csvs and merge them into a single dataframe
bigdf = pd.concat([pd.read_csv(f, low_memory=False, usecols=[
    'issue_d', 'loan_amnt', 'term', 'int_rate', 'installment',
    'emp_length', 'home_ownership', 'annual_inc', 'open_acc',
    'grade', 'addr_state', 'delinq_amnt', 'loan_status', 'tot_cur_bal'
]) for f in glob.glob('data/LoanStats*.csv')], ignore_index=True)

# drop all the empty rows
bigdf.dropna(subset=['term', 'issue_d'], inplace=True)

date_dictionary = {
    "Dec-18": 12,
    "Nov-18": 11,
    "Oct-18": 10,
    "Sep-18": 9,
    "Aug-18": 8,
    "Jul-18": 7,
    "Jun-18": 6,
    "May-18": 5,
    "Apr-18": 4,
    "Mar-18": 3,
    "Feb-18": 2,
    "Jan-18": 1,
}

bigdf["month_num"] = ""  # create new column
bigdf["month_num"] = bigdf["issue_d"].map(date_dictionary)  # map month numbers
bigdf["month_num"] = bigdf["month_num"].round(0).astype(int)  # convert to int from float

grade_dictionary = {
    "G": 7,
    "F": 6,
    "E": 5,
    "D": 4,
    "C": 3,
    "B": 2,
    "A": 1,
}

bigdf["grade_num"] = ""  # create new column
bigdf["grade_num"] = bigdf["grade"].map(grade_dictionary)  # map grade numbers
bigdf["grade_num"] = bigdf["grade_num"].round(0).astype(int)  # convert to int from float

bigdf_int_grade = bigdf.loc[:, ["loan_amnt", "month_num", "int_rate", "grade_num"]]
bigdf_int_grade['int_rate'].astype('str')
bigdf_int_grade['int_rate'] = bigdf_int_grade['int_rate'].str.replace('%', '')
bigdf_int_grade['int_rate'] = bigdf_int_grade['int_rate'].apply(pd.to_numeric)

bigdf_int_grade_A = bigdf_int_grade[bigdf_int_grade['grade_num'] == 1]
bigdf_int_grade_A = bigdf_int_grade_A.groupby(['month_num'])['int_rate'].mean()
grade_A = list(bigdf_int_grade_A)

bigdf_int_grade_B = bigdf_int_grade[bigdf_int_grade['grade_num'] == 2]
bigdf_int_grade_B = bigdf_int_grade_B.groupby(['month_num'])['int_rate'].mean()
grade_B = list(bigdf_int_grade_B)

bigdf_int_grade_C = bigdf_int_grade[bigdf_int_grade['grade_num'] == 3]
bigdf_int_grade_C = bigdf_int_grade_C.groupby(['month_num'])['int_rate'].mean()
grade_C = list(bigdf_int_grade_C)

bigdf_int_grade_D = bigdf_int_grade[bigdf_int_grade['grade_num'] == 4]
bigdf_int_grade_D = bigdf_int_grade_D.groupby(['month_num'])['int_rate'].mean()
grade_D = list(bigdf_int_grade_D)

bigdf_int_grade_E = bigdf_int_grade[bigdf_int_grade['grade_num'] == 5]
bigdf_int_grade_E = bigdf_int_grade_E.groupby(['month_num'])['int_rate'].mean()
grade_E = list(bigdf_int_grade_E)

bigdf_int_grade_F = bigdf_int_grade[bigdf_int_grade['grade_num'] == 6]
bigdf_int_grade_F = bigdf_int_grade_F.groupby(['month_num'])['int_rate'].mean()
grade_F = list(bigdf_int_grade_F)

bigdf_int_grade_G = bigdf_int_grade[bigdf_int_grade['grade_num'] == 7]
bigdf_int_grade_G = bigdf_int_grade_G.groupby(['month_num'])['int_rate'].mean()
grade_G = list(bigdf_int_grade_G)

print(bigdf_int_grade_A)
# Create a list of the months that we will use as our x axis
months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
intmarks = [5, 10, 15, 20, 25, 30]

x = np.arange(1, 13)

fig = plt.figure()
fig.show()
ax = fig.add_subplot(111)

ax.plot(x, grade_A, c='red', label='A')
ax.plot(x, grade_B, c='orange', label='B')
ax.plot(x, grade_C, c='yellow', label='C')
ax.plot(x, grade_D, c='green', label='D')
ax.plot(x, grade_E, c='blue', label='E')
ax.plot(x, grade_F, c='indigo', label='F')
ax.plot(x, grade_G, c='violet', label='G')
ax.yaxis.set_major_formatter(FormatStrFormatter('%.0f%%'))
ax.xaxis.set_ticks(np.arange(1, 13, 1))
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.draw()
plt.show()
