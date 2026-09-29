import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class SimplePublisher(Node):
    def __init__(self):
        super().__init__("simple_publisher")
        self.pub = self.create_publisher(String, "sampath", 10)

        self.counter = 0
        self.frequency = 1.0
        self.get_logger().info("publishing at %d" % self.frequency)
        self.timer = self.create_timer(self.frequency,self.timercallback)

    def timercallback(self):
        msg = String()
        msg.data = "hello sampath counter %d" % self.counter
        self.pub.publish(msg)
        self.counter += 1

def main():
    rclpy.init()
    publihser = SimplePublisher()
    rclpy.spin(publihser)
    publihser.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()