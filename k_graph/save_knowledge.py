"""This file contains the SaveKnowledge Class(ability)
"""
import pandas as pd

#from jarvis_backend.core.knowledge_graph import db_interface
from jarvis_backend.abilities.knowledge_graph.db_interface_prov import DBInterface

#TODO: DB Interface durch Interface von Lennard ersetzen

class SaveKnowledge():
    """This class can be used to save entity
    pairs to the database.
    """

    def __init__(self) -> None:
        pd.set_option('display.max_colwidth', 200)
        self.database = DBInterface()

    def save_multi(self, frame: any, username: str = None) -> bool:
        """Saves multiple datasets the database,
        using the db interface. Return true if ALL
        Data has been saved successfully.

        Args:
            frame (any): Dataframe, containing source, target, relation

        Returns:
            bool: True, False
        """
        result = False
        for _, row in frame.iterrows():
            result = self.database.save_knowledge(
                        username = username,
                        subj_node = row.source,
                        obj_node = row.target,
                        edge = row.edge)
        return result
