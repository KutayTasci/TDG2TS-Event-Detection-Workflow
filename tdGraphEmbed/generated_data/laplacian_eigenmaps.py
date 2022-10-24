import os

if 'DISPLAY' not in os.environ:
    disp_avlbl = False
    import matplotlib

    matplotlib.use('Agg')

import networkx as nx
import numpy as np
import scipy.sparse.linalg as lg
from time import time

import sys

sys.path.append('./')
sys.path.append(os.path.realpath(__file__))


class LaplacianEigenmaps():

    def __init__(self, d, **kwargs):
        ''' Initialize the LaplacianEigenmaps class
        Args:
            d: dimension of the embedding
        '''
        hyper_params = {
            'method_name': 'lap_eigmap_svd'
        }
        hyper_params.update(kwargs)
        for key in hyper_params.keys():
            self.__setattr__('_%s' % key, hyper_params[key])
        # for dictionary in hyper_params:
        for key in hyper_params:
            self.__setattr__('_%s' % key, hyper_params[key])
        self._d = d

    def get_method_name(self):
        return self._method_name

    def get_method_summary(self):
        return '%s_%d' % (self._method_name, self._d)

    def learn_embedding(self, graph = None, edge_f = None,
                        is_weighted = False, no_python = False):
        if not graph and not edge_f:
            raise Exception('graph/edge_f needed')
        graph = graph.to_undirected()
        t1 = time()
        L_sym = nx.normalized_laplacian_matrix(graph)

        w, v = lg.eigs(L_sym, k = self._d + 1, which = 'SM')
        t2 = time()
        self._X = v[:, 1:]

        p_d_p_t = np.dot(v, np.dot(np.diag(w), v.T))
        eig_err = np.linalg.norm(p_d_p_t - L_sym)
        print('Laplacian matrix recon. error (low rank): %f' % eig_err)
        return self._X, (t2 - t1)

    def get_embedding(self):
        return self._X

    def get_edge_weight(self, i, j):
        return np.exp(
            -np.power(np.linalg.norm(self._X[i, :] - self._X[j, :]), 2)
        )

    def get_reconstructed_adj(self, X = None, node_l = None):
        if X is not None:
            node_num = X.shape[0]
            self._X = X
        else:
            node_num = self._node_num
        adj_mtx_r = np.zeros((node_num, node_num))
        for v_i in range(node_num):
            for v_j in range(node_num):
                if v_i == v_j:
                    continue
                adj_mtx_r[v_i, v_j] = self.get_edge_weight(v_i, v_j)
        return adj_mtx_r
