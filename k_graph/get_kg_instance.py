"""This file contains the GetKGInstance Class (Ability)"""
import pandas as pd
import networkx as nx


class GetKGInstance():
    """This class can be used to create an instance of the
    knowledge graph (or parts of it) as nx object.
    """

    @staticmethod
    def get_kg_instance(pd_frame: pd.DataFrame) -> any:
        """This method returns the knowlede graph as nx object.

        Args:
            pd_frame (any): PD Data frame with subjects, objects
            and relations.
        """
        k_graph = nx.from_pandas_edgelist(  pd_frame,
                                            "source",
                                            "target",
                                            create_using=nx.MultiDiGraph()
                                        )
        return k_graph
