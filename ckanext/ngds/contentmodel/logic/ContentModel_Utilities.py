import ckanext.ngds.contentmodel.model.contentmodels
import datetime

def isNumber(s):
    """
    Checking if a String is a Number
    """
    try:
        float(s)
        return True
    except ValueError:
        pass
    
    return False
# def isNumber(s)

def isInteger(s):
    """
    Checking if a String is an Integer
    """
    try:
        int(s)
        return True
    except ValueError:
        pass
    
    return False
# def isInteger(s)

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)


class Error_Message:
    row = 0
    col = 0
    Types = enum('columnNameDoesntExist', 'nonOptionalCellEmpty', 'integerCellViolation', 'numericCellViolation', 'dateCellViolation', 'columnNameOptionalFalseMissing', 'systemError')    
    def __init__(self, row, col, Types, messge):
        self.row = row
        self.col = col
        self.errorType = Types
        self.message = message

class ContentModel_FieldInfoCell(object):
    '''
    field information cell
    '''

    def __init__(self, optional=None, typeString=None, name=None, description=None):
        self.optional    = optional
        self.typeString  = typeString
        self.name        = name
        self.description = description
        
    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        #return str(self.name)
        #return str(self.typeString) 
        return "{name:" + str(self.name) + ", type:" + str(self.typeString) + ", opt:" + str(self.optional) + "}"

# class ContentModel_FieldInfoCell(object)

def validate_header(fieldModelList, dataHeaderList, dataListList):
    print "about to start header checking"
    
    validation_messages = []
    # build link between dataHeaderList and fieldInfoList
    # fieldInfo_index = linkToFieldInfoFromHeader[headaer_index]
    linkToFieldInfoFromHeader = []
    for header in dataHeaderList:
        try:
            index = [i for i, field in enumerate(fieldModelList) if field.name == header]
            linkToFieldInfoFromHeader.append(index[0])
        except:
            msg = "header: %s could NOT be found in the field_info" %(header)
            print msg
            validation_messages.append({'row':0, 'col':0, 'errorType': 'columnNameDoesntExist', 'message':msg})
    print "linkToFieldInfoFromHeader"
    print linkToFieldInfoFromHeader
    print "about to finish header checking"
    return validation_messages
# def validate_header(fieldModelList, dataHeaderList, dataListList)

def validate_existence(fieldModelList, dataHeaderList, dataListList):
    print "about to start field existence checking"
    
    validation_messages = []
    # build link between dataHeaderList and fieldInfoList
    # fieldInfo_index = linkToFieldInfoFromHeader[headaer_index]
    linkToFieldInfoFromHeader = []
    for header in dataHeaderList:
        try:
            index = [i for i, field in enumerate(fieldModelList) if field.name == header]
            linkToFieldInfoFromHeader.append(index[0])
        except:
            pass
    
    OptionalFalseIndex = []
    for i in xrange(len(dataHeaderList)):
        try:
            if fieldModelList[linkToFieldInfoFromHeader[i]].optional == False:
                OptionalFalseIndex.append(i)
        except:
            pass
    print "OptionalFalseIndex:"
    print OptionalFalseIndex
    
    for jd in xrange(len(dataListList)):
        for i in xrange(len(OptionalFalseIndex)):
            data = dataListList[jd][OptionalFalseIndex[i]]
            if (len(data)==0) or (data.isspace()):
                if   len(data) == 0:
                    msg = "cell (%d,%d): null (field %s) is defined as optional false" %(jd+2, i+1,       dataHeaderList[OptionalFalseIndex[i]])
                elif data.isspace():
                    msg = "cell (%d,%d): '%s' (field %s) is defined as optional false" %(jd+2, i+1, data, dataHeaderList[OptionalFalseIndex[i]])
                print msg
                validation_messages.append({'row':jd+2, 'col':i+1, 'errorType': 'nonOptionalCellEmpty', 'message':msg})

        if len(validation_messages) > ckanext.ngds.contentmodel.model.contentmodels.checkfile_maxerror:
            break

    print "about to finish field existence checking"
    return validation_messages
# def validate_existence(fieldModelList, dataHeaderList, dataListList)

def validate_numericType(fieldModelList, dataHeaderList, dataListList):
    print "about to start numeric data type checking"
    
    validation_messages = []
    # build link between dataHeaderList and fieldInfoList
    # fieldInfo_index = linkToFieldInfoFromHeader[headaer_index]
    linkToFieldInfoFromHeader = []
    for header in dataHeaderList:
        try:
            index = [i for i, field in enumerate(fieldModelList) if field.name == header]
            linkToFieldInfoFromHeader.append(index[0])
        except:
            pass
    
    IntTypeIndex = []
    DoubleTypeIndex = []
    for i in xrange(len(dataHeaderList)):
        try:
            if   fieldModelList[linkToFieldInfoFromHeader[i]].typeString == 'int':
                IntTypeIndex.append(i)
            elif fieldModelList[linkToFieldInfoFromHeader[i]].typeString == 'double':
                DoubleTypeIndex.append(i)
        except:
            pass
    print "IntTypeIndex:"
    print IntTypeIndex
    print "DoubleTypeIndex:"
    print DoubleTypeIndex
    
    for jd in xrange(len(dataListList)):
        # check the int type
        for i in xrange(len(IntTypeIndex)):
            data = dataListList[jd][IntTypeIndex[i]]
            if isInteger(data) == False:
                if len(data) > 0:
                    msg = "cell (%d,%d): %s (field %s) is expected to be an Integer"   %(jd+2, i+1, data, dataHeaderList[IntTypeIndex[i]])
                    print msg
                    validation_messages.append({'row':jd+2, 'col':i+1, 'errorType': 'integerCellViolation', 'message':msg})

        # check the double type
        for i in xrange(len(DoubleTypeIndex)):
            data = dataListList[jd][DoubleTypeIndex[i]]
            if isNumber(data) == False:
                if len(data) > 0:
                    msg = "cell (%d,%d): %s (field %s) is expected to be a Numeric"   %(jd+2, i+1, data, dataHeaderList[DoubleTypeIndex[i]])
                    print msg
                    validation_messages.append({'row':jd+2, 'col':i+1, 'errorType': 'numericCellViolation', 'message':msg})

        if len(validation_messages) > ckanext.ngds.contentmodel.model.contentmodels.checkfile_maxerror:
            break

    print "about to finish field numeric checking"
    return validation_messages


def validate_dateType(fieldModelList, dataHeaderList, dataListList):
    print "about to start date data type checking"
    
    validation_messages = []
    # build link between dataHeaderList and fieldInfoList
    # fieldInfo_index = linkToFieldInfoFromHeader[headaer_index]
    linkToFieldInfoFromHeader = []
    for header in dataHeaderList:
        try:
            index = [i for i, field in enumerate(fieldModelList) if field.name == header]
            linkToFieldInfoFromHeader.append(index[0])
        except:
            pass
    
    DateTypeIndex = []  
    for i in xrange(len(dataHeaderList)):
        try:
            if   fieldModelList[linkToFieldInfoFromHeader[i]].typeString == 'datetime':
                DateTypeIndex.append(i)
        except:
            pass
    print "DateTypeIndex:"
    print DateTypeIndex

    
    for jd in xrange(len(dataListList)):
        # check the int type
        for i in xrange(len(DateTypeIndex)):
            data = dataListList[jd][DateTypeIndex[i]]
            try:
                timestamp = data[:-6]
                timestamp = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")
            except ValueError as e:
                print e
                msg = "cell (%d,%d): %s (field %s) is expected to be a ISO 1861 Format datetime"   %(jd+2, DateTypeIndex[i]+1, data, dataHeaderList[DateTypeIndex[i]])
                print msg
                validation_messages.append({'row':jd+2, 'col':DateTypeIndex[i]+1, 'errorType': 'dateCellViolation', 'message':msg})
                pass



        if len(validation_messages) > ckanext.ngds.contentmodel.model.contentmodels.checkfile_maxerror:
            break

    print "about to finish field datetime checking"
    return validation_messages
# def validate_numericType(fieldModelList, dataHeaderList, dataListList)

import ckan.controllers.storage as storage
from pylons import config

def get_url_for_file(label):
    # storage_controller = StorageController()
    resourcename_fullpath = None
    try:
        ofs = storage.get_ofs()
        BUCKET = config.get('ckan.storage.bucket', 'default')
        resourcename_fullpath = ofs.get_url(BUCKET,label)
    except:
        pass
    return resourcename_fullpath 
# def get_url_for_file(label)