import uuid

class Node:
    def __init__(self, component, name, is_input=False):
        self.id = str(uuid.uuid4())
        self.component = component
        self.name = name
        self.is_input = is_input
        self.value = False
        self.connections = [] # List of connected Nodes

    def connect(self, other_node):
        if other_node not in self.connections:
            self.connections.append(other_node)
            other_node.connections.append(self)

    def disconnect(self, other_node):
        if other_node in self.connections:
            self.connections.remove(other_node)
            other_node.connections.remove(self)

class Component:
    def __init__(self, name="Component"):
        self.id = str(uuid.uuid4())
        self.name = name
        self.inputs = {}
        self.outputs = {}
        self.position = (0, 0)

    def add_input(self, name):
        self.inputs[name] = Node(self, name, is_input=True)

    def add_output(self, name):
        self.outputs[name] = Node(self, name, is_input=False)

    def evaluate(self):
        pass

class AndGate(Component):
    def __init__(self):
        super().__init__("AND")
        self.add_input("A")
        self.add_input("B")
        self.add_output("Q")

    def evaluate(self):
        a = self.inputs["A"].value
        b = self.inputs["B"].value
        self.outputs["Q"].value = a and b

class OrGate(Component):
    def __init__(self):
        super().__init__("OR")
        self.add_input("A")
        self.add_input("B")
        self.add_output("Q")

    def evaluate(self):
        a = self.inputs["A"].value
        b = self.inputs["B"].value
        self.outputs["Q"].value = a or b

class NotGate(Component):
    def __init__(self):
        super().__init__("NOT")
        self.add_input("A")
        self.add_output("Q")

    def evaluate(self):
        self.outputs["Q"].value = not self.inputs["A"].value

class XorGate(Component):
    def __init__(self):
        super().__init__("XOR")
        self.add_input("A")
        self.add_input("B")
        self.add_output("Q")

    def evaluate(self):
        a = self.inputs["A"].value
        b = self.inputs["B"].value
        self.outputs["Q"].value = a != b

class NandGate(Component):
    def __init__(self):
        super().__init__("NAND")
        self.add_input("A")
        self.add_input("B")
        self.add_output("Q")

    def evaluate(self):
        a = self.inputs["A"].value
        b = self.inputs["B"].value
        self.outputs["Q"].value = not (a and b)

class Switch(Component):
    def __init__(self):
        super().__init__("Switch")
        self.add_output("Q")
        self.is_on = False

    def toggle(self):
        self.is_on = not self.is_on
        self.evaluate()

    def set_state(self, state):
        self.is_on = state
        self.evaluate()

    def evaluate(self):
        self.outputs["Q"].value = self.is_on

class Bulb(Component):
    def __init__(self):
        super().__init__("Bulb")
        self.add_input("A")
        self.is_lit = False

    def evaluate(self):
        self.is_lit = self.inputs["A"].value

class Circuit:
    def __init__(self):
        self.components = []
        self.wires = [] # List of tuples (node1, node2)

    def add_component(self, component):
        self.components.append(component)

    def remove_component(self, component):
        if component in self.components:
            self.components.remove(component)
            # Disconnect all nodes
            for node in list(component.inputs.values()) + list(component.outputs.values()):
                for connected_node in list(node.connections):
                    self.remove_wire(node, connected_node)

    def add_wire(self, node1, node2):
        # Basic validation: Don't connect input to input or output to output (though some logic allows it, let's be strict for now or lenient?)
        # Let's allow output to input.
        # Also check if already connected
        if (node1, node2) not in self.wires and (node2, node1) not in self.wires:
            node1.connect(node2)
            self.wires.append((node1, node2))

    def remove_wire(self, node1, node2):
        if (node1, node2) in self.wires:
            self.wires.remove((node1, node2))
            node1.disconnect(node2)
        elif (node2, node1) in self.wires:
            self.wires.remove((node2, node1))
            node2.disconnect(node1)

    def step(self):
        changed = False
        # 1. Propagate values from outputs to inputs via wires
        for node1, node2 in self.wires:
            source = None
            dest = None
            
            if not node1.is_input and node2.is_input:
                source = node1
                dest = node2
            elif not node2.is_input and node1.is_input:
                source = node2
                dest = node1
            
            if source and dest:
                if dest.value != source.value:
                    dest.value = source.value
                    changed = True

        # 2. Evaluate all components
        for component in self.components:
            # Capture old output values to detect changes
            old_outputs = {k: v.value for k, v in component.outputs.items()}
            component.evaluate()
            for k, v in component.outputs.items():
                if v.value != old_outputs[k]:
                    changed = True
        
        return changed

    def simulate(self, ticks=10):
        # Run for a maximum number of ticks or until stable
        for _ in range(ticks):
            if not self.step():
                break
