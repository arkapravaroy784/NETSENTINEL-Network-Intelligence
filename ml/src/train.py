"""Train reproducible development-only model artifacts from synthetic telemetry."""
from pathlib import Path
import joblib, numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from .features import FEATURES
def main():
 rng=np.random.default_rng(42);X=rng.normal([45,1,5,80,20,25,80,8,45,35,40],[20,3,3,25,8,15,50,4,20,20,15],(800,len(FEATURES)));y=np.where((X[:,1]>8)|(X[:,0]>100),"UPSTREAM_DEGRADATION","NORMAL")
 a,b,c,d=train_test_split(X,y,test_size=.2,random_state=42,stratify=y);model=Pipeline([("impute",SimpleImputer()),("scale",StandardScaler()),("classifier",RandomForestClassifier(n_estimators=150,random_state=42))]);model.fit(a,c);print(classification_report(d,model.predict(b),zero_division=0));Path("ml/models").mkdir(parents=True,exist_ok=True);joblib.dump({"model":model,"features":FEATURES,"dataset_version":"synthetic_v1"},"ml/models/root_cause_classifier.joblib")
if __name__=="__main__":main()
