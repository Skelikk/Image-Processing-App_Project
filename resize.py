import cv2

def resize_and_rotate(image, size=None, angle=0):

    # Resize the image
    if size is not None:
        image = cv2.resize(image, size, interpolation=cv2.INTER_LINEAR)
    
    # Get the image dimensions
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    
    # Create the rotation matrix
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, scale=1.0)
    
    # Perform the rotation
    rotated_image = cv2.warpAffine(image, rotation_matrix, (w, h))
    
    return rotated_image

# Example usage
if __name__ == "__main__":
    # Load an image
    image_path = r"C:\Users\Admaj\Downloads"
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Image could not be loaded.")
    else:
        # Resize and rotate the image
        resized_and_rotated_image = resize_and_rotate(image, size=(300, 300), angle=45)
        
        # Display the result
        cv2.imshow("Original Image", image)
        cv2.imshow("Resized & Rotated Image", resized_and_rotated_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()