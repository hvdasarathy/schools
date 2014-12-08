from flask import Flask, request, url_for, render_template
from flask_bootstrap import Bootstrap
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv('/home/hvdasarathy/mysite/relevant_data.csv')
zip_state = pd.read_table('/home/hvdasarathy/mysite/sc102a.txt', usecols = (17, 18))

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

def create_app():

    app = Flask(__name__, template_folder = '/home/hvdasarathy/mysite/templates/')
    app.secret_key = 'This is really unique and secret'
    Bootstrap(app)

    return app

app = create_app()

@app.route('/')
def input_zip():

    return render_template('index.html', results = url_for('output_schools'))

@app.route('/greet', methods=['POST'])
def output_schools():

    try:
        num = np.where(np.array(data['zip_codes']) == int(request.form["zip"]))[0]
    except ValueError:
        return render_template('error.html', home = url_for('input_zip'))

    if len(num) == 0:
        sec_check = np.where(zip_state['LZIP'] == int(request.form["zip"]))[0]
        if len(sec_check) == 0:
            return render_template('error.html', home = url_for('input_zip'))
        else:

            state = data['state'][num[0]]
            state_schools = np.where(data['state'] == state)[0]
            state_mean = np.mean(data['school_scores'][state_schools])

            return render_template('insufficient.html',state = state, state_mean = state_mean, home = url_for('input_zip'))
    else:
        state = data['state'][num[0]]
        state_schools = np.where(data['state'] == state)[0]
        state_mean = np.mean(data['school_scores'][state_schools])

        rows = len(num)
        output = [['School ID', 'School Name', 'School Score', 'State Mean Deviation']]
        for i in range(rows):
            array = []
            array.append(data['ncessch_id'][num[i]])
            array.append(data['school_name'][num[i]])
            array.append(data['school_scores'][num[i]])
            array.append(np.round((100*(data['school_scores'][num[i]]-state_mean)/state_mean), 2))

            output.append(array)

        score_average = np.mean([output[i][2] for i in range(1, len(output))])
        dev_average = np.mean([output[i][3] for i in range(1, len(output))])

        fig = plt.figure()
        plt.scatter([i for i in range(1, len(output))],[output[i][2] for i in range(1, len(output))], s = 50)
        plt.hlines(score_average, 0, len(output), linestyles = 'dashed')
        plt.hlines(state_mean, 0, len(output), linestyles = 'dotted')
        plt.hlines(nat_mean, -3, len(array) + 3, color = 'red')
        plt.title("School Scores in the Zip Code " + request.form["zip"])
        plt.xlabel("Schools")
        plt.ylabel("Scores")
        plt.legend(["School Scores","State Mean", "Zip Mean", "National Mean"], fontsize = 9)

        plt.gca().xaxis.set_major_locator(plt.NullLocator())

        for i in range(1,len(output)):
            plt.text(i, output[i][2] + 0.3, output[i][1], fontsize = 8)


        return render_template('table.html', output = output, n= rows, score_average = score_average, dev_average = dev_average, home=url_for('input_zip'))
