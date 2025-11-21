# Digital Logic Simulator

A Python-based Digital Logic Simulator with a Graphical User Interface (GUI). This application allows users to design, simulate, and analyze digital logic circuits using standard logic gates.

## Features

*   **Drag-and-Drop Interface:** Easily add components to the canvas and move them around.
*   **Standard Logic Gates:** Includes AND, OR, NOT, XOR, and NAND gates.
*   **Interactive Components:**
    *   **Switches:** Toggle inputs (ON/OFF).
    *   **Bulbs:** Visualize outputs (Lit/Unlit).
*   **Wiring:** Connect components by clicking on input/output nodes.
*   **Real-time Simulation:** Visual feedback of logic states (Red wires for High/True, Black for Low/False).
*   **Truth Table Generator:** Automatically generates a truth table for the current circuit configuration.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd logisim
    ```

2.  **Prerequisites:**
    *   Python 3.x installed.
    *   `tkinter` is usually included with Python. If not, you may need to install it (e.g., `sudo apt-get install python3-tk` on Linux).

3.  **Dependencies:**
    *   No external pip packages are required. The project uses only the Python standard library.

## Usage

1.  **Run the Application:**
    ```bash
    python main.py
    ```

2.  **Building a Circuit:**
    *   **Add Components:** Click the buttons on the top toolbar (AND, OR, NOT, etc.) to add them to the canvas.
    *   **Move Components:** Click and drag components to position them.
    *   **Connect Wires:**
        *   Click on a node (small circle on component edges).
        *   Move the mouse to another node.
        *   Click again to complete the connection.
    *   **Toggle Switches:** Click on a Switch component to toggle its state between ON and OFF.

3.  **Simulation:**
    *   The simulation runs continuously.
    *   Wires turn **Red** when the signal is HIGH (True).
    *   Wires turn **Black** when the signal is LOW (False).
    *   Bulbs light up **Yellow** when receiving a HIGH signal.

4.  **Truth Table:**
    *   Click the **"Truth Table"** button in the toolbar.
    *   A new window will appear showing the truth table for all Switches (Inputs) and Bulbs (Outputs) currently in the circuit.

## Project Structure

*   `main.py`: The main entry point of the application. Handles the GUI setup and event loop.
*   `logic_engine.py`: Contains the core logic for simulation (Circuit, Node, Gate classes).
*   `gui_components.py`: Defines the visual representation of components for the Tkinter canvas.
*   `test_logic.py`: Unit tests for the logic gates and circuit simulation.
*   `test_truth_table.py`: Unit tests for truth table generation logic.

## Testing

To run the unit tests:

```bash
python -m unittest test_logic.py
python -m unittest test_truth_table.py
```
