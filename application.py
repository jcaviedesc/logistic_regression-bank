from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import pickle
import json

pd.set_option('display.max_columns', 100)
pd.set_option('display.width', 500)

from forms import bankPredictionForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcdefghijklmnopqrst..'


@app.route('/result/')
def result_prediction():
    data = {}
    result_test = ""
    # datos_file = open('datos.txt')
    # data = json.loads(datos_file)
    # print(data)
    result_file = open("result.txt", "r")
    result_prediction = result_file.read()
    if int(result_prediction) == 1:
        result_test = "POSITIVO"
    else:
        result_test = "NEGATIVO"
    print(result_prediction)
    print(result_test)

    return render_template('result.html', dataframe=data, result=result_test)

@app.route('/bank-marketing/', methods=["GET", "POST"])
def bank_marketing():
    form = bankPredictionForm()
    if request.method == 'POST':
        if form.validate():
            transform = {}
            for item in form.data.items():
                key = item[0].replace("_", ".")
                transform[key] = [item[1]]

            print(transform.keys())
            transform['day_of_week'] = transform['day.of.week']
            transform.pop('csrf.token', None)
            transform.pop('day.of.week', None)
            # datos = open("datos.txt", "a")
            # datos.write(json.dumps(transform))
            # datos.close()

            df = pd.DataFrame.from_dict(transform)  
            print(df.head())
            
            min_max_scaler_file = open('minMaxScaler.p', 'rb')
            min_max_scaler = pickle.load(min_max_scaler_file)
            min_max_scaler_file.close() 
            
            df[['age', 'duration', 'campaign', 'pdays', 'previous', 'emp.var.rate', 'cons.price.idx', 'cons.conf.idx', 'euribor3m', 'nr.employed']] = min_max_scaler.transform(df[['age', 'duration', 'campaign', 'pdays', 'previous', 'emp.var.rate', 'cons.price.idx', 'cons.conf.idx', 'euribor3m', 'nr.employed']])
            print('\n=============================AFTER MIN_MAX_SCALER========================================\n')
            print(df)

            #OneHotEncoder. Attention: USE THE SAME ONEHOTENCODER OBJECT USED TO TRANSFORM THE TRAINING DATA
            enc_file = open('oneHotEncoder.p', 'rb')
            enc = pickle.load(enc_file)
            enc_file.close()

            enc_df = pd.DataFrame(enc.transform(df[['job','marital','education','default','housing', 'loan', 'contact', 'month', 'day_of_week', 'poutcome']]).toarray())
            df = df.join(enc_df)
            df = df.drop(['job','marital','education','default','housing', 'loan', 'contact', 'month', 'day_of_week', 'poutcome'],axis=1)
            print('\n=======================AFTER OneHotEncoder ============================\n')
            print(df)

            #Feature Selection. Attention: USE THE SAME SELECTOR OBJECT USED TO TRANSFORM THE TRAINING DATA 

            selector_file = open('selector.p','rb')
            selector = pickle.load(selector_file)
            selector_file.close()

            cols = selector.get_support(indices=True)
            print(cols)
            x_new_test = df.iloc[:,cols]
            print('\n=======================AFTER FEATURE SELECTION (Filter Method)============================\n')
            print(x_new_test)

            clf_file = open('clf.p', 'rb')
            clf = pickle.load(clf_file)
            clf_file.close()
            #Final prediction
            prediction = clf.predict(x_new_test)
            print("la resultado es=",prediction)
            f = open("result.txt", "w")
            f.write(str(prediction[0]))
            f.close()
      
      
            # render_template('result.html', dataframe=transform)
            return redirect(url_for('result_prediction'))
        return render_template('bankMarketing.html', form=form)
    else:
        return render_template('bankMarketing.html', form=form)

@app.route('/bank-excel/', methods=["GET", "POST"])
def bank_url():
    prediction = []
    if request.method == 'POST':
        url = request.form['url']

        df = pd.read_csv(url)
        df['emp.var.rate'] = df['emp.var.rate'].apply(lambda x: (x.replace(',','.'))).astype(float)
        df['cons.price.idx'] = df['cons.price.idx'].apply(lambda x: (x.replace(',','.'))).astype(float)
        df['cons.conf.idx'] = df['cons.conf.idx'].apply(lambda x: (x.replace(',','.'))).astype(float)
        df['euribor3m'] = df['euribor3m'].apply(lambda x: (x.replace(',','.'))).astype(float)
        df['nr.employed'] = df['nr.employed'].apply(lambda x: (x.replace(',','.'))).astype(float)
        print(df.head())
            
        min_max_scaler_file = open('minMaxScaler.p', 'rb')
        min_max_scaler = pickle.load(min_max_scaler_file)
        min_max_scaler_file.close() 
            
        df[['age', 'duration', 'campaign', 'pdays', 'previous', 'emp.var.rate', 'cons.price.idx', 'cons.conf.idx', 'euribor3m', 'nr.employed']] = min_max_scaler.transform(df[['age', 'duration', 'campaign', 'pdays', 'previous', 'emp.var.rate', 'cons.price.idx', 'cons.conf.idx', 'euribor3m', 'nr.employed']])
        print('\n=============================AFTER MIN_MAX_SCALER========================================\n')
        print(df)

        #OneHotEncoder. Attention: USE THE SAME ONEHOTENCODER OBJECT USED TO TRANSFORM THE TRAINING DATA
        enc_file = open('oneHotEncoder.p', 'rb')
        enc = pickle.load(enc_file)
        enc_file.close()

        enc_df = pd.DataFrame(enc.transform(df[['job','marital','education','default','housing', 'loan', 'contact', 'month', 'day_of_week', 'poutcome']]).toarray())
        df = df.join(enc_df)
        df = df.drop(['job','marital','education','default','housing', 'loan', 'contact', 'month', 'day_of_week', 'poutcome'],axis=1)
        print('\n=======================AFTER OneHotEncoder ============================\n')
        print(df)

        #Feature Selection. Attention: USE THE SAME SELECTOR OBJECT USED TO TRANSFORM THE TRAINING DATA 

        selector_file = open('selector.p','rb')
        selector = pickle.load(selector_file)
        selector_file.close()

        cols = selector.get_support(indices=True)
        print(cols)
        x_new_test = df.iloc[:,cols]
        print('\n=======================AFTER FEATURE SELECTION (Filter Method)============================\n')
        print(x_new_test)

        clf_file = open('clf.p', 'rb')
        clf = pickle.load(clf_file)
        clf_file.close()
        #Final prediction
        prediction = clf.predict(x_new_test)
        print("la resultado es=",prediction)
        f = open("result.txt", "w")
        f.write(str(prediction))
        f.close()
        redirect(url_for('result_prediction'))
    return render_template('bankExcel.html', results=prediction)
