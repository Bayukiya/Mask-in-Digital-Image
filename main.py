import cv2
import numpy as np

# 1. Load image and create a circular mask (The "Stencil")
img = cv2.imread('image.jpg')
mask = np.zeros(img.shape[:2], dtype="uint8")
cv2.circle(mask, (150, 150), 100, 255, -1)

# 2. Apply the mask using Bitwise AND (The "Gatekeeper")
# The mask parameter ensures operation only occurs in white regions
masked_img = cv2.bitwise_and(img, img, mask=mask)

# 3. Show the result
cv2.imshow("The Result", masked_img)
cv2.waitKey(0)
