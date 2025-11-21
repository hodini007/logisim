import tkinter as tk
from logic_engine import Component, Node

class GuiComponent:
    def __init__(self, component: Component, x, y):
        self.component = component
        self.x = x
        self.y = y
        self.width = 60
        self.height = 40
        self.color = "lightgray"
        self.selected = False
        
        # Update component position in logic engine (optional, but good for consistency)
        self.component.position = (x, y)

    def draw(self, canvas: tk.Canvas):
        # Draw body
        outline = "blue" if self.selected else "black"
        canvas.create_rectangle(self.x, self.y, self.x + self.width, self.y + self.height, 
                                fill=self.color, outline=outline, width=2, tags="component")
        
        # Draw label
        canvas.create_text(self.x + self.width/2, self.y + self.height/2, text=self.component.name)

        # Draw input nodes
        input_spacing = self.height / (len(self.component.inputs) + 1)
        for i, (name, node) in enumerate(self.component.inputs.items()):
            ny = self.y + input_spacing * (i + 1)
            nx = self.x
            self.draw_node(canvas, nx, ny, node)

        # Draw output nodes
        output_spacing = self.height / (len(self.component.outputs) + 1)
        for i, (name, node) in enumerate(self.component.outputs.items()):
            ny = self.y + output_spacing * (i + 1)
            nx = self.x + self.width
            self.draw_node(canvas, nx, ny, node)

    def draw_node(self, canvas, x, y, node):
        r = 4
        color = "red" if node.value else "black"
        # Store coordinates in node for wire drawing
        node.gui_x = x
        node.gui_y = y
        canvas.create_oval(x - r, y - r, x + r, y + r, fill=color, tags="node")

    def contains(self, x, y):
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.component.position = (self.x, self.y)

class SwitchGui(GuiComponent):
    def __init__(self, component, x, y):
        super().__init__(component, x, y)
        self.color = "white"

    def draw(self, canvas: tk.Canvas):
        super().draw(canvas)
        # Draw toggle state
        state_text = "ON" if self.component.is_on else "OFF"
        canvas.create_text(self.x + self.width/2, self.y + self.height + 10, text=state_text)

class BulbGui(GuiComponent):
    def __init__(self, component, x, y):
        super().__init__(component, x, y)
    
    def draw(self, canvas: tk.Canvas):
        # Draw body
        color = "yellow" if self.component.is_lit else "gray"
        outline = "blue" if self.selected else "black"
        canvas.create_oval(self.x, self.y, self.x + self.width, self.y + self.height, 
                           fill=color, outline=outline, width=2, tags="component")
        
        # Draw label
        canvas.create_text(self.x + self.width/2, self.y + self.height/2, text=self.component.name)

        # Draw input nodes (Bulb usually has 1 input)
        if "A" in self.component.inputs:
            node = self.component.inputs["A"]
            ny = self.y + self.height / 2
            nx = self.x
            self.draw_node(canvas, nx, ny, node)
