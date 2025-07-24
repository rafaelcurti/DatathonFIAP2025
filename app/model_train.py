
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from lightgbm import LGBMClassifier
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
import joblib
import os

@st.cache_resource(show_spinner=True)
def train_model(df):
    df = df.copy()
    df['contratado'] = df['foi_contratado']
    df['texto'] = df['cv'].fillna('') + ' ' + df['atividades'].fillna('') + ' ' + df['competencias'].fillna('')

    X_text = df['texto']
    y = df['contratado']

    tfidf = TfidfVectorizer(max_features=3000, stop_words='english')
    X_tfidf = tfidf.fit_transform(X_text)

    svd = TruncatedSVD(n_components=100, random_state=42)
    X_svd = svd.fit_transform(X_tfidf)

    smote = SMOTE(random_state=42)
    X_resampled, y_resampled = smote.fit_resample(X_svd, y)

    X_train, X_test, y_train, y_test = train_test_split(
        X_resampled, y_resampled, test_size=0.2, random_state=42
    )

    model = LGBMClassifier(random_state=42)
    model.fit(X_train, y_train)

    os.makedirs("models", exist_ok=True)
    joblib.dump(model, "models/model.joblib")
    joblib.dump(tfidf, "models/tfidf.joblib")
    joblib.dump(svd, "models/svd.joblib")

    return model, tfidf, svd
