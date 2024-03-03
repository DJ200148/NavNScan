import numpy as np
import cv2



def get_turn_direction_from_depth_data(depth_image, low_threshold=500, high_threshold=1000):
    h, w = depth_image.shape
    third_w = w // 3
    forth_h = h // 4

    # Divide the depth image into three sections: left, center, and right
    left = depth_image[:, :third_w]
    center = depth_image[:, third_w:2*third_w]
    right = depth_image[:, 2*third_w:]

    bot_left = left[3*forth_h:, :]
    bot_center = center[3*forth_h:, :]
    bot_right = right[3*forth_h:, :]

    top_left = left[:3*forth_h,:]
    top_center = center[:3*forth_h,:]
    top_right = right[:3*forth_h,:]

    # Filter the depth values that are below the threshold for each section
    bot_left_filtered = bot_left[bot_left < low_threshold]
    bot_center_filtered = bot_center[bot_center < low_threshold]
    bot_right_filtered = bot_right[bot_right < low_threshold]

    top_left_filtered = top_left[top_left < high_threshold]
    top_center_filtered = top_center[top_center < high_threshold]
    top_right_filtered = top_right[top_right < high_threshold]

    # Compute the summation of filtered depth values for each section
    bot_left_sum = np.sum(bot_left_filtered)
    bot_center_sum = np.sum(bot_center_filtered)
    bot_right_sum = np.sum(bot_right_filtered)

    top_left_sum = np.sum(top_left_filtered)
    top_center_sum = np.sum(top_center_filtered)
    top_right_sum = np.sum(top_right_filtered)

    # Check if there's an obstacle in the center section
    center_obstacle = top_center_sum > 0 or bot_center_sum > 0
    left_obstacle = top_left_sum > 0 or bot_left_sum > 0
    right_obstacle = top_right_sum > 0 or bot_right_sum > 0
    if center_obstacle:
        # If there's an obstacle in the center, check left and right sections
        if left_obstacle and right_obstacle:
            return 'stop'  # Both sides blocked
        elif left_obstacle:
            return 'right'  # Obstacle on the left
        elif right_obstacle:
            return 'left'  # Obstacle on the right
        else:
            return 'stop'
    else:
        return 'forward'  # Path is clear


def display_depth_colormap(depth_colormap):
    # Calculate positions for vertical lines at 1/3rd and 2/3rd of the width
    height, width = depth_colormap.shape[:2]
    one_third = int(width / 3)
    two_third = int(width * 2 / 3)
    
    # Calculate position for horizontal line at 3/4th of the height
    three_quarter_height = int(height * 3 / 4)
    
    # Draw vertical lines
    cv2.line(depth_colormap, (one_third, 0), (one_third, height), (255, 0, 0), 2)
    cv2.line(depth_colormap, (two_third, 0), (two_third, height), (255, 0, 0), 2)
    
    # Draw horizontal line at the bottom 1/4th
    cv2.line(depth_colormap, (0, three_quarter_height), (width, three_quarter_height), (255, 0, 0), 2)

    cv2.imshow('Depth Colormap', depth_colormap)