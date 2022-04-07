import re

def generate_measure_list(measure):
    return re.findall(r'[\d\.\d]+', measure)

def calculate_proportions(scale_list):
    scale_list = list(map(lambda x: float(x), scale_list))

    width = scale_list[0]
    height = scale_list[1]

    if width > height:
        height = height / width
        width = 1
    else:
        width = width / height
        height = 1

    return [width, height]

def calculate_x_proportion(scale):
    scale_list = generate_measure_list(scale)
    new_scale_list = calculate_proportions(scale_list)

    return new_scale_list[0]

def calculate_y_proportion(scale):
    scale_list = generate_measure_list(scale)
    new_scale_list = calculate_proportions(scale_list)

    return new_scale_list[1]

def get_highest_proportion(scale):
    scale_list = generate_measure_list(scale)
    return scale_list[0] if scale_list[0] > scale_list[1] else scale_list[1]

def get_x_measure(measure):
    scale_list = generate_measure_list(measure)
    return scale_list[0]

def get_y_measure(measure):
    scale_list = generate_measure_list(measure)
    return scale_list[1]
