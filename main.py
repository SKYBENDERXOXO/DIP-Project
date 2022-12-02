import cv2
import numpy as np
import copy
from core.filter import GuidedFilter

#All the tweakable parameters
INPUT_IMAGE_PATH = ".\input images\dark4.jpg"
OUTPUT_IMAGE_PATH = ".\output images"
gamma = 2
alpha = 0.5
radius = 20
eps = 0.001



def custom_hist(img_array):
    """
    STEP 1: Normalized cumulative histogram
    """
    #flatten image array and calculate histogram via binning
    histogram_array = np.bincount(img_array.flatten(), minlength=256)
    #normalize
    num_pixels = np.sum(histogram_array)
    histogram_array = histogram_array/num_pixels
    #cumulative histogram
    chistogram_array = np.cumsum(histogram_array)
    """
    STEP 2: Pixel mapping lookup table
    """
    transform_map = np.floor(255 * chistogram_array).astype(np.uint8)
    """
    STEP 3: Transformation
    """
    # flatten image array into 1D list
    img_list = list(img_array.flatten())
    # transform pixel values to equalize
    eq_img_list = [transform_map[p] for p in img_list]
    # reshape and write back into img_array
    eq_img_array = np.reshape(np.asarray(eq_img_list), img_array.shape)
    return eq_img_array



img = cv2.imread(INPUT_IMAGE_PATH)
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)[:,:,2]
# cv2.imshow("Gray image", gray_img)

cv2.imwrite(OUTPUT_IMAGE_PATH + "\\input_image.jpg", img)
cv2.imwrite(OUTPUT_IMAGE_PATH + "\\grayed_input_image.jpg", gray_img)

new_img = copy.deepcopy(gray_img)


for y in range(gray_img.shape[0]):
    for x in range(gray_img.shape[1]):
            new_img[y,x] = int(255 * ((gray_img[y,x]/255)**(1/gamma)))

cv2.imwrite(OUTPUT_IMAGE_PATH + "\\gamma_corrected.jpg", new_img)

hist_img = cv2.equalizeHist(gray_img)   
# hist_img = custom_hist(gray_img)
for y in range(gray_img.shape[0]):
    for x in range(gray_img.shape[1]):
            new_img[y,x] = (1 - alpha)*new_img[y,x] + alpha*hist_img[y,x]

cv2.imwrite(OUTPUT_IMAGE_PATH + "\\hist_equalized_image.jpg", hist_img)

cv2.imwrite(OUTPUT_IMAGE_PATH + "\\alpha_blended_image.jpg", new_img)


Oimg = copy.deepcopy(new_img)
ret, thresh1 = cv2.threshold(new_img, 0, 255, cv2.THRESH_BINARY +  cv2.THRESH_OTSU)
cv2.imwrite(OUTPUT_IMAGE_PATH + "\\otsu's_threshold.jpg", thresh1)

GF = GuidedFilter(new_img, radius, eps)

gf_res = GF.filter(thresh1)
cv2.imwrite(OUTPUT_IMAGE_PATH + "\\guided_filter_mask.jpg", gf_res)


for x in range(Oimg.shape[0]):
    for y in range(Oimg.shape[1]):
        Oimg[x,y] = gf_res[x,y]*Oimg[x,y] + (1-gf_res[x,y])*gray_img[x,y]

cv2.imwrite(OUTPUT_IMAGE_PATH + "\\grayed_output.jpg", new_img)

O_rgb = copy.deepcopy(cv2.cvtColor(img, cv2.COLOR_BGR2HSV))
O_rgb[:,:,2] = Oimg
O_rgb = cv2.cvtColor(O_rgb, cv2.COLOR_HSV2BGR)


# for y in range(img.shape[0]):
#     for x in range(img.shape[1]):
#         for c in range(img.shape[2]):
#             O_rgb[y,x,c] = img[y,x,c]*(Oimg[y,x]/gray_img[y,x])
cv2.imwrite(OUTPUT_IMAGE_PATH + "\\colored_output.jpg", new_img)

cv2.imwrite(OUTPUT_IMAGE_PATH + "\\final_comparison.jpg", np.hstack((img, O_rgb)))
