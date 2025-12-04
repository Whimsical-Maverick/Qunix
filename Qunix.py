from flask import Flask, render_template, request, jsonify
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import random

app = Flask(__name__)

# -------------------------
# Frontend route
# -------------------------
@app.route('/')
def index():
    return render_template('terminal.html')

# -------------------------
# Backend Command Processor
# -------------------------
@app.route('/command', methods=['POST'])
def process_command():
    data = request.get_json()
    command = data.get('command', '').strip().lower()

    # Basic commands
    if command == "help":
        return jsonify({
            "output": """Available Commands:
ls            → List directories
cat <file>    → View file contents
qcalc         → Perform quantum calculation
qbell         → Generate Bell pair (entanglement)
qmeasure N    → Measure N-qubit circuit
clear         → Clear terminal
exit          → Shutdown system
help          → Show this list"""
        })

    elif command == "ls":
        return jsonify({"output": "Documents   Downloads   QuantumOS"})

    elif command.startswith("cat"):
        return jsonify({"output": "This is a simulated file. Nothing to show yet."})

    elif command == "exit":
        return jsonify({"output": "System shutting down..."})

    # Quantum commands
    elif command == "qcalc":
    # Single-qubit superposition
        qc = QuantumCircuit(1, 1)
        qc.h(0)
        qc.measure(0, 0)

        sim = AerSimulator()
        result = sim.run(qc, shots=10).result()
        counts = result.get_counts()
        return jsonify({"output": f"Quantum superposition result: {counts}"})

    # Two-qubit Bell-state entanglement
    elif command == "qbell":
        qc = QuantumCircuit(2, 2)
        qc.h(0)
        qc.cx(0, 1)
        qc.measure([0, 1], [0, 1])

        sim = AerSimulator()
        result = sim.run(qc, shots=10).result()
        counts = result.get_counts()
        return jsonify({"output": f"Bell state entanglement results: {counts}"})
    
    # Measure arbitrary number of qubits
    elif command.startswith("qmeasure"):
        try:
            n = int(command.split()[1])
            qc = QuantumCircuit(n, n)
            for i in range(n):
               if random.random() > 0.5:
                  qc.x(i)
            qc.measure(range(n), range(n))

            sim = AerSimulator()
            result = sim.run(qc, shots=10).result()
            counts = result.get_counts()
            return jsonify({"output": f"Measured {n}-qubit system: {counts}"})

        except Exception as e:
            return jsonify({"output": "Usage: qmeasure N  (e.g., qmeasure 3)"})

    elif command == "clear":
        return jsonify({"output": "__clear__"})  # special flag for frontend

    else:
        return jsonify({"output": f"Command not found: {command}"})

# -------------------------
# Run
# -------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

