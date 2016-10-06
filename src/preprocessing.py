
def highpass_filter(image):
    for i,value in enumerate(image):
        if value <=3:
            image[i]=0
