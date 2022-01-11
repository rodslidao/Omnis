from python_utils.setup_objects import *

class Base_Node():
    def __init__(self, data, output_dict, dependent_interface):
        self._interfaces = data['interfaces']
        self._options = data['options']
        self._type = data['type']
        self._name=data['name']
        self._id = data['id']
        self._output_id = self.getInterface('Saida', 'id')
        self._input_id = self.getInterface('Entrada', 'id')
        self.interfaces_id = {interface[1]["id"] for  interface in self._interfaces}
        self.output_dict = output_dict
        self.dependent_interface = dependent_interface
    
    def getInterface(self, interface, value, idx=0):
        [op[1][value] for op in self._interfaces if interface in op][idx]
        
    def getOptions(self, option, idx=0):
        [op[1] for op in self._options if option in op][idx]

    def function(self, *args, **kwargs):
        pass
    def run(*args, **kwargs):
        pass
    def reset(*args, **kwargs):
        pass


#! Verificar se o nome "Octopus V1.1" foi trocado para "Octopus V1.1"
class MoveNode(Base_Node):
    def __init__(self, data, output_dict, dependent_interface):
        super().__init__(data, output_dict, dependent_interface)
        axis = ['X ', 'Y ', 'Z ']
        self._controller = self.getOptions('Hardware')
        self._movment = [(op[0], op[1]["value"]) for op in self._interfaces if op[0] in axis]
        self._speed = self._interfaces[1][1]["value"]
        self._movment.append(('F', self._speed))
        self.move = [{"axis":mv[0], "coordinate":mv[1], "channel":0, "await":True} for mv in self._movment]
        self._output = None


        self.dependent_interface
    def run(self, _id):
        if self.output_dict[_id]:    #! Validar input
            print(f"Movendo com {self._controller} para {self.move}")
            machine_objects[self._controller].M_G0(*self._movment, nonsync=None if isinstance(self.move[0], tuple) else True)
            self._output = True
            self.output_dict[self._output_id] = True
        
    def reset(self):
        self._output = None


class IdentifyNode(Base_Node):
    def __init__(self, data, output_dict, dependent_interface):
        super().__init__(data, output_dict, dependent_interface)
    
    def run(self, _id):
        self.output_dict[self._output_id] = Identifyer_objects["small_blue"].identify()
        cv2.imshow("Identificador", Identifyer_objects["small_blue"].drawData())
        cv2.waitKey(1)

class FilterNode(Base_Node):
    def __init__(self, data, output_dict, dependent_interface):
        super().__init__(data, output_dict, dependent_interface)
        self._this = self.getOptions("This")
        self._that = self.getOptions("That")
    
    def run(self, _id):
        if self.output_dict[_id]:
            self.output_dict[self._output_id] = cv2.cvtColor(self.output_dict[_id], getattr(cv2, f"COLOR_{self.this}2{self.that}"))


class BlurNode(Base_Node):
    def __init__(self, data, output_dict, dependent_interface):
        super().__init__(data, output_dict, dependent_interface)
        self._intensity = self.getOptions("Intensity")

    def run(self, _id):
        if self.output_dict[_id]:
            self.output_dict[self._output_id] = cv2.blur(self.output_dict[_id], (self._intensity, self._intensity))


class FindCountorNode(Base_Node):
    def __init__(self, data, output_dict, dependent_interface):
        super().__init__(data, output_dict, dependent_interface)
        self._method = self.getOptions("Method")
        self._mode = self.getOptions("Mode")

    def run(self, _id):
        contours, hierarchy = cv2.findContours(self.output_dict[_id], mode=getattr(cv2, self._mode), method=getattr(cv2, self._method))
        self.output_dict[self._output_id] = {'contours':contours, 'hierarchy':hierarchy}


class FilterCountorNode(Base_Node):
    def __init__(self, data, output_dict, dependent_interface):
        super().__init__(data, output_dict, dependent_interface)
        self._min_perimeter = self.getOptions("Perimetro Minimo")
        self._max_perimeter = self.getOptions("Perimetro Maximo")
        self._min_width = self.getOptions("Largura Minima")
        self._max_width = self.getOptions("Largura Maxima")
        self._min_height = self.getOptions("Altura Minima")
        self._max_height = self.getOptions("Altura Maxima")
        self._min_area = self.getOptions("Area Minima")
        self._max_area = self.getOptions("Area Maxima")
        self.image = camera_objects[self.getOptions("Camera")].read()
    
    def run(_id):

        dataset = set()
        for component in zip(self.output_dict[_id]['contours'], self.output_dict[_id]['hierarchy']):
            dimensions = {}
            currentContour = component[0]
            
            area = cv2.contourArea(currentContour)
            if area < self._min_area or area > self._max_area  : continue
            dimensions['area'] = area

            perimeter = cv2.arcLength(currentContour, True)
            if perimeter < self._min_perimeter or perimeter > self._max_perimeter: continue
            dimensions['perimeter'] = perimeter

            x, y, width, height = cv2.boundingRect(currentContour)
            
            if width < self._min_width or width > self._max_width: continue
            dimensions['width'] = width

            if height < self._min_height or height > self._max_height: continue
            dimensions['height'] = height

            box = np.int0(cv2.boxPoints(cv2.minAreaRect(currentContour)))
            
            sortedBoxX =sorted(box, key=lambda x: x[0])
            sortedBoxY =sorted(box, key=lambda x: x[1])
            A,B,C,D = tuple(sortedBoxX[0]), tuple(sortedBoxX[-1]), tuple(sortedBoxY[0]), tuple(sortedBoxY[-1])
            AB = (abs(A[0]-B[0])**2+abs(A[1]-B[1])**2)**0.5
            AC = (abs(A[0]-C[0])**2+abs(A[1]-C[1])**2)**0.5
            AD = (abs(A[0]-D[0])**2+abs(A[1]-D[1])**2)**0.5

            rectangle = ((xA, yA), (wA, hA))
            dimensions['rectangle'] = rectangle

            dots = {'A':A, 'B':B, 'C':C, 'D':D}
            dimensions['dots'] = dots

            rects = {'AB':AB, 'AC':AC, 'AD':AD}
            dimensions['rects'] = rects

            moments= cv2.moments(currentContour)
            cxA = int(moments["m10"] / moments["m00"])
            cyA = int(moments["m01"] / moments["m00"])

            center = (cxA, cyA)
            dimensions['center'] = center
            dataset.add(dimension_object(**dimensions))


class MathNode(Base_Node):
    def __init__(self, data, output_dict, dependent_interface):
        super().__init__(data, output_dict, dependent_interface)
        self._operation = self.getOptions("Operation")
        self._A = self.getOptions("A")
        self._B = self.getOptions("B")
        self.math_operations = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '*': lambda x, y: x * y,
            '/': lambda x, y: x / y,
            '^': lambda x, y: x ** y,
            '%': lambda x, y: x % y,
            '//': lambda x, y: x // y,
        }
    def run(self, _id):
        self.output_dict[self._output_id] = self.math_operations[self._operation](self._A, self._B)


class HsvMaskNode(Base_Node):
    def __init__(self, data, output_dict, dependent_interface):
        self.color_a = this.getOptions("Cor A")
        self.color_b = this.getOptions("Cor B")

    def run(self, _id):
        if self.output_dict[_id]:
            cv2.inRange(cv2.cvtColor(self.output_dict[_id], cv2.COLOR_BGR2HSV_FULL), np.array(color_range['lower']), np.array(color_range['upper']))
            # self.output_dict[self._output_id] = cv2.cvtColor(, cv2.COLOR_BGR2HSV)


class dimension_object:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


lista de dependencias {"ids das interfaces que o valor depende de outro lugar"}


f = 1
a = {'x':5, 'y':2}
b = {'z': a.get('x')}

a['x'] = 10

print(b)


