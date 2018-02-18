import os
import glob
import pandas as pd
import ipaddress

# The header of the UFW log files
names = ["Timestamp", "Customer ID", "Host", "Log file", "Log sequence no.", "Entry type", "Entry identifier",
         "User,if", "Reporting IP/host", "Source IP,if", "Source port,if", "Destination IP, if", "Destination Port, if",
         "Text field1", "Text field2", "Text field3", "Numeric field1", "Numeric field2"]

# Raw path of the ufw logs
path = r'C:\Users\Rahul\Desktop\Logs'
all_logs = glob.glob(os.path.join(path, "*.csv"))

# Show all the found log files
for i in all_logs:
    print(i, "\n", end="")

dfa = []
# Concatenating all log files into one
for f in all_logs:
    df = pd.read_csv(f, header=None)
    dfa.append(df)
result = pd.concat(dfa)
result.to_csv('res.csv')

# Dropping unwanted columns
result.drop(result.columns[[0, 1, 2, 3, 4, 5, 6, 7, 8, 14, 15, 16, 17]], axis=1, inplace=True)
result = result.T.reset_index(drop=True).T

# Converting IP Address to int form
result[0] = result[0].map(lambda x: (ipaddress.IPv4Address(x)))
# Another DF with only unique pings
unik = result.drop_duplicates(subset=0)

# Melting data to find counter
melt = pd.value_counts(result[0].values, sort=False)
print(type(melt))
'''
for k in result:
    print(k, "\t\t", end="")
'''