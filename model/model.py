import copy

import networkx as nx

from database.DAO import DAO

from geopy import distance



class Model:
    def __init__(self):
        self.grafo=nx.Graph()
        self.idMap={}
        self.solBest=None
        self.maxD=None
        pass

    def getAnni(self):
        return DAO.getAnniDAO()

    def getForme(self,anno):
        return DAO.getFormeDAO(anno)

    def creaGrafo(self,anno,forma):
        self.grafo.clear()
        nodi = DAO.getNodiDAO()
        self.grafo.add_nodes_from(nodi)
        for a in nodi:
            self.idMap[a.id]=a

        archi=DAO.getArchiDAO()
        for a in archi:
            self.grafo.add_edge(self.idMap[a[0]],self.idMap[a[1]])

        avv=DAO.getAvvistamentiDAO(anno,forma)
        for a in archi:
            if self.grafo[self.idMap[a[0]]][self.idMap[a[1]]]=={}:
                if a[0].lower() in avv.keys():
                    peso1=avv[a[0].lower()]
                else:
                    peso1=0
                if a[1].lower() in avv.keys():
                    peso2=avv[a[1].lower()]
                else:
                    peso2=0

                self.grafo[self.idMap[a[0]]][self.idMap[a[1]]]["peso"]= peso1+peso2
        return self.getSomma()
        pass

    def getSomma(self):
        res={}
        for a in list(self.grafo.nodes):
            somma=0
            for i in self.grafo.neighbors(a):
                if self.grafo[a][i]!= {}:
                    somma+=self.grafo[a][i]["peso"]
            res[a]=somma
        return res

    def getDetails(self):
        return len(self.grafo.nodes),len(self.grafo.edges)

    def cammino(self):
        self.solBest=[]
        self.maxD=0
        for start in list(self.grafo.nodes):
            self.ricorsione([start],start)
        res=[]
        for i in range(len(self.solBest)-1):
            res.append((self.solBest[i],self.solBest[i+1],self.grafo[self.solBest[i]][self.solBest[i+1]]["peso"],self.calcola([self.solBest[i],self.solBest[i+1]])))
        return res, self.maxD

    def ricorsione(self, parziale, start):
        succ=list(self.grafo.neighbors(start))
        ammissibili= self.getAmmissibili(parziale,succ,start)

        if self.isTerminale(ammissibili):
            c=self.calcola(parziale)
            if c>self.maxD:
                self.maxD=c
                self.solBest=copy.deepcopy(parziale)
        else:
            for a in ammissibili:
                if self.vaBene(parziale,a):
                    parziale.append(a)
                    self.ricorsione(parziale,a)
                    parziale.pop()
        pass

    def getAmmissibili(self, parziale, succ,start):
        if len(parziale)<2:
            return succ

        amm=[]

        for a in succ:
            if not self.grafo[start][a]=={}:

                if self.grafo[start][a]["peso"]> self.grafo[parziale[-2]][start]["peso"]:
                    amm.append(a)
        return amm


    def isTerminale(self, ammissibili):
        if len(ammissibili)==0:
            return True
        else:
            return False
        pass

    def calcola(self, parziale):
        somma=0
        for i in range(len(parziale)-1):
            latA=parziale[i].Lat
            lngA=parziale[i].Lng
            latB=parziale[i+1].Lat
            lngB=parziale[i+1].Lng

            somma+= distance.geodesic((latA,lngA),(latB,lngB)).km

        return somma
        pass

    def vaBene(self, parziale, a):
        return True
        pass
