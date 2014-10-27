The program built in the attached code takes a zip code as input and outputs
the school score. This school score is defined as the average of the 
percentage of students who were deemed to be at a proficient math level 
and proficient reading level at each school in the zip code.

In addition, the percentage deviation from the state mean is also provided
along with a plotting functionality. 

Note: Only schools with more than 200 valid results for both math and reading 
tests are taken into consideration. 

The file main.py drives the UI and generates the analytics values.

The inputs for main.py are relevant_data.csv and sc102a.txt. The file
relevant_data.csv is generated from data_wrangler.py which corrals all the
required and usable information from different databases into a single 
data file. The file sc102a.txt is also downloaded in data_wrangler.py.

The data can be downloaded from the following links if desired:
1. https://inventory.data.gov/dataset/d78fbf42-64ed-4988-ba19-c8b9d83a960e/resource/d684f5ca-fe78-40b5-93d3-71ba940f13b0/download/achvmntrsltsstateassmtsmathssy2010-11.csv
2. https://inventory.data.gov/dataset/d1f40ea1-0cda-49e1-8d12-3128c115db20/resource/b8160d45-b9b9-443c-8157-f381d6b90e42/download/achvmntrsltsstateassmtsrlasy201011.csv
3. http://nces.ed.gov/ccd/Data/zip/sc102a_txt.zip

The following Python libraries are required to run this code:
1. Pandas
2. NumPy
3. PySide
4. Matplotlib

All of these libraries are freely available for download.

After running the code, simply enter the desired zip code to see the schools
results in said zip code.