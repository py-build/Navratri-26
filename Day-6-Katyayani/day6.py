
import cv2
import numpy as np

# Load image
img = cv2.imread("6_katyayani.jpg")

if img is None:
    raise FileNotFoundError(
        "Place 6_katyayani.jpg beside this Python file."
    )

# Resolution: 500 x 500
img = cv2.resize(img, (500, 500),
                 interpolation=cv2.INTER_AREA)

# Detect detailed edges
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (3, 3), 0)
edges = cv2.Canny(gray, 35, 100)

# Find contours
contours, _ = cv2.findContours(
    edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE
)
contours = sorted(contours,
                  key=cv2.contourArea, reverse=True)

# Black canvas
art = np.zeros_like(img)

cv2.namedWindow("Python Neon Drawing",
                cv2.WINDOW_NORMAL)

stop = False

for contour in contours:
    if len(contour) < 3:
        continue

    points = contour.reshape(-1, 2)

    for i in range(1, len(points)):
        x1, y1 = map(int, points[i - 1])
        x2, y2 = map(int, points[i])

        # Original image colours
        colour = tuple(int(v) for v in img[y2, x2])

        # Fine, smooth lines
        cv2.line(art, (x1, y1), (x2, y2),
                 colour, 1, cv2.LINE_AA)

        # Update screen less often for faster drawing
        if i % 12 == 0:
            glow = cv2.GaussianBlur(
                art, (0, 0), 1.2
            )
            display = cv2.addWeighted(
                art, 1.0, glow, 0.15, 0
            )

            # Small moving cursor
            cv2.circle(display, (x2, y2), 3,
                       (100, 80, 255), -1,
                       cv2.LINE_AA)

            cv2.imshow("Python Neon Drawing", display)

            if cv2.waitKey(1) == 27:
                stop = True
                break

    if stop:
        break

# Save completed artwork
glow = cv2.GaussianBlur(art, (0, 0), 1.2)
final = cv2.addWeighted(art, 1.0, glow, 0.15, 0)

cv2.imwrite("katyayani_neon_art.png", final)
cv2.imshow("Final Artwork", final)

print("Saved: katyayani_neon_art.png")

cv2.waitKey(0)
cv2.destroyAllWindows()
