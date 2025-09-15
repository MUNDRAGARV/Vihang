The URDF contains all the xacro files needed to define the quadcopter in gazebo.
gazebo.xacro defines the robot for simulating it in gazebo
properties.xacro is used to define the parameters used in the main urdf file
sensors.xacro is for interfacing sensors with gazebo and ros
macros.xacro is defining all the macros for things like wings, body, etc
tilt_drone.urdf.xacro is the main urdf which inherits from all the above files

The gazebo.launch.py file launches the urdf in empty.sdf world in gazebo.