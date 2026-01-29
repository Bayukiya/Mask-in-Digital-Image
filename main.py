import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load and prepare images
path = 'wild_dogs.jpg'
img = cv2.imread(path)
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# --- 1. Geometric Mask (The "Stencil") ---
mask_geo = np.zeros(gray.shape, dtype="uint8")
h, w = gray.shape
cv2.circle(mask_geo, (w // 2, h // 2), min(h, w) // 3, 255, -1)
res_geo = cv2.bitwise_and(img_rgb, img_rgb, mask=mask_geo)

# --- 2. Color-Based Mask (The "Chroma Key") ---
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lower_green = np.array([35, 50, 50])
upper_green = np.array([85, 255, 255])
mask_color = cv2.inRange(hsv, lower_green, upper_green)
res_color = cv2.bitwise_and(img_rgb, img_rgb, mask=mask_color)

# --- 3. Intensity-Based Mask (The "Gatekeeper") ---
_, mask_bright = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
res_bright = cv2.bitwise_and(img_rgb, img_rgb, mask=mask_bright)

# --- 4. Soft Mask (The "Alpha Blend" - Expert Level) ---
# We blur the geometric mask to create a professional vignette
soft_mask = cv2.GaussianBlur(mask_geo.astype(float), (99, 99), 0) / 255.0
# We must use float multiplication for the blend, then convert back to uint8
res_soft = (img_rgb.astype(float) * soft_mask[:,:,np.newaxis]).astype(np.uint8)

# --- Final Display ---
titles = ['Original', 'Geometric', 'Color-Based', 'Intensity', 'Soft/Alpha']
images = [img_rgb, res_geo, res_color, res_bright, res_soft]

plt.figure(figsize=(20, 5))
for i in range(len(images)):
    plt.subplot(1, 5, i+1)
    plt.title(titles[i])
    plt.imshow(images[i])
    plt.axis('off')

plt.tight_layout()
plt.show()
