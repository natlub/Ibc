import csv

# how to write to a csv

RADEC=[]
reader = csv.reader(open('C:\Users\user\Desktop\\RADECtarg.csv', "rb"))  # 'C:\Users\user\Desktop\data2.csv'
for row in reader:
    RADEC += row
for n in range(0,len(RADEC)/2):
    RADEC[n:n+2]=[' '.join(RADEC[n:n+2])]

with open('C:\Users\user\Desktop\\radec.csv', 'wb') as f:
    writer = csv.writer(f)
    for val in RADEC:
        writer.writerow([val])
