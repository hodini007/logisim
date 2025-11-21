import tkinter as tk
from tkinter import ttk, messagebox
import itertools
from logic_engine import Circuit, AndGate, OrGate, NotGate, XorGate, NandGate, Switch, Bulb
from gui_components import GuiComponent, SwitchGui, BulbGui

class SimulatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Logic Simulator")
        self.root.geometry("1000x700")

        self.circuit = Circuit()
        self.gui_components = []
        self.selected_component = None
        self.drag_data = {"x": 0, "y": 0}
        
        self.wiring_mode = False
        self.start_node = None
        self.temp_wire = None

        self.create_widgets()
        self.run_simulation()

    def create_widgets(self):
        # Toolbar
        toolbar = tk.Frame(self.root, bd=1, relief=tk.RAISED)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        components = [
            ("AND", AndGate),
            ("OR", OrGate),
            ("NOT", NotGate),
            ("XOR", XorGate),
            ("NAND", NandGate),
            ("Switch", Switch),
            ("Bulb", Bulb)
        ]

        for name, cls in components:
            btn = tk.Button(toolbar, text=name, command=lambda c=cls: self.add_component(c))
            btn.pack(side=tk.LEFT, padx=2, pady=2)

        clear_btn = tk.Button(toolbar, text="Clear", command=self.clear_circuit)
        clear_btn.pack(side=tk.RIGHT, padx=2, pady=2)

        tt_btn = tk.Button(toolbar, text="Truth Table", command=self.generate_truth_table)
        tt_btn.pack(side=tk.RIGHT, padx=2, pady=2)

        # Canvas
        self.canvas = tk.Canvas(self.root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<Motion>", self.on_mouse_move)

    def add_component(self, component_cls):
        comp = component_cls()
        self.circuit.add_component(comp)
        
        # Place in center of visible canvas or default
        x, y = 100, 100
        
        if isinstance(comp, Switch):
            gui_comp = SwitchGui(comp, x, y)
        elif isinstance(comp, Bulb):
            gui_comp = BulbGui(comp, x, y)
        else:
            gui_comp = GuiComponent(comp, x, y)
            
        self.gui_components.append(gui_comp)
        self.redraw()

    def clear_circuit(self):
        self.circuit = Circuit()
        self.gui_components = []
        self.redraw()

    def redraw(self):
        self.canvas.delete("all")
        
        # Draw wires
        for node1, node2 in self.circuit.wires:
            # Find coordinates (stored in node objects during component draw)
            # We need to ensure components are drawn or at least positions updated before wires? 
            # Actually, we draw components first to update node positions, then wires?
            # No, wires should be behind components.
            # But we need node positions.
            # Let's draw components first to get node positions, then move wires to bottom?
            # Or just use stored positions if available.
            pass

        # Draw components first to update node positions
        for gui_comp in self.gui_components:
            gui_comp.draw(self.canvas)

        # Now draw wires using updated node positions
        for node1, node2 in self.circuit.wires:
            if hasattr(node1, 'gui_x') and hasattr(node2, 'gui_x'):
                color = "red" if node1.value else "black" # Simple visualization of state
                self.canvas.create_line(node1.gui_x, node1.gui_y, node2.gui_x, node2.gui_y, fill=color, width=2, tags="wire")

        # Draw temp wire
        if self.temp_wire:
            self.canvas.create_line(*self.temp_wire, fill="gray", dash=(4, 2))

    def get_node_at(self, x, y):
        # Check all components' nodes
        for gui_comp in self.gui_components:
            # Check inputs
            for node in gui_comp.component.inputs.values():
                if hasattr(node, 'gui_x'):
                    dist = ((node.gui_x - x)**2 + (node.gui_y - y)**2)**0.5
                    if dist < 10:
                        return node
            # Check outputs
            for node in gui_comp.component.outputs.values():
                if hasattr(node, 'gui_x'):
                    dist = ((node.gui_x - x)**2 + (node.gui_y - y)**2)**0.5
                    if dist < 10:
                        return node
        return None

    def on_click(self, event):
        x, y = event.x, event.y
        
        # Check for node click (Wiring)
        clicked_node = self.get_node_at(x, y)
        if clicked_node:
            if not self.wiring_mode:
                self.wiring_mode = True
                self.start_node = clicked_node
            else:
                # Complete wire
                self.circuit.add_wire(self.start_node, clicked_node)
                self.wiring_mode = False
                self.start_node = None
                self.temp_wire = None
            self.redraw()
            return

        # If wiring mode is on and we clicked empty space, cancel
        if self.wiring_mode:
            self.wiring_mode = False
            self.start_node = None
            self.temp_wire = None
            self.redraw()
            return

        # Check for component click
        for gui_comp in reversed(self.gui_components): # Topmost first
            if gui_comp.contains(x, y):
                self.selected_component = gui_comp
                self.drag_data["x"] = x
                self.drag_data["y"] = y
                
                # Handle Switch toggle
                if isinstance(gui_comp, SwitchGui):
                    # Simple toggle on click (could be refined to specific area)
                    gui_comp.component.toggle()
                
                gui_comp.selected = True
                # Deselect others
                for other in self.gui_components:
                    if other != gui_comp:
                        other.selected = False
                self.redraw()
                return
        
        # Clicked on background
        self.selected_component = None
        for comp in self.gui_components:
            comp.selected = False
        self.redraw()

    def on_drag(self, event):
        if self.selected_component:
            dx = event.x - self.drag_data["x"]
            dy = event.y - self.drag_data["y"]
            self.selected_component.move(dx, dy)
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y
            self.redraw()

    def on_release(self, event):
        pass # Drag end

    def on_mouse_move(self, event):
        if self.wiring_mode and self.start_node:
            self.temp_wire = (self.start_node.gui_x, self.start_node.gui_y, event.x, event.y)
            self.redraw()

    def run_simulation(self):
        self.circuit.simulate()
        self.redraw()
        self.root.after(100, self.run_simulation) # 10 FPS simulation

    def generate_truth_table(self):
        # Identify Inputs (Switches) and Outputs (Bulbs)
        switches = [c for c in self.circuit.components if isinstance(c, Switch)]
        bulbs = [c for c in self.circuit.components if isinstance(c, Bulb)]

        if not switches:
            messagebox.showinfo("Info", "No switches found. Add switches to generate a truth table.")
            return
        
        if not bulbs:
            messagebox.showinfo("Info", "No bulbs found. Add bulbs to generate a truth table.")
            return

        # Sort by name for consistent order
        switches.sort(key=lambda x: x.name)
        bulbs.sort(key=lambda x: x.name)

        headers = [s.name for s in switches] + [b.name for b in bulbs]
        data = []

        # Generate all combinations
        for values in itertools.product([False, True], repeat=len(switches)):
            # Set inputs
            for i, switch in enumerate(switches):
                switch.set_state(values[i])
            
            # Simulate to stabilize
            self.circuit.simulate(ticks=20)
            
            # Read outputs
            outputs = [b.is_lit for b in bulbs]
            
            # Format row (0/1 instead of False/True)
            row = [1 if v else 0 for v in values] + [1 if v else 0 for v in outputs]
            data.append(row)

        self.show_truth_table(headers, data)

    def show_truth_table(self, headers, data):
        window = tk.Toplevel(self.root)
        window.title("Truth Table")
        window.geometry("600x400")

        tree = ttk.Treeview(window, columns=headers, show="headings")
        
        for h in headers:
            tree.heading(h, text=h)
            tree.column(h, width=80, anchor="center")

        for row in data:
            tree.insert("", tk.END, values=row)

        tree.pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = SimulatorApp(root)
    root.mainloop()
