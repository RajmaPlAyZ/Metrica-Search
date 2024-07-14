import csv

class MetricaNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.frequency = 0  # To track the frequency of each word

class Metrica:
    def __init__(self):
        self.root = MetricaNode()

    def _to_str(self, item):
        """Convert the item to a string representation."""
        return str(item).lower()  # Convert to string and make it case-insensitive if applicable

    def insert(self, item):
        node = self.root
        item_str = self._to_str(item)
        for char in item_str:
            if char not in node.children:
                node.children[char] = MetricaNode()
            node = node.children[char]
        node.is_end_of_word = True
        node.frequency += 1

    def search_prefix(self, prefix, limit=5):
        node = self.root
        prefix_str = self._to_str(prefix)
        for char in prefix_str:
            if char not in node.children:
                return []
            node = node.children[char]
        return self._find_items_from_node(node, prefix_str, limit)

    def _find_items_from_node(self, node, prefix, limit):
        items = []
        self._dfs(node, prefix, items)
        items.sort(key=lambda x: (-x[1], x[0]))  # Sort by frequency (desc) and then lexicographically
        return [item for item, freq in items[:limit]]

    def _dfs(self, node, prefix, items):
        if node.is_end_of_word:
            items.append((prefix, node.frequency))
        for char, next_node in node.children.items():
            self._dfs(next_node, prefix + char, items)

    def delete(self, item):
        def _delete(node, item_str, depth):
            if depth == len(item_str):
                if not node.is_end_of_word:
                    return False
                node.is_end_of_word = False
                node.frequency = 0
                return len(node.children) == 0
            char = item_str[depth]
            if char not in node.children:
                return False
            should_delete_child = _delete(node.children[char], item_str, depth + 1)
            if should_delete_child:
                del node.children[char]
                return len(node.children) == 0
            return False

        item_str = self._to_str(item)
        _delete(self.root, item_str, 0)

    def display_all(self):
        all_items = []
        self._dfs_all(self.root, "", all_items)
        all_items.sort(key=lambda x: (-x[1], x[0]))  # Sort by frequency (desc) and then lexicographically
        for item, freq in all_items:
            print(f"{item}: {freq}")

    def _dfs_all(self, node, prefix, items):
        if node.is_end_of_word:
            items.append((prefix, node.frequency))
        for char, next_node in node.children.items():
            self._dfs_all(next_node, prefix + char, items)

    def load_from_file(self, filename):
        try:
            with open(filename, 'r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    for item in row:
                        self.insert(item)
            print(f"Data loaded from '{filename}' successfully.")
        except FileNotFoundError:
            print(f"File '{filename}' not found.")

    def save_to_file(self, filename):
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            all_items = []
            self._dfs_all(self.root, "", all_items)
            writer.writerow([item for item, freq in all_items])

