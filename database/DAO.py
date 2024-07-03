from database.DB_connect import DBConnect
from model.state import Stato


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAnniDAO():
        cnx=DBConnect.get_connection()
        cursor= cnx.cursor()
        query="""select distinct year(s.`datetime`) dateS
                from new_ufo_sightings.sighting s 
                order by dateS"""
        cursor.execute(query)
        res=[]
        for a in cursor:
            res.append(a[0])
        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getFormeDAO(anno):
        cnx=DBConnect.get_connection()
        cursor= cnx.cursor()
        query="""select distinct (s.shape)
                from new_ufo_sightings.sighting s 
                where s.shape is not null
                and s.shape <> ""
                and year (s.`datetime`)=%s
                order by s.shape """
        cursor.execute(query,(anno,))
        res=[]
        for a in cursor:
            res.append(a[0])
        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getNodiDAO():
        cnx=DBConnect.get_connection()
        cursor= cnx.cursor(dictionary=True)
        query="""select *
                from new_ufo_sightings.state s """
        cursor.execute(query)
        res=[]
        for a in cursor:
            res.append(Stato(**a))
        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getArchiDAO():
        cnx=DBConnect.get_connection()
        cursor= cnx.cursor(dictionary=False)
        query="""select *
from new_ufo_sightings.neighbor n 
where n.state1<n.state2  """
        cursor.execute(query)
        res=[]
        for a in cursor:
            res.append(a)
        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getAvvistamentiDAO(anno,forma):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=False)
        query = """select s.state ,count(s.id) 
                from new_ufo_sightings.sighting s 
                where year (s.`datetime`)=%s
                and s.shape =%s
                group by s.state   """
        cursor.execute(query,(anno,forma,))
        res = {}
        for a in cursor:
            res[a[0]]=a[1]
        cursor.close()
        cnx.close()
        return res