#Grovers' Quantum Search Algorithm(A solution to a 3-SAT problem is a string of bits, which makes it easy to map to a quantum circuit.)
#Visualising Grover's algorithm(Geometric Explanation)

#STEP 1
#We can represent quantum states through vectors. With search problems like these, there are only two vectors we care about: The solutions, and everything else.
#We'll call the superposition of all solution states '|Sqrt>', so for the SAT problem above:
# |Sqrt> = 1/Sqrt3(|000> + |011> + |101>), and we'll call the superposition of every other #state '✗':
# |✗>    = 1/Sqrt5(|001> + |010> + |100> + |110> + |111>)
# How many times do we need to query the oracle? To work this out, we'll have to work how #much each iteration rotates our state towards |Sqrt>. Let's say we're somewhere in the #middle of our algorithm, the state of our computer (|Psi>) is an angle (|Phi>) from the #starting state |s>. The angle between |Psi> and |✗> is Theta + Phi.
#Since the two vectors |Sqrt> and |✗> don't share any elements, they are perpendicular, so #we can draw them at right angles on a 2D plane. These will be our y- and x-axes, #respectively.
#The oracle reflects the state vector of our computer around |✗>, so the angle between our #new, reflected state vector (\Psi^'> and |✗) will also be Psi + Theta.
#Let's plot the states of our quantum computer on this plane at different points in the algorithm. The first state we'll plot is |s>. This is the state after step 1 (the #initialisation step). This state is an equal superposition of all computational basis #states. Since any possible state is either a solution or not a solution, we can write |s>  #as some combination of |Sqrt> and |✗>, so it sits in between them on the our plane; i.e,
# |s> = a|✗> + b|Sqrt>.
#Next we reflect through |s> . The angle between the state of our computer (|Psi^') and |s> 
#is 2Theta + Phi.
#For difficult problems, we'd expect there to be lots of possible inputs, but only a small #number of solutions. In this case, |s> would be much closer to |✗> than |Sqrt>  (i.e. the #angle, Theta, between them is small), so it's unlikely that measuring our qubits would #give us one of the computational basis states that make up . Our goal is to end up with #the computer in a state as close to |Sqrt> as possible. So, after one iteration, we know #the angle between the state of our computer and |s> is also 2Theta + Phi.

#STEP 2
#Next we pass our qubits through the circuit U_oracle. We saw above that, by definition, #U_oracle flips the phase of all solution states. In the 2D plane, this is a reflection #through the vector |✗>. I.e,:
# a|✗> + b|Sqrt> --> Oracle --> a|✗> - b|Sqrt>. Which means each iteration rotates the #state of our computer towards |Sqrt> by 2Theta .

#STEP 3
#We've just seen that we can reflect through the vector |✗>, so is there another vector could we reflect through that would move our state closer to |Sqrt> ? The answer is 'yes', we can reflect through the vector |s> . It may not be obvious at first how we can create a circuit that does this, but it's a relatively simple operation.
#Now we just need to work out how many lots of 2Theta fit into a right angle, and this will #be roughly the number of iterations needed to rotate |s> into |Sqrt> .
#Now our state vector is closer to |Sqrt> than before, which means we have a higher chance #of measuring one of our solution states. If there is a solution, we need to repeat steps 2 #and 3 approximately Sqrt(N) times to have the highest probability of measuring that #solution.
#So what's the angle Theta in terms of N ? With a bit of trigonometry, we know that 
#sin(Theta) is equal to the |Sqrt> component of |s> , divided by the length of |s> {which #is 1}.
#If there is only one solution state, then:
# |s> = 1/Sqrt(N) {|0> + |1> .... + |Sqrt> ....|N - 1>}. So sin(Theta) = 1/Sqrt(N).
#Now that our state vector is closer to |Sqrt> than before, which means we have a higher #chance of measuring one of our solution states. If there is only one solution, we need to #repeat steps 2 & 3 ~ Sqrt(N) times to have the highest probability of measuring that #solution.
#Finally, for difficult problems, Theta will be very small, which means we can use the #small angle approximation to say:
#    Theta = 1/Sqrt(N)radians.
#Since, for small Theta, we want to rotate |s> around Pi/2 radians, this means we need to #do roughly { [(Pi/2) / (2/Sqrt(N)] = [(Pi/4)(SqrtN)]} iterations. Since we query the #oracle once per iteration, the number of oracle queries needed is proportional to Sqrt(N), #if there is exactly one solution.



#Step 1: create an equal superposition of every possible input to the oracle by applying a #H-gate to each qubit. We’ll call this equal superposition state '|s>'
from qiskit import QuantumCircuit
init = QuantumCircuit(3)
init.h([0,1,2])
init.draw()
#Step 2: run the oracle circuit on these qubits using any circuit or hardware that changes #the phases of solution states.
#Step 3: Run a circuit called the 'diffusion operator' or 'diffuser' (U_s) on the qubits
from qiskit.circuit.library import GroverOperator
grover_operator = GroverOperator(oracle)
#Combine this into a circuit that performs Grover's algorithm
qc = init.compose(grover_operator)
qc.measure_all()
qc.draw()
#We then need to repeat steps 2 & 3 a few times depending on the size of the circuit. Note that step #2 is the step in which we query the oracle, so the number of times we do this is roughly proportional to the square root of the size of the number of possible inputs. If we repeat 2 & 3 enough times, then when we measure, we'll have a high chance of measuring a solution to the oracle.

#Finally, let's run this on a simulator and see what results we get:
# Simulate the circuit
from qiskit import Aer, transpile
sim = Aer.get_backend('aer_simulator')
t_qc = transpile(qc, sim)
counts = sim.run(t_qc).result().get_counts()
# plot the results
from qiskit.visualization import plot_histogram
plot_histogram(counts)

#We have a high probability of measuring one of the 3 solutions to the SAT problem.

#Circuits for Grover's algorithm
#For this demonstration, we'll create a circuit that flips the phase of the state |11> and #leaves everything else unchanged. Fortunately, we already know of a two-qubit gate that #does exactly that!
from qiskit import QuantumCircuit
oracle = QuantumCircuit(2)
oracle.cz(0,1)  # invert phase of |11>
oracle.draw()
#Here's a short function to show the matrix representation of this circuit:
def display_unitary(qc, prefix=""):
    """Simulates a simple circuit and display its matrix representation.
    Args:
        qc (QuantumCircuit): The circuit to compile to a unitary matrix
        prefix (str): Optional LaTeX to be displayed before the matrix
    Returns:
        None (displays matrix as side effect)
    """
    from qiskit import Aer
    from qiskit.visualization import array_to_latex
    sim = Aer.get_backend('aer_simulator')
    # Next, we'll create a copy of the circuit and work on
    # that so we don't change anything as a side effect
    qc = qc.copy()
    # Tell the simulator to save the unitary matrix of this circuit
    qc.save_unitary()
    unitary = sim.run(qc).result().get_unitary()
    display(array_to_latex(unitary, prefix=prefix))
display_unitary(oracle, "U_\\text{oracle}=") 
#Output : U_oracle =  1  0  0  0 
#                     0  1  0  0
#                     0  0  1  0
#                     0  0  0 -1

#Creating the diffuser
#Next we'll create a diffuser for two qubits. Remember that we want to do a reflection #around the state , so let's see if we can use the tools we already have to build a circuit #that does this reflection.

#We've already seen that the cz gate does a reflection around |11> (up to a global phase), #so if we know the transformation that maps |s>, we can:

#Do the transformation |s> --> |11>
#Reflect around |11> (i.e the cz gate)
#Do the transformation |11> --> |s> 
#We know that we can create the state |s> from the state |00>  by applying a H-gate to each #qubit. Since the H-gate is it's own inverse, applying H-gates to each qubit also does |s> # --> |00>.
diffuser = QuantumCircuit(2)
diffuser.h([0, 1])
diffuser.draw()
#Now we need to work out how we transform |00> to |11>. So applying an X-gate to each qubit #will do the transformation.
diffuser.x([0,1])
diffuser.draw()
#Now we have the transformation |s> --> |11>, we can apply our cz gate and reverse the transformation.
diffuser.cz(0,1)
diffuser.x([0,1])
diffuser.h([0,1])
diffuser.draw()
#We now have two circuits, Oracle and Diffuser, so we can put this together into a circuit #that performs Grover's algorithm. Remember the three steps:
#Initialise the qubits to the state |s>
#Perform the oracle
#Perform the diffuser
grover = QuantumCircuit(2)
grover.h([0,1])  # initialise |s>
grover = grover.compose(oracle)
grover = grover.compose(diffuser)
grover.measure_all()
grover.draw()
#And when we simulate, we can see a 100% probability of measuring |11>, which was the solution to our oracle!
from qiskit import Aer
sim = Aer.get_backend('aer_simulator')
sim.run(grover).result().get_counts() #Output: {'11': 1024}
#SAT problem doubles the number of possible solutions (i.e. entries to our database), so #the search space grows exponentially with the number of bits, thus the running time will #grow by roughly 2^n.

# Schöning’s algorithm(Random inputs to Satisfy clauses)
#For 3-SAT (although not (>3)-SAT), this algorithm grows with roughly 1.3334^n, which not #only beats random guessing, but also beats Grover's algorithm!
#If you create a circuit that carries out the bit-toggling part of Schöning's algorithm, #you can use this as the oracle and use Grover's algorithm to find the best "initial guess". It's a fun project to investigate it!


















































