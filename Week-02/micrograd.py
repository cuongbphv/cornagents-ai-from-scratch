"""
micrograd.py — SKELETON Tuần 2.

TỰ build một autograd engine scalar (tham chiếu repo mở karpathy/micrograd).
Mục tiêu: hiểu backprop = chain rule lan ngược qua computation graph.

Ý tưởng: mỗi `Value` lưu:
  - data    : giá trị số
  - grad    : ∂(output cuối)/∂(self), khởi tạo 0
  - _backward: hàm cục bộ cộng grad vào các "con" (toán hạng tạo ra nó)
  - _prev   : tập các Value cha trực tiếp

Chỗ TODO là phần BẠN tự điền. Tự code trước, đối chiếu Karpathy / check_grad.py sau.
"""

import math


class Value:
    def __init__(self, data, _children=(), _op=""):
        self.data = data
        self.grad = 0.0
        self._backward = lambda: None      # mặc định: không làm gì
        self._prev = set(_children)
        self._op = _op                     # để debug/vẽ graph

    # ---- Phép cộng ----
    def __add__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data + other.data, (self, other), "+")

        def _backward():
            # TODO: với z = a + b  =>  dz/da = 1, dz/db = 1
            #   self.grad  += 1.0 * out.grad
            #   other.grad += 1.0 * out.grad
            raise NotImplementedError("TODO: backward cho phép cộng")

        out._backward = _backward
        return out

    # ---- Phép nhân ----
    def __mul__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data * other.data, (self, other), "*")

        def _backward():
            # TODO: với z = a * b  =>  dz/da = b, dz/db = a
            #   self.grad  += other.data * out.grad
            #   other.grad += self.data  * out.grad
            raise NotImplementedError("TODO: backward cho phép nhân")

        out._backward = _backward
        return out

    # ---- Lũy thừa (số mũ hằng) ----
    def __pow__(self, p):
        assert isinstance(p, (int, float))
        out = Value(self.data ** p, (self,), f"**{p}")

        def _backward():
            # TODO: với z = a**p  =>  dz/da = p * a**(p-1)
            raise NotImplementedError("TODO: backward cho lũy thừa")

        out._backward = _backward
        return out

    # ---- Phi tuyến: tanh ----
    def tanh(self):
        t = math.tanh(self.data)
        out = Value(t, (self,), "tanh")

        def _backward():
            # TODO: d/dx tanh(x) = 1 - tanh(x)^2
            #   self.grad += (1 - t**2) * out.grad
            raise NotImplementedError("TODO: backward cho tanh")

        out._backward = _backward
        return out

    # ---- Phi tuyến: ReLU ----
    def relu(self):
        out = Value(self.data if self.data > 0 else 0.0, (self,), "relu")

        def _backward():
            # TODO: grad đi qua nếu input > 0, ngược lại = 0
            raise NotImplementedError("TODO: backward cho relu")

        out._backward = _backward
        return out

    # ---- backward: lan ngược toàn graph ----
    def backward(self):
        # 1) topological sort các node (con trước, cha sau)
        topo, visited = [], set()

        def build(v):
            if v not in visited:
                visited.add(v)
                for child in v._prev:
                    build(child)
                topo.append(v)

        build(self)

        # 2) grad của output cuối với chính nó = 1
        self.grad = 1.0
        # 3) gọi _backward theo thứ tự ngược của topo
        for node in reversed(topo):
            node._backward()

    # ---- tiện ích để viết biểu thức tự nhiên ----
    def __neg__(self):
        return self * -1

    def __sub__(self, other):
        return self + (-other)

    def __radd__(self, other):
        return self + other

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        return self * other ** -1

    def __repr__(self):
        return f"Value(data={self.data:.4f}, grad={self.grad:.4f})"


if __name__ == "__main__":
    # Ví dụ kiểm tra nhanh (sau khi điền xong TODO):
    a = Value(2.0)
    b = Value(-3.0)
    c = Value(10.0)
    e = a * b
    d = e + c
    f = d.tanh()
    f.backward()
    print("a", a, "b", b, "c", c)
    print("f", f)
