import cv2

source = "DOM.jpg"
destination = "newimg.jpeg"
scale_percent = 50
# method of opencv to read file
src = cv2.imread(source,cv2.IMREAD_UNCHANGED)

new_width = int(src.shape[1] * scale_percent / 100)
new_height =int(src.shape[0] * scale_percent / 100)


output = cv2.resize(src,(new_width,new_height))

cv2.imwrite(destination,output)
cv2.waitKey(0)

