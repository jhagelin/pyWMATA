import urllib.request, urllib.error, urllib.parse
from xml.dom.minidom import parseString

class WMATA(object):
    def __init__(self, apikey):
        self.apikey = apikey
        self.transferStations = {'C13':('BL','YL'), 'C07':('BL','YL'), 'F03':('YL','GR','BL','SV','OR'), 'D03':('YL','GR','BL','SV','OR'), 'B01':('RD','YL','GR'),
                                'F01':('RD','YL','GR'), 'A01':('BL','SV','OR','RD'), 'C01':('BL','SV','OR','RD'), 'D08':('SV','BL','OR'), 'C05':('BL','SV','OR'),
                                'K05':('OR','SV'), 'B06':('RD','YL','GR'), 'E06':('RD','YL','GR')}
        self.database = {
                            'RD':[('A15', 'Shady Grove'), ('A14', 'Rockville'), ('A13', 'Twinbrook'), ('A12', 'White Flint'), ('A11', 'Grosvenor'),
                                    ('A10', 'Medical Center'), ('A09', 'Bethesda'), ('A08', 'Friendship Heights'), ('A07', 'Tenleytown'),
                                    ('A06', 'Van Ness UDC'), ('A05', 'Cleveland Park'), ('A04', 'Woodley Park Zoo'), ('A03', 'Dupont Circle'),
                                    ('A02', 'Farragut North'), ('A01', 'Metro Center'), ('B01', 'Gallery Place'),('B02', 'Judiciary Square'),
                                    ('B03', 'Union Station'), ('B35', 'New York Avenue'), ('B04', 'Rhode Island Avenue'), ('B05', 'Brookland'),
                                    ('B06', 'Fort Totten'), ('B07', 'Takoma'), ('B08', 'Silver Spring'), ('B09', 'Forest Glen'), ('B10', 'Wheaton'),
                                    ('B11', 'Glenmont')],
                            'YL':[('C15', 'Huntington'), ('C14', 'Eisenhower Avenue'), ('C13', 'King Street'), ('C12', 'Braddock Road'),
                                    ('C10', 'National Arpt'), ('C09', 'Crystal City'), ('C08', 'Pentagon City'), ('C07', 'Pentagon'),
                                    ('F03', "L'Enfant Plaza"), ('F02', 'Archives'), ('F01', 'Gallery Place'), ('E01', 'Mt Vernon Sq'), ('E02', 'Shaw'),
                                    ('E03', 'U Street'), ('E04', 'Columbia Heights'), ('E05', 'Georgia Avenue'), ('E06', 'Fort Totten')],
                            'BL':[('J03', "Franconia-Springf'ld"), ('J02', 'Van Dorn St'),('C13', 'King Street'), ('C12', 'Braddock Road'),
                                    ('C10', 'National Arpt'), ('C09', 'Crystal City'), ('C08', 'Pentagon City'), ('C07', 'Pentagon'),
                                    ('C06', 'Arlington Cemetery'), ('C05', 'Rosslyn'), ('C04', 'Foggy Bottom'), ('C03', 'Farragut West'),
                                    ('C02', 'McPherson Square'), ('C01', 'Metro Center'), ('D01', 'Federal Triangle'), ('D02', 'Smithsonian'),
                                    ('D03', "L'Enfant Plaza"), ('D04', 'Federal Center SW'), ('D05', 'Capitol South'), ('D06', 'Eastern Market'),
                                    ('D07', 'Potomac Avenue'), ('D08', 'Stadium Armory'), ('G01', 'Benning Road'), ('G02', 'Capitol Heights'),
                                    ('G03', 'Addison Road'), ('G04', 'Morgan Blvd'), ('G05', 'Largo Town Center')],
                            'GR':[('E10', 'Greenbelt'), ('E09', 'College Park'), ('E08', 'Prince Georges Plaza'), ('E07', 'West Hyattsville'),
                                    ('E06', 'Fort Totten'), ('E05', 'Georgia Avenue'), ('E04', 'Columbia Heights'), ('E03', 'U Street'), ('E02', 'Shaw'),
                                    ('E01', 'Mt Vernon Sq'), ('F01', 'Gallery Place'), ('F02', 'Archives'), ('F03', "L'Enfant Plaza"),
                                    ('F04', 'Waterfront'), ('F05', 'Navy Yard'), ('F06', 'Anacostia'), ('F07', 'Congress Height'), ('F08', 'Southern Ave'),
                                    ('F09', 'Naylor Road'), ('F10', 'Suitland'), ('F11', 'Branch Avenue')],
                            'OR':[('D13', 'New Carrollton'), ('D12', 'Landover'), ('D11', 'Cheverly'), ('D10', 'Deanwood'), ('D09', 'Minnesota Avenue'),
                                    ('D08', 'Stadium Armory'), ('D07', 'Potomac Avenue'), ('D06', 'Eastern Market'), ('D05', 'Capitol South'),
                                    ('D04', 'Federal Center SW'), ('D03', "L'Enfant Plaza"), ('D02', 'Smithsonian'), ('D01', 'Federal Triangle'),
                                    ('C01', 'Metro Center'), ('C02', 'McPherson Square'), ('C03', 'Farragut West'), ('C04', 'Foggy Bottom'),
                                    ('C05', 'Rosslyn'), ('K01', 'Court House'), ('K02', 'Clarendon'), ('K03', 'Virginia Square'), ('K04', 'Ballston'),
                                    ('K05', 'E Falls Church'), ('K06', 'W Falls Church'), ('K07', 'Dunn Loring'), ('K08', 'Vienna')],
                            'SV':[('G05', 'Largo Town Center'), ('G04', 'Morgan Blvd'), ('G03', 'Addison Road'), ('G02', 'Capitol Heights'),
                                    ('G01', 'Benning Road'), ('D08', 'Stadium Armory'), ('D07', 'Potomac Avenue'), ('D06', 'Eastern Market'),
                                    ('D05', 'Capitol South'), ('D04', 'Federal Center SW'), ('D03', "L'Enfant Plaza"), ('D02', 'Smithsonian'),
                                    ('D01', 'Federal Triangle'), ('C01', 'Metro Center'), ('C02', 'McPherson Square'), ('C03', 'Farragut West'),
                                    ('C04', 'Foggy Bottom'), ('C05', 'Rosslyn'), ('K01', 'Court House'), ('K02', 'Clarendon'), ('K03', 'Virginia Square'),
                                    ('K04', 'Ballston'), ('K05', 'E Falls Church'), ('N01', 'McLean'), ('N02', 'Tysons Corner'), ('N03', 'Greensboro'),
                                    ('N04', 'Spring Hill'), ('N06', 'Wiehle-Reston East')]
                        }

    def getDirections(self, startStationCode, endStationCode):
        directionStations = []
        linesInCommon = []
        startLines = self.getLines(startStationCode)
        endLines = self.getLines(endStationCode)
        for startLine in startLines:
            for endLine in endLines:
                if startLine == endLine:
                    linesInCommon.append(startLine)
        startIndex = -1
        endIndex = -1
        for line in linesInCommon:
            for index,stationTuple in enumerate(self.database[line]):
                if stationTuple[0] == startStationCode:
                    startIndex = index
                if stationTuple[0] == endStationCode:
                    endIndex = index
            if startIndex == -1 and self.hasDuplicate(startStationCode) and endIndex == -1 and self.hasDuplicate(endStationCode):
                return self.getDirections(self.getDuplicate(startStationCode),self.getDuplicate(endStationCode))
            if startIndex == -1 and self.hasDuplicate(startStationCode):
                return self.getDirections(self.getDuplicate(startStationCode),endStationCode)
            if endIndex == -1 and self.hasDuplicate(endStationCode):
                return self.getDirections(startStationCode, self.getDuplicate(endStationCode))
            if startIndex < endIndex:
                directionStations.append((line,self.database[line][-1][1]))
            if endIndex < startIndex:
                directionStations.append((line,self.database[line][0][1]))
            break
        ###Do something here to take into account lines that do not always run?
        return directionStations

    def getTrainDepartures(self, stationcode, *direction):
        if not self.isStationCode(stationcode):
            stationcode = self.getStationcode(stationcode)
        dom = self.getDom('http://api.wmata.com/StationPrediction.svc/GetPrediction/' + stationcode + '?')
        arrivalTimes = []
        if not direction:
            for index,item in enumerate(dom.getElementsByTagName('Min')):
                arrivalTimes.append(self.processTimeToInt(item.toxml()))
            return arrivalTimes
        for index,item in enumerate(dom.getElementsByTagName('Min')):
            for directionStr in direction:
                if directionStr.lower() in dom.getElementsByTagName('DestinationName')[index].toxml().lower():
                    arrivalTimes.append(self.processTimeToInt(item.toxml()))
        return arrivalTimes

    def getConnectionTimes(self, startArrivalTimes, endArrivalTimes, startStationCode, endStationCode):
        output = [["" for x in range(10)] for x in range(10)]
        travelTime = self.getTravelTime(startStationCode, endStationCode)
        for indexStart,itemStart in enumerate(startArrivalTimes):
            for indexEnd,itemEnd in enumerate(endArrivalTimes):
                output[indexStart][indexEnd] = itemEnd - (itemStart + travelTime)
        return output

    def processTimeToInt(self, xml):
        return int(xml.lower().replace('<min>','').replace('</min>','').replace('brd','0').replace('arr', '0'))

    def getTravelTime(self, startStationCode, endStationCode):
        dom = self.getDom('https://api.wmata.com/Rail.svc/SrcStationToDstStationInfo?FromStationCode=' + startStationCode + '&ToStationCode=' + endStationCode + '&')
        return int(dom.getElementsByTagName('RailTime')[0].toxml().lower().replace('<railtime>','').replace('</railtime>',''))

    def getLines(self, stationCode, *recursion):
        lines = []
        for key,value in self.database.items():
            for code in value:
                if stationCode == code[0]:
                    lines.append(key)
        if self.hasDuplicate(stationCode) and not recursion:
            lines.extend(self.getLines(self.getDuplicate(stationCode),'Don\'t recurse'))
        return lines

    def isStationCode(self, stationcode):
        if len(stationcode) == 3:
            for line in self.database:
                for stationTuple in self.database[line]:
                    if stationTuple[0] == stationcode:
                        return True
        return False

    def isStationName(self, stationName):
        for line in self.database:
            for stationTuple in self.database[line]:
                if stationName.lower() in stationTuple[1].lower():
                    return True
        return False

    def getPath(self, startStationCode, endStationCode):
        if not self.isStationCode(startStationCode):
            startStationCode = self.getStationcode(startStationCode)
        if not self.isStationCode(endStationCode):
            endStationCode = self.getStationcode(endStationCode)
        startLines = self.getLines(startStationCode)
        endLines = self.getLines(endStationCode)
        for startLine in startLines:
            for endLine in endLines:
                if startLine == endLine:
                    return self._getPathSameLine_(startStationCode, endStationCode)
        transferLocations = []
        for key,value in self.transferStations.items():
            for startLine in startLines:
                for endLine in endLines:
                    if startLine in value:
                        if endLine in value:
                            transferLocations.append(key)
        minLocation = None
        totalLen = 10000
        for index,transferStation in enumerate(transferLocations):
            first = self._getPathSameLine_(startStationCode, transferStation)
            second = self._getPathSameLine_(transferStation, endStationCode)
            if len(first) + len(second) < totalLen:
                firstFin = first
                secondFin = second
                totalLen = len(first) + len(second)
                minLocation = transferStation
        first = firstFin[:-1]#remove last line so there are no duplicate stations in the list
        second = secondFin
        first[0] = first[0] + ' (Start towards ' + self.getDirections(startStationCode, minLocation)[0][1] + ')'
        second[0] = second[0] + ' (Transfer towards ' + self.getDirections(minLocation, endStationCode)[0][1] + ')'
        second[-1] = second[-1] + ' (Exit)'
        return [i.encode('ascii') for i in (first+second)] #concat them and return it! :)

    def getPathHumanReadable(self, startStationCode, endStationCode):
        path = self.getPath(startStationCode, endStationCode)
        output = ""
        output += ('Enter the metro at ' + path[0] + '\n')
        for stop in path:
            if 'Transfer' in stop:
                output += ('Transfer trains at ' + stop + '\n')
                break
        output += ('Exit the metro at ' + path[-1] + '\n')
        return output

    def getDuplicate(self, stationcode):
        if stationcode == 'B01':
            return 'F01'
        if stationcode == 'F01':
            return 'B01'
        if stationcode == 'B06':
            return 'E06'
        if stationcode == 'E06':
            return 'B06'
        if stationcode == 'F03':
            return 'D03'
        if stationcode == 'D03':
            return 'F03'
        if stationcode == 'C01':
            return 'A01'
        if stationcode == 'A01':
            return 'C01'
        return stationcode

    def hasDuplicate(self, stationcode):
        if self.getDuplicate(stationcode) == stationcode:
            return False
        return True

    def _getPathSameLine_(self, startStationCode, endStationCode):
        commonLines = []
        startLines = self.getLines(startStationCode)
        endLines = self.getLines(endStationCode)
        for startLine in startLines:
            for endLine in endLines:
                if startLine == endLine:
                    commonLines.append(startLine)
        path = []
        startIndex = -1
        endIndex = -1
        for line in commonLines:
            for index,stationTuple in enumerate(self.database[line]):
                if stationTuple[0] == startStationCode:
                    startIndex = index
                if stationTuple[0] == endStationCode:
                    endIndex = index
            if startIndex == -1 or endIndex == -1:
                for index,stationTuple in enumerate(self.database[line]):
                    if stationTuple[0] == self.getDuplicate(startStationCode):
                        startIndex = index
                    if stationTuple[0] == self.getDuplicate(endStationCode):
                        endIndex = index
            reverse = False
            if startIndex > endIndex:
                startIndex,endIndex = endIndex,startIndex
                reverse = True
            for i in range(startIndex, endIndex + 1):
                path.append(self.database[line][i][1])
            if reverse:
                path.reverse()
            break
        return path

    def getPathSameLine(self, startStationCode, endStationCode):
        path = self._getPathSameLine_(startStationCode, endStationCode)
        path[0]=path[0] + ' (Start towards ' + self.getDirections(startStationCode,endStationCode)[0][1]  + ')'
        path[-1] = path[-1] + ' (End)'
        return path

    def getIncidents(self):
        dom = self.getDom('https://api.wmata.com/Incidents.svc/Incidents?')
        incidents = []
        for incident in dom.getElementsByTagName('Description'):
            incidents.append(incident.toxml())
        return incidents

    def getIncidentsOnLine(self, line):
        dom = self.getDom('https://api.wmata.com/Incidents.svc/Incidents?')
        incidents = []
        for incidentIndex,incident in enumerate(dom.getElementsByTagName('Description')):
            if line in dom.getElementByTagName('LinesAffected')[incidentIndex].toxml():
                incidents.append(incident.toxml())
        return incidents

    def getElevatorEscalatorIncidentsAtStation(self, stationCode):
        dom = self.getDom('https://api.wmata.com/Incidents.svc/ElevatorIncidents?')
        if stationCode in dom.toxml():
            return True
        return False

    def getStationcode(self, stationName):
        for key in self.database:
            for stationTuple in self.database[key]:
                if stationName.lower() in stationTuple[1].lower():
                    return stationTuple[0]

    def getStationName(self, stationCode):
        for key in self.database:
            for stationTuple in self.database[key]:
                if stationTuple[0] == stationCode:
                    return stationTuple[1]

    def getDom(self, url):
        attempts = 0
        while attempts < 30: #Loop 30 times because the WMATA API sometimes just doesn't respond...
            try:
                xml = urllib.request.urlopen(url + 'api_key=' + self.apikey + '&subscription-key=' + self.apikey)
                return parseString(xml.read())
            except:
                attempts += 1
        print("Network communication error")
        exit(1)

    def getNearestStation(self, lat, lon):
        dom = self.getDom('https://api.wmata.com/Rail.svc/StationEntrances?Lat=' + lat + '&Lon=' + lon + '&Radius=0&')
        return dom.getElementsByTagName('StationCode1')[0].toxml().replace('<StationCode1>','').replace('</StationCode1>','')
