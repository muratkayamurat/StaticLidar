cmake_minimum_required(VERSION 3.0.2)
include($ENV{ROS_ROOT}/core/rosbuild/rosbuild.cmake)
set(EXECUTABLE_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/bin)
set(LIBRARY_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/lib)

project(staticlidar)

find_package(catkin REQUIRED COMPONENTS message_generation std_msgs sensor_msgs rospy geometry_msgs trajectory_msgs)

generate_messages(
  DEPENDENCIES
  std_msgs
  geometry_msgs
  trajectory_msgs
)
catkin_package(CATKIN_DEPENDS message_runtime std_msgs sensor_msgs)



catkin_install_python(PROGRAMS nodes/src/staticlidardriver.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

