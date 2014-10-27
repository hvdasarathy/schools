import pandas as pd
import numpy as np
import urllib
import zipfile

#The file below maps the NCESSCH ID of a school with the zip code of the school.
def data_wrangler():
    url = 'http://nces.ed.gov/ccd/Data/zip/sc102a_txt.zip'
    urllib.urlretrieve(url, 'sc102a_txt.zip')
    zipfile.ZipFile('sc102a_txt.zip').extractall()
    id_zip_map  = pd.read_table('sc102a.txt', usecols = (1, 17, 18))

    #Now. call the standard math and test results for schools in the nation.

    url1 = 'https://inventory.data.gov/dataset/d78fbf42-64ed-4988-ba19-c8b9d83a960e/resource/d684f5ca-fe78-40b5-93d3-71ba940f13b0/download/achvmntrsltsstateassmtsmathssy2010-11.csv'
    obj = urllib.urlopen(url1)
    math_test = pd.read_csv(obj, usecols =(4,5,6,7))
    print len(math_test)

    url2 = 'https://inventory.data.gov/dataset/d1f40ea1-0cda-49e1-8d12-3128c115db20/resource/b8160d45-b9b9-443c-8157-f381d6b90e42/download/achvmntrsltsstateassmtsrlasy201011.csv'
    obj2 = urllib.urlopen(url2)
    read_test = pd.read_csv(obj2, usecols = (4, 6, 7))
    print len(read_test)

    #Note: The two links above work very poorly when the internet connection is not good.
    #If that is the case it would probably better to simply go to the above links,
    #download the files and read them as shown in the following two lines.
    #As a check, the variable math_test should have length 91079 and the variable
    #read_test should have length 91121. All of the following code will work irrespective
    #of the lengths but in that case all the analysis will only be on a subset of the data.

    #math_test = pd.read_csv('achvmntrsltsstateassmtsmathssy201011.csv',usecols = (4, 5, 6, 7))
    #read_test = pd.read_csv('achvmntrsltsstateassmtsrlasy201011.csv',usecols = (4, 6, 7))

    sch_name = ['school_name']
    state = ['state']
    ncessch_id = ['ncessch_id']
    zip_codes = ['zip_codes']
    math_num = ['math_num']
    math_prof = ['math_prof']
    read_num = ['read_num']
    read_prof = ['read_prof']

    #We can only look at schools for which we have all the requisite data and so choose the intersection from the three data sets.
    valid_schools2 = set.intersection(*[set(math_test['ncessch']),set(read_test['ncessch']), set(id_zip_map['NCESSCH'])])
    #print len(valid_schools2)

    counter = 0
    #Having isolated the schools that we have data for, we pull the required information for each school.
    for x in valid_schools2:

        print counter

        num1 = np.where(np.array(id_zip_map['NCESSCH']) == x)[0][0]
        num2 = np.where(np.array(math_test['ncessch']) == long(x))[0][0]
        num3 = np.where(np.array(read_test['ncessch']) == long(x))[0][0]

        if math_test['ALL_MTH00numvalid_1011'][num2] >= 200  and read_test['ALL_RLA00numvalid_1011'][num3] >= 200:
    #Add this schools where there are atleast 200 hundred valid scores on the reading and writing
    #Add all the required information from the given datasets
            ncessch_id.append(x)
            zip_codes.append(id_zip_map['LZIP'][num1])
            state.append(id_zip_map['LSTATE'][num1])

            sch_name.append(math_test['schnam10'][num2])
            math_num.append(str(math_test['ALL_MTH00numvalid_1011'][num2]))
            math_prof.append(str(math_test['ALL_MTH00pctprof_1011'][num2]))

            read_num.append(str(read_test['ALL_RLA00numvalid_1011'][num3]))
            read_prof.append(str(read_test['ALL_RLA00pctprof_1011'][num3]))

        counter = counter + 1
    #This loop is more clerical and designed to make later code simpler so that each entry has length 2.
    for i in range(1, len(math_prof)):

        if len(str(math_prof[i])) == 1:
            math_prof[i] = '0' + math_prof[i]

        if len(str(read_prof[i])) == 1:
            read_prof[i] = '0' + read_prof[i]

        if ',' in sch_name[i]:
            sch_name[i] = sch_name[i].replace(',', '')

        print i

    relevant_data = []
    relevant_data.append(ncessch_id)
    relevant_data.append(sch_name)
    relevant_data.append(zip_codes)
    relevant_data.append(state)
    relevant_data.append(math_num)
    relevant_data.append(math_prof)
    relevant_data.append(read_num)
    relevant_data.append(read_prof)

    print len(math_prof)
    print len(read_prof)
    #Save this relevant data for analysis.
    np.savetxt('relevant_data.csv',np.transpose(relevant_data), delimiter = ',', fmt = '%s')

