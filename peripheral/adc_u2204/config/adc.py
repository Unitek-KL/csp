# coding: utf-8
"""*****************************************************************************
* Copyright (C) 2018 Microchip Technology Inc. and its subsidiaries.
*
* Subject to your compliance with these terms, you may use Microchip software
* and any derivatives exclusively with Microchip products. It is your
* responsibility to comply with third party license terms applicable to your
* use of third party software (including open source software) that may
* accompany Microchip software.
*
* THIS SOFTWARE IS SUPPLIED BY MICROCHIP "AS IS". NO WARRANTIES, WHETHER
* EXPRESS, IMPLIED OR STATUTORY, APPLY TO THIS SOFTWARE, INCLUDING ANY IMPLIED
* WARRANTIES OF NON-INFRINGEMENT, MERCHANTABILITY, AND FITNESS FOR A
* PARTICULAR PURPOSE.
*
* IN NO EVENT WILL MICROCHIP BE LIABLE FOR ANY INDIRECT, SPECIAL, PUNITIVE,
* INCIDENTAL OR CONSEQUENTIAL LOSS, DAMAGE, COST OR EXPENSE OF ANY KIND
* WHATSOEVER RELATED TO THE SOFTWARE, HOWEVER CAUSED, EVEN IF MICROCHIP HAS
* BEEN ADVISED OF THE POSSIBILITY OR THE DAMAGES ARE FORESEEABLE. TO THE
* FULLEST EXTENT ALLOWED BY LAW, MICROCHIP'S TOTAL LIABILITY ON ALL CLAIMS IN
* ANY WAY RELATED TO THIS SOFTWARE WILL NOT EXCEED THE AMOUNT OF FEES, IF ANY,
* THAT YOU HAVE PAID DIRECTLY TO MICROCHIP FOR THIS SOFTWARE.
*****************************************************************************"""
import math
global InterruptVector
global InterruptHandler
global InterruptHandlerLock
global adcInstanceName

###################################################################################################
########################################## Callbacks  #############################################
###################################################################################################

def updateADCInterruptStatus(symbol, event):

    Database.clearSymbolValue("core", InterruptVector)
    Database.setSymbolValue("core", InterruptVector, event["value"], 2)

    Database.clearSymbolValue("core", InterruptHandlerLock)
    Database.setSymbolValue("core", InterruptHandlerLock, event["value"], 2)

    Database.clearSymbolValue("core", InterruptHandler)

    if event["value"] == True:

        Database.setSymbolValue("core", InterruptHandler, adcInstanceName.getValue() + "_InterruptHandler", 2)
    else:
        Database.setSymbolValue("core", InterruptHandler, adcInstanceName.getValue() + "_Handler", 2)

def updateADCInterruptWarringStatus(symbol, event):

    if adcSym_INTENSET_RESRDY.getValue() == True:
        symbol.setVisible(event["value"])

def updateADCClockWarringStatus(symbol, event):

    if event["value"] == False:
        symbol.setVisible(True)
    else:
        symbol.setVisible(False)

def adcCalcSampleTime(symbol, event):
    clock_freq = Database.getSymbolValue("core", "CPU_CLOCK_FREQUENCY")
    component = int(adcInstanceName.getValue()[-1]) - 1
    prescaler = (Database.getSymbolValue("adc" + str(component), "ADC_CTRLB_PRESCALER"))
    prescaler = math.pow(2, prescaler+1)
    sample_cycles = adcSym_SAMPCTRL_SAMPLEN.getValue()
    data_width = adcSym_CTRLC_RESSEL.getSelectedKey()[:-3]
    conv_time = float((((int(sample_cycles) + int(data_width)) * int(prescaler) * 1000000) / clock_freq))
    symbol.setLabel("**** Conversion Time is " + str(conv_time) + " uS ****")

def adcEvesysConfigure(symbol, event):
    if(event["id"] == "ADC_EVCTRL_RESRDYEO"):
        Database.setSymbolValue("evsys", "GENERATOR_"+str(adcInstanceName.getValue())+"_RESRDY_ACTIVE", event["value"], 2)

    if(event["id"] == "ADC_WINDOW_OUTPUT_EVENT"):
        Database.setSymbolValue("evsys", "GENERATOR_"+str(adcInstanceName.getValue())+"_WINMON_ACTIVE", event["value"], 2)

    if (adcSym_CONV_TRIGGER.getValue() == "HW Event Trigger"):
        if (event["id"] == "ADC_EVCTRL_FLUSH"):
            if (event["value"] > 0):
                Database.setSymbolValue("evsys", "USER_"+str(adcInstanceName.getValue())+"_SYNC_READY", True, 2)
            else:
                Database.setSymbolValue("evsys", "USER_"+str(adcInstanceName.getValue())+"_SYNC_READY", False, 2)
        if (event["id"] == "ADC_EVCTRL_START"):
            if (event["value"] > 0):
                Database.setSymbolValue("evsys", "USER_"+str(adcInstanceName.getValue())+"_START_READY", True, 2)
            else:
                Database.setSymbolValue("evsys", "USER_"+str(adcInstanceName.getValue())+"_START_READY", False, 2)

def adcResultConfVisibility(symbol, event):
    symObj = event["symbol"]
    if (symObj.getSelectedKey() == "16BIT"):
        symbol.setVisible(True)
    else:
        symbol.setVisible(False)

def adcEventInputVisibility(symbol, event):
    if (adcSym_CONV_TRIGGER.getValue() != "HW Event Trigger"):
        symbol.setVisible(False)
    else:
        symbol.setVisible(True)

def adcOptionVisible(symbol, event):
    if(event["value"] != "Free Run"):
        symbol.setVisible(True)
    else:
        symbol.setVisible(False)

def adcWindowVisible(symbol, event):
    if (event["value"] > 0):
        symbol.setVisible(True)
    else:
        symbol.setVisible(False)

def adcSYSCTRLVisible(symbol, event):
    if (event["id"] == "ADC_INPUTCTRL_MUXPOS"):
        symObj = event["symbol"]
        if (symObj.getSelectedKey() == "BANDGAP"):
            symbol.setVisible(True)
        else:
            symbol.setVisible(False)

    if (event["id"] == "ADC_REFCTRL_REFSEL"):
        symObj = event["symbol"]
        if (symObj.getSelectedKey() == "INTREF"):
            symbol.setVisible(True)
        else:
            symbol.setVisible(False)

def adcOffsetVisible(symbol, event):
    if (event["value"] != 0):
        symbol.setVisible(True)
    else:
        symbol.setVisible(False)
###################################################################################################
########################################## Component  #############################################
###################################################################################################

def instantiateComponent(adcComponent):
    global InterruptVector
    global InterruptHandler
    global InterruptHandlerLock
    global adcInstanceName

    adcInstanceName = adcComponent.createStringSymbol("ADC_INSTANCE_NAME", None)
    adcInstanceName.setVisible(False)
    adcInstanceName.setDefaultValue(adcComponent.getID().upper())
    Log.writeInfoMessage("Running " + adcInstanceName.getValue())

    #clock enable
    Database.clearSymbolValue("core", adcInstanceName.getValue() + "_CLOCK_ENABLE")
    Database.setSymbolValue("core", adcInstanceName.getValue() + "_CLOCK_ENABLE", True, 2)

    #------------------------- ATDF Read -------------------------------------
    packageName = str(Database.getSymbolValue("core", "COMPONENT_PACKAGE"))
    #TODO
    packageName = "TQFP64"
    availablePins = []      # array to save available pins
    channel = []

    pinout = "SAMC21N"
    val = ATDF.getNode("/avr-tools-device-file/variants")
    children = val.getChildren()
    for index in range(0, len(children)):
        if packageName in children[index].getAttribute("package"):
            pinout = children[index].getAttribute("pinout")

    children = []
    val = ATDF.getNode("/avr-tools-device-file/pinouts/pinout@[name=\""+str(pinout)+"\"]")
    children = val.getChildren()
    for pad in range(0, len(children)):
        availablePins.append(children[pad].getAttribute("pad"))

    adc_signals = []
    adc = ATDF.getNode("/avr-tools-device-file/devices/device/peripherals/module@[name=\"ADC\"]/instance@[name=\""+adcInstanceName.getValue()+"\"]/signals")
    adc_signals = adc.getChildren()
    for pad in range(0, len(adc_signals)):
        group = adc_signals[pad].getAttribute("group")
        if (("AIN" in group) and ("index" in adc_signals[pad].getAttributeList())):
            padSignal = adc_signals[pad].getAttribute("pad")
            if padSignal in availablePins:
                channel.append(adc_signals[pad].getAttribute("group")+adc_signals[pad].getAttribute("index"))

    adcSym_MCU_FAMILY = adcComponent.createStringSymbol("ADC_MCU_FAMILY", None)
    adcSym_MCU_FAMILY.setVisible(False)
    node = ATDF.getNode("/avr-tools-device-file/devices")
    family = node.getChildren()[0].getAttribute("family")
    adcSym_MCU_FAMILY.setDefaultValue(node.getChildren()[0].getAttribute("family"))

    #prescaler configuration
    global adcSym_CTRLB_PRESCALER
    adcSym_CTRLB_PRESCALER = adcComponent.createKeyValueSetSymbol("ADC_CTRLB_PRESCALER", None)
    adcSym_CTRLB_PRESCALER.setLabel("Select Prescaler")
    adcSym_CTRLB_PRESCALER.setDefaultValue(1)
    adcSym_CTRLB_PRESCALER.setOutputMode("Key")
    adcSym_CTRLB_PRESCALER.setDisplayMode("Description")
    adcPrescalerNode = ATDF.getNode("/avr-tools-device-file/modules/module@[name=\"ADC\"]/value-group@[name=\"ADC_CTRLB__PRESCALER\"]")
    adcPrescalerValues = []
    adcPrescalerValues = adcPrescalerNode.getChildren()
    for index in range(0, len(adcPrescalerValues)):
        adcSym_CTRLB_PRESCALER.addKey(adcPrescalerValues[index].getAttribute("name"), adcPrescalerValues[index].getAttribute("value"), adcPrescalerValues[index].getAttribute("caption"))

    #sampling time
    global adcSym_SAMPCTRL_SAMPLEN
    adcSym_SAMPCTRL_SAMPLEN = adcComponent.createIntegerSymbol("ADC_SAMPCTRL_SAMPLEN", None)
    adcSym_SAMPCTRL_SAMPLEN.setLabel("Select Sample Length (cycles)")
    adcSym_SAMPCTRL_SAMPLEN.setMin(0)
    adcSym_SAMPCTRL_SAMPLEN.setMax(63)
    adcSym_SAMPCTRL_SAMPLEN.setDefaultValue(0)

    clock_freq = 48000000   #Database.getSymbolValue("core", "CPU_CLOCK_FREQUENCY")
    prescaler = adcSym_CTRLB_PRESCALER.getSelectedKey()[3:]
    sample_cycles = adcSym_SAMPCTRL_SAMPLEN.getValue()
    data_width = 12
    conv_time = float((((int(sample_cycles) + int(data_width)) * int(prescaler) * 1000000) / clock_freq))

    #Sampling time calculation
    adcSym_SAMPCTRL_SAMPLEN_TIME = adcComponent.createCommentSymbol("ADC_SAMPCTRL_SAMPLEN_TIME", None)
    adcSym_SAMPCTRL_SAMPLEN_TIME.setLabel("**** Conversion Time is " + str(conv_time) + " us ****")
    adcSym_SAMPCTRL_SAMPLEN_TIME.setDependencies(adcCalcSampleTime, ["core.CPU_CLOCK_FREQUENCY", \
        "ADC_SAMPCTRL_SAMPLEN", "ADC_CTRLB_PRESCALER", "ADC_CTRLC_RESSEL"])

    #reference selection
    adcSym_INPUTCTRL_GAIN = adcComponent.createKeyValueSetSymbol("ADC_INPUTCTRL_GAIN", None)
    adcSym_INPUTCTRL_GAIN.setLabel("Select Gain")
    default = 0
    adcSym_INPUTCTRL_GAIN.setOutputMode("Key")
    adcSym_INPUTCTRL_GAIN.setDisplayMode("Description")
    adcReferenceNode = ATDF.getNode("/avr-tools-device-file/modules/module@[name=\"ADC\"]/value-group@[name=\"ADC_INPUTCTRL__GAIN\"]")
    adcReferenceValues = []
    adcReferenceValues = adcReferenceNode.getChildren()
    for index in range(0, len(adcReferenceValues)):
        if adcReferenceValues[index].getAttribute("caption") == "1x":
            default = index
        adcSym_INPUTCTRL_GAIN.addKey(adcReferenceValues[index].getAttribute("name"), adcReferenceValues[index].getAttribute("value"),
        adcReferenceValues[index].getAttribute("caption"))
    adcSym_INPUTCTRL_GAIN.setDefaultValue(default)

    #reference selection
    adcSym_REFCTRL_REFSEL = adcComponent.createKeyValueSetSymbol("ADC_REFCTRL_REFSEL", None)
    adcSym_REFCTRL_REFSEL.setLabel("Select Reference")
    default = 0
    adcSym_REFCTRL_REFSEL.setOutputMode("Key")
    adcSym_REFCTRL_REFSEL.setDisplayMode("Description")
    adcReferenceNode = ATDF.getNode("/avr-tools-device-file/modules/module@[name=\"ADC\"]/value-group@[name=\"ADC_REFCTRL__REFSEL\"]")
    adcReferenceValues = []
    adcReferenceValues = adcReferenceNode.getChildren()
    for index in range(0, len(adcReferenceValues)):
        if adcReferenceValues[index].getAttribute("name") == "INTVCC1":
            default = index
        adcSym_REFCTRL_REFSEL.addKey(adcReferenceValues[index].getAttribute("name"), adcReferenceValues[index].getAttribute("value"),
        adcReferenceValues[index].getAttribute("caption"))
    adcSym_REFCTRL_REFSEL.setDefaultValue(default)

    #trigger
    global adcSym_CONV_TRIGGER
    adcSym_CONV_TRIGGER = adcComponent.createComboSymbol("ADC_CONV_TRIGGER", None, ["Free Run", "SW Trigger", "HW Event Trigger"])
    adcSym_CONV_TRIGGER.setDefaultValue("Free Run")
    adcSym_CONV_TRIGGER.setLabel("Select Conversion Trigger")

    adcSym_FLUSH_EVENT = adcComponent.createKeyValueSetSymbol("ADC_EVCTRL_FLUSH", adcSym_CONV_TRIGGER)
    adcSym_FLUSH_EVENT.setLabel("Flush Event Input")
    adcSym_FLUSH_EVENT.setVisible(False)
    adcSym_FLUSH_EVENT.setOutputMode("Value")
    adcSym_FLUSH_EVENT.setDisplayMode("Description")
    adcSym_FLUSH_EVENT.addKey("DISABLED", "0", "Disabled")
    adcSym_FLUSH_EVENT.addKey("ENABLED_RISING_EDGE", "1", "Enabled on Rising Edge")
    adcSym_FLUSH_EVENT.addKey("ENABLED_FALLING_EDGE", "2", "Enabled on Falling Edge")
    adcSym_FLUSH_EVENT.setDependencies(adcEventInputVisibility, ["ADC_CONV_TRIGGER"])

    adcSym_START_EVENT = adcComponent.createKeyValueSetSymbol("ADC_EVCTRL_START", adcSym_CONV_TRIGGER)
    adcSym_START_EVENT.setLabel("Start Event Input")
    adcSym_START_EVENT.setVisible(False)
    adcSym_START_EVENT.setOutputMode("Value")
    adcSym_START_EVENT.setDisplayMode("Description")
    adcSym_START_EVENT.addKey("DISABLED", "0", "Disabled")
    adcSym_START_EVENT.addKey("ENABLED_RISING_EDGE", "1", "Enabled on Rising Edge")
    adcSym_START_EVENT.addKey("ENABLED_FALLING_EDGE", "2", "Enabled on Falling Edge")
    adcSym_START_EVENT.setDependencies(adcEventInputVisibility, ["ADC_CONV_TRIGGER"])

    adcPositiveInputNode = ATDF.getNode("/avr-tools-device-file/modules/module@[name=\"ADC\"]/value-group@[name=\"ADC_INPUTCTRL__MUXPOS\"]")
    adcPositiveInputValues = []
    adcPositiveInputValues = adcPositiveInputNode.getChildren()

    adcSym_NUM_CHANNELS = adcComponent.createIntegerSymbol("ADC_NUM_CHANNELS", None)
    adcSym_NUM_CHANNELS.setVisible(False)
    adcSym_NUM_CHANNELS.setDefaultValue(len(adcPositiveInputValues))

    adcChannelMenu = adcComponent.createMenuSymbol("ADC_CHANNEL_MENU", None)
    adcChannelMenu.setLabel("Channel Configuration")

    #positive input
    adcSym_INPUTCTRL_MUXPOS = adcComponent.createKeyValueSetSymbol("ADC_INPUTCTRL_MUXPOS", adcChannelMenu)
    adcSym_INPUTCTRL_MUXPOS.setLabel("Select Positive Input")
    adcSym_INPUTCTRL_MUXPOS.setDefaultValue(0)
    adcSym_INPUTCTRL_MUXPOS.setOutputMode("Key")
    adcSym_INPUTCTRL_MUXPOS.setDisplayMode("Description")
    posInput = 0
    for index in range(0, len(adcPositiveInputValues)):
        if "AIN" in adcPositiveInputValues[index].getAttribute("name"):
            if adcPositiveInputValues[index].getAttribute("name") in channel:
                adcSym_MUXPOS_ENUM = adcComponent.createStringSymbol("ADC_MUXPOS_ENUM"+str(posInput), None)
                adcSym_MUXPOS_ENUM.setDefaultValue(adcPositiveInputValues[index].getAttribute("name"))
                adcSym_MUXPOS_ENUM.setVisible(False)
                posInput = posInput + 1
                adcSym_INPUTCTRL_MUXPOS.addKey(adcPositiveInputValues[index].getAttribute("name"), adcPositiveInputValues[index].getAttribute("value"),
                adcPositiveInputValues[index].getAttribute("caption"))
        else:
            adcSym_MUXPOS_ENUM = adcComponent.createStringSymbol("ADC_MUXPOS_ENUM"+str(posInput), None)
            adcSym_MUXPOS_ENUM.setDefaultValue(adcPositiveInputValues[index].getAttribute("name"))
            adcSym_MUXPOS_ENUM.setVisible(False)
            posInput = posInput + 1
            adcSym_INPUTCTRL_MUXPOS.addKey(adcPositiveInputValues[index].getAttribute("name"), adcPositiveInputValues[index].getAttribute("value"),
            adcPositiveInputValues[index].getAttribute("caption"))

    #negative input
    adcSym_INPUTCTRL_MUXNEG = adcComponent.createKeyValueSetSymbol("ADC_INPUTCTRL_MUXNEG", adcChannelMenu)
    adcSym_INPUTCTRL_MUXNEG.setLabel("Select Negative Input")
    adcSym_INPUTCTRL_MUXNEG.setOutputMode("Key")
    adcSym_INPUTCTRL_MUXNEG.setDisplayMode("Description")
    defaultIndex = 0
    gndIndex = 0
    adcNagativeInputNode = ATDF.getNode("/avr-tools-device-file/modules/module@[name=\"ADC\"]/value-group@[name=\"ADC_INPUTCTRL__MUXNEG\"]")
    adcNagativeInputValues = []
    adcNagativeInputValues = adcNagativeInputNode.getChildren()
    posInput = 0
    for index in range(0, len(adcNagativeInputValues)):
        if adcNagativeInputValues[index].getAttribute("name") == "GND":
            defaultIndex = gndIndex
        if "AIN" in adcNagativeInputValues[index].getAttribute("name"):
            if adcNagativeInputValues[index].getAttribute("name") in channel:
                adcSym_MUXNEG_ENUM = adcComponent.createStringSymbol("ADC_MUXNEG_ENUM"+str(posInput), None)
                adcSym_MUXNEG_ENUM.setDefaultValue(adcNagativeInputValues[index].getAttribute("name"))
                adcSym_MUXNEG_ENUM.setVisible(False)
                posInput = posInput + 1
                adcSym_INPUTCTRL_MUXNEG.addKey(adcNagativeInputValues[index].getAttribute("name"), adcNagativeInputValues[index].getAttribute("value"),
                adcNagativeInputValues[index].getAttribute("caption"))
                gndIndex += 1
        else:
            adcSym_MUXNEG_ENUM = adcComponent.createStringSymbol("ADC_MUXNEG_ENUM"+str(posInput), None)
            adcSym_MUXNEG_ENUM.setDefaultValue(adcNagativeInputValues[index].getAttribute("name"))
            adcSym_MUXNEG_ENUM.setVisible(False)
            posInput = posInput + 1
            adcSym_INPUTCTRL_MUXNEG.addKey(adcNagativeInputValues[index].getAttribute("name"), adcNagativeInputValues[index].getAttribute("value"),
            adcNagativeInputValues[index].getAttribute("caption"))
            gndIndex += 1
    adcSym_INPUTCTRL_MUXNEG.setDefaultValue(defaultIndex)
    
    adcSym_INPUTCTRL_INPUTSCAN = adcComponent.createIntegerSymbol("ADC_INPUTCTRL_INPUTSCAN", adcChannelMenu)
    adcSym_INPUTCTRL_INPUTSCAN.setLabel("Number of inputs to scan")
    adcSym_INPUTCTRL_INPUTSCAN.setDefaultValue(0)
    adcSym_INPUTCTRL_INPUTSCAN.setMin(0)
    adcSym_INPUTCTRL_INPUTSCAN.setMax(20)

    adcSym_INPUTCTRL_INPUTOFFSET = adcComponent.createIntegerSymbol("ADC_INPUTCTRL_INPUTOFFSET", adcChannelMenu)
    adcSym_INPUTCTRL_INPUTOFFSET.setLabel("Scan start offset")
    adcSym_INPUTCTRL_INPUTOFFSET.setDefaultValue(0)
    adcSym_INPUTCTRL_INPUTOFFSET.setMin(0)
    adcSym_INPUTCTRL_INPUTOFFSET.setMax(20)
    adcSym_INPUTCTRL_INPUTOFFSET.setVisible(False)
    adcSym_INPUTCTRL_INPUTOFFSET.setDependencies(adcOffsetVisible, ["ADC_INPUTCTRL_INPUTSCAN"])

    adcResultMenu = adcComponent.createMenuSymbol("ADC_RESULT_MENU", None)
    adcResultMenu.setLabel("Result Configuration")

    #resolution configuration
    global adcSym_CTRLC_RESSEL
    adcSym_CTRLC_RESSEL = adcComponent.createKeyValueSetSymbol("ADC_CTRLB_RESSEL", adcResultMenu)
    adcSym_CTRLC_RESSEL.setLabel("Select Result Resolution")
    adcSym_CTRLC_RESSEL.setDefaultValue(0)
    adcSym_CTRLC_RESSEL.setOutputMode("Key")
    adcSym_CTRLC_RESSEL.setDisplayMode("Description")
    adcResultResolutionNode = ATDF.getNode("/avr-tools-device-file/modules/module@[name=\"ADC\"]/value-group@[name=\"ADC_CTRLB__RESSEL\"]")
    adcResultResolutionValues = []
    adcResultResolutionValues = adcResultResolutionNode.getChildren()
    for index in range (0 , len(adcResultResolutionValues)):
        adcSym_CTRLC_RESSEL.addKey(adcResultResolutionValues[index].getAttribute("name"), adcResultResolutionValues[index].getAttribute("value"),
        adcResultResolutionValues[index].getAttribute("caption"))

    #Averaging
    adcSym_AVGCTRL_SAMPLENUM = adcComponent.createKeyValueSetSymbol("ADC_AVGCTRL_SAMPLENUM", adcSym_CTRLC_RESSEL)
    adcSym_AVGCTRL_SAMPLENUM.setLabel("Number of Accumulated Samples")
    adcSym_AVGCTRL_SAMPLENUM.setDefaultValue(0)
    adcSym_AVGCTRL_SAMPLENUM.setOutputMode("Key")
    adcSym_AVGCTRL_SAMPLENUM.setDisplayMode("Description")
    adcSym_AVGCTRL_SAMPLENUM.setVisible(False)
    adcResultResolutionNode = ATDF.getNode("/avr-tools-device-file/modules/module@[name=\"ADC\"]/value-group@[name=\"ADC_AVGCTRL__SAMPLENUM\"]")
    adcResultResolutionValues = []
    adcResultResolutionValues = adcResultResolutionNode.getChildren()
    for index in range (0 , len(adcResultResolutionValues)):
        adcSym_AVGCTRL_SAMPLENUM.addKey(adcResultResolutionValues[index].getAttribute("name"), adcResultResolutionValues[index].getAttribute("value"),
        adcResultResolutionValues[index].getAttribute("caption"))
    adcSym_AVGCTRL_SAMPLENUM.setDependencies(adcResultConfVisibility, ["ADC_CTRLB_RESSEL"])

    #division coefficient
    adcSym_AVGCTRL_ADJRES = adcComponent.createIntegerSymbol("ADC_AVGCTRL_ADJRES", adcSym_CTRLC_RESSEL)
    adcSym_AVGCTRL_ADJRES.setLabel("Number of Right Shifts")
    adcSym_AVGCTRL_ADJRES.setMin(0)
    adcSym_AVGCTRL_ADJRES.setMax(7)
    adcSym_AVGCTRL_ADJRES.setDefaultValue(0)
    adcSym_AVGCTRL_ADJRES.setVisible(False)
    adcSym_AVGCTRL_ADJRES.setDependencies(adcResultConfVisibility, ["ADC_CTRLB_RESSEL"])

    #left adjusted mode
    adcSym_CTRLC_LEFTADJ = adcComponent.createBooleanSymbol("ADC_CTRLB_LEFTADJ", adcResultMenu)
    adcSym_CTRLC_LEFTADJ.setLabel("Left Aligned Result")
    adcSym_CTRLC_LEFTADJ.setVisible(True)

    #interrupt mode
    global adcSym_INTENSET_RESRDY
    adcSym_INTENSET_RESRDY = adcComponent.createBooleanSymbol("ADC_INTENSET_RESRDY", adcResultMenu)
    adcSym_INTENSET_RESRDY.setLabel("Enable Result Ready Interrupt")

    #event out mode
    adcSym_EVCTRL_RSERDYEO = adcComponent.createBooleanSymbol("ADC_EVCTRL_RESRDYEO", adcResultMenu)
    adcSym_EVCTRL_RSERDYEO.setLabel("Enable Result Ready Event Out")

    adcWindowMenu = adcComponent.createMenuSymbol("ADC_WINDOW_CONFIG_MENU", None)
    adcWindowMenu.setLabel("Window Mode Configuration")

    #Configure mode for Window operation
    adcSym_CTRLC_WINMODE = adcComponent.createKeyValueSetSymbol("ADC_WINCTRL_WINMODE", adcWindowMenu)
    adcSym_CTRLC_WINMODE.setLabel("Select Window Monitor Mode")
    adcSym_CTRLC_WINMODE.setDefaultValue(0)
    adcSym_CTRLC_WINMODE.setOutputMode("Key")
    adcSym_CTRLC_WINMODE.setDisplayMode("Description")
    adcWindowConfigNode = ATDF.getNode("/avr-tools-device-file/modules/module@[name=\"ADC\"]/value-group@[name=\"ADC_WINCTRL__WINMODE\"]")
    adcWindowConfigValues = []
    adcWindowConfigValues = adcWindowConfigNode.getChildren()
    for index in range (0 , len(adcWindowConfigValues)):
        adcSym_CTRLC_WINMODE.addKey(adcWindowConfigValues[index].getAttribute("name"), adcWindowConfigValues[index].getAttribute("value"),
        adcWindowConfigValues[index].getAttribute("caption"))

    #Window upper threshold
    adcSym_WINUT = adcComponent.createIntegerSymbol("ADC_WINUT", adcWindowMenu)
    adcSym_WINUT.setLabel("Window Upper Threshold")
    adcSym_WINUT.setMin(-32768)
    adcSym_WINUT.setMax(32767)
    adcSym_WINUT.setDefaultValue(1024)
    adcSym_WINUT.setVisible(False)
    adcSym_WINUT.setDependencies(adcWindowVisible, ["ADC_WINCTRL_WINMODE"])

    #Window lower threshold
    adcSym_WINLT = adcComponent.createIntegerSymbol("ADC_WINLT", adcWindowMenu)
    adcSym_WINLT.setLabel("Window Lower Threshold")
    adcSym_WINLT.setMin(-32768)
    adcSym_WINLT.setMax(32767)
    adcSym_WINLT.setDefaultValue(512)
    adcSym_WINLT.setVisible(False)
    adcSym_WINLT.setDependencies(adcWindowVisible, ["ADC_WINCTRL_WINMODE"])

    global adcSym_INTENSET_WINMON
    adcSym_INTENSET_WINMON = adcComponent.createBooleanSymbol("ADC_INTENSET_WINMON", adcWindowMenu)
    adcSym_INTENSET_WINMON.setLabel("Enable Window Monitor Interrupt")
    adcSym_INTENSET_WINMON.setDefaultValue(False)
    adcSym_INTENSET_WINMON.setVisible(False)
    adcSym_INTENSET_WINMON.setDependencies(adcWindowVisible, ["ADC_WINCTRL_WINMODE"])

    #Enable Window Monitor Event Out
    adcSym_HW_INP_EVENT = adcComponent.createBooleanSymbol("ADC_WINDOW_OUTPUT_EVENT", adcWindowMenu)
    adcSym_HW_INP_EVENT.setLabel("Enable Window Monitor Event Out")
    adcSym_HW_INP_EVENT.setVisible(False)
    adcSym_HW_INP_EVENT.setDependencies(adcWindowVisible, ["ADC_WINCTRL_WINMODE"])

    adcSleepMenu = adcComponent.createMenuSymbol("ADC_SLEEP_MENU", None)
    adcSleepMenu.setLabel("Sleep Mode Configuration")

    #run in standby mode
    adcSym_CTRLA_RUNSTDBY = adcComponent.createBooleanSymbol("ADC_CTRLA_RUNSTDBY", adcSleepMenu)
    adcSym_CTRLA_RUNSTDBY.setLabel("Run During Standby")
    adcSym_CTRLA_RUNSTDBY.setVisible(True)

    adcSym_EVESYS_CONFIGURE = adcComponent.createIntegerSymbol("ADC_EVESYS_CONFIGURE", None)
    adcSym_EVESYS_CONFIGURE.setVisible(False)
    adcSym_EVESYS_CONFIGURE.setDependencies(adcEvesysConfigure, \
        ["ADC_WINDOW_OUTPUT_EVENT", "ADC_EVCTRL_RESRDYEO", "ADC_CONV_TRIGGER", "ADC_EVCTRL_FLUSH", "ADC_EVCTRL_START"])

    adcSym_SYSCTRL_COMMENT = adcComponent.createCommentSymbol("ADC_SYSCTRL_COMMENT", None)
    adcSym_SYSCTRL_COMMENT.setLabel("*********** Enable Vref output in SYSCTRL ***********")
    adcSym_SYSCTRL_COMMENT.setVisible(False)
    adcSym_SYSCTRL_COMMENT.setDependencies(adcSYSCTRLVisible, ["ADC_REFCTRL_REFSEL", "ADC_INPUTCTRL_MUXPOS"])
    ############################################################################
    #### Dependency ####
    ############################################################################
    InterruptVector = adcInstanceName.getValue() + "_INTERRUPT_ENABLE"
    InterruptHandler = adcInstanceName.getValue() + "_INTERRUPT_HANDLER"
    InterruptHandlerLock = adcInstanceName.getValue()+ "_INTERRUPT_HANDLER_LOCK"
    InterruptVectorUpdate = adcInstanceName.getValue() + "_INTERRUPT_ENABLE_UPDATE"

    # Interrupt Dynamic settings
    adcSym_UpdateInterruptStatus = adcComponent.createBooleanSymbol("ADC_INTERRUPT_STATUS", None)
    adcSym_UpdateInterruptStatus.setDependencies(updateADCInterruptStatus, ["ADC_INTENSET_RESRDY", "ADC_INTENSET_WINMON"])
    adcSym_UpdateInterruptStatus.setVisible(False)

    # Interrupt Warning status
    adcSym_IntEnComment = adcComponent.createCommentSymbol("ADC_INTERRUPT_ENABLE_COMMENT", None)
    adcSym_IntEnComment.setVisible(False)
    adcSym_IntEnComment.setLabel("Warning!!! "+adcInstanceName.getValue()+" Interrupt is Disabled in Interrupt Manager")
    adcSym_IntEnComment.setDependencies(updateADCInterruptWarringStatus, ["core." + InterruptVectorUpdate])

    # Clock Warning status
    adcSym_ClkEnComment = adcComponent.createCommentSymbol("ADC_CLOCK_ENABLE_COMMENT", None)
    adcSym_ClkEnComment.setVisible(False)
    adcSym_ClkEnComment.setLabel("Warning!!! " +adcInstanceName.getValue()+" Clock is Disabled in Clock Manager")
    adcSym_ClkEnComment.setDependencies(updateADCClockWarringStatus, ["core." + adcInstanceName.getValue() + "_CLOCK_ENABLE"])

    ###################################################################################################
    ####################################### Code Generation  ##########################################
    ###################################################################################################

    configName = Variables.get("__CONFIGURATION_NAME")

    adcModuleNode = ATDF.getNode("/avr-tools-device-file/modules/module@[name=\"ADC\"]")
    adcModuleID = adcModuleNode.getAttribute("id")

    adcSym_CommonHeaderFile = adcComponent.createFileSymbol("ADC_COMMON_HEADER", None)
    adcSym_CommonHeaderFile.setSourcePath("../peripheral/adc_"+adcModuleID+"/templates/plib_adc_common.h.ftl")
    adcSym_CommonHeaderFile.setOutputName("plib_adc_common.h")
    adcSym_CommonHeaderFile.setDestPath("/peripheral/adc/")
    adcSym_CommonHeaderFile.setProjectPath("config/" + configName + "/peripheral/adc/")
    adcSym_CommonHeaderFile.setType("HEADER")
    adcSym_CommonHeaderFile.setMarkup(True)

    adcSym_HeaderFile = adcComponent.createFileSymbol("ADC_HEADER", None)
    adcSym_HeaderFile.setSourcePath("../peripheral/adc_"+adcModuleID+"/templates/plib_adc.h.ftl")
    adcSym_HeaderFile.setOutputName("plib_"+adcInstanceName.getValue().lower()+".h")
    adcSym_HeaderFile.setDestPath("/peripheral/adc/")
    adcSym_HeaderFile.setProjectPath("config/" + configName + "/peripheral/adc/")
    adcSym_HeaderFile.setType("HEADER")
    adcSym_HeaderFile.setMarkup(True)

    adcSym_SourceFile = adcComponent.createFileSymbol("ADC_SOURCE", None)
    adcSym_SourceFile.setSourcePath("../peripheral/adc_"+adcModuleID+"/templates/plib_adc.c.ftl")
    adcSym_SourceFile.setOutputName("plib_"+adcInstanceName.getValue().lower()+".c")
    adcSym_SourceFile.setDestPath("/peripheral/adc/")
    adcSym_SourceFile.setProjectPath("config/" + configName + "/peripheral/adc/")
    adcSym_SourceFile.setType("SOURCE")
    adcSym_SourceFile.setMarkup(True)

    adcSym_SystemInitFile = adcComponent.createFileSymbol("ADC_SYS_INIT", None)
    adcSym_SystemInitFile.setType("STRING")
    adcSym_SystemInitFile.setOutputName("core.LIST_SYSTEM_INIT_C_SYS_INITIALIZE_PERIPHERALS")
    adcSym_SystemInitFile.setSourcePath("../peripheral/adc_"+adcModuleID+"/templates/system/initialization.c.ftl")
    adcSym_SystemInitFile.setMarkup(True)

    adcSym_SystemDefFile = adcComponent.createFileSymbol("ADC_SYS_DEF", None)
    adcSym_SystemDefFile.setType("STRING")
    adcSym_SystemDefFile.setOutputName("core.LIST_SYSTEM_DEFINITIONS_H_INCLUDES")
    adcSym_SystemDefFile.setSourcePath("../peripheral/adc_"+adcModuleID+"/templates/system/definitions.h.ftl")
    adcSym_SystemDefFile.setMarkup(True)
