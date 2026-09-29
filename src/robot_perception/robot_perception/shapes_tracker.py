#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from geometry_msgs.msg import Point

from cv_bridge import CvBridge

import cv2
import numpy as np


class ShapeTracker(Node):

    def __init__(self):

        super().__init__('shape_tracker')

        # ==================================================
        # PARAMETERS
        # ==================================================

        self.declare_parameter('shape', 'circle')

        self.target_shape = self.get_parameter(
            'shape'
        ).get_parameter_value().string_value

        self.get_logger().info(
            f"Tracking shape: {self.target_shape}"
        )

        # ==================================================
        # ROS2
        # ==================================================

        self.bridge = CvBridge()

        self.image_sub = self.create_subscription(
            Image,
            '/image_in',
            self.image_callback,
            10
        )

        # SAME TOPIC USED BY follow_ball.py
        self.ball_pub = self.create_publisher(
            Point,
            '/detected_ball',
            10
        )

    # ==================================================
    # SHAPE DETECTION
    # ==================================================

    def detect_shape(self, contour):

        shape = "unknown"

        peri = cv2.arcLength(contour, True)

        approx = cv2.approxPolyDP(
            contour,
            0.04 * peri,
            True
        )

        vertices = len(approx)

        # Circle
        if vertices > 8:
            shape = "circle"

        # Square / Rectangle
        elif vertices == 4:

            x, y, w, h = cv2.boundingRect(approx)

            aspect_ratio = float(w) / h

            if 0.95 <= aspect_ratio <= 1.05:
                shape = "square"
            else:
                shape = "rectangle"

        # Cylinder approximation
        elif 5 <= vertices <= 8:
            shape = "cylinder"

        return shape

    # ==================================================
    # IMAGE CALLBACK
    # ==================================================

    def image_callback(self, msg):

        frame = self.bridge.imgmsg_to_cv2(msg, "bgr8")

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        blur = cv2.GaussianBlur(gray, (5, 5), 0)

        _, thresh = cv2.threshold(
            blur,
            100,
            255,
            cv2.THRESH_BINARY
        )

        contours, _ = cv2.findContours(
            thresh,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        image_height, image_width = gray.shape

        for contour in contours:

            area = cv2.contourArea(contour)

            if area < 500:
                continue

            detected_shape = self.detect_shape(contour)

            # ==================================================
            # MATCH TARGET SHAPE
            # ==================================================

            if detected_shape == self.target_shape:

                x, y, w, h = cv2.boundingRect(contour)

                # Draw box
                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + w, y + h),
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    frame,
                    detected_shape,
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2
                )

                # ==================================================
                # CENTER CALCULATION
                # ==================================================

                center_x = x + w / 2
                center_y = y + h / 2

                # Normalize exactly like detect_ball.py
                norm_x = (center_x - image_width / 2) / (image_width / 2)
                norm_y = (center_y - image_height / 2) / (image_height / 2)

                # Approx size
                size = float(max(w, h)) / image_width

                # ==================================================
                # PUBLISH POINT
                # ==================================================

                point = Point()

                point.x = norm_x
                point.y = norm_y
                point.z = size

                self.ball_pub.publish(point)

                self.get_logger().info(
                    f"{detected_shape} detected | "
                    f"x={norm_x:.2f} "
                    f"y={norm_y:.2f} "
                    f"size={size:.2f}"
                )

                # Track only first matched object
                break

        cv2.imshow("Shape Tracker", frame)

        cv2.waitKey(1)


def main(args=None):

    rclpy.init(args=args)

    node = ShapeTracker()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()