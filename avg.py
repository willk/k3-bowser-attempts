import cv2
import numpy as np


# Function to calculate the average image from a part of a video
def calculate_average_image(video_path, start_frame, end_frame):
    # Initialize the video capture object
    cap = cv2.VideoCapture(video_path)

    # Set the starting frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    # Read the first frame
    ret, frame = cap.read()
    if not ret:
        print("Failed to read the video file or wrong start frame.")
        return None

    # Convert the first frame to float to avoid overflow during addition
    avg_image = np.float32(frame)

    # Loop through the frames
    for _ in range(start_frame + 1, end_frame + 1):
        # Read frame
        ret, frame = cap.read()
        if not ret:
            break

        # Accumulate the frames
        cv2.accumulate(frame, avg_image)

    # Calculate the average
    avg_image = avg_image / (end_frame - start_frame + 1)

    # Convert the average image to uint8 (normal image format)
    avg_image = np.uint8(avg_image)

    # Release the video capture object
    cap.release()

    return avg_image

# Example usage:
# Assuming the video file is located at 'path/to/video.mp4'
# and we want the average image of frames from 100 to 200.
# video_path = 'path/to/video.mp4'
# start_frame = 100
# end_frame = 200
# average_image = calculate_average_image(video_path, start_frame, end_frame)

# To save the average image:
# cv2.imwrite('average_image.png', average_image)

if __name__ == '__main__':
    avg_image = calculate_average_image('bowser_room.mp4', 20, 1429)
    cv2.imwrite('average_image.png', avg_image)
