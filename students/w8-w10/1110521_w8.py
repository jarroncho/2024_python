import tensorflow as tf
from datetime import datetime

# Define a simple function to add two numbers
@tf.function
def add_numbers(a, b, c):
    return (a + b) + c


# Create summary writer for TensorBoard
log_dir = "logs/1110505/" + datetime.now().strftime("%Y%m%d-%H%M%S")
writer = tf.summary.create_file_writer(log_dir)

# Use tf.summary.trace_on to trace the graph
tf.summary.trace_on(graph=True)

# Call the function with example values
a_value = tf.constant(3.0, dtype=tf.float32)
b_value = tf.constant(4.0, dtype=tf.float32)
c_value = tf.constant(4.0, dtype=tf.float32)

#b_value = tf.Variable(4.0, dtype=tf.float32, name='b_value_name')

result = add_numbers(a_value, b_value, c_value)

# Use tf.summary.trace_export to save the graph to TensorBoard
with writer.as_default():
    tf.summary.trace_export(name="graph_trace", step=0)

# Print the result
print(f'The sum of {a_value.numpy()} and {b_value.numpy()} and {c_value.numpy()} is: {result.numpy()}')

# To launch TensorBoard, use the following command in the terminal:
# tensorboard --logdir=path_to_logs_directory
# Replace "path_to_logs_directory" with the actual path to your logs directory.
