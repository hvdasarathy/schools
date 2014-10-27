import sys
import urllib
import zipfile
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import PySide.QtGui as qtgui
from data_wrangler import data_wrangler

#Load the data file generated from data_wrangler.py that has cleaned up the usable data.

try:
    data = pd.read_csv('relevant_data.csv')

except IOError:
    data_wrangler()
    data = pd.read_csv('relevant_data.csv')

zip_state = pd.read_table('sc102a.txt', usecols = (17, 18))

#We use a metric where we take the mean of the reading and math proficiency percentages as done below.
school_score = []

for i in range(0, len(data)):
    try:
        math = int(data['math_prof'][i][-2:])
    except ValueError:
        math = 1

    try:
        read = int(data['read_prof'][i][-2:])
    except ValueError:
        read = 1
    school_score.append((math + read)/2.0)

nat_mean = np.mean(school_score)

#Add this array to the dataset.
data['school_scores'] = pd.Series(school_score)
#print data
#<<<<Begin UI generation>>>>

class zip_school(qtgui.QWidget):

    def __init__(self):
        super(zip_school, self).__init__()

        self.initUI()

    def initUI(self):

#Add the features that we need for the UI
        lned = qtgui.QLineEdit(self)
        lned.move(100, 100)

        lbl = qtgui.QLabel(self)
        lbl.setText("Enter Zip Code:")
        lbl.move(15, 100)

        btn = qtgui.QPushButton("Search", self)
        btn.setText("Search")
        btn.move(100, 130)
#Connect on clicking of the button to the function that outputs the desired results.
        btn.clicked.connect(lambda: self.score_out(lned))

        self.setGeometry(200, 200, 600, 450)
        self.show()

#Begin the main output function:
    def score_out(self, givenlned):
#Find where in the dataset the input zip code lies.

#Create a Message Box Widget for use later.
        msgbox = qtgui.QMessageBox(self)

        try:
            num = np.where(np.array(data['zip_codes']) == int(givenlned.text()))[0]
        except ValueError:
            msgbox.setText("Please enter a valid zip code.")
            msgbox.show()
        zip_scores = []
        names = []


#If the given zip code does not exist in the given array run a secondary check to see if the
#zip code is a valid school district.
        if len(num) == 0:
            sec_check = np.where(zip_state['LZIP'] == int(givenlned.text()))[0]
            if len(sec_check) == 0:
                msgbox.setText("Please enter a valid zip code.")
                msgbox.show()
            else:
#This message is outputted if the zip code is accurate but there is insufficient/absent data.
#If the zip code is indeed valid, check which state this zip code is in and output the mean of all school scores for that state.
                state = zip_state['LSTATE'][sec_check[0]]
                state_rec = np.where(data['state'] == state)[0]
                state_mean = np.round(np.mean(data['school_scores'][state_rec]),2)

                txt = "Oops! Looks like this zip code is not in our database or has insufficent data. However, the state mean for " + state + ' = ' + str(state_mean)
                msgbox.setText(txt)
                msgbox.show()

        else:
        #Show the table if there exist records of the schools in that zip code.

        #Isolate the state-wide values

            state = data['state'][num[0]]
            state_schools = np.where(data['state'] == state)[0]
            state_mean = np.mean(data['school_scores'][state_schools])

            #Generate and populate the table widget with:

            #1. The school ID
            #2. The School Name
            #3. The School Score
            #4. The Percentage Difference of the school score from the state's mean score

            tabwidget = qtgui.QTableWidget(len(num) + 1, 4, self)
            tabwidget.setHorizontalHeaderLabels(['School ID', 'School Name', 'School Score', 'State Mean Deviation'])
            tabwidget.setVerticalHeaderItem(len(num), qtgui.QTableWidgetItem('Zip Code Average'))
            row = 0

            for row in range(len(num)):

                #Add the school IDs
                item1 = qtgui.QTableWidgetItem(str(data['ncessch_id'][num[row]]))
                tabwidget.setItem(row, 0, item1)

                ##The school names
                item2 = qtgui.QTableWidgetItem(str(data['school_name'][num[row]]))
                tabwidget.setItem(row, 1, item2)
                names.append(str(data['school_name'][num[row]]))

                #The school scores computed above
                item3 = qtgui.QTableWidgetItem(str(data['school_scores'][num[row]]))
                tabwidget.setItem(row, 2, item3)
                zip_scores.append(data['school_scores'][num[row]])

                #The deviation from the state mean for each school
                item4 = qtgui.QTableWidgetItem(str(np.round((100*(data['school_scores'][num[row]]-state_mean)/state_mean), 2)))
                tabwidget.setItem(row, 3, item4)

            #The mean of all school scores in the zip code
            item5 = qtgui.QTableWidgetItem(str(np.round(np.mean(data['school_scores'][num]),2)))
            tabwidget.setItem(len(num), 2, item5)
            zip_mean = np.round(np.mean(data['school_scores'][num]),2)

            #The mean deviation from the state mean of the zip code
            item6 = qtgui.QTableWidgetItem(str(np.round(np.mean(100*(data['school_scores'][num]-state_mean)/state_mean),2)))
            tabwidget.setItem(len(num), 3, item6)

            tabwidget.setColumnWidth(3, 100)
            tabwidget.setGeometry(15, 170,450,200)

#Now add a button that adds a plotting functionality to data in the table
            newbtn = qtgui.QPushButton("Plot this!", self)
            newbtn.setText("Plot this!")
            newbtn.move(350, 380)

            tabwidget.show()
            newbtn.show()

            newbtn.clicked.connect(lambda: self.plot(zip_scores, state_mean, zip_mean, names, givenlned))

    def plot(self, array, num1, num2, nms, givenlned):

        #Create the plot for the zip code
        plt.scatter([i for i in range(len(array))],array, s = 50)
        plt.hlines(num1, -3, len(array) + 3, linestyles = 'dashed')
        plt.hlines(num2, -3, len(array) + 3, linestyles = 'dotted')
        plt.hlines(nat_mean, -3, len(array) + 3, color = 'red')
        plt.title("School Scores in the Zip Code " + givenlned.text())
        plt.xlabel("Schools")
        plt.ylabel("Scores")
        plt.legend(["School Scores","State Mean", "Zip Mean", "National Mean"], fontsize = 9)

        plt.gca().xaxis.set_major_locator(plt.NullLocator())

        for i in range(len(nms)):
            plt.text(i, array[i] + 0.3, nms[i], fontsize = 8)

        plt.show()

def main():

    app = qtgui.QApplication(sys.argv)
    ex = zip_school()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()