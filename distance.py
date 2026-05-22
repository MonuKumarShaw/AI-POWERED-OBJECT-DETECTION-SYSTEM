KNOWN_WIDTH = 7.5
FOCAL_LENGTH = 650

def calculate_distance(width_in_frame):

    distance = (KNOWN_WIDTH *
                FOCAL_LENGTH) / width_in_frame

    return round(distance, 2)