from sklearn.ensemble import IsolationForest
from .features import rows_to_matrix
def train(rows): return IsolationForest(contamination=.05,random_state=42).fit(rows_to_matrix(rows))
def infer(model,rows): return model.predict(rows_to_matrix(rows)).tolist()
