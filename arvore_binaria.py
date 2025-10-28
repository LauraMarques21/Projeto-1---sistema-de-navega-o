"""
árvore_binaria.py
Implementação de uma Árvore Binária de Busca (BST) com:
- insert, search, remove
- percursos recursivos: inorder, preorder, postorder
- função opcional de balanceamento pelo algoritmo DSW (Day–Stout–Warren)
Complexidade:
- Inserção/Busca/Remoção: O(h) (onde h é a altura; pior caso O(n))
- Percursos: O(n)
"""

from typing import Optional, Callable, List, Any


class BSTNode:
    def __init__(self, key: int, name: str = "", data: Any = None):
        self.key = key
        self.name = name
        self.data = data  # pode armazenar objeto cidade, grafos, etc.
        self.left: Optional['BSTNode'] = None
        self.right: Optional['BSTNode'] = None

    def __repr__(self):
        return f"BSTNode(key={self.key}, name='{self.name}')"


class BinarySearchTree:
    def __init__(self):
        self.root: Optional[BSTNode] = None

    def insert(self, key: int, name: str = "", data: Any = None):
        """Insere (key, name, data) na BST."""
        def _insert(node, key, name, data):
            if node is None:
                return BSTNode(key, name, data)
            if key < node.key:
                node.left = _insert(node.left, key, name, data)
            elif key > node.key:
                node.right = _insert(node.right, key, name, data)
            else:
                # chave já existe -> atualiza dados
                node.name = name
                node.data = data
            return node
        self.root = _insert(self.root, key, name, data)

    def search(self, key: int) -> Optional[BSTNode]:
        """Busca nó pela chave. O(h)."""
        node = self.root
        while node:
            if key == node.key:
                return node
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        return None

    def _min_node(self, node: BSTNode) -> BSTNode:
        current = node
        while current.left:
            current = current.left
        return current

    def remove(self, key: int):
        """Remove nó pela chave. O(h)."""
        def _remove(node, key):
            if node is None:
                return None
            if key < node.key:
                node.left = _remove(node.left, key)
            elif key > node.key:
                node.right = _remove(node.right, key)
            else:
                # encontrado
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
            return node
        self.root = _remove(self.root, key)

    # Percursos
    def inorder(self, visit: Callable[[BSTNode], None]):
        def _inorder(node):
            if node:
                _inorder(node.left)
                visit(node)
                _inorder(node.right)
        _inorder(self.root)

    def preorder(self, visit: Callable[[BSTNode], None]):
        def _preorder(node):
            if node:
                visit(node)
                _preorder(node.left)
                _preorder(node.right)
        _preorder(self.root)

    def postorder(self, visit: Callable[[BSTNode], None]):
        def _postorder(node):
            if node:
                _postorder(node.left)
                _postorder(node.right)
                visit(node)
        _postorder(self.root)

    # --- DSW algorithm para transformar BST em árvore balanceada ---
    def _tree_to_vine(self):
        """Converte árvore em uma 'vine' (lista ligada para a direita)."""
        pseudo_root = BSTNode(0)
        pseudo_root.right = self.root
        tail = pseudo_root
        rest = tail.right
        while rest:
            if rest.left is None:
                tail = rest
                rest = rest.right
            else:
                # rotação direita
                left = rest.left
                rest.left = left.right
                left.right = rest
                tail.right = left
                rest = left
        self.root = pseudo_root.right

    def _compress(self, count):
        """Faz count rotações esquerdas consecutivas a partir do pseudo-root."""
        pseudo_root = BSTNode(0)
        pseudo_root.right = self.root
        scanner = pseudo_root
        for _ in range(count):
            child = scanner.right
            if child is None:
                break
            next_child = child.right
            # rotação esquerda
            scanner.right = next_child
            child.right = next_child.left
            next_child.left = child
            scanner = next_child
        self.root = pseudo_root.right

    def dsw_balance(self):
        """
        Balanceamento DSW:
        1) transforma em vine (lista)
        2) calcula m = 2^floor(log2(n+1)) - 1
        3) primeiro compress n - m vezes, depois repetidamente compress m/2, m/4...
        Complexidade: O(n)
        """
        # contar nós
        n = 0
        node = self.root
        # conta usando inorder
        def _count(nod):
            nonlocal n
            if nod:
                _count(nod.left)
                n += 1
                _count(nod.right)
        _count(self.root)
        if n <= 1:
            return
        self._tree_to_vine()
        # maior m = 2^floor(log2(n+1)) - 1
        m = 1
        while m <= n:
            m = m << 1
        m = (m >> 1) - 1
        self._compress(n - m)
        while m > 1:
            m = m >> 1
            self._compress(m)
