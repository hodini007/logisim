from logic_engine import Circuit, AndGate, OrGate, NotGate, Switch, Bulb

def test_and_gate():
    c = Circuit()
    s1 = Switch()
    s2 = Switch()
    and_gate = AndGate()
    bulb = Bulb()

    c.add_component(s1)
    c.add_component(s2)
    c.add_component(and_gate)
    c.add_component(bulb)

    c.add_wire(s1.outputs["Q"], and_gate.inputs["A"])
    c.add_wire(s2.outputs["Q"], and_gate.inputs["B"])
    c.add_wire(and_gate.outputs["Q"], bulb.inputs["A"])

    # 0 AND 0 = 0
    s1.set_state(False)
    s2.set_state(False)
    c.simulate()
    assert bulb.is_lit == False, "0 AND 0 failed"

    # 1 AND 0 = 0
    s1.set_state(True)
    s2.set_state(False)
    c.simulate()
    assert bulb.is_lit == False, "1 AND 0 failed"

    # 0 AND 1 = 0
    s1.set_state(False)
    s2.set_state(True)
    c.simulate()
    assert bulb.is_lit == False, "0 AND 1 failed"

    # 1 AND 1 = 1
    s1.set_state(True)
    s2.set_state(True)
    c.simulate()
    assert bulb.is_lit == True, "1 AND 1 failed"
    
    print("AND Gate Test Passed")

def test_not_gate():
    c = Circuit()
    s1 = Switch()
    not_gate = NotGate()
    bulb = Bulb()

    c.add_component(s1)
    c.add_component(not_gate)
    c.add_component(bulb)

    c.add_wire(s1.outputs["Q"], not_gate.inputs["A"])
    c.add_wire(not_gate.outputs["Q"], bulb.inputs["A"])

    # NOT 0 = 1
    s1.set_state(False)
    c.simulate()
    assert bulb.is_lit == True, "NOT 0 failed"

    # NOT 1 = 0
    s1.set_state(True)
    c.simulate()
    assert bulb.is_lit == False, "NOT 1 failed"

    print("NOT Gate Test Passed")

if __name__ == "__main__":
    test_and_gate()
    test_not_gate()
