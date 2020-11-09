from flask import Flask, render_template, request
import numpy as np
import pickle
import pandas as pd
from sklearn.preprocessing import scale

app= Flask(__name__)

model=pickle.load(open('model.pkl', 'rb'))

@app.route("/")
def home():
    return render_template('index.html')



@app.route('/predict',methods=['POST'])
def predict():
    
    never_credit=[]
    A_income=[]
    C_income=[]
    LoanAmount=[]
    Loan_Amount_Term=[]
    Family=[]    
    
    
    never_credit.append(float(request.form["Never_Credit"]))
    A_income.append(float(request.form['ApplicantIncome']))
    C_income.append(float(request.form['CoapplicantIncome']))
    LoanAmount.append(float(request.form['LoanAmount']))
    Loan_Amount_Term.append(float(request.form['Loan_Amount_Term']))
    Family.append(float(request.form['Family_Member']))
    
    df=pd.DataFrame()
    df['Never_Credit']=never_credit
    df['ApplicantIncome']=A_income
    df["CoapplicantIncome"]=C_income
    df['LoanAmount']=LoanAmount
    df['Loan_Amount_Term']=Loan_Amount_Term
    df['Total_Income']= df['ApplicantIncome']+df["CoapplicantIncome"]
    df['Refund_Time']=df['LoanAmount']/df['Loan_Amount_Term']
    df['Income_pond']=df['Total_Income']/Family    
    #On ordonne nos colonnes
    df= df[['Never_Credit','Total_Income', 'Refund_Time','Income_pond',
    'ApplicantIncome','CoapplicantIncome', 'LoanAmount',"Loan_Amount_Term"]]     
    df.iloc[:,1:]=scale(df.iloc[:,1:])
    prediction = model.predict(df)
    df['Loan_Status']=prediction
    
    if prediction==1:
        output= "Emprunt Accepté"
    else:
        output="Emprunt Refusé"
            
    return render_template('./index.html', prediction_text="{}".format(output))

if __name__ == "__main__":
    app.run(debug=True)