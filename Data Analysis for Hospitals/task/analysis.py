import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option("display.max_columns", 15)

general = pd.read_csv("C:/my_courses/Jetbrains_academy/test/general.csv")
prenatal = pd.read_csv("C:/my_courses/Jetbrains_academy/test/prenatal.csv")
sports = pd.read_csv("C:/my_courses/Jetbrains_academy/test/sports.csv")

# print(general.head())
# print(prenatal.head())
# print(sports.head())
# Stage 2/5: Merge them!


prenatal.rename(columns={"HOSPITAL":'hospital', 'Sex':'gender'}, inplace=True)
sports.rename(columns={'Hospital':'hospital', 'Male/female':'gender'}, inplace=True)

# print(general.head())
# print(prenatal.head())
# print(sports.head())

df = pd.concat([general, prenatal, sports], ignore_index=True)
df.drop(columns='Unnamed: 0', inplace=True)
#print(df.sample(n=20, random_state=30))


# Stage 3/5: Improve your dataset

df.dropna(how='all', inplace=True)
#print(df.sample(n=20, random_state=30))

# replacing 'woman' or 'female' in gender column by 'f' and the same for 'male' and 'man'
df.loc[np.logical_or(df['gender']=='female', df['gender'] == 'woman'), 'gender'] = 'f'
df.loc[np.logical_or(df['gender']=='male', df['gender'] == 'man'), 'gender'] = 'm'

# replacing the empty gender column values for prenatal patients with 'f'
condition = np.logical_and(df['hospital']=='prenatal', df['gender'].isna())
df.loc[condition, "gender"] = 'f'

# filling the missing values with 0
values = {"bmi":0, "diagnosis":0, "blood_test":0, "ecg":0, "ultrasound":0, "mri":0, "xray":0, "children":0, "months":0}
df.fillna(value=values, inplace=True)

#df[np.logical_or(df['gender'] == 'male', df['gender'] == 'man')] = 'm'

# print(df.shape)
# print(df.sample(n=20, random_state=30))


# Stage 4/5: The Statistics

"1- which hospital has the highest number of patients?"
group = df.groupby('hospital').apply(lambda x : x.count())['hospital']


#print(df.head())

#print("The answer to the 1st question is general")

"2- What share of the patients in the general hospital suffers from stomach-related issues?"

log1 = np.logical_and(df["hospital"]=='general', df['diagnosis']=='stomach')
cond = df["hospital"]=='general'
share = df.loc[log1, 'hospital'].count() / df.loc[cond,"hospital"].count()

#print(f"The answer to the 2nd question is {round(share, 3)}")

"3-What share of the patients in the sports hospital suffers from dislocation-related issues?"

cond1 = np.logical_and(df['hospital']=='sports', df['diagnosis']=='dislocation')
cond2 = df['hospital']=='sports'

share3 = df.loc[cond1,'hospital'].count() / df.loc[cond2, "hospital"].count()

#print(f"The answer to the 3rd question is {round(share3, 3)}")

"4- What is the difference in the median ages of the patients in the general and sports hospitals?"

median1 = np.median(df.loc[df['hospital'] == 'general', 'age'])
median2 = np.median(df.loc[df['hospital'] == 'sports', 'age'])
#print(f'The answer to the 4th question is {round(median1-median2, 3)}')

"5-In which hospital the blood test was taken the most often, how many blood test was taken?"

new_df = df.melt(id_vars='blood_test', value_vars='hospital')
list_1 = ['general','prenatal','sports']
test_g = new_df.loc[(new_df['value']=='general') & (new_df['blood_test']=='t'),"value"].count()
test_p = new_df.loc[(new_df['value']=='prenatal') & (new_df['blood_test']=='t'),"value"].count()
test_s = new_df.loc[(new_df['value']=='sports') & (new_df['blood_test']=='t'),"value"].count()

list_2 = [test_g, test_p, test_s]
hos_type = list_1[list_2.index(max(list_2))]
#print(f"The answer to the 5th question is {hos_type}, {max(list_2)} blood tests")


# Stage 5/5: Visualize it!

"1- What is the most common age of a patient among all hospitals?"
df.age.hist(bins=[0, 15, 35, 55, 70, 80])
plt.show()
print("The answer tot the 1st question: 15-35")

"2-What is the most common diagnosis among patients in all hospitals?"
df.groupby("diagnosis").size().plot(kind='pie')
plt.show()
print("The answer to the 2nd question: pregnancy")

"3- Violin plot of height distribution by hospitals"
sns.violinplot(x=df.hospital, y=df.height)
print("The answer to the 3rd question: It's because the height values are in feet rather than in meters")
plt.show()














