from ml.src.features import rows_to_matrix
def test_missing_becomes_zero(): assert rows_to_matrix([{'latency_ms':None}]).shape==(1,11)
