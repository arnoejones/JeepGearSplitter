# Purpose: Calculate RPM and MPH values
#
# Author:      Arno E Jones
#
# Created:     7/13/2018
# Copyright:   (c) jonesar 2018 - 2019
# Licence:     This code can be freely shared and modified as long as the author is credited with the original (this) version.
#-------------------------------------------------------------------------------

import math

class JeepGearSplitter():

    def __init__(self, jeep_model, differentialGearRatio, tireDiameter, gearSelected, transmissionType, rubicon, fourLowEngaged):
        self.jeep_model = jeep_model
        self.differentialGearRatio = differentialGearRatio
        self.tireDiameter = tireDiameter
        self.gearSelected = gearSelected
        self.transmissionType = transmissionType
        self.rubicon = rubicon
        self.fourLowEngaged = fourLowEngaged

    # arguments for calculating Speed from RPM
    def calculateSpeedFromRpm(differentialGearRatio, tireDiameter, transmissionGearRatio, transferCaseRatio):

        speedList = []
        rpmList = []

        for rpm in range(0, 7000, 100):
            rpmList.append(rpm)
            speedList.append(float("{0:.1f}".format(((rpm * tireDiameter * math.pi * 60) /
                                                     (transmissionGearRatio * transferCaseRatio * differentialGearRatio * 63360)))))
        rpm_mph_list = [rpmList, speedList]

        return rpm_mph_list


    # arguments for calculating RPM from Speed
    def calculateRpmFromSpeed(differentialGearRatio, tireDiameter, transmissionGearRatio, transferCaseRatio):

        mphList = []
        rpmList = []

        if transferCaseRatio > 1:
            maxSpeed = 50  # don't get stupid with speeds when in low-range
        else:
            maxSpeed = 130  # not likely you'll survive at greater speeds.

        for mph in range(0, maxSpeed, 5):
            mphList.append(mph)
            # don't display ridiculous RPM readings on the graph
            if (int((mph * transmissionGearRatio * transferCaseRatio * differentialGearRatio * 63360) / (tireDiameter * math.pi * 60))) < 7000:
                rpmList.append(int(
                     (mph * transmissionGearRatio * transferCaseRatio * differentialGearRatio * 63360) /
                                                      (tireDiameter * math.pi * 60)))
        mph_rpm_list = []
        mph_rpm_list.append(mphList)
        mph_rpm_list.append(rpmList)

        return mph_rpm_list

    def calculateTireDiameter(mph, tranny_gear, tcase, diff, rpm):
        tire = ((mph * tranny_gear * tcase * diff * 63360) / (rpm * 60 * math.pi))
        return tire
