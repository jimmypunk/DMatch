PROJECT( layoutSegmentation_proj )
FIND_PACKAGE( OpenCV REQUIRED )
ADD_EXECUTABLE( layoutSegmentation layoutSegmentation.cpp )
TARGET_LINK_LIBRARIES( layoutSegmentation ${OpenCV_LIBS} )
