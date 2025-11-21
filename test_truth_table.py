from logic_engine import Circuit, AndGate, Switch, Bulb
import itertools

def test_truth_table_logic():
    c = Circuit()
    s1 = Switch()
    s2 = Switch()
    and_gate = AndGate()
    bulb = Bulb()

    s1.name = "A"
    s2.name = "B"
    bulb.name = "Q"

    c.add_component(s1)
    c.add_component(s2)
    c.add_component(and_gate)
    c.add_component(bulb)

    c.add_wire(s1.outputs["Q"], and_gate.inputs["A"])
    c.add_wire(s2.outputs["Q"], and_gate.inputs["B"])
    c.add_wire(and_gate.outputs["Q"], bulb.inputs["A"])

    switches = [s1, s2]
    bulbs = [bulb]

    print(f"Truth Table for {and_gate.name}:")
    print(f"{s1.name} | {s2.name} | {bulb.name}")
    print("-" * 10)

    expected_results = [
        (False, False, False),
        (False, True, False),
        (True, False, False),
        (True, True, True)
    ]

    for i, values in enumerate(itertools.product([False, True], repeat=len(switches))):
        for j, switch in enumerate(switches):
            switch.set_state(values[j])
        
        c.simulate(ticks=20)
        
        output = bulb.is_lit
        print(f"{int(values[0])} | {int(values[1])} | {int(output)}")
        
        assert values[0] == expected_results[i][0]
        assert values[1] == expected_results[i][1]
        assert output == expected_results[i][2], f"Failed at {values}"

    print("Truth Table Logic Verified!")

if __name__ == "__main__":
    test_truth_table_logic()
