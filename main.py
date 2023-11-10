import cv2
from skimage.metrics import structural_similarity as ssim
import argparse
from decimal import Decimal, ROUND_HALF_UP
from screeninfo import get_monitors

DEBUG = False


# Compare two images for similarity
def compare_images(imageA, imageB):
    # Compute SSIM between two images
    s = ssim(imageA, imageB, multichannel=True)
    return s


# Get the resolution of the screen to center video
def get_screen_resolution():
    for m in get_monitors():
        return m.width, m.height


def main(video_path, screenshot_path):
    # Read the screenshot
    screenshot = cv2.imread(screenshot_path)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    frame_count = 0
    similar_frames = []
    match_found = False
    first_run = True

    # Loop over the frames of the video
    while True:
        ret, frame = cap.read()

        # If the frame isn't read correctly, break out.
        if not ret:
            print("Can't read frame (stream end?). Exiting ...")
            break

        frame_count += 1

        # Convert the frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Compare the current frame to the screenshot
        similarity = compare_images(screenshot, gray_frame)

        # If the similarity is high, record the frame number and percent similar
        # Set the match_found to true, reset that once our similarity drops
        if similarity > 0.8:
            if not match_found:
                match_found = True
                number = Decimal(similarity * 100).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                similar_frames.append((frame_count, number))
                # Be more verbose if debugging
                if DEBUG:
                    print(f"Frame {frame_count}, SSIM: {number}")
        else:
            match_found = False

        # Show video, for debugging
        if DEBUG:
            # Get the screen resolution
            screen_width, screen_height = get_screen_resolution()

            # Resize the frame to be 5 times larger than the original
            enlarged_frame = cv2.resize(frame, None, fx=5, fy=5, interpolation=cv2.INTER_LINEAR)

            # Create a named window that can be manipulated
            cv2.namedWindow('Frame', cv2.WINDOW_NORMAL)

            # Set the window size
            cv2.resizeWindow('Frame', enlarged_frame.shape[1], enlarged_frame.shape[0])

            # Calculate the position to center the window
            x_pos = screen_width // 2 - enlarged_frame.shape[1] // 2
            y_pos = screen_height // 2 - enlarged_frame.shape[0] // 2

            if first_run:
                first_run = False
                # Move the window to the center of the screen
                cv2.moveWindow('Frame', x_pos, y_pos)
            cv2.imshow('Frame', enlarged_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

    high = -1
    low = 101
    if similar_frames:
        for frame in similar_frames:
            if frame[1] < low:
                low = frame[1]
            if frame[1] > high:
                high = frame[1]
            print(f"Similar frames found at: {frame[0]}, {frame[1]}% similar.")
        print(f'There were {len(similar_frames)} attempts.')
        print(f'low: {low}, high: {high}')
    else:
        print("No similar frames found.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find out how many attempts Barb took")
    parser.add_argument("video_path", help="Path to the MP4 video file")
    parser.add_argument("screenshot_path", help="Path to the screenshot")

    args = parser.parse_args()

    main(args.video_path, args.screenshot_path)
