import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
from xgboost import XGBClassifier
import numpy as np
from sklearn.model_selection import train_test_split

df = pd.read_csv("datasetCredit.csv")

# Split data into train and test sets
train_set, test_set = train_test_split(df, test_size=0.1, random_state=42)

# Separate the target variable (status) from the predictor variables
y_train = train_set['status']
X_train = train_set.drop(columns=['status'])

# Initialize the XGBoost classifier
xgbc = XGBClassifier()

# Train the XGBoost classifier on the training set
xgbc.fit(X_train, y_train)


def validate_int(input_str):
    if input_str.isdigit():
        return True
    elif input_str == "":
        return True
    else:
        return False

root = tk.Tk()
root.geometry("800x400")

# Creating Labels
label_loan_amount = ttk.Label(root, text="Loan Amount:", font=("Helvetica", 13))
label_interest = ttk.Label(root, text="Interest:", font=("Helvetica", 13))
label_gender = ttk.Label(root, text="Gender:", font=("Helvetica", 13))
label_term = ttk.Label(root, text="Term:", font=("Helvetica", 13))
label_income = ttk.Label(root, text="Income:", font=("Helvetica", 13))
label_region = ttk.Label(root, text="Region:", font=("Helvetica", 13))
label_age = ttk.Label(root, text="Age:", font=("Helvetica", 13))
label_credit_type = ttk.Label(root, text="Credit Type:", font=("Helvetica", 13))
label_loan_type = ttk.Label(root, text="Loan Type:", font=("Helvetica", 13))
label_credit_score = ttk.Label(root, text="Credit Score:", font=("Helvetica", 13))

# Creating Entry boxes
entry_loan_amount = ttk.Entry(root)
entry_interest = ttk.Entry(root)
int_validate = root.register(validate_int)
entry_term = ttk.Entry(root, width=20, validate="key", validatecommand=(int_validate, '%P'))
entry_income = ttk.Entry(root, width=20, validate="key", validatecommand=(int_validate, '%P'))
entry_cscore = ttk.Entry(root, width=20, validate="key", validatecommand=(int_validate, '%P'))

age_values = ['25-34', '35-44', '45-54', '55-64', '65-74', 'Less than 25', 'Over 74']
age = tk.StringVar(root)
age.set(age_values[0])
drop_down_age = ttk.OptionMenu(root, age, *age_values)

credit_type_values = ['CIB', 'CRIF', 'EQUI', 'EXP']
credit_type = tk.StringVar(root)
credit_type.set(credit_type_values[0])
drop_down_credit = ttk.OptionMenu(root, credit_type, *credit_type_values)

loan_type_values = ['Personal', 'Home', 'Gold', 'Education']
loan_type = tk.StringVar(root)
loan_type.set(loan_type_values[0])
drop_down_loan = ttk.OptionMenu(root, loan_type, *loan_type_values)

# Create a button to store the values
def store_values():
    loan_amount = int(entry_loan_amount.get())
    interest = float(entry_interest.get())
    selected_gender = gender.get()
    term = int(entry_term.get())
    income = entry_income.get()
    selected_region = region.get()
    selected_age = age.get()
    selected_credit_type = credit_type.get()
    selected_loan_type = loan_type.get()
    creditScore = int(entry_cscore.get())

    lst = [loan_amount,interest,0.405,2850.52,term,458898.4518,income,creditScore,74.129,38.10,0,0,0,0,0,1,1,1,1,0,1,1,1,0,0,1,0,0,0,1,0,0,0,1,0,1,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0]
    if(selected_region == 0):
        lst[-4]=1
    elif(selected_region == 1):
        lst[-1]=1
    else:
        lst[-2] = 1

    if(selected_age == 'Less than 25'):
        lst[-6] = 1
    elif(selected_age == 'Over 74'):
        lst[-5] = 1
    elif(selected_age == '65-74'):
        lst[-7] = 1
    elif (selected_age =='55-64'):
        lst[-8] = 1
    elif (selected_age == '45-54'):
        lst[-9] = 1
    elif (selected_age == '35-44'):
        lst[-10] = 1
    else:
        lst[-11] = 1

    if(selected_credit_type == 0):
        lst[-15] = 1
    elif(selected_credit_type == 1):
        lst[-14] = 1
    elif(selected_credit_type == 2):
        lst[-13] = 1
    else:
        lst[-12] = 1

    if(selected_gender == 0):
        lst[27] = 1
    elif(selected_gender == 1):
        lst[25] = 1
    elif(selected_gender == 2):
        lst[28] = 1
    else:
        lst[26] = 1
    arr = np.array(lst, dtype=np.float32)
    status = xgbc.predict(arr.reshape(1, -1))[0]
    if status == 0:
        status_str = "Rejected"
    else:
        status_str = "Approved"

    result = tk.messagebox.showinfo("Loan Status", f"Your loan application is {status_str}.")


# Layout using place
label_loan_amount.place(relx=0.35, rely=0.1)
entry_loan_amount.place(relx=0.5, rely=0.1)

label_interest.place(relx=0.4, rely=0.17)
entry_interest.place(relx=0.5, rely=0.17)

label_gender.place(relx=0.4, rely=0.24)
# Creating Radio Buttons
gender_values = ['Male', 'Female', 'Prefer not to say', 'Joint']
gender = tk.StringVar(root)
gender.set(gender_values[0])
for idx, value in enumerate(gender_values):
    rb = ttk.Radiobutton(root, text=value, variable=gender, value=value)
    rb.place(relx=0.5+idx*0.135, rely=0.24)

label_term.place(relx=0.4, rely=0.31)
entry_term.place(relx=0.5, rely=0.31)

label_income.place(relx=0.4, rely=0.38)
entry_income.place(relx=0.5, rely=0.38)

label_region.place(relx=0.4, rely = 0.45)
# Creating Radio Buttons
region_values = ['North', 'South', 'Central']
region = tk.StringVar(root)
region.set(region_values[0])
for idx, value in enumerate(region_values):
    rb = ttk.Radiobutton(root, text=value, variable=region, value=value)
    rb.place(relx=0.5 + idx * 0.135, rely=0.45)

label_age.place(relx=0.4, rely=0.52)
drop_down_age.place(relx=0.5, rely=0.52)

label_credit_type.place(relx=0.37, rely=0.59)
drop_down_credit.place(relx=0.5, rely=0.59)

label_loan_type.place(relx=0.37, rely=0.66)
drop_down_loan.place(relx=0.5, rely=0.66)

label_credit_score.place(relx = 0.35, rely=0.73)
entry_cscore.place(relx=0.5,rely=0.73)

button_store = ttk.Button(root, text="Predict", command=store_values, width=20)
button_store.place(relx=0.5, rely=0.80)

root.mainloop()
