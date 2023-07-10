import networkx as nx
from networkx.algorithms import bipartite
import algorithm.bine_helper.train
from argparse import ArgumentParser, FileType, ArgumentDefaultsHelpFormatter
import argparse


def run():
    #G = G_.copy()
    # TODO 받아온 graph로 함수 호출하기

    args = argparse.Namespace()
    args.train_data = r'../dataset/bine_train.dat'
    args.test_data = r'../dataset/bine_test.dat'
    args.model_name = r'bine'
    args.vectors_u = r'../dataset/bine_vectors_u.dat'
    args.vectors_v = r'../dataset/bine_vectors_v.dat'
    args.case_train = r'../data/wiki/case_train.dat'
    args.case_test = r'../data/wiki/case_test.dat'
    args.ws = 5
    args.ns = 4
    args.d = 128
    args.maxT = 32
    args.minT = 1
    args.p = 0.15
    args.alpha = 0.01
    args.beta = 0.01
    args.gamma = 0.1
    args.lam = 0.01
    args.max_iter = 50
    args.top_n = 10
    args.rec = 0
    args.lip = 0
    args.large = 0
    args.mode = 'hits'

    algorithm.bine_helper.train.train_by_sampling(args)
