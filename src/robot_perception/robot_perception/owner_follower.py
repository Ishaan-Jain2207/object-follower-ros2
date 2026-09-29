#!/usr/bin/env python3
import time
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point,Twist
class OwnerFollower(Node):
    SEARCHING=0;TRACKING=1
    def __init__(self):
        super().__init__("owner_follower")
        self.create_subscription(Point,"/detected_ball",self.ball_callback,10)
        self.pub=self.create_publisher(Twist,"/cmd_vel_tracker",10)
        for n,v in [("search_speed",5.0),("kp",1.2),("forward_speed",5.0),("desired_size",0.32),("size_tolerance",0.03),("timeout",1.0),("max_angular",0.8),("max_linear",0.25)]:
            self.declare_parameter(n,v)
        self.search_speed=self.get_parameter("search_speed").value
        self.kp=self.get_parameter("kp").value
        self.forward_speed=self.get_parameter("forward_speed").value
        self.desired_size=self.get_parameter("desired_size").value
        self.size_tol=self.get_parameter("size_tolerance").value
        self.timeout=self.get_parameter("timeout").value
        self.max_ang=self.get_parameter("max_angular").value
        self.max_lin=self.get_parameter("max_linear").value
        self.last_seen=0.0;self.target_x=0.0;self.target_size=0.0;self.state=self.SEARCHING
        self.create_timer(0.05,self.loop)
    def ball_callback(self,msg):
        self.target_x=msg.x;self.target_size=msg.z;self.last_seen=time.time();self.state=self.TRACKING
    def loop(self):
        cmd=Twist()
        if time.time()-self.last_seen>self.timeout:self.state=self.SEARCHING
        if self.state==self.SEARCHING:
            cmd.angular.z=self.search_speed
        else:
            cmd.angular.z=max(-self.max_ang,min(self.max_ang,-self.kp*self.target_x))
            if self.target_size<self.desired_size-self.size_tol:cmd.linear.x=self.forward_speed
            elif self.target_size>self.desired_size+self.size_tol:cmd.linear.x=-0.08
            cmd.linear.x=max(-self.max_lin,min(self.max_lin,cmd.linear.x))
        self.pub.publish(cmd)
def main(args=None):
    rclpy.init(args=args);n=OwnerFollower()
    try:rclpy.spin(n)
    except KeyboardInterrupt:pass
    n.destroy_node();rclpy.shutdown()
if __name__=="__main__":main()
