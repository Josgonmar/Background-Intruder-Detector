import cv2
import numpy as np

class IntruderDetector():
    __camera = None
    __background_model = None
    __frame_count = 0
    __kernel_size = (5, 5)
    __min_area_threshold = 0.05 # Modify this value to make the detector more sensitive
    __max_num_contours = 3
    __something_detected = False

    def __init__(self, num_hist_frames):
        try:
            self.__camera = cv2.VideoCapture(0)
            self.__createBackgroundModel(num_hist_frames)
        except:
            print('[ERROR] No camera device found.')
    
    def run(self):
        while self.__camera.isOpened():
            has_frame, frame = self.__camera.read()
            if not has_frame:
                break

            mask = self.__background_model.apply(frame)
            eroded_mask = cv2.erode(mask, np.ones(self.__kernel_size, np.uint8))

            contours, __ = cv2.findContours(eroded_mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

            if len(contours) > 0:
                sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
                max_contour_area = cv2.contourArea(sorted_contours[0])

                frame_contour_area_prop = max_contour_area / (int(self.__camera.get(cv2.CAP_PROP_FRAME_WIDTH) * self.__camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
                
                if frame_contour_area_prop >= self.__min_area_threshold:
                    for idx in range(min(self.__max_num_contours, len(sorted_contours))):
                        xc, yc, wc, hc = cv2.boundingRect(sorted_contours[idx])
                        if idx == 0:
                            x1 = xc
                            y1 = yc
                            x2 = xc + wc
                            y2 = yc + hc
                        else:
                            x1 = min(x1, xc)
                            y1 = min(y1, yc)
                            x2 = max(x2, xc + wc)
                            y2 = max(y2, yc + hc)
                    
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0,0,255), thickness = 2)
                    if not self.__something_detected:
                        self.__something_detected = True
                        print('[INFO] Intruder(s) detected!!!')
            else:
                self.__something_detected = False

            cv2.imshow('Camera vision. Press Q to close the window.', frame)
            key = cv2.waitKey(1)
            if key == ord('Q') or key == ord('q') or key == 27:
                break
        
        cv2.destroyAllWindows()
        print('[INFO] Camera closed. Finishing process...')
    
    def __createBackgroundModel(self, num_hist_frames):
        self.__background_model = cv2.createBackgroundSubtractorKNN(history = num_hist_frames)
        seconds_to_wait = num_hist_frames / int(self.__camera.get(cv2.CAP_PROP_FPS))
        print('[INFO] Creating the background model. Please do not move the camera for about', seconds_to_wait, 'second(s).')

        while self.__frame_count < num_hist_frames:
            _, frame = self.__camera.read()
            self.__background_model.apply(frame)
            self.__frame_count+=1
        
        print('[INFO] Model successfully created')


if __name__ == "__main__":
    IntruderDetector_obj = IntruderDetector(300)
    IntruderDetector_obj.run()