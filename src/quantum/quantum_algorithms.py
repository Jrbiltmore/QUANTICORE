
from qiskit import QuantumCircuit, Aer, execute

def run_quantum_circuit():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    simulator = Aer.get_backend('statevector_simulator')
    result = execute(qc, simulator).result()
    return result.get_statevector()
