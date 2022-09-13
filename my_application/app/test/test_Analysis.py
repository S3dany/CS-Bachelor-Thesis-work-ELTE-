from unittest import TestCase, mock
import os
import pandas as pd
from networkx.readwrite import json_graph
import networkx as nx
from app import Analysis
import json
from pandas.testing import assert_frame_equal


class Test(TestCase):
    def setUp(self):

        self.file_path = os.path.join('app\\test\\test_files', 'file_1_ok.csv')
        self.d_graph_path = os.path.join('app\\test\\test_files', 'graph.json')
        self.sub_graph_0_path = os.path.join('app\\test\\test_files', 'sub_graph_0.json')
        self.sub_graph_1_path = os.path.join('app\\test\\test_files', 'sub_graph_1.json')
        self.sub_graph_2_path = os.path.join('app\\test\\test_files', 'sub_graph_2.json')
        self.max_cycle_path = os.path.join('app\\test\\test_files', 'max_cycle_graph.json')
        self.updated_graph_path = os.path.join('app\\test\\test_files', 'updated_graph.json')

        self.country_df_path = os.path.join('app\\test\\test_files', 'country_df.csv')
        self.cycles_df_path = os.path.join('app\\test\\test_files', 'country_df.csv')
        self.initial_df_path = os.path.join('app\\test\\test_files', 'country_df.csv')
        self.transactions_df_path = os.path.join('app\\test\\test_files', 'country_df.csv')

        with open(self.d_graph_path) as f:
            self.js_graph = json.load(f)
        f.close()
        with open(self.sub_graph_0_path) as f:
            self.sub_g_0 = json.load(f)
        f.close()
        with open(self.sub_graph_1_path) as f:
            self.sub_g_1 = json.load(f)
        f.close()
        with open(self.sub_graph_2_path) as f:
            self.sub_g_2 = json.load(f)
        f.close()
        with open(self.max_cycle_path) as f:
            self.max_cycle_graph = json.load(f)
        f.close()
        with open(self.updated_graph_path) as f:
            self.updated_graph = json.load(f)
        f.close()

        self.main_graph = json_graph.node_link_graph(self.js_graph)
        self.strongly_connected_components = [{'AF', 'RU', 'FR'}, {'EG', 'US'}, {'HU', 'RO'}]
        self.sub_graphs = [json_graph.node_link_graph(self.sub_g_0), json_graph.node_link_graph(self.sub_g_1),
                           json_graph.node_link_graph(self.sub_g_2)]

        self.max_cycle_flow = [1500.0, json_graph.node_link_graph(self.max_cycle_graph), ('AF', 'FR')]

        self.to_update = json_graph.node_link_graph(self.sub_g_0)
        self.update_flow = Analysis.find_max_cycle_flow_sum(self.to_update)
        self.updated_graph_result = json_graph.node_link_graph(self.updated_graph)

    def test_create_directed_graph(self):
        self.assertTrue(nx.is_isomorphic(self.main_graph, Analysis.create_directed_graph(pd.read_csv(self.file_path))))

    def test_find_strongly_connected_components(self):
        self.assertEqual(Analysis.find_strongly_connected_components(self.main_graph),
                         self.strongly_connected_components)

    def test_get_subgraphs(self):
        for i in range(len(self.sub_graphs)):
            self.assertTrue(nx.is_isomorphic(Analysis.get_subgraphs(self.main_graph)[i],
                            self.sub_graphs[i]))

    def test_find_max_cycle_flow_sum(self):
        result = Analysis.find_max_cycle_flow_sum(self.sub_graphs[0])
        self.assertEqual(result[0], self.max_cycle_flow[0])
        self.assertTrue(nx.is_isomorphic(result[1], self.max_cycle_flow[1]))
        self.assertEqual(result[2], self.max_cycle_flow[2])

    def test_update_directed_graph(self):
        self.assertTrue(nx.is_isomorphic(self.updated_graph_result,
                                         Analysis.update_directed_graph(self.to_update, self.update_flow)))

    def test_choose_max_cycle_flow(self):
        result = Analysis.choose_max_cycle_flow(self.sub_graphs[0])
        self.assertEqual(self.update_flow[0], result[0])
        self.assertTrue(nx.is_isomorphic(self.update_flow[1], result[1]))
        self.assertEqual(self.update_flow[2], result[2])

    def test_analyse(self):
        file = open(self.file_path, 'r')
        result = Analysis.analyse(file)
        file.close()

        self.assertTrue(result[5].equals(pd.read_csv("app\\test\\test_files\\country_df.csv", dtype={"local_amount": "float64"})))
        self.assertTrue(result[4].equals(pd.read_csv("app\\test\\test_files\\initial_df.csv", dtype={"amount": "float64"})))
        self.assertEquals(result[2], 2700.0)
        self.assertEquals(result[3], 4301.32)
        self.assertEquals(result[6], 8)
        self.assertEquals(result[7], 8)
        self.assertEquals(result[8], 7)
        self.assertEquals(result[9], 3)
        self.assertEquals(result[10], 7)
        self.assertEquals(result[11], 5)





