"""This file contains the PrintGraph Class(Ability)"""
import networkx as nx
import matplotlib.pyplot as plt

class PrintGraph():
    """This class can be used to print the knowledge graph
    as 2D image.
    """

    @staticmethod
    def print_graph(pd_frame: any):
        """This method prints a knowledge graph.

        Args:
            pd_frame (any): PD Data frame with subjects, objects
            and relations.
        """
        k_graph = nx.from_pandas_edgelist(  pd_frame,
                                            "source",
                                            "target",
                                            create_using=nx.MultiDiGraph()
                                        )
        node_deg = nx.degree(k_graph)
        layout = nx.spring_layout(k_graph, k=0.15, iterations=20)
        plt.figure(num=None, figsize=(120, 90), dpi=80)
        nx.draw_networkx(
            k_graph,
            node_size=[int(deg[1]) * 500 for deg in node_deg],
            arrowsize=20,
            linewidths=1.5,
            pos=layout,
            edge_color='red',
            edgecolors='black',
            node_color='white',
            )
        labels = dict(zip(list(zip(pd_frame.source, pd_frame.target)),
                    pd_frame['edge'].tolist()))
        nx.draw_networkx_edge_labels(k_graph, pos=layout, edge_labels=labels,
                                    font_color='red')
        plt.axis('off')

        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        fp = tempfile.NamedTemporaryFile()

        with open(f"{fp.name}.jpg", 'wb') as temp_file:
            temp_file.write(buf.getvalue())

        buf.close()

        return temp_file
