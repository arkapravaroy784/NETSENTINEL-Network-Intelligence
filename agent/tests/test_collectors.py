import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'src'))
from netsentinel_agent.collectors import jitter
def test_jitter_mean_absolute_successive_difference(): assert jitter([10,20,40])==15
def test_jitter_missing(): assert jitter([None,10]) is None
