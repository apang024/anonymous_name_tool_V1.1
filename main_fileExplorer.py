# 10 number userID ex:14256 44578
# 00012 81619

#  function?
# h(k) = k mod n
# Here, h(k) is the  value obtained by dividing the key value k by size of  table n using the remainder. It is best that n is a prime number as that makes sure the keys are distributed with more uniformity.
# An example of the Division Method is as follows −

# k=1276
# n=10
# h(1276) = 1276 mod 10
# = 6

# Load pandas
import pandas as pd
import csv
import os
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

print ('Please choose the file you want to anonymize.')
file_path = filedialog.askopenfilename()
folder_path = os.path.split(file_path)[0]
file_name = os.path.basename(file_path).split('/')[-1]

# Initialize variables
names = []
firstName = []
lastName = []
hashAvail = []
netID = []
output = []

# Populate First Name and Last Name arrays
with open('names_1.txt') as f:
    for line in f:
        names.append(line)
        firstName.append(line.split()[0])
        lastName.append(line.split()[1])
        hashAvail.append(1)

# Read csv file
df = pd.read_csv(file_path)
df = df[df.role == 'Student']

# Update column names if necessary
# Enables support for log files from learn.zybooks.com and Mode
df.columns = df.columns.str.replace('\(US/Pacific\)', '', regex=True)
df.columns = df.columns.str.replace('is_submission', 'submission')
df.columns = df.columns.str.replace('content_resource_id', 'lab_id')

# Extract userIDs
for i, row in enumerate(df.itertuples()):
    # Check uniquness of the user_id since they are hashed
    isUnique = 0
    hashedUserID = row.user_id  % len(firstName)
    if (hashAvail[hashedUserID]):
        isUnique = 1
    else:
        print('Multiple rows may have the same name. Please use a larger set of names')
    
    # FIXME: use isUnique to rehash until unique

    # Update original log file
    df.iat[i,5] = firstName[hashedUserID]
    df.iat[i,6] = lastName[hashedUserID]
    df.iat[i,7] = firstName[hashedUserID] + '.' + lastName[hashedUserID] + '@fakeuniv.edu'

    # # Keep an array of ids and names
    # output.append(str(hashedUserID) + ' ' + firstName[hashedUserID] + ' ' + lastName[hashedUserID])

print ('Your anonymized file was placed in the same folder as the given file.')
df.to_csv(folder_path + '/anonymous_' + file_name, index=False)

# with open("output.csv", "w") as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(['name'])
#     writer.writerows(output)