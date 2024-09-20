

# lambda example
x = lambda a : a + 10

def add_10(a):
    return a + 10

print("lambda:",x(5))

print("function:",add_10(5))


# lambda example, key is a function
data = [(1, 5), (3, 2), (2, 8)]
print("orginal data:",data)

def get_key(x):
    return x[0]

#sorted_data = sorted(data, key=lambda x: x[0])
sorted_data = sorted(data, key=get_key)
print("sortd data ",sorted_data)  # Output: [(3, 2), (1, 5), (2, 8)]def add_10(a):
