class DbClass:
    def __init__(self):
        import mysql.connector as connector

        self.__dsn = {
            "host": "localhost",
            "user": "root",
            "passwd": "W4ERmytd",
            "db": "weerstation"
        }

        self.__connection = connector.connect(**self.__dsn)
        self.__cursor = self.__connection.cursor()

    # def getDataFromDatabase(self):
    #     # Query zonder parameters
    #     sqlQuery = "SELECT * FROM tablename"
    #
    #     self.__cursor.execute(sqlQuery)
    #     result = self.__cursor.fetchall()
    #     self.__cursor.close()
    #     return result

    def getDataFromDatabaseMetVoorwaarde(self, voorwaarde):
        # Query met parameters
        sqlQuery = "SELECT meting.SensorWaarde FROM meting WHERE SensorID = '{param1}'"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery.format(param1=voorwaarde)

        self.__cursor.execute(sqlCommand)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result

    def setTempToDatabase(self, waarde, tijdstip):
        sqlQuery = "UPDATE `weerstation`.`meting` SET `SensorWaarde`=('{param1}'), `Tijdstip`=('{param2}') WHERE `SensorID`='1';" % (
        waarde, tijdstip)
        sqlCommand = sqlQuery.format(param1=waarde, param2=tijdstip)

        self.__cursor.execute(sqlCommand)
        self.__connection.commit()
        self.__cursor.close()

    def setLightToDatabase(self, waarde, tijdstip):
        sqlQuery = "UPDATE `weerstation`.`meting` SET `SensorWaarde`=('{param1}'), `Tijdstip`=('{param2}') WHERE `SensorID`='2';" % (
        waarde, tijdstip)
        sqlCommand = sqlQuery.format(param1=waarde, param2=tijdstip)

        self.__cursor.execute(sqlCommand)
        self.__connection.commit()
        self.__cursor.close()

    def setPressureToDatabase(self, waarde, tijdstip):
        sqlQuery = "UPDATE `weerstation`.`meting` SET `SensorWaarde`=('{param1}'), `Tijdstip`=('{param2}') WHERE `SensorID`='3';" % (
        waarde, tijdstip)
        sqlCommand = sqlQuery.format(param1=waarde, param2=tijdstip)

        self.__cursor.execute(sqlCommand)
        self.__connection.commit()
        self.__cursor.close()

    def setHumidityToDatabase(self, waarde, tijdstip):
        sqlQuery = "UPDATE `weerstation`.`meting` SET `SensorWaarde`=('{param1}'), `Tijdstip`=('{param2}') WHERE `SensorID`='4';" % (
            waarde, tijdstip)
        sqlCommand = sqlQuery.format(param1=waarde, param2=tijdstip)

        self.__cursor.execute(sqlCommand)
        self.__connection.commit()
        self.__cursor.close()


        # def setHumidityToDatabase(self, waarde):
        #     sqlQuery = "INSERT INTO meting (SensorID) VALUES ('{param1}') WHERE SensorID = 4"
        #     sqlCommand = sqlQuery.format(param1=waarde)
        #
        #     self.__cursor.execute(sqlCommand)
        #     self.__connection.commit()
        #     self.__cursor.close()