from itertools import zip_longest

line_size = 25
layer_size = line_size * 6

data = [int(i) for i in open('input.txt', 'r').readline().strip()]

def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

layers = grouper(data, layer_size)

min_zeros_layer = min(layers, key=lambda x: sum(i == 0 for i in x))
num_ones = sum(i == 1 for i in min_zeros_layer)
num_twos = sum(i == 2 for i in min_zeros_layer)

print("1:", num_ones * num_twos)


def merge_layers(layer_top, layers):
    try:
        output = [p2 if p1 == 2 else p1 for p1, p2 in zip(layer_top, next(layers))]
    except StopIteration:
        return layer_top

    return merge_layers(output, layers)

def pixel(pixel):
    return 'X' if pixel else ' '

layers = grouper(data, layer_size)
output = merge_layers(next(layers), layers)

print("2:")
[print(''.join(map(pixel, line)), sep='\n') for line in grouper(output, line_size)]
