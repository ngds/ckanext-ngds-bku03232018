import datetime
import dateutil.parser as parser

class Field():

    field_name = ""
    field_type = ""
    field_description = ""
    field_optional = bool()

    def __init__(self, field):
        self.field_name = field.get("name", "")
        self.field_type = field.get("type", "")
        self.field_description = field.get("description", "")
        self.field_optional = field.get("optional", "")

    def validate_field(self, data):
        """Check that the data matches the required type: string, double or dateTime"""
        msg = None

        # String type
        if self.field_type == "string":
            try:
                data = str(data)
            except:
                if self.field_optional == False:
                    msg = "Error! " + self.field_name + ": Type must be string. Changing " + data + " to Missing"
                else:
                    msg = "Warning! " + self.field_name + ": Not recognized as a string. Deleting " + data
                    data = ""
            if data == "" and self.field_optional == False:
                data = "Missing"
                msg = "Warning! " + self.field_name + ": Can't be blank. Changing to Missing"

        # Double type
        elif self.field_type == "double":
            if data != "":
                try:
                    data = float(data)
                except:
                    if self.field_optional == False:
                        msg = "Warning! " + self.field_name + ": Type must be double. Changing " + str(data) + " to -9999"
                        data = -9999
                    else:
                        msg = "Warning! " + self.field_name + ": Not recognized as a double. Deleting " + str(data)
                        data = ""
            else:
                if self.field_optional == False:
                    data = -9999
                    msg = "Warning! " + self.field_name + ": Can't be blank. Changing to -9999"

        # DateTime type
        elif self.field_type == "dateTime":
            if data != "":
                try:
                    data = (parser.parse(data, default=datetime.datetime(1901, 01, 01, 00, 00, 00))).isoformat()
                except:
                    if self.field_optional == False:
                        msg = "Warning! " + self.field_name + ": Type must be dateTime. Changing " + str(data) + " to 1901-01-01T00:00:00"
                        data = datetime.datetime(1901, 01, 01, 00, 00, 00).isoformat()
                    else:
                        msg = "Warning! " + self.field_name + ": Not recognized as a date. Deleting " + str(data)
                        data = ""
            else:
                if self.field_optional == False:
                    data = datetime.datetime(1901, 01, 01, 00, 00, 00).isoformat()
                    msg = "Warning! " + self.field_name + ": Can't be blank. Changing to " + data

        # Improper schema or new type
        else:
            msg = "Error! " + self.field_name + ": Not indicated in schema to be string, double or dateTime"

        return msg, data

    def fix_format(self, data):
        """Fix a few minor formatting issues"""
        msg = None

        if data == "":
            return msg, data

        try:
            data_strip = data.strip()
            if data != data_strip:
                data = data_strip
                msg = "Notice! " + self.field_name + ": Removed trailing and leading whitespace in " + data
        except:
            pass

        if data == "nil:missing":
            data = "Missing"
            msg = "Notice! " + self.field_name + ": Changed nil:missing to " + data

        return msg, data

    def check_uri(self, data, primaryURIField, used_uris):
        """Check that the URI is formatted correctly and, if it is the primary URI, that it is not repeated"""
        msg = None

        # URI field names which must start with http://resources.usgin.org/uri-gin/ and follow other specs below
        uri_gin_fields = ["ObservationURI", "ParentWellURI", "SamplingFeatureURI", "HeaderURI", "WellBoreURI", "WellHeaderURI"]
        uri_gin_fields.append(primaryURIField.field_name)

        if data == "" or data == "Missing":
            return msg, data, used_uris

        if "URI" in self.field_name:
            # Remove any carriage returns in the URI
            if "\n" in data:
                data = data.replace("\n", "")
                msg = "Notice! " + self.field_name + ": Removed carriage return in " + data
            # Remove any whitespace in the URI, unless there is a pipe character indicating multiple URIs
            if " " in data and not "|" in data:
                data = data.replace(" ", "")
            # If the value is not blank or the word Missing and the field name is not MetadataURI or SourceURI or SourceCitationURI
            if data != "" and data != "Missing" and self.field_name in uri_gin_fields:
                # If the value does not start with "http://resources.usgin.org/uri-gin/"
                if data.find("http://resources.usgin.org/uri-gin/") != 0:
                    msg = "Error! " + self.field_name + ": URI needs to start with http://resources.usgin.org/uri-gin/. Change " + data
                # If the last character is not a backslash add one
                if data[len(data)-1] != "/":
                    data = data + "/"
                    msg = "Notice! " + self.field_name + ": Added missing '/' to the end of " + data
                # If the URI has less than 7 backslashes it does not have enough parts
                if data.count("/") < 7:
                    msg = "Error! " + self.field_name + ": URI field does not have enough components. Change " + data
                # If the current field is the primary URI field there can be no duplicates
                if self.field_name == primaryURIField.field_name:
                    # If the current URI is already in the list of URIs there is an error
                    if data in used_uris:
                        msg = "Error! " + self.field_name + ": URI has already been used. Change " + data
                    # If the current URI is not in the list of URIs add it
                    else:
                        used_uris.append(data)

        return msg, data, used_uris

    def check_temp_units(self, data, temp_units):
        """The temperature units must either be F or C and must be consistent throughout the entire dataset"""
        msg = None

        if data == "":
            return msg, data, temp_units

        if self.field_name == "TemperatureUnits":
            if data.lower() == "f" or data.lower() == "c" or data.lower() == "farenheit" or data.lower() == "celsius":
                if temp_units == "":
                    temp_units = data.lower()
                else:
                    if data.lower() != temp_units:
                        msg = "Error! " + self.field_name + ": Temperature unit " + temp_units + " has already been specified for this data. All units must be consistent. Change " + data
            else:
                msg = "Error! " + self.field_name + ": Temperature unit " + data + " is not valid"

        return msg, data, temp_units

    def check_srs(self, data, srs):
        """Check that the SRS field is consistent throughout the entire dataset"""
        msg = None

        if "SRS" in self.field_name:
            # If the SRS column indicates EPSG:4326 (WGS84)
            if "4326" in data or "84" in data:
                data = "EPSG:4326"
            # If the SRS column indicates EPSG:4269 (NAD83)
            elif "4269" in data or "83" in data:
                data = "EPSG:4269"
            # If the SRS column indicates EPSG:4267 (NAD27)
            elif "4267" in data or "27" in data:
                data = "EPSG:4267"

            if srs == "":
                srs = data
            else:
                if data != srs:
                    msg = "Error! " + self.field_name + ": Coordinate system " + srs + " has already been specified for this data. Coordinate system must remain consistent. Change " + data

        return msg, data, srs

    def check_domain(self, data):
        """Check specified fields for valid data"""
        msg = None

        if self.field_name == "LatDegree" or self.field_name == "LatDegreeWGS84":
            if not (data >= -90 and data <= 90):
                msg = "Error! " + self.field_name + ": Latitude must be between -90 and 90. Change " + str(data)
        elif self.field_name == "LongDegreeWGS84" or self.field_name == "LongDegree":
            if not (data >= -180 and data <= 180):
                msg = "Error! " + self.field_name + ": Longitude must be between -180 and 180. Change " + str(data)
        elif self.field_name == "MaximumRecordedTemperature" or self.field_name == "MeasuredTemperature" or self.field_name == "CorrectedTemperature" or self.field_name == "Temperature":
            if not (data >= 0 and data <= 999) and data != -999 and data != -9999 and data != "":
                msg = "Error! " + self.field_name + ":Temperature must be between 0 and 999. Change " + str(data)

        return msg, data

    def check_field_length(self, data, long_fields):
        """Check for data longer than 255 characters"""

        try:
            long_fields[self.field_name]
        except:
            long_fields[self.field_name] = False
        if len(str(data)) > 255:
            long_fields[self.field_name] = True

        return long_fields