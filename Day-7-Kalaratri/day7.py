
import cv2
import numpy as np

img = cv2.imread("7_kalaratri.jpg")
if img is None:
    raise FileNotFoundError("Put photo.jpg beside this code")

img = cv2.resize(img, (500, 500))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 60, 150)

contours, _ = cv2.findContours(
    edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE
)
contours = sorted(
    contours, key=cv2.contourArea, reverse=True
)

art = np.zeros_like(img)

for contour in contours:
    if len(contour) < 8:
        continue

    for i in range(1, len(contour)):
        p1 = tuple(contour[i - 1][0])
        p2 = tuple(contour[i][0])

        # Use the original image colour
        x, y = p2
        colour = tuple(int(v) for v in img[y, x])
        cv2.line(art, p1, p2, colour, 2, cv2.LINE_AA)

        # Update the cursor less often for faster tracing
        if i % 60 == 0:
            glow = cv2.GaussianBlur(art, (0, 0), 1)
            display = cv2.addWeighted(
                art, 1, glow, 1, 0
            )

            cv2.circle(
                display, p2, 8, (255, 80, 255), -1
            )

            cv2.imshow("Python Drawing", display)

            if cv2.waitKey(1) == 27:
                break

    if cv2.waitKey(1) == 27:
        break

# Save final artwork
glow = cv2.GaussianBlur(art, (0, 0), 1)
final = cv2.addWeighted(art, 1, glow, 1, 0)

cv2.waitKey(0)
cv2.destroyAllWindows()
