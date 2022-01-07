
import numexpr as ne
import numpy as np
import cv2

from omnis.opencv.macrofilter import cor, colorRange, areaRange, Kernel

class dimension():
    def __init__(self, center, dots, area, rects, rectangle):
        self.area = area
        self.rectangle = rectangle
        self.dots = dots
        self.rects = rects
        self.center = center

class Identifyer():
    def __init__(self, name, cam, machine, _filter, autoColor=True, **kwargs):
        self.filter = _filter #macro.makeFilter(**filter_data)[name]
        self.name = name
        self.cam = cam
        self.machine = machine
        self.AC = autoColor
        pass

    def function(self, image, filter_obj) -> dict:
        color_range  = filter_obj.colorRange.get('cv2_hsv')
        hsv_mask = cv2.inRange(cv2.cvtColor(image, cv2.COLOR_BGR2HSV_FULL), np.array(color_range['lower']), np.array(color_range['upper']))
        better_hsv = cv2.morphologyEx(
                cv2.morphologyEx(hsv_mask, cv2.MORPH_CLOSE, filter_obj.kernel_A),
                                                cv2.MORPH_OPEN,  filter_obj.kernel_B)


        contours, hierarchy = cv2.findContours(better_hsv, mode=getattr(cv2, filter_obj.mode), method=getattr(cv2, filter_obj.method))
        #cv2.imshow("Processimg", image)
        data = []
        try:
            hierarchy = hierarchy[0]
        except TypeError:
            return data
        for component in zip(contours, hierarchy):
            currentContour = component[0]
            area = cv2.contourArea(currentContour)
            template = {}
            areas = filter_obj.areaRange.getRange(unit='px')['px']
            if areas['min'] < area < areas['max']:

                template["area"] = area

                xA, yA, wA, hA = cv2.boundingRect(currentContour)
                template["rectangle"] = ((xA, yA), (wA, hA))

                boxA = np.int0(cv2.boxPoints(cv2.minAreaRect(currentContour)))
                
                sortedBoxX =sorted(boxA, key=lambda x: x[0])
                sortedBoxY =sorted(boxA, key=lambda x: x[1])
                A,B,C,D = tuple(sortedBoxX[0]), tuple(sortedBoxX[-1]), tuple(sortedBoxY[0]), tuple(sortedBoxY[-1])

                AB = (abs(A[0]-B[0])**2+abs(A[1]-B[1])**2)**0.5
                AC = (abs(A[0]-C[0])**2+abs(A[1]-C[1])**2)**0.5
                AD = (abs(A[0]-D[0])**2+abs(A[1]-D[1])**2)**0.5
                # M =  (int((abs(A[0]-B[0])/2)+A[0]), int((abs(C[1]-D[1])/2)+C[1]))
                # template["center"] = M
                
                template["dots"] = {'A':A, 'B':B, 'C':C, 'D':D}
                template["rects"] = {'AB':AB, 'AC':AC, 'AD':AD}

                momentsA = cv2.moments(currentContour)
                cxA = int(momentsA["m10"] / momentsA["m00"])
                cyA = int(momentsA["m01"] / momentsA["m00"])
                template["center"] = (cxA, cyA)
                
                data.append(template)
        return data 

    def identify(self) -> dict:
        if self.AC:
            _min, _max = self.defineColor(self.cam.read())
            self.filter.colorRange.lower = cor(_min, 'cv2_hsv')
            self.filter.colorRange.upper = cor(_max, 'cv2_hsv')

        data = self.function(self.cam.read(), self.filter)
        self.dataset = set()
        for n in data:
            self.dataset.add(dimension(**n))
        return self.dataset

    def defineColor(self, img_color):
        # procura na amostra de cor, a cor dominante
        rgb_base = self.rgbDominantColor(img_color)
        
        # cria uma imagem de amostra que contenha somente a cor dominante
        rgb_base_img = np.zeros([200, 200, 3], np.uint8)
        for c in range(0,3):
            rgb_base_img[:, :, c] = np.zeros([200, 200]) + rgb_base[c]

        # converte a amosta de cor dominante pra hsv
        hsv_bkg = cv2.cvtColor(rgb_base_img, cv2.COLOR_BGR2HSV_FULL)

        #acha os valores correspondentes em hsv tirando uma média de toda a imagem (como é feita de uma cor só, a média é a conversão direta)
        hsv_bkg_median = np.mean(np.array(hsv_bkg), axis=(1,0)).tolist()
        
        # cria um range minimo  máximo usando a média - n% ('n%' é definido pelo objeto)
        hsv_bkg_median_max = list(map(lambda x: x+(x*0.3), hsv_bkg_median))
        hsv_bkg_median_min = list(map(lambda x: x-(x*0.3), hsv_bkg_median))


        return hsv_bkg_median_min, hsv_bkg_median_max

    def rgbDominantColor(self, a):
        a2D = a.reshape(-1,a.shape[-1])
        col_range = (256, 256, 256) # generically : a2D.max(0)+1
        eval_params = {'a0':a2D[:,0],'a1':a2D[:,1],'a2':a2D[:,2],
                    's0':col_range[0],'s1':col_range[1]}
        a1D = ne.evaluate('a0*s0*s1+a1*s0+a2',eval_params)
        return np.unravel_index(np.bincount(a1D).argmax(), col_range)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.__dict__})"

class Filter:
    def __init__(self, name, colorRange_args, areaRange_args, kernel_args, mode_args, method_args):
        self.name = name
        #self.colorRange = colorRange(**colorRange_args)
        list([setattr(self, f"colorRange_{idx}", colorRange(**k)) for idx, k in enumerate(colorRange_args)])
        
        #self.areaRange = areaRange(**areaRange_args)
        list([setattr(self, f"areaRange_{idx}", areaRange(**k)) for idx, k in enumerate(areaRange_args)])
        
        list([setattr(self, f"kernel_{idx}", Kernel(**k)) for idx, k in enumerate(kernel_args)])
        list([setattr(self, f"mode_{idx}", k["name"]) for idx, k in enumerate(mode_args)])
        list([setattr(self, f"method_{idx}", k["name"]) for idx, k in enumerate(method_args)])
        # self.mode = mode
        # self.method = method
