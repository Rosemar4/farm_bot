#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import math

class ObstacleAvoidance(Node):
    def __init__(self):
        super().__init__('obstacle_avoidance')
        
        # Publishers and Subscribers
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.scan_sub = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10
        )
        
        # Parameters
        self.safe_distance = 1.0  # meters
        self.linear_speed = 0.5   # m/s
        self.angular_speed = 0.8  # rad/s
        
        self.get_logger().info('Obstacle Avoidance Node Started')
        
    def scan_callback(self, msg):
        """Process LiDAR data and control robot movement"""
        
        # Divide scan into regions
        ranges = msg.ranges
        num_readings = len(ranges)
        
        # Define sectors (front, left, right)
        front_start = int(num_readings * 0.4)
        front_end = int(num_readings * 0.6)
        left_start = int(num_readings * 0.6)
        left_end = int(num_readings * 0.85)
        right_start = int(num_readings * 0.15)
        right_end = int(num_readings * 0.4)
        
        # Get minimum distances in each sector
        front_ranges = [r for r in ranges[front_start:front_end] if not math.isinf(r) and r > 0]
        left_ranges = [r for r in ranges[left_start:left_end] if not math.isinf(r) and r > 0]
        right_ranges = [r for r in ranges[right_start:right_end] if not math.isinf(r) and r > 0]
        
        front_min = min(front_ranges) if front_ranges else float('inf')
        left_min = min(left_ranges) if left_ranges else float('inf')
        right_min = min(right_ranges) if right_ranges else float('inf')
        
        # Create Twist message
        twist = Twist()
        
        # Decision making for obstacle avoidance
        if front_min > self.safe_distance:
            # Path is clear, move forward
            twist.linear.x = self.linear_speed
            twist.angular.z = 0.0
            self.get_logger().info('Moving forward', throttle_duration_sec=1.0)
            
        elif front_min <= self.safe_distance:
            # Obstacle detected in front
            twist.linear.x = 0.0
            
            # Decide which direction to turn
            if left_min > right_min:
                # More space on the left, turn left
                twist.angular.z = self.angular_speed
                self.get_logger().info('Obstacle ahead! Turning left', throttle_duration_sec=1.0)
            else:
                # More space on the right, turn right
                twist.angular.z = -self.angular_speed
                self.get_logger().info('Obstacle ahead! Turning right', throttle_duration_sec=1.0)
        
        # Publish velocity command
        self.cmd_vel_pub.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = ObstacleAvoidance()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        # Stop the robot
        twist = Twist()
        node.cmd_vel_pub.publish(twist)
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()