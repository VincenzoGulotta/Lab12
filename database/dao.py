from database.DB_connect import DBConnect
from model.connessione import Connessione

class DAO:
    """
    Implementare tutte le funzioni necessarie a interrogare il database.
    """
    @staticmethod
    def get_connessioni_anno(year):
        cnx = DBConnect.get_connection()
        if cnx is None:
            print("Errore di connessione!")
            return None
        cursor = cnx.cursor()
        connessioni = []    # Questa è una lista di oggetti Connessione(id1, id2, peso)
        query = """select id_rifugio1, id_rifugio2, distanza, difficolta
                   from connessione
                   where anno <= %s"""
        cursor.execute(query, (year,))
        try:
            for row in cursor:
                if row[3] == "facile":
                    difficolta = 1
                elif row[3] == "media":
                    difficolta = 1.5
                else:
                    difficolta = 2
                peso = float(row[2])*difficolta
                connessione = Connessione(id_rifugio1 = int(row[0]),
                                          id_rifugio2 = int(row[1]),
                                          peso = peso)
                connessioni.append(connessione)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            cnx.close()
        return connessioni

    @staticmethod
    def get_rifugi():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor()
        rifugi = {}     # Questo è un dizionario avente come chiave l'id del rifugio, e come contenuto
                        # una stringa formattata "nome_rifugio (località_rifugio)"
        query = """select id, nome, localita
                   from rifugio"""
        cursor.execute(query)
        if cnx is None:
            print("Errore di connessione!")
        try:
            for row in cursor:
                rifugi[row[0]] = f"{row[1]} ({row[2]})"
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            cnx.close()
        return rifugi

