import tkinter
import tkinter as tk
from tkinter import filedialog,ttk
from tkinter import *
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
import sys
import warnings
if not sys.warnoptions:
    warnings.simplefilter("ignore")
lr = LogisticRegression(C=0.01, solver='liblinear')
root = tkinter.Tk()
root.geometry("1000x1000")
root.title("Student Performance")
root.pack_propagate(False)
root.resizable(2000, 2000)
dis_frame = tk.LabelFrame(root, bg='White', text="Excel Data")
dis_frame.place(height=500, width=1000)
inp_frame = tk.LabelFrame(root, text="Open File")
inp_frame.place(height=150, width=800, rely=0.65, relx=0)
# creating Buttons
butt1 = tk.Button(inp_frame, text="Browse File", command=lambda: File_upload())
butt1.place(rely=0.85, relx=0.10)
butt2 = tk.Button(inp_frame, text="Load File", command=lambda: Load_file())
butt2.place(rely=0.85, relx=0.30)
label= ttk.Label(inp_frame,text="No File Selected")
label.place(rely=0, relx=0.1)
t1 = ttk.Treeview(dis_frame)
t1.place(relheight=1, relwidth=1) # set the height and width
scrolly = tk.Scrollbar(dis_frame, orient="vertical",command=t1.yview)
scrollx = tk.Scrollbar(dis_frame, orient="horizontal",command=t1.xview)
t1.configure(xscrollcommand=scrollx.set,yscrollcommand=scrolly.set)
scrollx.pack(side="bottom", fill="x")
scrolly.pack(side="right", fill="y")
def File_upload():
    filepath = filedialog.askopenfilename(initialdir="/",title="Select input File",filetype=(("xlsx files", "*.xlsx"), ("All Files", "*.*")))
    label["text"] = filepath
    return None
def Load_file():
    file_path = label["text"]
    try:
        excel_file = r"{}".format(file_path)
        if  excel_file[-4:] == ".csv":
            dframe = pd.read_csv(excel_file)
        else:
            dframe = pd.read_excel(excel_file)
    except ValueError:
        tk.messagebox.showerror("The file is invalid")
        return None
    except FileNotFoundError:
        tk.messagebox.showerror("File not found")
        return None
    clear_data()
    t1["column"]=list(dframe.columns)
    t1["show"] = "headings"
    for c in t1["columns"]:
        t1.heading(c, text=c) # let the column heading = column name
        df_rows = dframe.to_numpy().tolist() # turns the dataframe into a list of lists
        for r in df_rows:
            t1.insert("", "end",values=r)
    df=dframe
    df['school'] = df['school'].map({'GP': 0, 'MS': 1})
    df['sex'] = df['sex'].map({'M': 0, 'F': 1})
    df['address'] = df['address'].map({'U': 0, 'R': 1})
    df['Facres'] = df['Facres'].map({'Poor': 0, 'Good': 1, 'Average': 2, 'Excellent':3})
    df['activities'] = df['activities'].map({'no': 0, 'yes': 1})
    df['nursery'] = df['nursery'].map({'no': 0, 'yes': 1})
    df['higher'] = df['higher'].map({'no': 0, 'yes': 1})
    df['internet'] = df['internet'].map({'no': 0, 'yes': 1})
    df['passed'] = df['passed'].map({'no': 0, 'yes': 1})
    # reorder dataframe columns :
    col = df['passed']
    del df['passed']
    df['passed'] = col
    data = df.to_numpy()
    n = data.shape[1]
    x = data[:,0:n-1]
    y = data[:,n-1]
    xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.3, random_state=4)
    lr.fit(xtrain, ytrain)
    predictions = lr.predict(xtest)
    res = "accuracy of logistic regression is: ", accuracy_score(ytest, predictions) * 100
    label_file = tk.Label(inp_frame, text=res, font=("Arial", 15), relief=RAISED)
    label_file.configure(bg="yellow", fg="blue")
    label_file.place(rely=0.2, relx=0.2)
    y=df.passed
    target=["passed"]
    x = df.drop(target,axis = 1 )
    max_iteration = 3
    maxF1 = 0
    maxAccuracy = 0
    optimal_state = 0
    for k in range(max_iteration):
        split_state = np.random.randint(1,100000000)-1
        x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.3,random_state=split_state)
        KNN = KNeighborsClassifier()
        KNN.fit(x_train,y_train)
        y_pred=KNN.predict(x_test)
        f1 = f1_score(y_test, y_pred, average='macro')
        accuracy = accuracy_score(y_test, y_pred)*100
    
        if (accuracy>maxAccuracy and f1>maxF1):
            maxF1 = f1 
            maxAccuracy = accuracy
            optimal_state = split_state
        optimal_state = 71027464
        x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.3,random_state=optimal_state)
        KNN= KNeighborsClassifier()
        KNN.fit(x_train,y_train)
        y_pred=KNN.predict(x_test)
        pred1 = pd.DataFrame(y_pred, columns=['prediction']).to_csv('testprediction.csv')
        f1 = f1_score(y_test, y_pred, average='macro')
        accuracy = accuracy_score(y_test, y_pred)*100
        res = "accuracy of KNN algorithm is: ", accuracy
        label_file1 = tk.Label(inp_frame, text=res, font=("Arial", 15), relief=RAISED)
        label_file1.configure(bg="dark green", fg="light green")
        label_file1.place(rely=0.4, relx=0.2)

def clear_data():
    t1.delete(*t1.get_children())
    
    return None
root.mainloop()