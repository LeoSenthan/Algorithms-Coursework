class LLRBBST(AbstractSearchInterface):
    RED = True
    BLACK = False

    class _Node:
        def __init__(self, key, color):
            self.key = key
            self.color = color
            self.left = None
            self.right = None

    def __init__(self):
        self.root = None

    def _is_red(self, node):
        return node is not None and node.color == self.RED

    def _rotate_left(self, h):
        x = h.right
        h.right = x.left
        x.left = h
        x.color = h.color
        h.color = self.RED
        return x

    def _rotate_right(self, h):
        x = h.left
        h.left = x.right
        x.right = h
        x.color = h.color
        h.color = self.RED
        return x

    def _flip_colors(self, h):
        h.color = self.RED
        if h.left is not None:
            h.left.color = self.BLACK
        if h.right is not None:
            h.right.color = self.BLACK

    def insertElement(self, element):
        inserted = False

        def _insert(h, key):
            nonlocal inserted
            if h is None:
                inserted = True
                return self._Node(key, self.RED)

            if key < h.key:
                h.left = _insert(h.left, key)
            elif key > h.key:
                h.right = _insert(h.right, key)
            else:
                return h

            if self._is_red(h.right) and not self._is_red(h.left):
                h = self._rotate_left(h)
            if self._is_red(h.left) and self._is_red(h.left.left):
                h = self._rotate_right(h)
            if self._is_red(h.left) and self._is_red(h.right):
                self._flip_colors(h)

            return h

        self.root = _insert(self.root, element)
        if self.root is not None:
            self.root.color = self.BLACK

        return inserted

    def searchElement(self, element):
        found = False
        current = self.root

        while current is not None:
            if element < current.key:
                current = current.left
            elif element > current.key:
                current = current.right
            else:
                found = True
                break

        return found
