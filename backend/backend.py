from fastapi import FastAPI
import tldextract
import pandas as pd
import joblib

app = FastAPI()

preprocessor = joblib.load('preprocessor.pkl')
model = joblib.load('model.pkl')

risk_words = ['login','admin','update','secure','account']
def get_features(url):
    extracted_object = tldextract.extract(url)
    size = len(url)
    https = url.startswith('https://')
    subdomain = extracted_object.subdomain
    #domain = extracted_object.domain
    suffix = extracted_object.suffix
    dots = url.count('.')
    dashes = url.count('-')
    numbers = sum(c.isdigit() for c in url)
    risky=0
    for d in risk_words:
        if d in url:
            risky+=1
    f_slash = sum(c == '/' for c in url)
    b_slash = sum(c == '\\' for c in url)
    underscore = sum(c == '_' for c in url)
    at = True if '@' in url else False
    #return size, https, subdomain, suffix, dots, dashes, numbers, login, f_slash, b_slash, underscore, at
    return {
        'size' : size,
        'https' : https,
        'subdomain' : subdomain,
        'suffix' : suffix,
        'dots' : dots,
        'dashes' : dashes,
        'numbers' : numbers,
        'risky' : risky,
        'f_slash' : f_slash,
        'b_slash' : b_slash,
        'underscore' : underscore,
        'at' : at
    }
    

@app.post
def predict(url:str)->bool:
    df = pd.DataFrame([get_features(url)])
    df = preprocessor.transform(df)
    prediction=model.predict(df)
    return prediction