"""This module contains the knowledge graph actor."""

from typing import List
from uuid import uuid4
import pandas as pd


from jarvis_backend.abilities.ability import Ability
from jarvis_backend.abilities.knowledge_graph.get_kg_instance import GetKGInstance
from jarvis_backend.abilities.knowledge_graph.load_knowledge import LoadKnowledge
from jarvis_backend.abilities.knowledge_graph.extract_knowledge import ExtractKnowlegde
from jarvis_backend.abilities.knowledge_graph.save_knowledge import SaveKnowledge
from jarvis_backend.abilities.knowledge_graph.print_graph import PrintGraph
from jarvis_backend.abilities.knowledge_graph.sentence_generation import SentenceGenerator

class KnowledgeGraph(Ability):
    """This class contains the knowledge_graph actor. This actor contains all
    knowledge graph related features and methods."""

    actor_name = "knowledge_graph"

    def __init__(self) -> None:
        super().__init__(process_id=uuid4())
        self.knowledge_extractor = ExtractKnowlegde()
        self.knowledge_saver = SaveKnowledge()
        self.knowledge_loader = LoadKnowledge()
        self.kg_instance = GetKGInstance()
        self.graph_visual = PrintGraph()
        self.sentence_generator = SentenceGenerator()

    def run(self):
        print("Running Knowledge Graph...")

    def extract_knowledge(self, sentences : List[str]) -> pd.DataFrame:
        """Analyzes multiple sentences (a text) and generates multiple
        entity pairs. Returns the entity pairs as pd.DataFrame.

        Args:
            sentences (List[str]): Sentences to be analyzed.

        Returns:
            pd.DataFrame: Extracted knowledge as entity pairs.
        """
        enitity_pairs = []
        relations = []
        for sentence in sentences:
            entities = self.knowledge_extractor.get_entities(sentence)
            if entities is not None:
                enitity_pairs.append(self.knowledge_extractor.get_entities(sentence))
                relations.append(self.knowledge_extractor.get_relation(sentence))
        #Extract subjects
        source = [i[0] for i in enitity_pairs]
        #Extract objects
        target = [i[1] for i in enitity_pairs]
        #Build frame
        ##Das hier gehört eigentlich auch in den tree builder!
        pd_frame = pd.DataFrame({'source': source, 'target': target, 'edge': relations})
        return pd_frame

    def save_knowledge(self, pd_frame: pd.DataFrame, username : str = None) -> any:
        """Saves priveously extracted knowledge to the knowledge database.

        Args:
            pd_frame (pd.DataFrame): Pandas dataframe with entity pairs.
            username (str, optional): Username, if set, the data will be stored onto a
            user specific (private) graph. Defaults to None.

        Returns:
            any: Result (Json)
        """
        result = self.knowledge_saver.save_multi(pd_frame, username)
        return result

    def load_knowledge(    self,
                username : str = None,
                node : str = None,
                relation : str = None,
                depth : int = None) -> any:
        """This methods loads knowledge from the knowledge base and converts
        it to a pandas dataframe.

        Args:
            username (str, optional): Name of the current user. Defaults to None.
            node (str, optional): Root node. Defaults to None.
            relation (str, optional): Relation type. Defaults to None.
            depth (int, optional): Depth for depth searcch. Defaults to None.

        Returns:
            any: PD Frame with nodes and relations.
        """
        if username is not None:
            if depth is not None:
                if node is not None and relation is None:
                    pass
                if node is None and relation is not None:
                    pass
                if None not in (username, node, relation):
                    pass
            else:
                result = self.knowledge_loader.load_kg_complete(username=username)
                source = [json_string['start'] for json_string in result]
                target = [json_string['target'] for json_string in result]
                edge = [json_string['relation'] for json_string in result]
                pd_frame = pd.DataFrame({'source': source, 'target': target, 'edge': edge})
                return pd_frame
        else:
            result = self.knowledge_loader.load_kg_complete()
            source = [json_string['start'] for json_string in result]
            target = [json_string['target'] for json_string in result]
            edge = [json_string['relation'] for json_string in result]
            pd_frame = pd.DataFrame({'source': source, 'target': target, 'edge': edge})
            return pd_frame
        return False

    def get_kg_instance(self, data_frame: pd.DataFrame) -> any:
        """Creates a knowledge graph instance as nx object and returns it.

        Args:
            data_frame (pd.DataFrame): DataFrames to be used in the graph.

        Returns:
            any: KG as nx object
        """
        kg_instance = self.kg_instance.get_kg_instance(pd_frame = data_frame)
        return kg_instance

    def print_graph(self, data_frame: any):
        """This method can be used to show a the KGraph (graphically)

        Args:
            frame (any): Pandas data frame (source, target, edge)
        """
        self.graph_visual.print_graph(pd_frame=data_frame)

    def generate_sentences(self, data_frame: pd.DataFrame) -> List[str]:
        """Generates a List of sentences from a pd.DataFrame

        Args:
            data_frame (pd.DataFrame): Data_frame with sentence(s)

        Returns:
            str: List of genrated Sentences
        """
        return self.sentence_generator.generate_sentences(df = data_frame)

    def generate_text(self, data_frame: pd.DataFrame) -> str:
        """Generates a text from a pd.DataFrame

        Args:
            data_frame (pd.DataFrame): Data_frame with sentence(s)

        Returns:
            str: text
        """
        return self.sentence_generator.generate_text(df = data_frame)
