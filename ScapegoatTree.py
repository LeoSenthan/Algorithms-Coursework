class ScapegoatNode:
    def __init__(self, value, parent=None):
        self.value: str = value
        self.left: ScapegoatNode | None = None
        self.right: ScapegoatNode | None = None
        self.parent: ScapegoatNode | None = parent
        self.size = 1

class ScapegoatTree():

    def __init__(self):
        self.root: ScapegoatNode | None = None
        self.tree_size: int = 0
        # Precomputed ln(1/alpha) for alpha=0.7
        self._ln_inv_alpha = 0.35667494393
        self.a_weight = 0.7

    def _max_depth(self, n: int) -> float:
        if n <= 1:
            return 0.0
        # log_{1/alpha}(n) = ln(n) / ln(1/alpha)
        # Use bit_length for ln(n): ln(n) = log2(n) * ln(2)
        LN2 = 0.69314718056
        shift = n.bit_length() - 1  # equivalent to floor(log2(n))
        m = n / (1 << shift)  # n / 2^shift, which is in [1, 2)
        y = (m - 1.0) / (m + 1.0)
        y2 = y * y
        # ln(n) = ln(2) * shift * ln(m) where m is in [1, 2)
        # ln(m) calculated using the area hyperbolic tangent series expansion
        ln_n = LN2 * (shift + 2.0 * y * (1.0 + y2 *
                      (1.0/3 + y2 * (1.0/5 + y2 * 1.0/7))))
        return ln_n / self._ln_inv_alpha

    def get_size(self, node):
        if node is None:
            return 0
        return 1 + self.get_size(node.left) + self.get_size(node.right)

    def find_scapegoat(self, element: 'ScapegoatNode'):
        child = element
        child_size = 1
        parent = child.parent

        while parent is not None:
            parent_size = parent.size  # Use the stored size attribute
            if child_size > self.a_weight * parent_size:
                return parent
            child = parent
            child_size = parent_size
            parent = parent.parent

        return None

    def collect_elements(self, node, result=None):
        if result is None:
            result = []
        if node is None:
            return result
        self.collect_elements(node.left, result)
        result.append(node.value)
        self.collect_elements(node.right, result)
        return result

    def rebuild_subtree(self, elements, lo, hi, parent=None):
        if lo > hi:
            return None
        mid = (lo + hi) // 2
        node = ScapegoatNode(elements[mid], parent=parent)
        node.left = self.rebuild_subtree(elements, lo, mid - 1, parent=node)
        node.right = self.rebuild_subtree(elements, mid + 1, hi, parent=node)
        node.size = 1 + (node.left.size if node.left else 0) + \
            (node.right.size if node.right else 0)
        return node

    def insertElement(self, element) -> bool:
        inserted_node = None
        depth = 0
        current = self.root
        if self.root is None:
            self.root = ScapegoatNode(element)
            self.tree_size = 1
            return True
        while current is not None:
            current.size += 1  # Increment size for all ancestors
            if element == current.value:
                current.size -= 1  # Revert size increment for duplicates
                return False  # Duplicate, do not insert
            elif element < current.value:
                if current.left is None:
                    current.left = ScapegoatNode(element, parent=current)
                    inserted_node = current.left
                    depth += 1
                    break
                else:
                    current = current.left
                    depth += 1
            else:
                if current.right is None:
                    current.right = ScapegoatNode(element, parent=current)
                    inserted_node = current.right
                    depth += 1
                    break
                else:
                    current = current.right
                    depth += 1
        self.tree_size += 1
        if inserted_node is not None and depth > self._max_depth(self.tree_size):
            scapegoat = self.find_scapegoat(inserted_node)
            # Rebuild the subtree rooted at the scapegoat node to be perfectly balanced
            if scapegoat:
                elements = self.collect_elements(scapegoat)
                rebuilt = self.rebuild_subtree(elements, 0, len(
                    elements) - 1, parent=scapegoat.parent)

                if scapegoat.parent is None:
                    self.root = rebuilt
                elif scapegoat.parent.left == scapegoat:
                    scapegoat.parent.left = rebuilt
                else:
                    scapegoat.parent.right = rebuilt
        return True

    def searchElement(self, element) -> bool:
        current = self.root
        while current is not None:
            if element == current.value:
                return True
            elif element < current.value:
                current = current.left
            else:
                current = current.right
        return False