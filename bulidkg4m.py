#!/usr/bin/env python3
# coding: utf-8
# File: MilitaryGraph.py
# Author: zpeng
# Date: 22-10-20

import os
import json
import codecs
from py2neo import Graph,Node

class MilitaryGraph:
    def __init__(self):
        c_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        self.datapath = os.path.join(c_dir,'military.json')
        self.g = Graph('http://localhost:7474/',auth=("zp","123456"))
    
    def read_nodes(self):
        
        # 节点类别
        military_sys = [] #实体名称
        categorys = [] #类别
        performances = [] #性能指标
        locations = [] #地点
        deploys = [] #部署方式
        exps = [] #案例

        militarysys_infos = [] #系统信息
        
        # 实体关系
        rels_per = [] #实体和性能的关系
        rels_subcategory = [] #实体与小类之间的关系
        rels_categorys = [] #大类与小类之间的关系
        rels_rootcategory =[] #大类和根节点之间的关系
        rels_loca = [] #实体与地点的关系
        rels_deploy = [] #实体与部署的关系
        rels_exp = [] #实体与案例的关系

        cont = 0
        for data in open(self.datapath):
            militarysys_dict = {}
            cont +=1
            print(cont)
            data_json = json.loads(data)
            militarysys = data_json['name']
            militarysys_dict['name'] = militarysys
            military_sys.append(militarysys)
            militarysys_dict['desc'] = ''
            militarysys_dict['category'] = ''
            militarysys_dict['performance'] = ''
            militarysys_dict['location'] = ''
            militarysys_dict['deploy'] = ''
            militarysys_dict['exp'] = ''

            if 'performance' in data_json:
                performances += data_json['performance']
                for performance in data_json['performance']:
                    rels_per.append([militarysys,performance])
            if 'desc' in data_json:
                militarysys_dict['desc'] = data_json['desc']
            if 'location' in data_json:
                locations += data_json['location']
                for location in data_json['location']:
                    rels_loca.append([militarysys,location])
            if 'deploy' in data_json:
                deploys += data_json['deploy']
                for deploy in data_json['deploy']:
                    rels_deploy.append([militarysys,deploy])
            if 'exp' in data_json:
                exps += data_json['exp']
                for exp in data_json['exp']:
                    rels_exp.append([militarysys,exp])
            if 'category' in data_json:
                cure_categorys = data_json['category']
                if len(cure_categorys) == 2:
                    rels_rootcategory.append([cure_categorys[1],cure_categorys[0]])
                    rels_subcategory.append([militarysys,cure_categorys[1]])
                if len(cure_categorys) == 3:
                    root = cure_categorys[0]
                    big = cure_categorys[1]
                    small = cure_categorys[2]
                    rels_rootcategory.append([big,root])
                    rels_categorys.append([small,big])
                    rels_subcategory.append([militarysys,small])

                militarysys_dict['category'] = cure_categorys
                categorys += cure_categorys

            militarysys_infos.append(militarysys_dict)
        return militarysys_infos, set(military_sys),set(locations),set(performances),set(categorys),set(exps),set(deploys),\
            rels_per,rels_loca,rels_deploy,rels_exp,rels_subcategory,rels_categorys,rels_rootcategory
    
    '''创建实体节点'''
    def create_node(self, label, nodes):
        count = 0
        for node_name in nodes:
            node = Node(label, name=node_name)
            self.g.create(node)
            count += 1
            print(count, len(nodes))
        return

    def create_militarysys_nodes(self, militarysys_infos):
        count = 0
        for militarysys_dict in militarysys_infos:
            node = Node("MSYS", name=militarysys_dict['name'], desc=militarysys_dict['desc'],
                        performance = militarysys_dict['performance'],
                        category=militarysys_dict['category'] ,location=militarysys_dict['location'],
                        deploy=militarysys_dict['deploy'],exp=militarysys_dict['exp'])
            self.g.create(node)
            count += 1
            print(count)
        return   
    
    
    def create_graphnodes(self):
        militarysys_infos, military_sys,locations,performances,categorys,exps,deploys,\
            rels_per,rels_loca,rels_deploy,rels_exp,rels_subcategory,rels_categorys,rels_rootcategory = self.read_nodes()
        self.create_militarysys_nodes(militarysys_infos)
        self.create_node('LOCA',locations)
        self.create_node('PERF',performances)
        self.create_node('CATE',categorys)
        print(len(categorys))
        self.create_node('EXPS',exps)
        self.create_node('DEPLOY',deploys)
        return

    '''创建实体关联边'''
    def create_graphrels(self):
        militarysys_infos, military_sys,locations,performances,categorys,exps,deploys,\
            rels_per,rels_loca,rels_deploy,rels_exp,rels_subcategory,rels_categorys,rels_rootcategory = self.read_nodes()
        self.create_relationship('MSYS','PERF',rels_per,'performances','性能指标')
        self.create_relationship('MSYS','LOCA',rels_loca,'locations','位置')
        self.create_relationship('MSYS','DEPLOY',rels_deploy,'deploys','部署')
        self.create_relationship('MSYS','CATE',rels_subcategory,'belongsto','所属类别')
        self.create_relationship('CATE','CATE',rels_categorys,'belongsto','属于')
        self.create_relationship('CATE','CATE',rels_rootcategory,'belongsto','属于')
        self.create_relationship('MSYS','EXPS',rels_exp,'examples','案例')

    
    def create_relationship(self, start_node, end_node, edges, rel_type, rel_name):
        count = 0
        # 去重处理
        set_edges = []
        for edge in edges:
            set_edges.append('###'.join(edge))
        all = len(set(set_edges))
        for edge in set(set_edges):
            edge = edge.split('###')
            p = edge[0]
            q = edge[1]
            query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                start_node, end_node, p, q, rel_type, rel_name)
            try:
                self.g.run(query)
                count += 1
                print(rel_type, count, all)
            except Exception as e:
                print(e)
        return

    '''导出数据txt格式'''   
    def export_txtdata(self):
        militarysys_infos, military_sys,locations,performances,categorys,exps,deploys,\
            rels_per,rels_loca,rels_deploy,rels_exp,rels_subcategory,rels_categorys,rels_rootcategory = self.read_nodes()
        f_military_sys = open('militarysys.txt', 'w+')
        f_locations = open('locations.txt', 'w+')
        f_performances = open('performances.txt', 'w+')
        f_categorys = open('categorys.txt', 'w+')
        f_exps = open('exps.txt', 'w+')
        f_deploys = open('deploys.txt', 'w+')

        f_military_sys.write('\n'.join(list(military_sys)))
        f_locations.write('\n'.join(list(locations)))
        f_performances.write('\n'.join(list(performances)))
        f_categorys.write('\n'.join(list(categorys)))
        f_exps.write('\n'.join(list(exps)))
        f_deploys.write('\n'.join(list(deploys)))

        f_military_sys.close()
        f_locations.close()
        f_performances.close()
        f_categorys.close()
        f_exps.close()
        f_deploys.close()

        return
        
    '''导出数据为json格式'''
    def export_data(self,data,path):
        if isinstance(data[0],str):
            data = sorted([d.strip("...") for d in set(data)])
        with codecs.open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def export_entitys_relations(self):
        militarysys_infos, military_sys,locations,performances,categorys,exps,deploys,\
            rels_per,rels_loca,rels_deploy,rels_exp,rels_subcategory,rels_categorys,rels_rootcategory = self.read_nodes()
        #导出实体，属性
        self.export_data(list(military_sys),'./graph_data/military_sys.json')
        self.export_data(list(locations),'./graph_data/locations.json')
        self.export_data(list(performances),'./graph_data/performances.json')
        self.export_data(list(categorys),'./graph_data/categorys.json')
        self.export_data(list(exps),'./graph_data/exps.json')
        self.export_data(list(deploys),'./graph_data/deploys.json')
        #导出关系
        self.export_data(rels_per,'./graph_data/rels_per.json')
        self.export_data(rels_loca,'./graph_data/rels_loca.json')
        self.export_data(rels_deploy,'./graph_data/rels_deploy.json')
        self.export_data(rels_exp,'./graph_data/rels_exp.json')
        self.export_data(rels_subcategory,'./graph_data/rels_subcategory.json')
        self.export_data(rels_categorys,'./graph_data/rels_categorys.json')
        self.export_data(rels_rootcategory,'./graph_data/rels_rootcategory.json')




if __name__ == '__main__':
    handler = MilitaryGraph()
    print("step1:导入图谱节点中")
    handler.create_graphnodes()
    print("step2:导入图谱边中")      
    handler.create_graphrels()   
    # print("step3:导出数据")
    # handler.export_entitys_relations()










    
