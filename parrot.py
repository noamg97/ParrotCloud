import cv2

hsv_min = (0, 100, 150)
hsv_max = (50, 255, 255)
min_umbrella_radius = 10

def main(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, hsv_min, hsv_max)
    mask = cv2.erode(mask, None, iterations=3)
    mask = cv2.dilate(mask, None, iterations=3)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, 
        cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        if radius > min_umbrella_radius:
            cv2.circle(frame, (int(x), int(y)), int(radius),
                (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)

    height, width, _ = frame.shape
    print width, height
    print center
    forward = (2.0 * center[0] / width) - 1
    rightword = (2.0 * center[1] / height) - 1
    print forward, rightword

    cv2.imshow('a', mask)
    cv2.imshow('b', frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return forward, rightword


if __name__ == '__main__':
    img = cv2.imread(r'a.jpg')
    img = cv2.resize(img, (640, 480))
    main(img)