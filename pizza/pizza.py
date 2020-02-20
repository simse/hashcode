# Input
max_slices = 0
pizza_types = []
pizza_types_count = 0

# Read input from file
input_file = open('input/e_also_big.in', 'r')
meta_line = input_file.readline()
pizza_line = input_file.readline()
input_file.close()

max_slices = int(meta_line.split(' ')[0])
pizza_types_count = int(meta_line.split(' ')[1])
#pizza_types = pizza_line.split(' ')

for pizza in pizza_line.split(' '):
    pizza_types.append(int(pizza))
    # print("Adding: {} to list...".format(int(pizza)))

# pizza_types.sort()


# Runtime
current_total = 0
index_pizzas = []

for x in range(int(pizza_types_count / 2)):
    # To fill
    i = x
    to_fill = max_slices - current_total
    largest = pizza_types[pizza_types_count-i-1]
    smallest = pizza_types[i]

    print(i)
    print("to fill: {}".format(to_fill))
    print(current_total)
    print(pizza_types[i])
    print(pizza_types[pizza_types_count - i - 1])
    print("-")

    # Check if largest and smallest element can fit
    if smallest + largest <= to_fill:
        current_total += smallest + largest
        index_pizzas.append(i)
        index_pizzas.append(pizza_types_count-i-1)

        continue

    # Check if largest element can fit
    if largest <= to_fill:
        current_total += largest
        index_pizzas.append(pizza_types_count-i-1)

        continue

    # Check if smallest element can fit
    if smallest <= to_fill:
        current_total += smallest
        index_pizzas.append(i)

        continue

def optimize():
    global current_total
    global max_slices

    largest_remaining_number = 0
    largest_remaining_number_index = 0
    for x in range(pizza_types_count):
        if x not in index_pizzas:
            if pizza_types[x] > largest_remaining_number:
                largest_remaining_number = pizza_types[x]
                largest_remaining_number_index = x



    print("The largest number left: ", largest_remaining_number)

    # Replace a smaller number with a bigger number
    lower_bound = largest_remaining_number - (max_slices-current_total)
    upper_bound = largest_remaining_number - 1

    print("LB: {}, UB: {}\n\n".format(lower_bound, upper_bound))


    index_to_replace = -1
    current = 0
    for i in range(len(index_pizzas)-1):
        n = pizza_types[index_pizzas[i]]
        if n > current and n > lower_bound and n < upper_bound:
            current = n
            index_to_replace = i


    print(index_to_replace)
    print(current)

    if index_to_replace == -1:
        return False

    # Execute the replacement
    index = index_pizzas[index_to_replace]
    value = pizza_types[index]
    current_total -= value
    current_total += largest_remaining_number
    index_pizzas[index_to_replace] = largest_remaining_number_index

    return True


while optimize():
    pass


print("TOTAL: {} ({} below wanted)\nTYPES: {}\nTO ORDER: {}\n\n".format(current_total, max_slices-current_total, len(index_pizzas), index_pizzas))

# formal output
index_pizzas.sort()
print(len(index_pizzas))
for i in index_pizzas:
    print(i, end=" ")
print("")
