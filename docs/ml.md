# ML

The development pipeline uses a fixed random seed and performs splitting before preprocessing to avoid leakage. Isolation Forest is available for unsupervised anomaly scoring; the trainer stores a joblib model, feature list, and synthetic dataset version. The bundled training command intentionally reports metrics generated from its actual synthetic training run. Synthetic labels are for demonstration only and must not be represented as production accuracy.
