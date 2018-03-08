import os
import glob
import pandas as pd
import ipaddress
import matplotlib.pyplot as plt


class log:
    names = ["Timestamp", "Customer ID", "Host", "Log file", "Log sequence no.", "Entry type", "Entry identifier",
         "User,if", "Reporting IP/host", "Source IP,if", "Source port,if", "Destination IP, if", "Destination Port, if",
         "Text field1", "Text field2", "Text field3", "Numeric field1", "Numeric field2"]
		 
	#The path of our log file is a shared folders here	 
    path = r"/media/sf_ClipLog/"

    def __init__(self):
	    #Finds all Logs files in our Folder
        self.all_logs = glob.glob(os.path.join(log.path, "*.csv"))
        self.concatlog()

	#COncatenates all log files into one.	
    def concatlog(self):
        self.dfa = []
        for f in self.all_logs:
            self.df = pd.read_csv(f, header=None)
            self.dfa.append(self.df)
        self.result = pd.concat(self.dfa)
        self.result.to_csv('res.csv')    

    def dataready(self):
        self.result.drop(self.result.columns[[0, 1, 2, 3, 4, 5, 6, 7, 8, 14, 15, 16, 17]], axis=1, inplace=True)    
        self.result = self.result.T.reset_index(drop=True).T
        # Converting IP Address to int form
        self.result[0] = self.result[0].map(lambda x: (ipaddress.IPv4Address(x)))
        # Another DF with only unique pings
        self.unik = self.result.drop_duplicates(subset=0)
        # Melting data to find count of IPs
        self.ip_melt = pd.value_counts(self.result[0].values, sort=True)
        # Melted data to find count of ports Ports
        self.port_melt = pd.value_counts(self.result[3].values, sort=True)
    
    # Function to print the total number of IP encountered.
    def count_unik(self):
        print(len(self.unik.index), "IPs")
    
    
    # Function to print 'n' first IPs
    def unik_ip(self):
        n = int(input("Enter the 'N'\n"))
        print("The top", n, "IPs are: ")
        print(self.ip_melt[0:n])


    # Function to plot top IPs
    def ip_plt(self):
        n = int(input("Enter the 'N':\n"))
        pplt = self.ip_melt[:n]
        pplt.plot(kind='bar')
        plt.show()
    
   # Function to print the top n Ports
    def unik_ports():
        n = int(input("Enter the 'N':\n"))
        print(self.port_melt[0:n])

    # Function to print a plot of ports
    def port_plt():
        n = int(input("Enter the 'N':\n"))
        pplt = self.port_melt[:n]
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

logx = log()
logx.dataready()

mn = int(input())
if mn == 1:
    logx.count_unik()
elif mn == 2:
    logx.unik_ip()
elif mn == 3:
    logx.ip_plt()
elif mn == 4:
    logx.unik_ports()
elif mn == 5:
    logx.port_plt()
