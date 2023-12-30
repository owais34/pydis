from src.structs.rlist import RList

def test_puleft():
    test_list = RList()
    elements = ["1","2","3","4","5"]
    for e in elements:
        test_list.push_left(e)
    
    assert len(elements) == test_list.get_length()

def test_puright():
    test_list = RList()
    elements = ["1","2","3","4","5"]
    for e in elements:
        test_list.push_right(e)
    
    assert len(elements) == test_list.get_length()

def test_poleft():
    test_list = RList()
    elements = ["1","2","3","4","5"]
    for e in elements:
        test_list.push_right(e)
    assert ("1" == test_list.pop_left() and "2" == test_list.pop_left()  and "3" == test_list.pop_left())

def test_poright():
    test_list = RList()
    elements = ["1","2","3","4","5"]
    for e in elements:
        test_list.push_right(e)
    assert ("5" == test_list.pop_right() and "4" == test_list.pop_right()  and "3" == test_list.pop_right())

def test_posleft():
    test_list = RList()
    elements = ["1","2","3","4","5"]
    for e in elements:
        test_list.push_right(e)
    assert 2 == test_list.pos_from_left("3")

def test_posleft_2():
    test_list = RList()
    elements = ["1","2","3","4","5"]
    for e in elements:
        test_list.push_right(e)
    assert None == test_list.pos_from_left("9")

def test_get_index():
    test_list = RList()
    elements = ["1","2","3","4","5"]
    for e in elements:
        test_list.push_right(e)
    assert "2" == test_list.get_index(1)

def test_get_index_2():
    test_list = RList()
    elements = ["1","2","3","4","5"]
    for e in elements:
        test_list.push_right(e)
    assert "5" == test_list.get_index(-1)

def test_get_index_3():
    test_list = RList()
    elements = ["1","2","3","4","5"]
    for e in elements:
        test_list.push_right(e)
    assert None == test_list.get_index(-6)

def test_get_index_3():
    test_list = RList()
    elements = ["1","2","3","4","5"]
    for e in elements:
        test_list.push_right(e)
    assert None == test_list.get_index(6)

def test_range():
    test_list = RList()
    elements = ["1","2","3","4","5"]
    for e in elements:
        test_list.push_right(e)
    
    assert elements[0:3] == test_list.range(0,2)

def test_range2():
    test_list = RList()
    elements = ["1","2","3","4","5"]
    for e in elements:
        test_list.push_right(e)
    
    assert elements[-3:] == test_list.range(-3,-1)

def test_remove():
    test_list = RList()
    elements = ["1","1","1","1","1"]
    for e in elements:
        test_list.push_right(e)
    
    assert 5 == test_list.remove("1", 0)

def test_remove():
    test_list = RList()
    elements = ["1","1","1","1","1"]
    for e in elements:
        test_list.push_right(e)
    
    assert 1 == test_list.remove("1", 1)

def test_remove_1():
    test_list = RList()
    elements = ["1","1","1","1","1"]
    for e in elements:
        test_list.push_right(e)
    
    assert 2 == test_list.remove("1", -2)
