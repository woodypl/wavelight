import Leap, sys, math
from phue import *

class GestureListener(Leap.Listener):
    VELOCITY_THRESHOLD = -600 # m/s
    NOTE_HOLD = 40000 # microseconds
    MULTISAMPLE_THRESHOLD = 0.5
    BRIDGE_IP = 'CHANGEME'
    BRIDGE_USERNAME = 'FILLMEIN'
    
    def on_init(self, controller):
        print "Initialized. Connecting to bridge\n"
        self.bridge = Bridge(self.BRIDGE_IP, self.BRIDGE_USERNAME)

    def on_connect(self,controller):
        print "LeapMotion connected\n"
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)
        try:
                self.bridge.connect()
        except:
                print "Bridge not connected!"
        print "Bridge connected\n"
        

    def on_frame(self, controller):
        # Get the most recent frame
        frame = controller.frame()
        #print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
        #    frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))

        for gesture in frame.gestures():  
          if gesture.type == Leap.Gesture.TYPE_SWIPE:
                swipe = Leap.SwipeGesture(gesture)
                #print "Swipe id: %d, state: %s, position: %s, direction: %s, speed: %f" % (
                #    gesture.id, gesture.state,
                #    swipe.position, swipe.direction, swipe.speed)
                #If the gesture has been finished, handle it
                if gesture.state == Leap.Gesture.STATE_STOP: self.handle_swipe(swipe)
          elif gesture.type == Leap.Gesture.TYPE_CIRCLE:
                circle = Leap.CircleGesture(gesture)
                self.handle_circle(controller, circle) 

    def handle_swipe(self, swipe):
        print "Finished swipe to {0} at speed {1}".format( "right" if (swipe.direction[0] > 0) else "left", swipe.speed)
        if swipe.speed > 1000:
            self.bridge.lights[0].transitiontime = 0
        else:
            self.bridge.lights[0].transitiontime = 10
        if swipe.direction[0] > 0:
                self.bridge.lights[0].on = True
        else:
                self.bridge.lights[0].on = False
 
    def handle_circle(self, controller, circle):
        # Determine clock direction using the angle between the pointable and the circle normal
        if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/4:
                clockwiseness = 1
                self.bridge.lights[0].brightness = self.bridge.lights[0].brightness+4
        else:
                clockwiseness = 0
                self.bridge.lights[0].brightness = self.bridge.lights[0].brightness-4

        # Calculate the angle swept since the last frame
        swept_angle = 0
        if circle.state != Leap.Gesture.STATE_START:
            previous_update = Leap.CircleGesture(controller.frame(1).gesture(circle.id))
            swept_angle =  (circle.progress - previous_update.progress) * 2 * Leap.PI

        print "Circle id: %d, %s, progress: %f, radius: %f, angle: %f degrees, %s" % (
                circle.id, circle.state, circle.progress, circle.radius, swept_angle * Leap.RAD_TO_DEG, clockwiseness)
        

                                    

 
def main():
    listener = GestureListener()
    controller = Leap.Controller()
    
    controller.add_listener(listener)
   
    try: 
        sys.stdin.readline()
    finally:
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()
