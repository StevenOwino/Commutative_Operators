
#Create First Simple Circuit


#The Toffoli gate, invented by Tommaso Toffoli, is a universal reversible logic gate, which #means that any reversible circuit can be constructed from Toffoli gates. It is also known #as the controlled-controlled-not gate, which describes its action. It has 3-bit inputs and #outputs; if the first two bits are both set to 1, it inverts the third bit, otherwise all #bits stay the same. It is basically an AND gate.
#The Toffoli gate is essentially the atom of mathematics. It is the simplest element, from #which every other problem-solving technique can be compiled.


from qiskit import QuantumCircuit
from qiskit.providers.aer import AerSimulator
qc = QuantumCircuit(3, 3)
# measure qubits 0, 1 & 2 to classical bits 0, 1 & 2 respectively
qc.measure([0,1,2], [0,1,2])
qc.draw()
sim = AerSimulator()   # make new simulator object
job = sim.run(qc)      # run the experiment
result = job.result()  # get the results
result.get_counts()    # interpret the results as a "counts" dictionary  {'000': 1024}

#Encodimg An Input
# Create quantum circuit with 3 qubits and 3 classical bits:
qc = QuantumCircuit(3, 3)
qc.x([0,1])  # Perform X-gates on qubits 0 & 1 (NOT Gate)
qc.measure([0,1,2], [0,1,2])
qc.draw()    # returns a drawing of the circuit
job = sim.run(qc)      # run the experiment
result = job.result()  # get the results
result.get_counts()    # interpret the results as a "counts" dictionary  {'011': 1024}

# Create quantum circuit with 2 qubits and 2 classical bits
qc = QuantumCircuit(2, 2)
qc.x(0)
qc.cx(0,1)  # CNOT controlled by qubit 0 and targeting qubit 1
qc.measure([0,1], [0,1])
display(qc.draw())     # display a drawing of the circuit
job = sim.run(qc)      # run the experiment
result = job.result()  # get the results
# interpret the results as a "counts" dictionary
print("Result: ", result.get_counts())   Result:  {'11': 1024}

#Create Half Adder and test {1 + 1 = 1 0}
from qiskit import QuantumCircuit
qc = QuantumCircuit(3, 3)
qc.cx(0,2)
qc.cx(1,2)
qc.ccx(0,1,3)

test_qc = QuantumCircuit(4,2)
# First, our circuit should encode an input (here '11')
test_qc.x(0)
test_qc.x(1)

# Next, it should carry out the adder circuit we created
test_qc.cx(0,2)
test_qc.cx(1,2)
test_qc.ccx(0,1,3)

# Finally, we will measure the bottom two qubits to extract the output
test_qc.measure(2,0)
test_qc.measure(3,1)
test_qc.draw()
job = sim.run(test_qc)  # run the experiment
result = job.result()   # get the results
result.get_counts()     # interpret the results as a “counts” dictionary {'10': 1024}
