import tkinter as tk
from geometry_msgs.msg import Twist
import rclpy
from rclpy.node import Node


class RosNode(Node):
    def __init__(self):
        super().__init__('tkinter_publisher')
        self.publisher_ = self.create_publisher(Twist, '/diff_cont/cmd_vel_unstamped', 10)

    def publish_twist(self, linear_x, angular_z):
        twist_msg = Twist()
        twist_msg.linear.x = linear_x
        twist_msg.angular.z = angular_z
        self.publisher_.publish(twist_msg)


class GUI:
    def __init__(self, ros_node):
        self.ros_node = ros_node
        self.root = tk.Tk()
        self.root.bind('<KeyPress>', self.on_key_press)
        self.linear_x = 0.0
        self.angular_z = 0.0

    def on_key_press(self, event):
        if event.keysym == 'Up':
            self.linear_x = 0.7
        elif event.keysym == 'Left':
            self.linear_x = 0.0
            self.angular_z = 1.0
        elif event.keysym == 'Right':
            self.linear_x = 0.0
            self.angular_z = -1.0
        elif event.keysym == 'Down':
            self.angular_z = 0.0
            self.linear_x = -0.7
        elif event.keysym == "z":
            self.linear_x = 0.0
            self.angular_z = 0.0

        self.publish_twist()

    def publish_twist(self):
        self.ros_node.publish_twist(self.linear_x, self.angular_z)


def main():
    rclpy.init()
    ros_node = RosNode()
    gui = GUI(ros_node)
    gui.root.mainloop()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
