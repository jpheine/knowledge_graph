"""This module contains the provisional db interface for the knowledge graphö
"""
from jarvis_backend.db_services.db_wrapper import DBWrapper

class DBInterface():
    """This class is used to extracted knowledge as
    entity pairs from a sentence. The entity pairs
    can be further processed.
    """

    def save_knowledge( self,
                        subj_node: str,
                        obj_node: str,
                        edge: str,
                        username: str = None) -> bool:
        """This method creates a table in the database or insert into an existing table on
        the database. The tablename are node_a.

        Args:
            username (str): is None or the username. None = public and "user" = private.
            node_a (str): Node A is the name of the table.
            node_b (str): Node B is the target node.
            edge (str): Egde is the relation from node a to node b.

        Returns:
            bool: isValid
        """
        if username is not None:
            try:
                DBWrapper.query_select(f'{username}_KG')
                self.insert_into_kg(subj_node, obj_node, edge, username)
                return True
            except:
                self.create_kg(username)
                self.insert_into_kg(subj_node, obj_node, edge, username)
                return True
        else:
            try:
                DBWrapper.query_select('public_KG')
                self.insert_into_kg(subj_node, obj_node, edge, username)
                return True
            except:
                self.create_kg()
                self.insert_into_kg(subj_node, obj_node, edge, username)
                return True
        return False

    def select_kg(  self,
                    depth: int = 1,
                    root_node = None,
                    username: str = None) -> any:
        """This methods selects the whole graph of a user or the public knowledge graph.

        Args:
            username (str): is None or the username. None = public and "user" = private.

        Returns:
            str: response (JSON Format)
        """
        try:
            if None not in (depth, root_node):
                if username:
                    node_list = DBWrapper.query_select(f'{username}_KG', ["start"], root_node)
                    return node_list
                node_list = DBWrapper.query_select(f'public_KG', ['start'], root_node)
                return node_list
            else:
                if username:
                    node_list = DBWrapper.query_select(f'{username}_KG')
                    return node_list
                node_list = DBWrapper.query_select(f'public_KG')
                return node_list
        except:
            return False


    @staticmethod
    def create_kg(username: str = None) -> bool:
        """This method creates a table on the database.
        The table looks like node a: (relation,node_b).

        Args:
            start_node (str): Node A is the name of the table.
            node_b (str): Node B is the target node.
            edge (str): Egde is the relation from node a to node b.
            username (str): is None or the username. None = public and "user" = private.

        Returns:
            bool: isValid
        """
        fields = ["start", "target", "relation"]
        types = ["CHAR(60)", "CHAR(60)", "CHAR(60)"]
        if username is not None:
            try:
                DBWrapper.query_create_table(f'{username}_KG', fields, types)
                return True
            except:
                return False
        else:
            try:
                DBWrapper.query_create_table(f'public_KG', fields, types)
                return True
            except:
                return True

    @staticmethod
    def insert_into_kg(subj_node : str, obj_node : str, edge : str, username : str = None):
        """This method inserts nodes into the knowledge base"""
        fields = ["start", "target", "relation"]
        values = [subj_node, obj_node, edge]
        if username is not None:
            try:
                DBWrapper.query_insert(f'{username}_KG', fields, values)
                return True
            except:
                return False
        else:
            try:
                DBWrapper.query_insert(f'public_KG', fields, values)
                return True
            except:
                return False
