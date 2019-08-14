import u3

d = u3.U3()
d.getCalibrationData()


def reset():
    test = 1


def run_stimulation(lj_io):
    d.setDOState(lj_io['channel'], 1)
    d.setDOState(lj_io['channel'], 0)


def read_digital(lj_io):
    return d.getDIState(lj_io['channel'])


def read_analog(lj_io):
    # d.configIO(FIOAnalog = 31) #AIN0-4 are analog inputs, 5-8 are digital (b00011111)
    # AIN4_REGISTER = 4
    return d.getAIN(lj_io['channel'])