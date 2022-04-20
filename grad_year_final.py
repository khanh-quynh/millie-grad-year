import pandas as pd
import numpy as np

df = pd.read_csv("grad_year.csv")
df["Grad_Year"].replace(np.NaN, -1, inplace = True)
df["Grad_Year"].replace("None", -1, inplace = True)

df.insert(4,'Grad_Year_New',"")

email_dict = {}
email_lst = df['email'].to_list()

handle_lst = []
domain_lst = []
for i in range(len(email_lst)):
    email = str(email_lst[i])
    e = email.split('@')
    handle, domain = e[0], e[-1]
    handle_lst.append(handle)
    domain_lst.append(domain)
    
    if domain not in email_dict:
        email_dict[domain] = []
    email_dict[domain].append(handle)

df.insert(3, "Handle", handle_lst)
df.insert(4, "Domain", domain_lst)


df_email = pd.DataFrame.from_dict(email_dict, orient = 'index')
#print(df_email)

df_pattern = pd.read_csv("grad_year_pattern.csv")

df_pattern.drop([0,1])
df_pattern = df_pattern.rename(columns={"Unnamed: 0": "Domain", "Unnamed: 1": "Pattern"})
df_pattern.head()

print(df_pattern["Pattern"].unique())

df_pattern["Pattern"].replace("x", np.NaN, inplace = True)

first_two = df_pattern.loc[df_pattern["Pattern"] == "[:2]"]
last_two = df_pattern.loc[df_pattern["Pattern"] == "[-2:]"]
first_four = df_pattern.loc[df_pattern["Pattern"] == "[4:]"]
last_four = df_pattern.loc[df_pattern["Pattern"] == "[-4:]"]
middle = df_pattern.loc[df_pattern["Pattern"] == "[-4:-2]"]

new_grad = []

for i in range(len(df["Domain"])):
    # Graduation year lies in first two char
    if df["Domain"][i] in first_two["Domain"].to_list():
        if df["Handle"][i][:2].isnumeric() == True:
            new_grad.append(int("20" + df["Handle"][i][:2]))
        else:
            new_grad.append(df["Grad_Year"][i])
            
    # Graduation year lies in last two char        
    elif df["Domain"][i] in last_two["Domain"].to_list():
        if df["Handle"][i][-2:].isnumeric() == True:
            new_grad.append(int("20" + df["Handle"][i][-2:]))
        else:
            new_grad.append(df["Grad_Year"][i])
            
    # Graduation year lies in first four char          
    elif df["Domain"][i] in first_four["Domain"].to_list():
        if df["Handle"][i][4:].isnumeric() == True:
            new_grad.append(int(df["Handle"][i][4:]))
        else:
            new_grad.append(df["Grad_Year"][i])
    
    # Graduation year lies in last four char  
    elif df["Domain"][i] in last_four["Domain"].to_list():
        if df["Handle"][i][-4:].isnumeric() == True:
            new_grad.append(int(df["Handle"][i][-4:]))
        else:
            new_grad.append(df["Grad_Year"][i])
    
    # Graduation year is the middle char
    elif df["Domain"][i] in middle["Domain"].to_list():
            new_grad.append(int("20" + df["Handle"][i][-4:-2]))
            
    elif df["Domain"][i] == "sherborne.com" or df["Domain"][i] == "wycombeabbey.com":
        if df["Handle"][i][0:2] == "15":
            new_grad.append(2022)
        elif df["Handle"][i][0:2]  == "16":
            new_grad.append(2023)
        elif df["Handle"][i][0:2]  == "17":
            new_grad.append(2024)
            
    else: new_grad.append(df["Grad_Year"][i])

df["Grad_Year_New"] = new_grad

print(df["Grad_Year"].unique())
print(df["Grad_Year_New"].unique())

check_lst = []
for i in range(len(df)):
    if df["Grad_Year_New"][i] != df["Grad_Year"][i] or df["Grad_Year_New"][i] == -1:
        check_lst.append("1")
    else:
        check_lst.append("0")

df.insert(7, "Check", check_lst)

#print(df)

#df.to_csv("testing.csv")