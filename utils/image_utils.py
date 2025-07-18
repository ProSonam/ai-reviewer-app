from PIL import ImageEnhance

def enhance_image(image):
    # Enhance brightness
    enhancer_brightness = ImageEnhance.Brightness(image)
    image = enhancer_brightness.enhance(1.2)

    # Enhance sharpness
    enhancer_sharpness = ImageEnhance.Sharpness(image)
    image = enhancer_sharpness.enhance(1.5)

    return image

