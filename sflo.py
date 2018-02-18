import os
import glob
import pandas as pd
import ipaddress
import matplotlib.pyplot as plt

# The header of the UFW log files
names = ["Timestamp", "Customer ID", "Host", "Log file", "Log sequence no.", "Entry type", "Entry identifier",
         "User,if", "Reporting IP/host", "Source IP,if", "Source port,if", "Destination IP, if", "Destination Port, if",
         "Text field1", "Text field2", "Text field3", "Numeric field1", "Numeric field2"]

# Raw path of the ufw logs
path = r'C:\Users\Rahul\Desktop\Logs'
all_logs = glob.glob(os.path.join(path, "*.csv"))

# Show all the found log files
# for i in all_logs:
#    print(i, "\n", end="")

# Concatenating all log files into one
dfa = []
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
# Melting data to find count of IPs
ip_melt = pd.value_counts(result[0].values, sort=True)
# Melted data to find count of ports Ports
port_melt = pd.value_counts(result[3].values, sort=True)


# Function to print the total number of IP encountered.
def count_unik():
    print(len(unik.index), "IPs")
    
    
# Function to print 'n' first IPs
def unik_ip():
    n = int(input("Enter the 'N'\n"))
    print("The top", n, "IPs are: ")
    print(ip_melt[0:n])


# Function to plot top IPs
def ip_plt():
    n = int(input("Enter the 'N':\n"))
    pplt = ip_melt[:n]
    pplt.plot(kind='bar')
    plt.show()
    
    
# Function to print the top n Ports
def unik_ports():
    n = int(input("Enter the 'N':\n"))
    print(port_melt[0:n])


# Function to print a plot of ports
def port_plt():
    n = int(input("Enter the 'N':\n"))
    pplt = port_melt[:n]
    pplt.plot(kind='bar')
    plt.show()


# Menu
print("###Menu###")
print("Enter desired command:")
print("1. No. of unique IPs encountered.")
print("2. Top 'N' no. of IPs.")
print("3. Plot Top 'N' IPs")
print("4. Top 'N' no. of Ports being used.")
print("5. Plot Top 'N' ports.")
mn = int(input())
if mn == 1:
    count_unik()
elif mn == 2:
    unik_ip()
elif mn == 3:
    ip_plt()
elif mn == 4:
    unik_ports()
elif mn == 5:
    port_plt()
