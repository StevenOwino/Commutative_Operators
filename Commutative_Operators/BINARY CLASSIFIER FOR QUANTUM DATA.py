# BINARY CLASSIFIER FOR QUANTUM DATA(One qubit binary classification) USING TFQ
#https://github.com/tensorflow/quantum/blob/research/binary_classifier/binary_classifier.ipynb
#Quantum data is represented on a Bloch sphere:
#First by generating data to be classified
#Secondly by removing/minimizing superpositions in the input quantum data 
#by parameterizing a rotation gate
#Thirdly by measuring along the Z axis of the Bloch sphere to convert
#the quantum data into classical data for maximum useful information
#Fourthly follows a classical post-processing two-output 
#SoftMax layer which outputs probabilities for the data to come from
#category a or category b
#Fifthly, a categorical cross entropy is computed between 
#the predictions and the labels.
#An optimizer is used to update both the quantum and classical
#portions of the hybrid model.
#OUTCOME: Use the trained hybrid model to classify new quantum datapoints

#STEP 1: Generate Quantum Data using Cirq
import cirq, random, sympy
import numpy as np
import tensorflow as tf
import tensorflow_quantum as tfq

def generate_dataset(
	qubit, theta_a, theta_b, num_samples):
	q_data = []
	labels = []
	blob_size = abs(theta_a - theta_b / 5
	for _ in range(num_samples):
		coin = random.random()
		spread_x, spread_y = np.random.uniform(
			-blob_size, blob_size, 2)
		if coin < 0.5:
			label = [1,0]
			angle = theta_a + spread_y
		else:
			label = [0,1]
			angle = theta_b + spread_y
		labels.append(label)
		q.data.append(cirq.Circuit(
			cirq.Ry(-angle)(qubit),
			cirq.Rx(-spread_x)(qubit)))
    return (tfq.convert_to_tensor(q_data),
    	    np.array(labels))
#STEP 2: Picking some parameter values i.e, DIFFERENTIATOR
#Enabling Backpropagation through parameterized quantum circuit 
#Using a universal quantum discriminator(single parameterized 
#linear rotatation and measurement along a non-linear Z axis)
qubit = cirq.GridQubit(0, 0)
theta_a = 1
theta_b = 4
num_samples = 200
q_data, labels = generate_dataset(
	qubit, theta_a, theta_b, num_samples)
theta = sympy.Symbol('theta')
q_model = cirq.circuit(cirq.Ry(theta)(qubit))
q_data_input = tf.keras.Input(
	shape = (), dtype = tf.dtypes.string)
expectation = tfq.layers.PQC(
	q_model, cirq.layers.Z(qubit))
expectation_output = expectation(q_data_input)
#STEP 3: Attach the model to a classifier to complete the hybrid model
#The quantum layers appear among classical layers inside standard Keras model
classifier = tf.keras.layers.Dense(
	2, activation = tf.keras.activations.softmax)
classifier_output = classifier(
	expectation_output)
model = tf.keras.Model(inputs = q_data_input, 
	outputs = classifier_output)
#STEP 4 and 5: Train the hybrid model on the quantum data defined
#Loss function is used as the cross entropy between the labels and 
#the classical NN; Optimized by parameter updates
optimizer = tf.keras.optimizers.Adam(
	learning_rate = 0.1)
loss = tf.keras.losses.CategoricalCrossentropy()
model.compile(optimizer = optimizer, loss = loss)
history = model.fit(
	x = q_data, y = labels, epoch = 50)
#OUTCOME: Classify new quantum datapoints
test_data =, _ = generate_dataset(
	qubit, theta_a, theta_b, 1)
p = model.predict(test_data)[0]
print(f"prob(a) = {p[0]: .4f}, prob(b) = {p[1]: .4f}")



