"""
arvore_avl.py
Implementação de Árvore AVL (balanceamento automático).
Funcionalidades:
- insert, remove, search
- rotações (simples e duplas)
- percursos: inorder / preorder / postorder
Complexidade:
- Inserção/Remoção/Busca: O(log n)
"""

from typing import Optional, Callable, Any
from grafo import Graph  # cada cidade terá um grafo local


class AVLNode:
    def __init__(self, key: int, name: str = "", data: Any = None):
        self.key = key
        self.name = name
        self.data = data if data is not None else None
        self.left: Optional['AVLNode'] = None
        self.right: Optional['AVLNode'] = None
        self.height = 1

    def __repr__(self):
        return f"AVLNode(key={self.key}, name='{self.name}', h={self.height})"


class AVLTree:
    def __init__(self):
        self.root: Optional[AVLNode] = None

    def _height(self, node: Optional[AVLNode]) -> int:
        return node.height if node else 0

    def _update_height(self, node: AVLNode):
        node.height = 1 + max(self._height(node.left), self._height(node.right))

    def _balance_factor(self, node: AVLNode) -> int:
        return self._height(node.left) - self._height(node.right)

    def _rotate_right(self, y: AVLNode) -> AVLNode:
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        self._update_height(y)
        self._update_height(x)
        return x

    def _rotate_left(self, x: AVLNode) -> AVLNode:
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        self._update_height(x)
        self._update_height(y)
        return y

    def _rebalance(self, node: AVLNode) -> AVLNode:
        self._update_height(node)
        bf = self._balance_factor(node)
        # Left heavy
        if bf > 1:
            if self._balance_factor(node.left) < 0:
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        # Right heavy
        if bf < -1:
            if self._balance_factor(node.right) > 0:
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        return node

    def insert(self, key: int, name: str = "", data: Any = None):
        """Insere e rebalanceia automaticamente. O(log n) amortizado."""
        def _insert(node, key, name, data):
            if node is None:
                # se não passou data, cria um novo Graph para a cidade
                if data is None:
                    data = {'graph': Graph()}
                return AVLNode(key, name, data)
            if key < node.key:
                node.left = _insert(node.left, key, name, data)
            elif key > node.key:
                node.right = _insert(node.right, key, name, data)
            else:
                # atualiza
                node.name = name
                node.data = data or node.data
                return node
            return self._rebalance(node)
        self.root = _insert(self.root, key, name, data)

    def search(self, key: int) -> Optional[AVLNode]:
        node = self.root
        while node:
            if key == node.key:
                return node
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        return None

    def _min_node(self, node: AVLNode) -> AVLNode:
        current = node
        while current.left:
            current = current.left
        return current

    def remove(self, key: int):
        """Remove e rebalanceia. O(log n)."""
        def _remove(node, key):
            if node is None:
                return None
            if key < node.key:
                node.left = _remove(node.left, key)
            elif key > node.key:
                node.right = _remove(node.right, key)
            else:
                # nó encontrado
                if node.left is None:
                    return node.right
                elif node.right is None:
                    return node.left
                else:
                    successor = self._min_node(node.right)
                    node.key = successor.key
                    node.name = successor.name
                    node.data = successor.data
                    node.right = _remove(node.right, successor.key)
            return self._rebalance(node) if node else None
        self.root = _remove(self.root, key)

    # percursos
    def inorder(self, visit: Callable[[AVLNode], None]):
        def _inorder(node):
            if node:
                _inorder(node.left)
                visit(node)
                _inorder(node.right)
        _inorder(self.root)

    def preorder(self, visit: Callable[[AVLNode], None]):
        def _preorder(node):
            if node:
                visit(node)
                _preorder(node.left)
                _preorder(node.right)
        _preorder(self.root)

    def postorder(self, visit: Callable[[AVLNode], None]):
        def _postorder(node):
            if node:
                _postorder(node.left)
                _postorder(node.right)
                visit(node)
        _postorder(self.root)
