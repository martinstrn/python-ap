import pytest
import mymath

import sys
sys.setrecursionlimit(60)

def test_fact_zero():
    assert mymath.fact(0) == 1

def test_fact_negative():
    with pytest.raises(ValueError):
        mymath.fact(-1)

def test_fact_non_integers():
    with pytest.raises(TypeError):
        mymath.fact(4.5)
    with pytest.raises(TypeError):
        mymath.fact("5")
