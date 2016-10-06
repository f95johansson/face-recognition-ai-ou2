
def highpass_filter(image):
    for i,value in enumerate(image):
        if value <= 5/32:
            image[i] = 0
