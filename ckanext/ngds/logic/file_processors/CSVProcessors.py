__author__ = 'kaffeine'


def hottest_well_temp(fp):
    hwt = 0
    for row in fp:
        if hwt < row['MaximumRecordedTemperature']:
            hwt = row['MaximumRecordedTemperature']
    return hwt


def coolest_well_temp(fp):
    cwt = 0
    init_v = 0
    for row in fp:
        if init_v == 0:
            cwt = row['MaximumRecordedTemperature']
        if cwt > row['MaximumRecordedTemperature'] and row['MaximumRecordedTemperature'] != 0:
            cwt = row['MaximumRecordedTemperature']
    return cwt