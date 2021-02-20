import cv2
import numpy as np
from lib import line, vector, point


class Detector:
    kernel_ouverture = np.ones((4, 4), np.uint8)
    kernel_dilatation = np.ones((6, 6), np.uint8)

    def __init__(self, path):
        self.innerPath = "../" + path
        self.absolutePath = path
        self.reader = cv2.VideoCapture(self.absolutePath)
        self.list = []
        self.lines = []
        self.points = []

    def read_video(self):
        print("Reading video")
        self.reader.set(cv2.CAP_PROP_POS_FRAMES, 0)
        tot_frame = self.reader.get(cv2.CAP_PROP_FRAME_COUNT)
        previous_percent = -1
        while True:
            ret, frame = self.reader.read()
            if ret:
                current_frame = self.reader.get(cv2.CAP_PROP_POS_FRAMES)
                percent = int((current_frame / tot_frame) * 100)
                if percent % 10 == 0:
                    if previous_percent != percent:
                        print(percent, "%")
                previous_percent = percent

                grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                mask_ouvert = cv2.morphologyEx(grey, cv2.MORPH_OPEN, self.kernel_ouverture)
                edges = cv2.Canny(mask_ouvert, 50, 150, apertureSize=3)
                lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
                if lines is not None:
                    for rho, theta in lines[0]:
                        self.add_list(rho, theta)
            else:
                break
        print("End of reading\n")

    def add_list(self, rho, theta):
        added = False
        for i in range(len(self.list)):
            if abs(theta - self.list[i][0][1]) <= 0.1 * self.list[i][0][1]:
                self.list[i] += [[rho, theta]]
                added = True
        if not added:
            self.list.append([[rho, theta]])

    def sort_list(self):
        for work_list in self.list:
            n = len(work_list)
            for i in range(n):
                for j in range(0, n - i - 1):
                    if work_list[j][0] <= work_list[j + 1][0]:
                        work_list[j], work_list[j + 1] = work_list[j + 1], work_list[j]

    def clean_list(self):
        for work_list in self.list:
            bases = []
            previous_base = 0
            for i in range(len(work_list)):
                if not abs(previous_base - work_list[i][0]) <= 5:
                    bases.append(work_list[i][0])
                    previous_base = work_list[i][0]

            groups = []
            for i in range(len(bases)):
                added = False
                for j in range(len(groups)):
                    if abs(groups[j][0] - bases[i]) <= 200:
                        groups[j] += [bases[i]]
                        added = True
                if not added:
                    groups.append([bases[i]])

            if len(groups) > 1:
                sizes = []
                for g in groups:
                    sizes.append(len(g))

                max_i = 0
                for s in range(1, len(sizes)):
                    if sizes[s] >= sizes[max_i]:
                        max_i = s
                new_bases = groups[max_i]

                sup_index = []
                for i in range(len(work_list)):
                    if work_list[i][0] not in new_bases:
                        sup_index.append(i)
                for i in range(len(sup_index)):
                    work_list.pop(sup_index[i])
                    sup_index = [item - 1 for item in sup_index]

            value = work_list[0][0]
            work_index = 0
            for work_tuple in work_list:
                if abs(value - work_tuple[0]) <= abs(value) * 0.1:
                    work_index += 1
                else:
                    break

            mean_list = np.mean(work_list[:work_index], axis=0)
            self.lines.append(line.Line(mean_list[0], mean_list[1]))

    def get_points(self):
        line1, line2 = self.lines[0], self.lines[1]
        start_point = line1.get_intersection(line2)
        self.points.append(start_point)

        best_frame = self.determine_best_frame(start_point, [255, 255, 255])
        self.reader.set(cv2.CAP_PROP_POS_FRAMES, best_frame)
        size = [self.reader.get(cv2.CAP_PROP_FRAME_HEIGHT), self.reader.get(cv2.CAP_PROP_FRAME_WIDTH)]
        ret, frame = self.reader.read()

        if ret:
            hls = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)

            for work_line in self.lines:
                threshold = 0
                working_vector = vector.Vector(- work_line.vector.b, work_line.vector.a)

                if working_vector.orientation() == 1 or working_vector.orientation() == 2:
                    working_vector = - working_vector

                working_point = start_point * (working_vector * 10)
                working_pixel = [int(working_point.y), int(working_point.x)]

                while threshold < 50:
                    next_point = working_point * (working_vector * 2)
                    next_pixel = [int(next_point.y), int(next_point.x)]

                    if 0 < next_pixel[0] < size[0] and 0 < next_pixel[1] < size[1]:
                        threshold = abs(
                            int(hls[next_pixel[0], next_pixel[1]][0]) - int(hls[working_pixel[0], working_pixel[1]][0]))
                        working_point, working_pixel = next_point, next_pixel
                    else:
                        threshold = 10000000

                if not threshold == 10000000:
                    self.points.append(working_point)

                else:
                    working_point = start_point * (working_vector * 200)
                    threshold, distance = 0, 0

                    if working_vector.orientation() == 0:
                        normal_vector = vector.Vector(working_vector.b, - working_vector.a)
                    elif working_vector.orientation() == 3:
                        normal_vector = vector.Vector(- working_vector.b, working_vector.a)
                    else:
                        distance = 10000000

                    while distance < 30:
                        normal_point = working_point
                        normal_pixel = [int(normal_point.y), int(normal_point.x)]

                        if 0 < normal_pixel[0] < size[0] and 0 < normal_pixel[1] < size[1]:
                            working_frame = frame[normal_pixel[0], normal_pixel[1]]
                            threshold = 0

                            while threshold < 50:
                                next_point = normal_point * normal_vector
                                next_pixel = [int(next_point.y), int(next_point.x)]

                                if 0 < next_pixel[0] < size[0] and 0 < next_pixel[1] < size[1]:
                                    next_frame = frame[next_pixel[0], next_pixel[1]]
                                    threshold = np.mean(abs(next_frame.astype(int) - working_frame.astype(int)))
                                    normal_point = next_point
                                else:
                                    threshold = 10000000
                            if threshold != 10000000:
                                distance = working_point.distance(normal_point)
                                working_point *= (working_vector * 2)

                        else:
                            distance = 10000000

                        if distance > 100:
                            distance = 0
                    if threshold != 10000000 and distance != 10000000:
                        self.points.append(working_point)
            if len(self.points) == 3:
                vector_1 = point.vectorize(self.points[0], self.points[1])
                vector_2 = point.vectorize(self.points[0], self.points[2])
                point_1 = self.points[1] * vector_2
                point_2 = self.points[2] * vector_1
                last_point = point_1.equidistant(point_2)
                self.points.append(last_point)

    def determine_best_frame(self, target, color):
        self.reader.set(cv2.CAP_PROP_POS_FRAMES, 0)
        position = [int(target.y), int(target.x)]
        best_frame = 0
        value = 10000000
        while True:
            ret, frame = self.reader.read()
            if ret:
                pixel = frame[position[0], position[1]]
                next_value = np.mean(abs(color - pixel.astype(int)))
                if next_value < value:
                    value = next_value
                    best_frame = self.reader.get(cv2.CAP_PROP_POS_FRAMES)
            else:
                return best_frame

    def trace(self):
        print("Tracing lines and points")
        size = (1920, 1080)
        fourcc = cv2.VideoWriter_fourcc(*'DIVX')
        out = cv2.VideoWriter('output/outpy.avi', fourcc, self.reader.get(cv2.CAP_PROP_FPS), size)
        self.reader.set(cv2.CAP_PROP_POS_FRAMES, 0)
        tot_frame = self.reader.get(cv2.CAP_PROP_FRAME_COUNT)
        previous_percent = -1

        while True:
            ret, frame = self.reader.read()
            if ret:
                current_frame = self.reader.get(cv2.CAP_PROP_POS_FRAMES)
                percent = int((current_frame / tot_frame) * 100)
                if percent % 10 == 0:
                    if previous_percent != percent:
                        print(percent, "%")
                previous_percent = percent

                disp_frame = frame
                for work_line in self.lines:
                    point1, point2 = work_line.get_tracing_point()
                    cv2.line(disp_frame, point1, point2, color=(0, 0, 255), thickness=2)
                for work_point in self.points:
                    cv2.circle(disp_frame, (int(work_point.x), int(work_point.y)), radius=2, color=(0, 255, 0),
                               thickness=2)
                out.write(disp_frame)
            else:
                break
        print("End of tracing lines and points\n")
        out.release()
