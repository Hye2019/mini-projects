'''

Author: Heidi Ye
Date: March 7 2019
'''

import image

def clip(value, min=0, max=255):
    """ Clip the given value so that it it is an integer falling within the given range """
    if value < min:
        return min
    elif value > max:
        return max
    else:
        return int(value)
    
def contrastTransform(pixel, contrast):
    """ Return a copy of given image pixel with contrast adjusted by given factor """
    # get RGB components of the pixel
    red = pixel.getRed()
    green = pixel.getGreen()
    blue = pixel.getBlue()

    # adjust intensity of each component by same factor (darker < 1 < brighter)
    pixel.setRed( clip(red * contrast) )
    pixel.setGreen( clip(green * contrast) )
    pixel.setBlue( clip(blue * contrast) )
    
    return pixel
    
def adjustContrast(img, contrast):
    """
        Return a copy of given img with the contrast adjusted by given factor.
        @param  contrast values [0..1) reduce contrast;  values > 1 increase contrast
    """
    # create an empty image of same dimension
    filtered_image = image.EmptyImage(img.getWidth(), img.getHeight())
    
    # for each pixel in the image, img
    for row in range(img.getHeight()):
        for col in range(img.getWidth()):
            
            # get the pixel value
            p = img.getPixel(col, row)

            # apply contrast filter to the pixel
            p = contrastTransform(p, contrast)
    
            # set the corresponding pixel in the filtered image
            filtered_image.setPixel(col,row, p)
           
    return filtered_image

def brightnessTransform(pixel, brightness):
    """ Return a copy of given image pixel with contrast adjusted by given factor """
    # get RGB components of the pixel
    red = pixel.getRed()
    green = pixel.getGreen()
    blue = pixel.getBlue()

    # adjust intensity of each component by same factor (darker < 1 < brighter)
    pixel.setRed( clip(red + brightness) )
    pixel.setGreen( clip(green + brightness) )
    pixel.setBlue( clip(blue + brightness) )
    
    return pixel

def adjustBrightness(img, brightness):
    """
        Return a copy of given img with the contrast adjusted by given factor.
        @param  contrast values [0..1) reduce contrast;  values > 1 increase contrast
    """
    # create an empty image of same dimension
    filtered_image = image.EmptyImage(img.getWidth(), img.getHeight())
    
    # for each pixel in the image, img
    for row in range(img.getHeight()):
        for col in range(img.getWidth()):
            
            # get the pixel value
            p = img.getPixel(col, row)

            # apply contrast filter to the pixel
            p = brightnessTransform(p, brightness)
    
            # set the corresponding pixel in the filtered image
            filtered_image.setPixel(col,row, p)
           
    return filtered_image

def brightnessAndContrastTransform(pixel, brightness, contrast):
    """ Return a copy of given image pixel with contrast adjusted by given factor """
    # get RGB components of the pixel
    red = pixel.getRed()
    green = pixel.getGreen()
    blue = pixel.getBlue()

    # adjust intensity of each component by same factor (darker < 1 < brighter)
    pixel.setRed( clip((red * contrast) + brightness))
    pixel.setGreen( clip((green * contrast) + brightness))
    pixel.setBlue( clip((blue * contrast) + brightness))
    
    return pixel

def adjustBrightnessAndContrast(img,brightness,contrast):
    """
        Return a copy of given img with the contrast adjusted by given factor.
        @param  contrast values [0..1) reduce contrast;  values > 1 increase contrast
    """
    # create an empty image of same dimension
    filtered_image = image.EmptyImage(img.getWidth(), img.getHeight())
    
    # for each pixel in the image, img
    for row in range(img.getHeight()):
        for col in range(img.getWidth()):
            
            # get the pixel value
            p = img.getPixel(col, row)

            # apply contrast filter to the pixel
            p = brightnessAndContrastTransform(p, brightness, contrast)
    
            # set the corresponding pixel in the filtered image
            filtered_image.setPixel(col,row, p)
           
    return filtered_image

def greyTransform(pixel):
    """ Return a copy of given image pixel with contrast adjusted by given factor """
    # get RGB components of the pixel
    red = pixel.getRed()
    green = pixel.getGreen()
    blue = pixel.getBlue()

    # adjust intensity of each component by same factor (darker < 1 < brighter)
    pixel.setRed( clip((red+green+blue)/3) )
    pixel.setGreen( clip((red+green+blue)/3) )
    pixel.setBlue( clip((red+green+blue)/3) )
    
    return pixel 

def adjustGrey(img):
    """
        Return a copy of given img with in greyscale
    """
    # create an empty image of same dimension
    filtered_image = image.EmptyImage(img.getWidth(), img.getHeight())
    
    # for each pixel in the image, img
    for row in range(img.getHeight()):
        for col in range(img.getWidth()):
            
            # get the pixel value
            p = img.getPixel(col, row)

            # apply contrast filter to the pixel
            p = greyTransform(p)
    
            # set the corresponding pixel in the filtered image
            filtered_image.setPixel(col,row, p)
           
    return filtered_image

def isGreen(pixel):
    '''
    Determines if a pixel green. Return true if yes, otherwise returns false.
    '''
    if pixel.getRed() <= 1 and pixel.getBlue() <= 1 and pixel.getGreen() >= 254:
        return True
    else:
        return False

def superposeGreenScreen(minion_img,original_img):
    '''
    Superposes minion image onto cap u image
    '''
    green_screen_img = image.EmptyImage(minion_img.getWidth(), minion_img.getHeight()) # Sets up window with same dimensions as minion image
    for row in range(green_screen_img.getHeight()):
        for col in range(green_screen_img.getWidth()):
            p = minion_img.getPixel(col, row)
            if isGreen(p):
                p = original_img.getPixel(col,row) # if pixel from minion image is green, return corresponding pixel from cap u image.
            green_screen_img.setPixel(col,row, p)
    return green_screen_img
    
def main():
    IMAGE_FILE = 'cap.gif'
    MINION_FILE = 'minion-greenscreen.gif'
    CONTRAST = 0.8  # factor for contrast transform < 1 for reduced contrast, > 1 for more contrast
    BRIGHTNESS = 100
    

    # open and display the image from file
    original_img = image.Image(IMAGE_FILE)
    win1 = image.ImageWin(original_img.getWidth(), original_img.getHeight())
    original_img.draw(win1)
    
    minion_img = image.Image(MINION_FILE)
    win3 = image.ImageWin(minion_img.getWidth(), minion_img.getHeight())
    minion_img.draw(win3)
    
    # Create a transformed copy of the image and display it    
    transformed_img = adjustBrightnessAndContrast(original_img,BRIGHTNESS,CONTRAST)
    transformed_img = adjustGrey(original_img)
    win2 = image.ImageWin(transformed_img.getWidth(), transformed_img.getHeight())
    transformed_img.draw(win2)
    
    # Create a transformed copy of the image and display it    
    green_screen_img = superposeGreenScreen(minion_img,original_img)
    transformed_img = adjustGrey(original_img)
    win4 = image.ImageWin(green_screen_img.getWidth(), green_screen_img.getHeight())
    green_screen_img.draw(win4)
    
    
main()