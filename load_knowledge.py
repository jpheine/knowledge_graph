"""This file contains the LoadKnowledge Class(Ability)"""
# from jarvis_backend.core.knowledge_graph import db_interface
from jarvis_backend.abilities.knowledge_graph.db_interface_prov import DBInterface

class LoadKnowledge():
    """This class can be used to load knowledge
    from the database (entity pairs).
    """

    def __init__(self) -> None:
        self.database = DBInterface()

    def load_kg_complete(self, username : str = None):
        """This method loads a complete knowledge graph (either private or
        shared) from the database.

        Args:
            username (str, optional): Username, if a private graph is wanted. Defaults to None.
        """
        result = self.database.select_kg(username=username)
        return result

    def load_kg_partly(self, username : str = None, root_node : str = None, depth : int = 1):
        """This method is used to load a party knowledge graph.
        Depth is used.

        Args:
            root_node(str, optional): Root node. Defaults to None.
            username (str, optional): Username, if a private graph is wanted. Defaults to None.
            depth (int, optional): Depth from root node. Defaults to 1.
        """
        pass
