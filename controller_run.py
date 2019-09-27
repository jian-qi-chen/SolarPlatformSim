#! /usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import getopt, sys, math

Ts = 10 # minutes, time step
preh = 24*60 # minutes, prediction horizon
Npi = 6 # number of prediction interval, SHOULD BE 6 OTHERWISE rewrite constraints in MATLAB
Lpi = int(preh/Ts/Npi) # prediction interval (in time steps)
Nts = int(preh/Ts) # number of time step in the prediction horizon
ECMAX_wh = 10 #maximum stored energy in battery in Watt hour
ECMAX = ECMAX_wh * 3600 / 1000 # in KJoules

sim_len = 10 # simulation length in number of Nts, e.g. if Nts*Ts = 24 hour, then sim_len = 10 means 10 days
he_factor = 0.0015 # havested_energy_in_one_time_step(KJ) = he_factor * ETR(Wh/m^2)_read_in_solar_file. 
other_pow  = 0.1 # in W, constant power other than the FPGA face detector part 

def main(argv):
    CaseStudy()

class RHController:
    def __init__(self, csv_file_name, naive_v=0):
        exec(open('matrices.py').read())
        self.candidates = ReadCSV(csv_file_name)
        self.CR = None
        self.SelectionIndex = None
        self.totalSelection = len(self.candidates)
        self.MicroArchIndex = None
        self.PrevMicroArchIndex = None
        self.reconfig = None # 1 - needs reconfiguration, 0 - does not need
        self.ss = None #shift step (stride)
        self.sf = None #scale factor
        self.latency = None # in ms
        self.energy = None # in mJ, energy per frame
        self.accuracy = None
        self.fps = 10 # frame per second
        self.other_power = 0 #constant power that is not consumed by face detector, in W
        self.desired_power = None # U0 in W, not the actual selection
        self.target_clock_cycle = None
        self.power = None
        self.f_flg = 0
        self.naive = naive_v # if 1: use naive controller instead of receding horizon controller

    def SetFPS(self, new_fps):
        self.fps = float(new_fps)

    def SetOtherPower(self, new_other_power):
        self.other_power = float(new_other_power)

    # X - in KJ, the state vector [Ec, ~Es(t), ~Es(t+L),...]', returns the desired power in W
    def GetDesiredPower(self, X):
        if np.all(self.H1.dot(X) <= self.K1):
            U0 = self.B1.dot(X) + self.C1
            self.CR = 1
        elif np.all(self.H2.dot(X) <= self.K2):
            U0 = self.B2.dot(X) + self.C2
            self.CR = 2
        elif np.all(self.H3.dot(X) <= self.K3):
            U0 = self.B3.dot(X) + self.C3
            self.CR = 3
        elif np.all(self.H4.dot(X) <= self.K4):
            U0 = self.B4.dot(X) + self.C4
            self.CR = 4
        elif np.all(self.H5.dot(X) <= self.K5):
            U0 = self.B5.dot(X) + self.C5
            self.CR = 5
        elif np.all(self.H6.dot(X) <= self.K6):
            U0 = self.B6.dot(X) + self.C6
            self.CR = 6
        elif np.all(self.H7.dot(X) <= self.K7):
            U0 = self.B7.dot(X) + self.C7
            self.CR = 7
        elif np.all(self.H8.dot(X) <= self.K8):
            U0 = self.B8.dot(X) + self.C8
            self.CR = 8
        elif np.all(self.H9.dot(X) <= self.K9):
            U0 = self.B9.dot(X) + self.C9
            self.CR = 9
        elif np.all(self.H10.dot(X) <= self.K10):
            U0 = self.B10.dot(X) + self.C10
            self.CR = 10
        elif np.all(self.H11.dot(X) <= self.K11):
            U0 = self.B11.dot(X) + self.C11
            self.CR = 11
        elif np.all(self.H12.dot(X) <= self.K12):
            U0 = self.B12.dot(X) + self.C12
            self.CR = 12
        elif np.all(self.H13.dot(X) <= self.K13):
            U0 = self.B13.dot(X) + self.C13
            self.CR = 13
        elif np.all(self.H14.dot(X) <= self.K14):
            U0 = self.B14.dot(X) + self.C14
            self.CR = 14
        elif np.all(self.H15.dot(X) <= self.K15):
            U0 = self.B15.dot(X) + self.C15
            self.CR = 15
        elif np.all(self.H16.dot(X) <= self.K16):
            U0 = self.B16.dot(X) + self.C16
            self.CR = 16
        elif np.all(self.H17.dot(X) <= self.K17):
            U0 = self.B17.dot(X) + self.C17
            self.CR = 17
        elif np.all(self.H18.dot(X) <= self.K18):
            U0 = self.B18.dot(X) + self.C18
            self.CR = 18
        elif np.all(self.H19.dot(X) <= self.K19):
            U0 = self.B19.dot(X) + self.C19
            self.CR = 19
        elif np.all(self.H20.dot(X) <= self.K20):
            U0 = self.B20.dot(X) + self.C20
            self.CR = 20
        elif np.all(self.H21.dot(X) <= self.K21):
            U0 = self.B21.dot(X) + self.C21
            self.CR = 21
        elif np.all(self.H22.dot(X) <= self.K22):
            U0 = self.B22.dot(X) + self.C22
            self.CR = 22
        elif np.all(self.H23.dot(X) <= self.K23):
            U0 = self.B23.dot(X) + self.C23
            self.CR = 23
        elif np.all(self.H24.dot(X) <= self.K24):
            U0 = self.B24.dot(X) + self.C24
            self.CR = 24
        elif np.all(self.H25.dot(X) <= self.K25):
            U0 = self.B25.dot(X) + self.C25
            self.CR = 25
        elif np.all(self.H26.dot(X) <= self.K26):
            U0 = self.B26.dot(X) + self.C26
            self.CR = 26
        elif np.all(self.H27.dot(X) <= self.K27):
            U0 = self.B27.dot(X) + self.C27
            self.CR = 27
        elif np.all(self.H28.dot(X) <= self.K28):
            U0 = self.B28.dot(X) + self.C28
            self.CR = 28
        elif np.all(self.H29.dot(X) <= self.K29):
            U0 = self.B29.dot(X) + self.C29
            self.CR = 29
        elif np.all(self.H30.dot(X) <= self.K30):
            U0 = self.B30.dot(X) + self.C30
            self.CR = 30
        elif np.all(self.H31.dot(X) <= self.K31):
            U0 = self.B31.dot(X) + self.C31
            self.CR = 31
        elif np.all(self.H32.dot(X) <= self.K32):
            U0 = self.B32.dot(X) + self.C32
            self.CR = 32
        elif np.all(self.H33.dot(X) <= self.K33):
            U0 = self.B33.dot(X) + self.C33
            self.CR = 33
        elif np.all(self.H34.dot(X) <= self.K34):
            U0 = self.B34.dot(X) + self.C34
            self.CR = 34
        elif np.all(self.H35.dot(X) <= self.K35):
            U0 = self.B35.dot(X) + self.C35
            self.CR = 35
        elif np.all(self.H36.dot(X) <= self.K36):
            U0 = self.B36.dot(X) + self.C36
            self.CR = 36
        elif np.all(self.H37.dot(X) <= self.K37):
            U0 = self.B37.dot(X) + self.C37
            self.CR = 37
        elif np.all(self.H38.dot(X) <= self.K38):
            U0 = self.B38.dot(X) + self.C38
            self.CR = 38
        elif np.all(self.H39.dot(X) <= self.K39):
            U0 = self.B39.dot(X) + self.C39
            self.CR = 39
        elif np.all(self.H40.dot(X) <= self.K40):
            U0 = self.B40.dot(X) + self.C40
            self.CR = 40
        elif np.all(self.H41.dot(X) <= self.K41):
            U0 = self.B41.dot(X) + self.C41
            self.CR = 41
        elif np.all(self.H42.dot(X) <= self.K42):
            U0 = self.B42.dot(X) + self.C42
            self.CR = 42
        elif np.all(self.H43.dot(X) <= self.K43):
            U0 = self.B43.dot(X) + self.C43
            self.CR = 43
        elif np.all(self.H44.dot(X) <= self.K44):
            U0 = self.B44.dot(X) + self.C44
            self.CR = 44
        elif np.all(self.H45.dot(X) <= self.K45):
            U0 = self.B45.dot(X) + self.C45
            self.CR = 45
        elif np.all(self.H46.dot(X) <= self.K46):
            U0 = self.B46.dot(X) + self.C46
            self.CR = 46
        elif np.all(self.H47.dot(X) <= self.K47):
            U0 = self.B47.dot(X) + self.C47
            self.CR = 47
        elif np.all(self.H48.dot(X) <= self.K48):
            U0 = self.B48.dot(X) + self.C48
            self.CR = 48
        elif np.all(self.H49.dot(X) <= self.K49):
            U0 = self.B49.dot(X) + self.C49
            self.CR = 49
        elif np.all(self.H50.dot(X) <= self.K50):
            U0 = self.B50.dot(X) + self.C50
            self.CR = 50
        elif np.all(self.H51.dot(X) <= self.K51):
            U0 = self.B51.dot(X) + self.C51
            self.CR = 51
        elif np.all(self.H52.dot(X) <= self.K52):
            U0 = self.B52.dot(X) + self.C52
            self.CR = 52
        elif np.all(self.H53.dot(X) <= self.K53):
            U0 = self.B53.dot(X) + self.C53
            self.CR = 53
        elif np.all(self.H54.dot(X) <= self.K54):
            U0 = self.B54.dot(X) + self.C54
            self.CR = 54
        elif np.all(self.H55.dot(X) <= self.K55):
            U0 = self.B55.dot(X) + self.C55
            self.CR = 55
        elif np.all(self.H56.dot(X) <= self.K56):
            U0 = self.B56.dot(X) + self.C56
            self.CR = 56
        elif np.all(self.H57.dot(X) <= self.K57):
            U0 = self.B57.dot(X) + self.C57
            self.CR = 57
        elif np.all(self.H58.dot(X) <= self.K58):
            U0 = self.B58.dot(X) + self.C58
            self.CR = 58
        elif np.all(self.H59.dot(X) <= self.K59):
            U0 = self.B59.dot(X) + self.C59
            self.CR = 59
        elif np.all(self.H60.dot(X) <= self.K60):
            U0 = self.B60.dot(X) + self.C60
            self.CR = 60
        elif np.all(self.H61.dot(X) <= self.K61):
            U0 = self.B61.dot(X) + self.C61
            self.CR = 61
        elif np.all(self.H62.dot(X) <= self.K62):
            U0 = self.B62.dot(X) + self.C62
            self.CR = 62
        elif np.all(self.H63.dot(X) <= self.K63):
            U0 = self.B63.dot(X) + self.C63
            self.CR = 63
        elif np.all(self.H64.dot(X) <= self.K64):
            U0 = self.B64.dot(X) + self.C64
            self.CR = 64
        elif np.all(self.H65.dot(X) <= self.K65):
            U0 = self.B65.dot(X) + self.C65
            self.CR = 65
        elif np.all(self.H66.dot(X) <= self.K66):
            U0 = self.B66.dot(X) + self.C66
            self.CR = 66
        elif np.all(self.H67.dot(X) <= self.K67):
            U0 = self.B67.dot(X) + self.C67
            self.CR = 67
        elif np.all(self.H68.dot(X) <= self.K68):
            U0 = self.B68.dot(X) + self.C68
            self.CR = 68
        elif np.all(self.H69.dot(X) <= self.K69):
            U0 = self.B69.dot(X) + self.C69
            self.CR = 69
        elif np.all(self.H70.dot(X) <= self.K70):
            U0 = self.B70.dot(X) + self.C70
            self.CR = 70
        elif np.all(self.H71.dot(X) <= self.K71):
            U0 = self.B71.dot(X) + self.C71
            self.CR = 71
        elif np.all(self.H72.dot(X) <= self.K72):
            U0 = self.B72.dot(X) + self.C72
            self.CR = 72
        elif np.all(self.H73.dot(X) <= self.K73):
            U0 = self.B73.dot(X) + self.C73
            self.CR = 73
        elif np.all(self.H74.dot(X) <= self.K74):
            U0 = self.B74.dot(X) + self.C74
            self.CR = 74
        elif np.all(self.H75.dot(X) <= self.K75):
            U0 = self.B75.dot(X) + self.C75
            self.CR = 75
        elif np.all(self.H76.dot(X) <= self.K76):
            U0 = self.B76.dot(X) + self.C76
            self.CR = 76
        elif np.all(self.H77.dot(X) <= self.K77):
            U0 = self.B77.dot(X) + self.C77
            self.CR = 77
        elif np.all(self.H78.dot(X) <= self.K78):
            U0 = self.B78.dot(X) + self.C78
            self.CR = 78
        elif np.all(self.H79.dot(X) <= self.K79):
            U0 = self.B79.dot(X) + self.C79
            self.CR = 79
        elif np.all(self.H80.dot(X) <= self.K80):
            U0 = self.B80.dot(X) + self.C80
            self.CR = 80
        elif np.all(self.H81.dot(X) <= self.K81):
            U0 = self.B81.dot(X) + self.C81
            self.CR = 81
        elif np.all(self.H82.dot(X) <= self.K82):
            U0 = self.B82.dot(X) + self.C82
            self.CR = 82
        elif np.all(self.H83.dot(X) <= self.K83):
            U0 = self.B83.dot(X) + self.C83
            self.CR = 83
        elif np.all(self.H84.dot(X) <= self.K84):
            U0 = self.B84.dot(X) + self.C84
            self.CR = 84
        elif np.all(self.H85.dot(X) <= self.K85):
            U0 = self.B85.dot(X) + self.C85
            self.CR = 85
        elif np.all(self.H86.dot(X) <= self.K86):
            U0 = self.B86.dot(X) + self.C86
            self.CR = 86
        elif np.all(self.H87.dot(X) <= self.K87):
            U0 = self.B87.dot(X) + self.C87
            self.CR = 87
        elif np.all(self.H88.dot(X) <= self.K88):
            U0 = self.B88.dot(X) + self.C88
            self.CR = 88
        elif np.all(self.H89.dot(X) <= self.K89):
            U0 = self.B89.dot(X) + self.C89
            self.CR = 89
        elif np.all(self.H90.dot(X) <= self.K90):
            U0 = self.B90.dot(X) + self.C90
            self.CR = 90
        elif np.all(self.H91.dot(X) <= self.K91):
            U0 = self.B91.dot(X) + self.C91
            self.CR = 91
        elif np.all(self.H92.dot(X) <= self.K92):
            U0 = self.B92.dot(X) + self.C92
            self.CR = 92
        elif np.all(self.H93.dot(X) <= self.K93):
            U0 = self.B93.dot(X) + self.C93
            self.CR = 93
        elif np.all(self.H94.dot(X) <= self.K94):
            U0 = self.B94.dot(X) + self.C94
            self.CR = 94
        elif np.all(self.H95.dot(X) <= self.K95):
            U0 = self.B95.dot(X) + self.C95
            self.CR = 95
        elif np.all(self.H96.dot(X) <= self.K96):
            U0 = self.B96.dot(X) + self.C96
            self.CR = 96
        elif np.all(self.H97.dot(X) <= self.K97):
            U0 = self.B97.dot(X) + self.C97
            self.CR = 97
        elif np.all(self.H98.dot(X) <= self.K98):
            U0 = self.B98.dot(X) + self.C98
            self.CR = 98
        elif np.all(self.H99.dot(X) <= self.K99):
            U0 = self.B99.dot(X) + self.C99
            self.CR = 99
        elif np.all(self.H100.dot(X) <= self.K100):
            U0 = self.B100.dot(X) + self.C100
            self.CR = 100
        elif np.all(self.H101.dot(X) <= self.K101):
            U0 = self.B101.dot(X) + self.C101
            self.CR = 101
        elif np.all(self.H102.dot(X) <= self.K102):
            U0 = self.B102.dot(X) + self.C102
            self.CR = 102
        elif np.all(self.H103.dot(X) <= self.K103):
            U0 = self.B103.dot(X) + self.C103
            self.CR = 103
        elif np.all(self.H104.dot(X) <= self.K104):
            U0 = self.B104.dot(X) + self.C104
            self.CR = 104
        elif np.all(self.H105.dot(X) <= self.K105):
            U0 = self.B105.dot(X) + self.C105
            self.CR = 105
        elif np.all(self.H106.dot(X) <= self.K106):
            U0 = self.B106.dot(X) + self.C106
            self.CR = 106
        elif np.all(self.H107.dot(X) <= self.K107):
            U0 = self.B107.dot(X) + self.C107
            self.CR = 107
        elif np.all(self.H108.dot(X) <= self.K108):
            U0 = self.B108.dot(X) + self.C108
            self.CR = 108
        elif np.all(self.H109.dot(X) <= self.K109):
            U0 = self.B109.dot(X) + self.C109
            self.CR = 109
        elif np.all(self.H110.dot(X) <= self.K110):
            U0 = self.B110.dot(X) + self.C110
            self.CR = 110
        elif np.all(self.H111.dot(X) <= self.K111):
            U0 = self.B111.dot(X) + self.C111
            self.CR = 111
        elif np.all(self.H112.dot(X) <= self.K112):
            U0 = self.B112.dot(X) + self.C112
            self.CR = 112
        elif np.all(self.H113.dot(X) <= self.K113):
            U0 = self.B113.dot(X) + self.C113
            self.CR = 113
        elif np.all(self.H114.dot(X) <= self.K114):
            U0 = self.B114.dot(X) + self.C114
            self.CR = 114
        elif np.all(self.H115.dot(X) <= self.K115):
            U0 = self.B115.dot(X) + self.C115
            self.CR = 115
        elif np.all(self.H116.dot(X) <= self.K116):
            U0 = self.B116.dot(X) + self.C116
            self.CR = 116
        elif np.all(self.H117.dot(X) <= self.K117):
            U0 = self.B117.dot(X) + self.C117
            self.CR = 117
        elif np.all(self.H118.dot(X) <= self.K118):
            U0 = self.B118.dot(X) + self.C118
            self.CR = 118
        elif np.all(self.H119.dot(X) <= self.K119):
            U0 = self.B119.dot(X) + self.C119
            self.CR = 119
        elif np.all(self.H120.dot(X) <= self.K120):
            U0 = self.B120.dot(X) + self.C120
            self.CR = 120
        elif np.all(self.H121.dot(X) <= self.K121):
            U0 = self.B121.dot(X) + self.C121
            self.CR = 121
        elif np.all(self.H122.dot(X) <= self.K122):
            U0 = self.B122.dot(X) + self.C122
            self.CR = 122
        elif np.all(self.H123.dot(X) <= self.K123):
            U0 = self.B123.dot(X) + self.C123
            self.CR = 123
        elif np.all(self.H124.dot(X) <= self.K124):
            U0 = self.B124.dot(X) + self.C124
            self.CR = 124
        elif np.all(self.H125.dot(X) <= self.K125):
            U0 = self.B125.dot(X) + self.C125
            self.CR = 125
        elif np.all(self.H126.dot(X) <= self.K126):
            U0 = self.B126.dot(X) + self.C126
            self.CR = 126
        elif np.all(self.H127.dot(X) <= self.K127):
            U0 = self.B127.dot(X) + self.C127
            self.CR = 127
        elif np.all(self.H128.dot(X) <= self.K128):
            U0 = self.B128.dot(X) + self.C128
            self.CR = 128
        elif np.all(self.H129.dot(X) <= self.K129):
            U0 = self.B129.dot(X) + self.C129
            self.CR = 129
        elif np.all(self.H130.dot(X) <= self.K130):
            U0 = self.B130.dot(X) + self.C130
            self.CR = 130
        elif np.all(self.H131.dot(X) <= self.K131):
            U0 = self.B131.dot(X) + self.C131
            self.CR = 131
        elif np.all(self.H132.dot(X) <= self.K132):
            U0 = self.B132.dot(X) + self.C132
            self.CR = 132
        elif np.all(self.H133.dot(X) <= self.K133):
            U0 = self.B133.dot(X) + self.C133
            self.CR = 133
        elif np.all(self.H134.dot(X) <= self.K134):
            U0 = self.B134.dot(X) + self.C134
            self.CR = 134
        elif np.all(self.H135.dot(X) <= self.K135):
            U0 = self.B135.dot(X) + self.C135
            self.CR = 135
        elif np.all(self.H136.dot(X) <= self.K136):
            U0 = self.B136.dot(X) + self.C136
            self.CR = 136
        elif np.all(self.H137.dot(X) <= self.K137):
            U0 = self.B137.dot(X) + self.C137
            self.CR = 137
        elif np.all(self.H138.dot(X) <= self.K138):
            U0 = self.B138.dot(X) + self.C138
            self.CR = 138
        elif np.all(self.H139.dot(X) <= self.K139):
            U0 = self.B139.dot(X) + self.C139
            self.CR = 139
        elif np.all(self.H140.dot(X) <= self.K140):
            U0 = self.B140.dot(X) + self.C140
            self.CR = 140
        elif np.all(self.H141.dot(X) <= self.K141):
            U0 = self.B141.dot(X) + self.C141
            self.CR = 141
        elif np.all(self.H142.dot(X) <= self.K142):
            U0 = self.B142.dot(X) + self.C142
            self.CR = 142
        elif np.all(self.H143.dot(X) <= self.K143):
            U0 = self.B143.dot(X) + self.C143
            self.CR = 143
        elif np.all(self.H144.dot(X) <= self.K144):
            U0 = self.B144.dot(X) + self.C144
            self.CR = 144
        elif np.all(self.H145.dot(X) <= self.K145):
            U0 = self.B145.dot(X) + self.C145
            self.CR = 145
        elif np.all(self.H146.dot(X) <= self.K146):
            U0 = self.B146.dot(X) + self.C146
            self.CR = 146
        elif np.all(self.H147.dot(X) <= self.K147):
            U0 = self.B147.dot(X) + self.C147
            self.CR = 147
        elif np.all(self.H148.dot(X) <= self.K148):
            U0 = self.B148.dot(X) + self.C148
            self.CR = 148
        elif np.all(self.H149.dot(X) <= self.K149):
            U0 = self.B149.dot(X) + self.C149
            self.CR = 149
        elif np.all(self.H150.dot(X) <= self.K150):
            U0 = self.B150.dot(X) + self.C150
            self.CR = 150
        elif np.all(self.H151.dot(X) <= self.K151):
            U0 = self.B151.dot(X) + self.C151
            self.CR = 151
        elif np.all(self.H152.dot(X) <= self.K152):
            U0 = self.B152.dot(X) + self.C152
            self.CR = 152
        elif np.all(self.H153.dot(X) <= self.K153):
            U0 = self.B153.dot(X) + self.C153
            self.CR = 153
        elif np.all(self.H154.dot(X) <= self.K154):
            U0 = self.B154.dot(X) + self.C154
            self.CR = 154
        elif np.all(self.H155.dot(X) <= self.K155):
            U0 = self.B155.dot(X) + self.C155
            self.CR = 155
        elif np.all(self.H156.dot(X) <= self.K156):
            U0 = self.B156.dot(X) + self.C156
            self.CR = 156
        elif np.all(self.H157.dot(X) <= self.K157):
            U0 = self.B157.dot(X) + self.C157
            self.CR = 157
        elif np.all(self.H158.dot(X) <= self.K158):
            U0 = self.B158.dot(X) + self.C158
            self.CR = 158
        elif np.all(self.H159.dot(X) <= self.K159):
            U0 = self.B159.dot(X) + self.C159
            self.CR = 159
        elif np.all(self.H160.dot(X) <= self.K160):
            U0 = self.B160.dot(X) + self.C160
            self.CR = 160
        elif np.all(self.H161.dot(X) <= self.K161):
            U0 = self.B161.dot(X) + self.C161
            self.CR = 161
        elif np.all(self.H162.dot(X) <= self.K162):
            U0 = self.B162.dot(X) + self.C162
            self.CR = 162
        elif np.all(self.H163.dot(X) <= self.K163):
            U0 = self.B163.dot(X) + self.C163
            self.CR = 163
        elif np.all(self.H164.dot(X) <= self.K164):
            U0 = self.B164.dot(X) + self.C164
            self.CR = 164
        elif np.all(self.H165.dot(X) <= self.K165):
            U0 = self.B165.dot(X) + self.C165
            self.CR = 165
        elif np.all(self.H166.dot(X) <= self.K166):
            U0 = self.B166.dot(X) + self.C166
            self.CR = 166
        elif np.all(self.H167.dot(X) <= self.K167):
            U0 = self.B167.dot(X) + self.C167
            self.CR = 167
        elif np.all(self.H168.dot(X) <= self.K168):
            U0 = self.B168.dot(X) + self.C168
            self.CR = 168
        elif np.all(self.H169.dot(X) <= self.K169):
            U0 = self.B169.dot(X) + self.C169
            self.CR = 169
        elif np.all(self.H170.dot(X) <= self.K170):
            U0 = self.B170.dot(X) + self.C170
            self.CR = 170
        elif np.all(self.H171.dot(X) <= self.K171):
            U0 = self.B171.dot(X) + self.C171
            self.CR = 171
        elif np.all(self.H172.dot(X) <= self.K172):
            U0 = self.B172.dot(X) + self.C172
            self.CR = 172
        elif np.all(self.H173.dot(X) <= self.K173):
            U0 = self.B173.dot(X) + self.C173
            self.CR = 173
        elif np.all(self.H174.dot(X) <= self.K174):
            U0 = self.B174.dot(X) + self.C174
            self.CR = 174
        elif np.all(self.H175.dot(X) <= self.K175):
            U0 = self.B175.dot(X) + self.C175
            self.CR = 175
        elif np.all(self.H176.dot(X) <= self.K176):
            U0 = self.B176.dot(X) + self.C176
            self.CR = 176
        elif np.all(self.H177.dot(X) <= self.K177):
            U0 = self.B177.dot(X) + self.C177
            self.CR = 177
        elif np.all(self.H178.dot(X) <= self.K178):
            U0 = self.B178.dot(X) + self.C178
            self.CR = 178
        elif np.all(self.H179.dot(X) <= self.K179):
            U0 = self.B179.dot(X) + self.C179
            self.CR = 179
        elif np.all(self.H180.dot(X) <= self.K180):
            U0 = self.B180.dot(X) + self.C180
            self.CR = 180
        elif np.all(self.H181.dot(X) <= self.K181):
            U0 = self.B181.dot(X) + self.C181
            self.CR = 181
        elif np.all(self.H182.dot(X) <= self.K182):
            U0 = self.B182.dot(X) + self.C182
            self.CR = 182
        elif np.all(self.H183.dot(X) <= self.K183):
            U0 = self.B183.dot(X) + self.C183
            self.CR = 183
        elif np.all(self.H184.dot(X) <= self.K184):
            U0 = self.B184.dot(X) + self.C184
            self.CR = 184
        elif np.all(self.H185.dot(X) <= self.K185):
            U0 = self.B185.dot(X) + self.C185
            self.CR = 185
        elif np.all(self.H186.dot(X) <= self.K186):
            U0 = self.B186.dot(X) + self.C186
            self.CR = 186
        elif np.all(self.H187.dot(X) <= self.K187):
            U0 = self.B187.dot(X) + self.C187
            self.CR = 187
        elif np.all(self.H188.dot(X) <= self.K188):
            U0 = self.B188.dot(X) + self.C188
            self.CR = 188
        elif np.all(self.H189.dot(X) <= self.K189):
            U0 = self.B189.dot(X) + self.C189
            self.CR = 189
        elif np.all(self.H190.dot(X) <= self.K190):
            U0 = self.B190.dot(X) + self.C190
            self.CR = 190
        elif np.all(self.H191.dot(X) <= self.K191):
            U0 = self.B191.dot(X) + self.C191
            self.CR = 191
        elif np.all(self.H192.dot(X) <= self.K192):
            U0 = self.B192.dot(X) + self.C192
            self.CR = 192
        elif np.all(self.H193.dot(X) <= self.K193):
            U0 = self.B193.dot(X) + self.C193
            self.CR = 193
        elif np.all(self.H194.dot(X) <= self.K194):
            U0 = self.B194.dot(X) + self.C194
            self.CR = 194
        elif np.all(self.H195.dot(X) <= self.K195):
            U0 = self.B195.dot(X) + self.C195
            self.CR = 195
        elif np.all(self.H196.dot(X) <= self.K196):
            U0 = self.B196.dot(X) + self.C196
            self.CR = 196
        elif np.all(self.H197.dot(X) <= self.K197):
            U0 = self.B197.dot(X) + self.C197
            self.CR = 197
        elif np.all(self.H198.dot(X) <= self.K198):
            U0 = self.B198.dot(X) + self.C198
            self.CR = 198
        elif np.all(self.H199.dot(X) <= self.K199):
            U0 = self.B199.dot(X) + self.C199
            self.CR = 199
        elif np.all(self.H200.dot(X) <= self.K200):
            U0 = self.B200.dot(X) + self.C200
            self.CR = 200
        elif np.all(self.H201.dot(X) <= self.K201):
            U0 = self.B201.dot(X) + self.C201
            self.CR = 201
        elif np.all(self.H202.dot(X) <= self.K202):
            U0 = self.B202.dot(X) + self.C202
            self.CR = 202
        elif np.all(self.H203.dot(X) <= self.K203):
            U0 = self.B203.dot(X) + self.C203
            self.CR = 203
        elif np.all(self.H204.dot(X) <= self.K204):
            U0 = self.B204.dot(X) + self.C204
            self.CR = 204
        elif np.all(self.H205.dot(X) <= self.K205):
            U0 = self.B205.dot(X) + self.C205
            self.CR = 205
        elif np.all(self.H206.dot(X) <= self.K206):
            U0 = self.B206.dot(X) + self.C206
            self.CR = 206
        elif np.all(self.H207.dot(X) <= self.K207):
            U0 = self.B207.dot(X) + self.C207
            self.CR = 207
        elif np.all(self.H208.dot(X) <= self.K208):
            U0 = self.B208.dot(X) + self.C208
            self.CR = 208
        elif np.all(self.H209.dot(X) <= self.K209):
            U0 = self.B209.dot(X) + self.C209
            self.CR = 209
        elif np.all(self.H210.dot(X) <= self.K210):
            U0 = self.B210.dot(X) + self.C210
            self.CR = 210
        elif np.all(self.H211.dot(X) <= self.K211):
            U0 = self.B211.dot(X) + self.C211
            self.CR = 211
        elif np.all(self.H212.dot(X) <= self.K212):
            U0 = self.B212.dot(X) + self.C212
            self.CR = 212
        elif np.all(self.H213.dot(X) <= self.K213):
            U0 = self.B213.dot(X) + self.C213
            self.CR = 213
        elif np.all(self.H214.dot(X) <= self.K214):
            U0 = self.B214.dot(X) + self.C214
            self.CR = 214
        elif np.all(self.H215.dot(X) <= self.K215):
            U0 = self.B215.dot(X) + self.C215
            self.CR = 215
        elif np.all(self.H216.dot(X) <= self.K216):
            U0 = self.B216.dot(X) + self.C216
            self.CR = 216
        elif np.all(self.H217.dot(X) <= self.K217):
            U0 = self.B217.dot(X) + self.C217
            self.CR = 217
        elif np.all(self.H218.dot(X) <= self.K218):
            U0 = self.B218.dot(X) + self.C218
            self.CR = 218
        elif np.all(self.H219.dot(X) <= self.K219):
            U0 = self.B219.dot(X) + self.C219
            self.CR = 219
        elif np.all(self.H220.dot(X) <= self.K220):
            U0 = self.B220.dot(X) + self.C220
            self.CR = 220
        elif np.all(self.H221.dot(X) <= self.K221):
            U0 = self.B221.dot(X) + self.C221
            self.CR = 221
        elif np.all(self.H222.dot(X) <= self.K222):
            U0 = self.B222.dot(X) + self.C222
            self.CR = 222
        elif np.all(self.H223.dot(X) <= self.K223):
            U0 = self.B223.dot(X) + self.C223
            self.CR = 223
        elif np.all(self.H224.dot(X) <= self.K224):
            U0 = self.B224.dot(X) + self.C224
            self.CR = 224
        else:
            print('Error: cannot determine critical region!')
            return None

        self.desired_power = U0
        return U0

    # X - in KJ, the state vector [Ec, ~Es(t), ~Es(t+L),...]', returns the power of selected mode in Watt
    # U0 - the desired power at current time, in W
    def GetSelection(self,X):
        if self.naive == 0:
            return self.GetSelection_RH(X)
        else:
            return self.GetSelection_naive(X)

    def GetSelection_RH(self,X):
        U0 = self.GetDesiredPower(X)

        for i,cand in enumerate(self.candidates):
            power_diff = abs(cand[5]*self.fps/1000 + self.other_power - U0)
            if i == 0:
                min_power_diff = power_diff
                self.SelectionIndex = i
            elif power_diff < min_power_diff:
                min_power_diff = power_diff
                self.SelectionIndex = i

        self.PrevMicroArchIndex = self.MicroArchIndex
        self.MicroArchIndex = self.candidates[self.SelectionIndex][0]
        self.reconfig = (self.PrevMicroArchIndex != self.MicroArchIndex)
        self.ss = self.candidates[self.SelectionIndex][2]
        self.sf = self.candidates[self.SelectionIndex][3]
        self.latency = self.candidates[self.SelectionIndex][4]
        self.energy = self.candidates[self.SelectionIndex][5] / 1000 # in J
        self.accuracy = self.candidates[self.SelectionIndex][6]
        if len(self.candidates[self.SelectionIndex]) >= 8:
            self.target_clock_cycle = self.candidates[self.SelectionIndex][7]

        self.desired_power = U0 # in W
        self.power = (self.energy * self.fps) #in W

        return self.power 

    def GetSelection_naive(self,X):
        mode_num = len(self.candidates)
        step = ECMAX / mode_num
        candidates = sorted(self.candidates,key=lambda p:p[5]) #sort by energy, low to high

        for i in range(mode_num):
            if X[0][0] >= i*step and X[0][0] <= (i+1)*step:
                SelectionIndex = i
                break
        
        self.PrevMicroArchIndex = self.MicroArchIndex
        self.MicroArchIndex = candidates[SelectionIndex][0]
        self.reconfig = (self.PrevMicroArchIndex != self.MicroArchIndex)
        self.ss = candidates[SelectionIndex][2]
        self.sf = candidates[SelectionIndex][3]
        self.latency = candidates[SelectionIndex][4]
        self.energy = candidates[SelectionIndex][5] / 1000 # in J
        self.accuracy = candidates[SelectionIndex][6]
        if len(candidates[SelectionIndex]) >= 8:
            self.target_clock_cycle = candidates[SelectionIndex][7]

        self.desired_power = (self.energy * self.fps) # in W
        self.power = (self.energy * self.fps) #in W

        return self.power

    # clock_list is a list of clock cycle periods that are avalible for DFS, in ns
    def SetOpFreq(self,clock_list):
        # if the operating frequency in clock_list is same with the target frequency of any design in the candidates
        # then there is no need for other high frequency designs to scale down to that clock frequency
        # e.g. we have clock_list = [10,20,50], and cadidates' target clock cycle A = 10, B = 20,
        # then A would never scale down to 20ns or 50ns, while B can operate at either 20ns or 50ns.
        target_clk = list( map(lambda p: p[7], self.candidates) )
        alt_clk = []
        for cycle in clock_list:
            if not cycle in target_clk:
                target_clk_diff = list(map(lambda p: cycle - p, target_clk))
                min_diff = 99999
                for i,diff in enumerate(target_clk_diff):
                    if diff > 0 and diff < min_diff:
                        tar_cycle = target_clk[i]
                        min_diff = diff

                alt_clk.append([cycle,tar_cycle])

        # candidates: 0 - micro architecture index, 2 - shift step, 3 - scale factor, 4 - latency (ms), 5 - energy (mJ), 6 - accuracy, 7 - target clock cycle(ns), 8 -FPS, 9 - power(W)
        new_candidates = []
        for cand in self.candidates:
            cur_FPS = 1000/cand[4]
            cur_power = cand[5] * cur_FPS / 1000 #in W
            new_cand = [cand[0],cand[1],cand[2],cand[3],cand[4],cand[5],cand[6],cand[7],cur_FPS,cur_power]
            new_candidates.append(new_cand)

            for cycle_pair in alt_clk:
                if cand[7] == cycle_pair[1]:
                    cur_latency = cand[4]*cycle_pair[0]/cand[7]
                    cur_FPS = 1000/cur_latency
                    cur_power = cand[5] * cur_FPS / 1000 #in W
                    new_cand = [cand[0],cand[1],cand[2],cand[3],cur_latency,cand[5],cand[6],cycle_pair[0],cur_FPS,cur_power]
                    new_candidates.append(new_cand)

        self.candidates = new_candidates
        WriteNewCand(self.candidates,'new_candidates.csv')
        self.f_flg = 1
    
    def GetSelectionDFS(self,X):
        if self.f_flg == 0:
            print('To enable DFS, needs to SetOpFreq(clock_list) first')
            return None

        if self.naive == 0:
            return self.GetSelectionDFS_RH(X)
        else:
            return self.GetSelectionDFS_naive(X)

    def GetSelectionDFS_RH(self,X):
        U0 = self.GetDesiredPower(X)

        for i,cand in enumerate(self.candidates):
            power_diff = abs(cand[9] + self.other_power - U0)
            if i == 0:
                min_power_diff = power_diff
                self.SelectionIndex = i
            elif power_diff < min_power_diff:
                min_power_diff = power_diff
                self.SelectionIndex = i

        self.PrevMicroArchIndex = self.MicroArchIndex
        self.MicroArchIndex = self.candidates[self.SelectionIndex][0]
        self.reconfig = (self.PrevMicroArchIndex != self.MicroArchIndex)
        self.ss = self.candidates[self.SelectionIndex][2]
        self.sf = self.candidates[self.SelectionIndex][3]
        self.latency = self.candidates[self.SelectionIndex][4]
        self.energy = self.candidates[self.SelectionIndex][5] / 1000 # in J
        self.accuracy = self.candidates[self.SelectionIndex][6]
        self.target_clock_cycle = self.candidates[self.SelectionIndex][7]
        self.fps = self.candidates[self.SelectionIndex][8]
        self.power = self.candidates[self.SelectionIndex][9] # in W

        self.desired_power = U0 # in W

        return self.power #in W

    def GetSelectionDFS_naive(self,X):
        mode_num = len(self.candidates)
        step = ECMAX / mode_num
        candidates = sorted(self.candidates,key=lambda p:p[9]) #sort by power, low to high

        for i in range(mode_num):
            if X[0][0] >= i*step and X[0][0] <= (i+1)*step:
                SelectionIndex = i
                break
        
        self.PrevMicroArchIndex = self.MicroArchIndex
        self.MicroArchIndex = candidates[SelectionIndex][0]
        self.reconfig = (self.PrevMicroArchIndex != self.MicroArchIndex)
        self.ss = candidates[SelectionIndex][2]
        self.sf = candidates[SelectionIndex][3]
        self.latency = candidates[SelectionIndex][4]
        self.energy = candidates[SelectionIndex][5] / 1000 # in J
        self.accuracy = candidates[SelectionIndex][6]
        self.target_clock_cycle = candidates[SelectionIndex][7]
        self.fps = candidates[SelectionIndex][8]
        self.power = candidates[SelectionIndex][9] # in W

        self.desired_power = self.power # in W

        return self.power #in W

# read Pareto-optimal design files
def ReadCSV(csv_file_name):
    with open(csv_file_name,'r') as f:
        content = f.read().splitlines()[1:]

    # 0 - Microarchitecture number, 1 - index, 2 - shift step, 3 - scale factor, 4 - latency, 5 - energy(mJ), 6 - accuracy, 7 - target clock cycle(ns) (optional)
    content_split = map(lambda p: p.split(','), content)

    ret_list = []
    for design in content_split:
        design_f = list(map(float, design))
        design_f[0] = int(design_f[0])
        design_f[1] = int(design_f[1])
        design_f[2] = int(design_f[2])
        ret_list.append(design_f)

    return ret_list

def WriteNewCand(candidates,file_name):
    with open(file_name,'w') as f:
        f.write('micro architecture #, index, scale factor, latency (ms), energy (mJ), accuracy, operating clock cycle(ns), FPS, power(W)\n')
        for cand  in candidates:
            for item in cand:
                f.write(str(item))
                if item != cand[-1]:
                    f.write(',')
                else:
                    f.write('\n')

# read solar radiation file (national solar radiation data base)
# read from the offset th hour, return two lists: estimated energy and real energy
def ReadSolarRadiation(est_file_name, real_file_name, offset=1):
    # every line in the file is one hour
    num_hour = int( (sim_len+1) * preh / 60 ) #number of lines need to be read
    nts_hour = int( 60/Ts ) #number of time step(Ts) per hour

    # reads real havested energy
    with open(real_file_name,'r') as f:
        content = f.read().splitlines()[offset:(num_hour+offset)]
 
    real_energy = map(lambda p: [ he_factor * int(p.split(',')[15]) ]*nts_hour, content)
    real = sum(real_energy,[])

    # reads estimated havested energy
    with open(est_file_name,'r') as f:
        content = f.read().splitlines()[1:]

    content_rebuild = []
    for i in range(num_hour):
        content_rebuild.append( content[(offset-1+i)%24] )

    est_energy = map(lambda p: [ he_factor * int(p.split(',')[1]) ]*nts_hour, content_rebuild)
    est = sum(est_energy,[])
    
    return (est, real)

def RunSimulationFixedFPS():
    # read data of havested energy over time
    est_energy, real_energy = ReadSolarRadiation('solar_data_statics.csv','solar_data.csv',241)

    # Initialization
    RHCtrl_ad = RHController('DSEresults/pareto_optimal.csv',naive_v=1)
    RHCtrl_ad.SetOtherPower(other_pow)
    X0 = 15*3600/1000 # initial_battery_level in KJoules
    battery_level_t = []
    accuracy_t = []
    sim_length = sim_len*Nts # simulation time length in time step Ts

    # start simulation, t is time in time step Ts
    for t in range(0,sim_length):

        est_energy_L = [] # list of estimated havested energy in every perdiction interval L
        for i in range(Npi):
            cur_est_energy = 0
            for j in range(Lpi):
                cur_est_energy += est_energy[t+i*Lpi+j]

            est_energy_L.append(cur_est_energy)

        # state vector X
        Xsv = [ [X0], [est_energy_L[0]], [est_energy_L[1]], [est_energy_L[2]], [est_energy_L[3]], [est_energy_L[4]], [est_energy_L[5]] ]

        power_real = RHCtrl_ad.GetSelection(Xsv) # controller make decision, power in W
        if power_real == None:
            accuracy_t.append(-1)
            return #debug
        battery_level_t.append(X0)
        X0 = X0 - (power_real + other_pow)*Ts*60/1000 + real_energy[t] #update battery level, in KJ
        if X0 > ECMAX:
            X0 = ECMAX
        if X0 < 0:
            X0 = X0 + (power_real + other_pow)*Ts*60/1000 # not using energy, add the energy comsumption back
            accuracy_t.append(0)
        else:
            accuracy_t.append(RHCtrl_ad.accuracy)

    # Plot battery level, accuracy over time
    x_time = range(0,sim_length*Ts,Ts) #in minites
    x_time_h = list( map(lambda p: p/60, x_time) )
    y_est_hav_power = list( map(lambda p: 1000*p/Ts/60, est_energy[0:sim_length]) ) #estimated havest power
    y_real_hav_power = list( map(lambda p: 1000*p/Ts/60, real_energy[0:sim_length]) )

    plt.subplot(3,1,1)
    plt.plot(x_time_h, accuracy_t,'r-')
    plt.ylim(-0.05,1.05)
    plt.ylabel('Accuracy')

    plt.subplot(3,1,2)
    plt.plot(x_time_h, battery_level_t, 'b-')
    plt.ylabel('Battery level (KJ)')

    plt.subplot(3,1,3)
    plt.plot(x_time_h, y_est_hav_power, '--')
    plt.plot(x_time_h, y_real_hav_power, '-')
    plt.legend(['estimated','real'])
    plt.ylabel('Havesting power (W)')
    plt.xlabel('Time(hour)')

    plt.show()

# This is a universal function to run simulation in time domian.
# Arguments -- type: 'DFS', 'FIXFPS'; candidate_file: name of the candidate design csv file; 
# Arguments(optional) -- sim_length: simulation period in Ts; naive: 1 means using naive control, otherwise reverse horizon controller; clock_list: required for 'DFS' sim type, list of operation clock cycle in ns;
# Arguments(optional) -- o_power: constant power other than face detector in W; solar_offset: offset of solar radiation data in hour, >=1, 1 means start from the 1st hour of 01/01/2010; init_bat: initial battery level in Wh; fixfps: the fixed fps in 'FIXFPS' mode
# return value: [time_list, accuracy_list, fps_list, cons_power_list, est_hav_power_list, real_hav_power_list, bat_lev_list]
# return value -- time_list: list of time points in hour; accuracy_list: accuracy(precision) over time; fps_list: frame rate(in fps) over time; cons_power_list: consumed power by face detector over time;
# return value -- est_hav_power_list: estimated havesting power over time; real_hav_power_list: real havesting power over time; bat_lev_list: battery level over time, in Wh 
def RunSimulation(sim_type, candidate_file, sim_length=sim_len*Nts, naive=0, clock_list=None, o_power=other_pow, solar_offset=265, init_bat=ECMAX/2, fixfps=10 ):
    # read data of havested energy over time
    est_energy, real_energy = ReadSolarRadiation('solar_data_statics.csv','solar_data.csv',solar_offset)

    # Initialization
    if sim_type=='DFS':
        if clock_list==None:
            print('Need to specify clock_list for "DFS" simulation.\n')
            return None
        RHCtrl_ad = RHController(candidate_file,naive_v=naive)
        RHCtrl_ad.SetOpFreq(clock_list)
    elif sim_type=='FIXFPS':
        RHCtrl_ad = RHController(candidate_file,naive_v=naive)
        RHCtrl_ad.SetFPS(fixfps)
    else:
        print('Error: invalid sim_type.\n')

    RHCtrl_ad.SetOtherPower(o_power)
    X0 = init_bat # initial_battery_level in KJoules
    battery_level_t = []
    accuracy_t = []
    fps_t = []
    cons_power_list = []

    # start simulation, t is time in time step Ts
    for t in range(0,sim_length):

        est_energy_L = [] # list of estimated havested energy in every perdiction interval L
        for i in range(Npi):
            cur_est_energy = 0
            for j in range(Lpi):
                cur_est_energy += est_energy[t+i*Lpi+j]

            est_energy_L.append(cur_est_energy)

        # state vector X
        Xsv = [ [X0], [est_energy_L[0]], [est_energy_L[1]], [est_energy_L[2]], [est_energy_L[3]], [est_energy_L[4]], [est_energy_L[5]] ]

        if sim_type=='DFS':
            power_real = RHCtrl_ad.GetSelectionDFS(Xsv) # controller make decision, power in W
        elif sim_type=='FIXFPS':
            power_real = RHCtrl_ad.GetSelection(Xsv)

        if power_real == None:
            accuracy_t.append(-1)
            fps_t.append(-1)
            cons_power_list.append(-1)
            return #debug
        battery_level_t.append(X0)
        X0 = X0 - (power_real + other_pow)*Ts*60/1000 + real_energy[t] #update battery level, in KJ
        if X0 > ECMAX:
            X0 = ECMAX

        if X0 < 0:
            X0 = X0 + (power_real + other_pow)*Ts*60/1000 # not using energy, add the energy comsumption back
            accuracy_t.append(0)
            fps_t.append(0)
            cons_power_list.append(0)
        else:
            accuracy_t.append(RHCtrl_ad.accuracy)
            fps_t.append(RHCtrl_ad.fps)
            cons_power_list.append(RHCtrl_ad.power)

    # Plot battery level, accuracy over time
    x_time = range(0,sim_length*Ts,Ts) #in minites
    time_list = list( map(lambda p: p/60, x_time) )
    accuracy_list = accuracy_t
    fps_list = fps_t
    est_hav_power_list = list( map(lambda p: 1000*p/Ts/60, est_energy[0:sim_length]) ) #estimated havest power
    real_hav_power_list = list( map(lambda p: 1000*p/Ts/60, real_energy[0:sim_length]) )
    bat_lev_list = list( map(lambda p: p/3.6, battery_level_t) )

    return (time_list, accuracy_list, fps_list, cons_power_list, est_hav_power_list, real_hav_power_list, bat_lev_list)

def CaseStudy():
    # 1- adaptive three modes
    time_list, accuracy_list_1, fps_list_1, cons_power_list_1, est_hav_power_list, real_hav_power_list, bat_lev_list_1 = RunSimulation('DFS', 'candidates_ad.csv',naive=1, clock_list=[5,10,20] )
    # 2 - static three modes (same micro-architecture, three frequencies)
    time_list, accuracy_list_2, fps_list_2, cons_power_list_2, est_hav_power_list, real_hav_power_list, bat_lev_list_2 = RunSimulation('DFS', 'candidates_st.csv',naive=1, clock_list=[5,8,20] )
    # 3 - static one mode
    time_list, accuracy_list_3, fps_list_3, cons_power_list_3, est_hav_power_list, real_hav_power_list, bat_lev_list_3 = RunSimulation('DFS', 'candidates_st.csv',naive=1, clock_list=[5] )

    ## first type of graph
    plt.figure(1,figsize=(10,12))
    plt.rcParams.update({'font.size':14})

    plt.subplot(3,1,1)
    plt.plot(time_list, fps_list_1,'-')
    plt.plot(time_list, fps_list_2,'--')
    plt.plot(time_list, fps_list_3,':')
    plt.legend(['adaptive','static','no DFS'], framealpha=0.3)
    plt.ylim(-0.2,14)
    plt.ylabel('Frame rate (fps)')
    plt.xlim(min(time_list),max(time_list))

    plt.subplot(3,1,2)
    plt.plot(time_list, bat_lev_list_1, '-')
    plt.plot(time_list, bat_lev_list_2, '--')
    plt.plot(time_list, bat_lev_list_3, ':')
    plt.legend(['adaptive','static','no DFS'], framealpha=0.3)
    plt.ylabel('Battery level (Wh)')
    plt.xlim(min(time_list),max(time_list))

    plt.subplot(3,1,3)
    plt.plot(time_list, real_hav_power_list, '-')
#    plt.legend(['estimated','real'])
    plt.ylabel('Havested power (W)')
    plt.xlabel('Time(hour)')
    plt.xlim(min(time_list),max(time_list))

    plt.savefig('plot_try1.png',dpi=300)
    plt.show()

    ## second type of graph ( USED IN PAPER )
    fig = plt.figure(2,figsize=(10,17))
    plt.subplots_adjust(hspace=0.28)

    ax1_1 = fig.add_subplot(412)
    p1 = ax1_1.plot(time_list, fps_list_1,'-',label='frame',color='darkorange')
    ax1_1.set_ylim(-0.5,14)
    ax1_1.set_ylabel('Frame rate [fps]')
    ax1_2 = ax1_1.twinx()
    ax1_2.yaxis.set_label_position('right')
    p2 = ax1_2.plot(time_list, bat_lev_list_1, '--',label='battery')
    ax1_2.set_ylim(-0.5,12)
    ax1_2.set_ylabel('Battery level [Wh]')
    plt.xlim(min(time_list),max(time_list))
    plt.title('adaptive')
    plt.legend(p1+p2,['Frame rate','Battery level'],loc=3,framealpha=0.3,fontsize='small')

    ax2_1 = fig.add_subplot(413)
    p1 = ax2_1.plot(time_list, fps_list_2,'-',label='frame',color='darkorange')
    ax2_1.set_ylim(-0.5,14)
    ax2_1.set_ylabel('Frame rate [fps]')
    ax2_2 = ax2_1.twinx()
    p2 = ax2_2.plot(time_list, bat_lev_list_2, '--',label='battery')
    ax2_2.set_ylim(-0.5,12)
    ax2_2.set_ylabel('Battery level [Wh]')
    plt.xlim(min(time_list),max(time_list))
    plt.title('static')
    plt.legend(p1+p2,['Frame rate','Battery level'],loc=3,framealpha=0.3,fontsize='small')

    ax3_1 = fig.add_subplot(414)
    p1 = ax3_1.plot(time_list, fps_list_3,'-',label='frame',color='darkorange')
    ax3_1.set_ylim(-0.5,14)
    ax3_1.set_ylabel('Frame rate [fps]')
    ax3_2 = ax3_1.twinx()
    p2 = ax3_2.plot(time_list, bat_lev_list_3, '--',label='battery')
    ax3_2.set_ylim(-0.5,12)
    ax3_2.set_ylabel('Battery level [Wh]')
    plt.xlim(min(time_list),max(time_list))
    plt.title('no DFS')
    plt.legend(p1+p2,['Frame rate','Battery level'],loc=3,framealpha=0.3,fontsize='small')
    ax3_1.xaxis.set_label_coords(0.5,-0.2)
    ax3_1.set_xlabel('Time [hour]')


    plt.subplot(4,1,1)
    plt.xlim(min(time_list),max(time_list))
    plt.plot(time_list, real_hav_power_list, '-')
#    plt.legend(['estimated','real'])
    plt.ylabel('Havested power [W]')
    

    plt.savefig('plot_try2.png',dpi=300)
    plt.show()

    avg_fps_1 = sum(fps_list_1)/len(fps_list_1)
    avg_fps_2 = sum(fps_list_2)/len(fps_list_2)
    avg_fps_3 = sum(fps_list_3)/len(fps_list_3)
    downtime_1 = fps_list_1.count(0) * Ts / 60 # in hours
    downtime_2 = fps_list_2.count(0) * Ts / 60
    downtime_3 = fps_list_3.count(0) * Ts / 60

    print('Adaptive - 3 modes')
    print('average FPS:',avg_fps_1)
    print('downtime (hours):',downtime_1)
    print('Static - 3 modes')
    print('average FPS:',avg_fps_2)
    print('downtime (hours):',downtime_2)
    print('Static - no DFS')
    print('average FPS:',avg_fps_3)
    print('downtime (hours):',downtime_3)


if __name__ == "__main__":
    main(sys.argv[1:])