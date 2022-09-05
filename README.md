# Background-Intruder-Detector
Detect intruders real-time using a camera. This program uses a [OpenCV](https://docs.opencv.org/3.4/db/d88/classcv_1_1BackgroundSubtractorKNN.html#ae1efd8a9c7287f0b01ff024d3eaeff0a) motion detector based on a background/foreground segmentation model in order to highlight all contours that do not belong to the scene previously learned.

## Dependencies:
* [Python](https://www.python.org/doc/) - 3.10.5
* [OpenCV](https://docs.opencv.org/4.6.0/) - 4.6.0
* [Numpy](https://numpy.org/doc/stable/) - 1.22.4

## How to use:
1. Place the camera pointing at the zone you'd like to check. Keep in mind that once the program is running, the camera should not move at all.

2. Go to the */src* folder and execute this:
```console
    $ python IntruderDetector.py
```

3. After a few seconds, a message will be printed in the console indicating that everything is ready! Anything that shows up in front of the camera will be detected and highlighted with a red square.

## License:
Feel free to use this programa whatever you like!