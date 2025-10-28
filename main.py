"""
main.py
Interface de linha de comando simples para gerenciar cidades (AVL) e grafos locais (bairros).
Funcionalidades:
- Cadastrar / Remover cidades (AVL)
- Mostrar percursos (pre, in, post)
- Criar / Editar grafos da cidade (adicionar bairros e rotas)
- Executar BFS, DFS e Dijkstra em grafos locais
- Exibir complexidades teóricas após cada operação
"""

from arvore_avl import AVLTree
from grafo import Graph
import sys

avl = AVLTree()


def show_complexity(operation: str):
    tabela = {
        "insercao_avl": "O(log n)",
        "remocao_avl": "O(log n)",
        "search_avl": "O(log n)",
        "bfs": "O(V + E)",
        "dfs": "O(V + E)",
        "dijkstra": "O(E log V)",
    }
    print(f"Complexidade ({operation}): {tabela.get(operation, '—')}")


def cadastrar_cidade():
    try:
        idc = int(input("ID da cidade (inteiro): ").strip())
    except ValueError:
        print("ID inválido.")
        return
    nome = input("Nome da cidade: ").strip()
    # cria node com grafo vazio
    data = {'graph': Graph()}
    avl.insert(idc, nome, data)
    print(f"Cidade '{nome}' (ID {idc}) cadastrada.")
    show_complexity("insercao_avl")


def remover_cidade():
    try:
        idc = int(input("ID da cidade a remover: ").strip())
    except ValueError:
        print("ID inválido.")
        return
    node = avl.search(idc)
    if node is None:
        print("Cidade não encontrada.")
        return
    avl.remove(idc)
    print(f"Cidade ID {idc} removida.")
    show_complexity("remocao_avl")


def mostrar_percursos():
    def visit(node):
        print(f"ID: {node.key} | Nome: {node.name} | Altura: {getattr(node, 'height', '—')}")
    print("Pré-ordem:")
    avl.preorder(visit)
    print("\nIn-ordem:")
    avl.inorder(visit)
    print("\nPós-ordem:")
    avl.postorder(visit)


def selecionar_cidade() -> object:
    try:
        idc = int(input("ID da cidade: ").strip())
    except ValueError:
        print("ID inválido.")
        return None
    node = avl.search(idc)
    if node is None:
        print("Cidade não encontrada.")
        return None
    return node


def menu_grafo(node):
    g: Graph = node.data.get('graph')
    if g is None:
        g = Graph()
        node.data['graph'] = g
    while True:
        print(f"\n--- Grafo da cidade '{node.name}' (ID {node.key}) ---")
        print("1. Adicionar bairro ( vértice )")
        print("2. Adicionar rota (aresta) entre bairros")
        print("3. Listar bairros")
        print("4. BFS a partir de bairro")
        print("5. DFS a partir de bairro")
        print("6. Dijkstra (caminho mínimo)")
        print("0. Voltar")
        op = input("Escolha: ").strip()
        if op == "1":
            v = input("Nome/ID do bairro a adicionar: ").strip()
            g.add_vertex(v)
            print(f"Bairro '{v}' adicionado.")
        elif op == "2":
            u = input("Origem (bairro): ").strip()
            v = input("Destino (bairro): ").strip()
            w_str = input("Peso (distância) [enter=1]: ").strip()
            w = float(w_str) if w_str else 1.0
            g.add_vertex(u)
            g.add_vertex(v)
            g.add_edge(u, v, w)
            print(f"Rota adicionada: {u} -> {v} (peso {w})")
        elif op == "3":
            print("Bairros:", g.vertices())
        elif op == "4":
            start = input("Bairro inicial: ").strip()
            if start not in g.adj:
                print("Bairro não existe.")
            else:
                ordem = g.bfs(start)
                print("Ordem BFS:", ordem)
                show_complexity("bfs")
        elif op == "5":
            start = input("Bairro inicial: ").strip()
            if start not in g.adj:
                print("Bairro não existe.")
            else:
                ordem = g.dfs(start)
                print("Ordem DFS:", ordem)
                show_complexity("dfs")
        elif op == "6":
            src = input("Bairro origem: ").strip()
            dst = input("Bairro destino: ").strip()
            if src not in g.adj or dst not in g.adj:
                print("Origem ou destino inexistente.")
            else:
                dist, path = g.shortest_path(src, dst)
                if path:
                    print(f"Distância: {dist} | Caminho: {path}")
                else:
                    print("Sem caminho entre os nós.")
                show_complexity("dijkstra")
        elif op == "0":
            break
        else:
            print("Opção inválida.")


def main_menu():
    while True:
        print("\n=== Sistema de Cidades e Rotas ===")
        print("1. Cadastrar cidade")
        print("2. Remover cidade")
        print("3. Mostrar percursos da árvore (pré/in/post)")
        print("4. Acessar grafo local de uma cidade")
        print("5. Balancear a árvore AVL com DSW (apenas para comparação - usa BST temporária)")
        print("0. Sair")
        op = input("Escolha: ").strip()
        if op == "1":
            cadastrar_cidade()
        elif op == "2":
            remover_cidade()
        elif op == "3":
            mostrar_percursos()
        elif op == "4":
            node = selecionar_cidade()
            if node:
                menu_grafo(node)
        elif op == "5":
            # demonstração: converte AVL para BST, aplica DSW e oferece impressão
            print("Operação experimental: exportando AVL para BST, aplicando DSW (balanceamento por vine).")
            from arvore_binaria import BinarySearchTree
            bst = BinarySearchTree()

            def collect_insert(n):
                bst.insert(n.key, n.name, n.data)
            avl.inorder(collect_insert)

            print("BST criada a partir de AVL (inorder). Aplicando DSW...")
            bst.dsw_balance()
            print("Árvore BST balanceada (DSW). Percurso inorder da árvore resultante:")
            bst.inorder(lambda x: print(f"ID {x.key} | Nome {x.name}"))
            print("Observação: essa operação não altera a AVL original — é apenas demonstração.")
        elif op == "0":
            print("Saindo...")
            sys.exit(0)
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    print("Inicializando sistema. Árvore AVL vazia criada.")
    main_menu()
