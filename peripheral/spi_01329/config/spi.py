"""*****************************************************************************
* Copyright (C) 2018-2019 Microchip Technology Inc. and its subsidiaries.
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

################################################################################
#### Register Information ####
################################################################################
# SPICON Register
spiValGrp_SPI1CON_MSTEN = ATDF.getNode('/avr-tools-device-file/modules/module@[name="SPI"]/value-group@[name="SPI1CON__MSTEN"]')
spiBitField_SPI1CON_MSTEN = ATDF.getNode('/avr-tools-device-file/modules/module@[name="SPI"]/register-group@[name="SPI"]/register@[name="SPI1CON"]/bitfield@[name="MSTEN"]')

spiValGrp_SPI1CON_MSSEN = ATDF.getNode('/avr-tools-device-file/modules/module@[name="SPI"]/value-group@[name="SPI1CON__MSSEN"]')
spiBitField_SPI1CON_MSSEN = ATDF.getNode('/avr-tools-device-file/modules/module@[name="SPI"]/register-group@[name="SPI"]/register@[name="SPI1CON"]/bitfield@[name="MSSEN"]')

spiValGrp_SPI1CON_MODE = ATDF.getNode('/avr-tools-device-file/modules/module@[name="SPI"]/value-group@[name="SPI1CON__MODE32"]')
spiBitField_SPI1CON_MODE = ATDF.getNode('/avr-tools-device-file/modules/module@[name="SPI"]/register-group@[name="SPI"]/register@[name="SPI1CON"]/bitfield@[name="MODE32"]')

spiValGrp_SPI1CON_CKE = ATDF.getNode('/avr-tools-device-file/modules/module@[name="SPI"]/value-group@[name="SPI1CON__CKE"]')
spiBitField_SPI1CON_CKE = ATDF.getNode('/avr-tools-device-file/modules/module@[name="SPI"]/register-group@[name="SPI"]/register@[name="SPI1CON"]/bitfield@[name="CKE"]')

spiValGrp_SPI1CON_CKP = ATDF.getNode('/avr-tools-device-file/modules/module@[name="SPI"]/value-group@[name="SPI1CON__CKP"]')
spiBitField_SPI1CON_CKP = ATDF.getNode('/avr-tools-device-file/modules/module@[name="SPI"]/register-group@[name="SPI"]/register@[name="SPI1CON"]/bitfield@[name="CKP"]')

spiValGrp_SPI1CON_MSSEN = ATDF.getNode('/avr-tools-device-file/modules/module@[name="SPI"]/value-group@[name="SPI1CON__MSSEN"]')
spiBitField_SPI1CON_MSSEN = ATDF.getNode('/avr-tools-device-file/modules/module@[name="SPI"]/register-group@[name="SPI"]/register@[name="SPI1CON"]/bitfield@[name="MSSEN"]')

spiValGrp_SPI1CON_MCLKSEL = ATDF.getNode('/avr-tools-device-file/modules/module@[name="SPI"]/value-group@[name="SPI1CON__MCLKSEL"]')
spiBitField_SPI1CON_MCLKSEL = ATDF.getNode('/avr-tools-device-file/modules/module@[name="SPI"]/register-group@[name="SPI"]/register@[name="SPI1CON"]/bitfield@[name="MCLKSEL"]')

################################################################################
#### Global Variables ####
################################################################################

global interruptsChildren
interruptsChildren = ATDF.getNode('/avr-tools-device-file/devices/device/interrupts').getChildren()

global dummyDataDict
dummyDataDict = {
                    "(AUDEN=1) 24-bit Data, 32-bit FIFO, 32-bit Channel/64-bit Frame/(AUDEN=0) 32-bit Data" : 0xFFFFFFFF,
                    "(AUDEN=1) 32-bit Data, 32-bit FIFO, 32-bit Channel/64-bit Frame/(AUDEN=0) 32-bit Data" : 0xFFFFFFFF,
                    "(AUDEN=1) 16-bit Data, 16-bit FIFO, 32-bit Channel/64-bit Frame/(AUDEN=0) 16-bit Data" : 0xFFFF,
                    "(AUDEN=1) 16-bit Data, 16-bit FIFO, 16-bit Channel/32-bit Frame/(AUDEN=0) 8-bit Data"  : 0xFF,
                }

################################################################################
#### Business Logic ####
################################################################################

def setSPIInterruptData(status):

    for id in InterruptVector:
        Database.setSymbolValue("core", id, status, 1)

    for id in InterruptHandlerLock:
        Database.setSymbolValue("core", id, status, 1)

    for id in InterruptHandler:
        interruptName = id.split("_INTERRUPT_HANDLER")[0]
        if status == True:
            Database.setSymbolValue("core", id, interruptName + "_InterruptHandler", 1)
        else:
            Database.setSymbolValue("core", id, interruptName + "_Handler", 1)

def updateSPIInterruptData(symbol, event):

    if event["id"] == "SPI_INTERRUPT_MODE":
        setSPIInterruptData(event["value"])

    status = False

    for id in InterruptVectorUpdate:
        id = id.replace("core.", "")
        if Database.getSymbolValue("core", id) == True:
            status = True
            break

    if spiSymInterruptMode.getValue() == True and status == True:
        symbol.setVisible(True)
    else:
        symbol.setVisible(False)

def _get_enblReg_parms(vectorNumber):

    # This takes in vector index for interrupt, and returns the IECx register name as well as
    # mask and bit location within it for given interrupt
    index = int(vectorNumber / 32)
    regName = "IEC" + str(index)
    bitPosn = int(vectorNumber % 32)
    bitMask = hex(1 << bitPosn)

    return regName, str(bitPosn), str(bitMask)

def _get_statReg_parms(vectorNumber):

    # This takes in vector index for interrupt, and returns the IFSx register name as well as
    # mask and bit location within it for given interrupt
    index = int(vectorNumber / 32)
    regName = "IFS" + str(index)
    bitPosn = int(vectorNumber % 32)
    bitMask = hex(1 << bitPosn)

    return regName, str(bitPosn), str(bitMask)

def _get_bitfield_names(node, outputList):

    valueNodes = node.getChildren()

    for bitfield in valueNodes:   ##  do this for all <value > entries for this bitfield
        dict = {}
        if bitfield.getAttribute("caption").lower() != "reserved":  ##  skip (unused) reserved fields
            dict["desc"] = bitfield.getAttribute("caption")
            dict["key"] = bitfield.getAttribute("caption")

            ##  Get rid of leading '0x', and convert to int if was hex
            value = bitfield.getAttribute("value")

            if(value[:2] == "0x"):
                temp = value[2:]
                tempint = int(temp, 16)
            else:
                tempint = int(value)

            dict["value"] = str(tempint)
            outputList.append(dict)

def getIRQnumber(string):

    for param in interruptsChildren:
        name = param.getAttribute("name")
        if string == name:
            irq_index = param.getAttribute("index")
            break

    return irq_index

##  Dependency Function to show or hide the warning message depending on Clock enable/disable status
def ClockStatusWarning(symbol, event):

    symbol.setVisible(not event["value"])

def ClockModeInfo(symbol, event):

    CPHAINDEX = Database.getSymbolValue(spiInstanceName.getValue().lower(), "SPI_SPICON_CLK_PH")
    CPOLINDEX = Database.getSymbolValue(spiInstanceName.getValue().lower(), "SPI_SPICON_CLK_POL")

    if event["id"] == "SPI_SPICON_CLK_PH":
        CPHA = int(event["symbol"].getKeyValue(event["value"]))
        CPOL = 1 if CPOLINDEX == 0 else 0
    elif event["id"] == "SPI_SPICON_CLK_POL":
        CPOL = int(event["symbol"].getKeyValue(event["value"]))
        CPHA = 1 if CPHAINDEX == 0 else 0
    if (CPOL == 0) and (CPHA == 0):
        symbol.setLabel("***SPI Mode 0 is Selected***")
    elif (CPOL == 0) and (CPHA == 1):
        symbol.setLabel("***SPI Mode 1 is Selected***")
    elif (CPOL == 1) and (CPHA == 0):
        symbol.setLabel("***SPI Mode 2 is Selected***")
    else:
        symbol.setLabel("***SPI Mode 3 is Selected***")

def showMasterDependencies(symbol, event):

    if event["symbol"].getKey(event["value"]) == "Master mode":
        symbol.setVisible(True)
    else:
        symbol.setVisible(False)

def calculateBRGValue(clkfreq, baudRate):

    t_brg = ((int(clkfreq/baudRate) / 2) - 1)
    baudHigh = int (clkfreq / (2 * (t_brg + 1)))
    baudLow = int (clkfreq / (2 * (t_brg + 2)))
    errorHigh = baudHigh - baudRate
    errorLow = baudRate - baudLow

    if errorHigh > errorLow:
        t_brg +=1

    ## Baud rate register is a 13 bit register
    if t_brg < 0:
        t_brg = 0
        Log.writeErrorMessage("SPI Clock source Frequency is low for the desired baud rate")
    elif t_brg > 8191:
        t_brg = 8191
        Log.writeErrorMessage("Desired baud rate is low for current SPI Source Clock Frequency")

    return int(t_brg)

def SPIBRG_ValueUpdate(symbol, event):

    clkSelect = Database.getSymbolValue(spiInstanceName.getValue().lower(), "SPI_MASTER_CLOCK")
    BaudRate = int (Database.getSymbolValue(spiInstanceName.getValue().lower(), "SPI_BAUD_RATE"))

    if event["id"] == "SPI_MASTER_CLOCK":
        clkSelect = int(event["value"])
    elif event["id"] == "SPI_BAUD_RATE":
        ## This means there is change in baud rate provided by user in GUI
        BaudRate = int (event["value"])

    if clkSelect == 1:
        clkFreq = int(Database.getSymbolValue("core", "CONFIG_SYS_CLK_PBCLK2_FREQ"))
    else:
        clkFreq = int(Database.getSymbolValue("core", "CONFIG_SYS_CLK_REFCLK1_FREQ"))

    t_brg = calculateBRGValue(clkFreq, BaudRate)
    symbol.setValue(t_brg, 1)

def SPI_MasterFreqValueUpdate(symbol,event):

    clkSelect = Database.getSymbolValue(spiInstanceName.getValue().lower(), "SPI_MASTER_CLOCK")

    if event["id"] == "SPI_MASTER_CLOCK":
        clkSelect = int(event["value"])

    if clkSelect == 1:
        clkFreq = int(Database.getSymbolValue("core", "CONFIG_SYS_CLK_PBCLK2_FREQ"))
    else:
        clkFreq = int(Database.getSymbolValue("core", "CONFIG_SYS_CLK_REFCLK1_FREQ"))

    symbol.setValue(clkFreq, 1)

def DummyData_ValueUpdate(symbol, event):

    symbol.setValue(dummyDataDict[event["symbol"].getKey(event["value"])], 1)

    symbol.setMax(dummyDataDict[event["symbol"].getKey(event["value"])])

def instantiateComponent(spiComponent):

    global spiInstanceName
    global InterruptVector
    global InterruptHandlerLock
    global InterruptHandler
    global InterruptVectorUpdate
    global spiSymInterruptMode

    InterruptVector = []
    InterruptHandler = []
    InterruptHandlerLock = []
    InterruptVectorUpdate = []

    spiInstanceName = spiComponent.createStringSymbol("SPI_INSTANCE_NAME", None)
    spiInstanceName.setVisible(False)
    spiInstanceName.setDefaultValue(spiComponent.getID().upper())
    Log.writeInfoMessage("Running " + spiInstanceName.getValue())

    spiInstanceNum = spiComponent.createStringSymbol("SPI_INSTANCE_NUM", None)
    spiInstanceNum.setVisible(False)
    componentName = str(spiComponent.getID())
    instanceNum = filter(str.isdigit,componentName)
    spiInstanceNum.setDefaultValue(instanceNum)

    spiSymInterruptMode = spiComponent.createBooleanSymbol("SPI_INTERRUPT_MODE", None)
    spiSymInterruptMode.setLabel("Enable Interrrupts ?")
    spiSymInterruptMode.setDefaultValue(True)

    ## Fault Interrrupt Setup
    spiIrqFault = spiInstanceName.getValue() + "_FAULT"
    spiFaultVectorNum = int(getIRQnumber(spiIrqFault))

    enblRegName, enblBitPosn, enblMask = _get_enblReg_parms(spiFaultVectorNum)
    statRegName, statBitPosn, statMask = _get_statReg_parms(spiFaultVectorNum)

    ## IEC REG
    spiIEC = spiComponent.createStringSymbol("SPI_FLT_IEC_REG", None)
    spiIEC.setDefaultValue(enblRegName)
    spiIEC.setVisible(False)

    ## IEC REG MASK
    spiIECMask = spiComponent.createStringSymbol("SPI_FLT_IEC_REG_MASK", None)
    spiIECMask.setDefaultValue(enblMask)
    spiIECMask.setVisible(False)

    ## IFS REG
    spiIFS = spiComponent.createStringSymbol("SPI_FLT_IFS_REG", None)
    spiIFS.setDefaultValue(statRegName)
    spiIFS.setVisible(False)

    ## IFS REG MASK
    spiIFSMask = spiComponent.createStringSymbol("SPI_FLT_IFS_REG_MASK", None)
    spiIFSMask.setDefaultValue(statMask)
    spiIFSMask.setVisible(False)

    ## SPI RX Interrupt
    spiIrqrRx = spiInstanceName.getValue() + "_RX"
    InterruptVector.append(spiIrqrRx + "_INTERRUPT_ENABLE")
    InterruptHandler.append(spiIrqrRx + "_INTERRUPT_HANDLER")
    InterruptHandlerLock.append(spiIrqrRx + "_INTERRUPT_HANDLER_LOCK")
    InterruptVectorUpdate.append("core." + spiIrqrRx + "_INTERRUPT_ENABLE_UPDATE")
    spiRxVectorNum = int(getIRQnumber(spiIrqrRx))

    enblRegName, enblBitPosn, enblMask = _get_enblReg_parms(spiRxVectorNum)
    statRegName, statBitPosn, statMask = _get_statReg_parms(spiRxVectorNum)

    ## IEC REG
    spiRXIEC = spiComponent.createStringSymbol("SPI_RX_IEC_REG", None)
    spiRXIEC.setDefaultValue(enblRegName)
    spiRXIEC.setVisible(False)

    ## IEC REG MASK
    spiRXIECMask = spiComponent.createStringSymbol("SPI_RX_IEC_REG_MASK", None)
    spiRXIECMask.setDefaultValue(enblMask)
    spiRXIECMask.setVisible(False)

    ## IFS REG
    spiRXIFS = spiComponent.createStringSymbol("SPI_RX_IFS_REG", None)
    spiRXIFS.setDefaultValue(statRegName)
    spiRXIFS.setVisible(False)

    ## IFS REG MASK
    spiRXIFSMask = spiComponent.createStringSymbol("SPI_RX_IFS_REG_MASK", None)
    spiRXIFSMask.setDefaultValue(statMask)
    spiRXIFSMask.setVisible(False)

    ##SPI TX Interrupt
    spiIrqTx = spiInstanceName.getValue() + "_TX"
    InterruptVector.append(spiIrqTx + "_INTERRUPT_ENABLE")
    InterruptHandler.append(spiIrqTx + "_INTERRUPT_HANDLER")
    InterruptHandlerLock.append(spiIrqTx + "_INTERRUPT_HANDLER_LOCK")
    InterruptVectorUpdate.append("core." + spiIrqTx + "_INTERRUPT_ENABLE_UPDATE")
    spiTxVectorNum = int(getIRQnumber(spiIrqTx))

    enblRegName, enblBitPosn, enblMask = _get_enblReg_parms(spiTxVectorNum)
    statRegName, statBitPosn, statMask = _get_statReg_parms(spiTxVectorNum)

    ## IEC REG
    spiTXIEC = spiComponent.createStringSymbol("SPI_TX_IEC_REG", None)
    spiTXIEC.setDefaultValue(enblRegName)
    spiTXIEC.setVisible(False)

    ## IEC REG MASK
    spiTXIECMask = spiComponent.createStringSymbol("SPI_TX_IEC_REG_MASK", None)
    spiTXIECMask.setDefaultValue(enblMask)
    spiTXIECMask.setVisible(False)

    ## IFS REG
    spiTXIFS = spiComponent.createStringSymbol("SPI_TX_IFS_REG", None)
    spiTXIFS.setDefaultValue(statRegName)
    spiTXIFS.setVisible(False)

    ## IFS REG MASK
    spiTXIFSMask = spiComponent.createStringSymbol("SPI_TX_IFS_REG_MASK", None)
    spiTXIFSMask.setDefaultValue(statMask)
    spiTXIFSMask.setVisible(False)

    ## MSTEN Selection Bit
    msten_names = []
    _get_bitfield_names(spiValGrp_SPI1CON_MSTEN, msten_names)
    spiSym_SPICON_MSTEN = spiComponent.createKeyValueSetSymbol( "SPI_MSTR_MODE_EN",None)
    spiSym_SPICON_MSTEN.setLabel(spiBitField_SPI1CON_MSTEN.getAttribute("caption"))
    spiSym_SPICON_MSTEN.setDefaultValue(0)
    spiSym_SPICON_MSTEN.setReadOnly(True)
    spiSym_SPICON_MSTEN.setOutputMode( "Value" )
    spiSym_SPICON_MSTEN.setDisplayMode( "Description" )
    for ii in msten_names:
        spiSym_SPICON_MSTEN.addKey( ii['key'],ii['value'], ii['desc'] )

    ## CLock Polarity
    clkpol_names = []
    _get_bitfield_names(spiValGrp_SPI1CON_CKP, clkpol_names)
    spiSym_SPICON_CLKPOL = spiComponent.createKeyValueSetSymbol( "SPI_SPICON_CLK_POL",None)
    spiSym_SPICON_CLKPOL.setLabel(spiBitField_SPI1CON_CKP.getAttribute("caption"))
    spiSym_SPICON_CLKPOL.setDefaultValue(1)
    spiSym_SPICON_CLKPOL.setOutputMode( "Value" )
    spiSym_SPICON_CLKPOL.setDisplayMode( "Description" )
    for ii in clkpol_names:
        spiSym_SPICON_CLKPOL.addKey( ii['key'],ii['value'], ii['desc'] )

    ## Clock Phase Bit
    clkph_names = []
    _get_bitfield_names(spiValGrp_SPI1CON_CKE, clkph_names)
    spiSym_SPICON_CLKPH = spiComponent.createKeyValueSetSymbol( "SPI_SPICON_CLK_PH",None)
    spiSym_SPICON_CLKPH.setLabel(spiBitField_SPI1CON_CKE.getAttribute("caption"))
    spiSym_SPICON_CLKPH.setDefaultValue(1)
    spiSym_SPICON_CLKPH.setOutputMode( "Value" )
    spiSym_SPICON_CLKPH.setDisplayMode( "Description" )
    for ii in clkph_names:
        spiSym_SPICON_CLKPH.addKey( ii['key'],ii['value'], ii['desc'] )

    ## Slave slect pin enable bit
    ssen_names = []
    _get_bitfield_names(spiValGrp_SPI1CON_MSSEN, ssen_names)
    spiSym_SPICON_MSSEN = spiComponent.createKeyValueSetSymbol( "SPI_SPICON_MSSEN",None)
    spiSym_SPICON_MSSEN.setLabel(spiBitField_SPI1CON_MSSEN.getAttribute("caption"))
    spiSym_SPICON_MSSEN.setDefaultValue(0)
    spiSym_SPICON_MSSEN.setOutputMode( "Value" )
    spiSym_SPICON_MSSEN.setDisplayMode( "Description" )
    for ii in ssen_names:
        spiSym_SPICON_MSSEN.addKey( ii['key'],ii['value'], ii['desc'] )

    ## SPI data width(Mode)
    mode_names = []
    _get_bitfield_names(spiValGrp_SPI1CON_MODE, mode_names)
    spiSym_SPICON_MODE = spiComponent.createKeyValueSetSymbol( "SPI_SPICON_MODE",None)
    spiSym_SPICON_MODE.setLabel(spiBitField_SPI1CON_MODE.getAttribute("caption"))
    spiSym_SPICON_MODE.setDefaultValue(3)
    spiSym_SPICON_MODE.setOutputMode( "Value" )
    spiSym_SPICON_MODE.setDisplayMode( "Description" )
    for ii in mode_names:
        spiSym_SPICON_MODE.addKey( ii['key'],ii['value'], ii['desc'] )

    ## SPI Master clock
    msclk_names = []
    _get_bitfield_names(spiValGrp_SPI1CON_MCLKSEL, msclk_names)
    spiSym_SPI1CON_MCLKSEL = spiComponent.createKeyValueSetSymbol( "SPI_MASTER_CLOCK",None)
    spiSym_SPI1CON_MCLKSEL.setLabel(spiBitField_SPI1CON_MCLKSEL.getAttribute("caption"))
    spiSym_SPI1CON_MCLKSEL.setDefaultValue(1)
    spiSym_SPI1CON_MCLKSEL.setOutputMode( "Value" )
    spiSym_SPI1CON_MCLKSEL.setReadOnly(False)
    spiSym_SPI1CON_MCLKSEL.setDisplayMode( "Description" )
    for ii in msclk_names:
        spiSym_SPI1CON_MCLKSEL.addKey( ii['key'],ii['value'], ii['desc'] )

    spiSym_Baud_Rate = spiComponent.createIntegerSymbol("SPI_BAUD_RATE", None)
    spiSym_Baud_Rate.setLabel("Baud Rate in Hz")
    spiSym_Baud_Rate.setDefaultValue(1000000)
    spiSym_Baud_Rate.setMin(1)
    spiSym_Baud_Rate.setDependencies(showMasterDependencies, ["SPI_MSTR_MODE_EN"])

    ## Baud Rate generation
    if int(spiSym_SPI1CON_MCLKSEL.getValue()) == 1:
        spiMasterFreq = int(Database.getSymbolValue("core", "CONFIG_SYS_CLK_PBCLK2_FREQ"))
    else:
        spiMasterFreq = int(Database.getSymbolValue("core", "CONFIG_SYS_CLK_REFCLK1_FREQ"))

    defaultSPIBR = calculateBRGValue(spiMasterFreq, spiSym_Baud_Rate.getValue())

    spiSym_SPIBRG_VALUE = spiComponent.createIntegerSymbol("SPI_BRG_VALUE", None)
    spiSym_SPIBRG_VALUE.setDefaultValue(defaultSPIBR)
    spiSym_SPIBRG_VALUE.setVisible(False)
    spiSym_SPIBRG_VALUE.setDependencies(SPIBRG_ValueUpdate, ["SPI_BAUD_RATE", "SPI_MASTER_CLOCK", "CONFIG_SYS_CLK_PBCLK2_FREQ", "CONFIG_SYS_CLK_REFCLK1_FREQ"])

    spiSym_MasterFreq_VALUE = spiComponent.createIntegerSymbol("SPI_MASTER_FREQ_VALUE", None)
    spiSym_MasterFreq_VALUE.setDefaultValue(spiMasterFreq)
    spiSym_MasterFreq_VALUE.setVisible(False)
    spiSym_MasterFreq_VALUE.setDependencies(SPI_MasterFreqValueUpdate, ["SPI_MASTER_CLOCK", "CONFIG_SYS_CLK_PBCLK2_FREQ", "CONFIG_SYS_CLK_REFCLK1_FREQ"])

    spiSymDummyData = spiComponent.createHexSymbol("SPI_DUMMY_DATA", None)
    spiSymDummyData.setLabel("Dummy Data")
    spiSymDummyData.setDescription("Dummy Data to be written during SPI Read")
    spiSymDummyData.setDefaultValue(0xFF)
    spiSymDummyData.setMin(0x0)
    spiSymDummyData.setDependencies(DummyData_ValueUpdate, ["SPI_SPICON_MODE"])

    spiSymClockModeComment = spiComponent.createCommentSymbol("SPI_CLOCK_MODE_COMMENT", None)
    spiSymClockModeComment.setLabel("***SPI Mode 0 Selected***")
    spiSymClockModeComment.setDependencies(ClockModeInfo, ["SPI_SPICON_CLK_POL", "SPI_SPICON_CLK_PH"])

    ############################################################################
    #### Interrupt Dependency ####
    ############################################################################

    setSPIInterruptData(spiSymInterruptMode.getValue())

    spiSymIntEnComment = spiComponent.createCommentSymbol("SPI_INTRRUPT_ENABLE_COMMENT", None)
    spiSymIntEnComment.setLabel("Warning!!! " + spiInstanceName.getValue() + " Interrupt is Disabled in Interrupt Manager")
    spiSymIntEnComment.setVisible(False)
    spiSymIntEnComment.setDependencies(updateSPIInterruptData, ["SPI_INTERRUPT_MODE"] + InterruptVectorUpdate)

    ###################################################################################################
    ####################################### Driver Symbols ############################################
    ###################################################################################################

    #SPI 8-bit Character size Mask
    spiSym_CHSIZE_8BIT = spiComponent.createStringSymbol("SPI_CHARSIZE_BITS_8_BIT_MASK", None)
    spiSym_CHSIZE_8BIT.setDefaultValue("0x00000000")
    spiSym_CHSIZE_8BIT.setVisible(False)

    #SPI 16-bit Character size Mask
    spiSym_CHSIZE_16BIT = spiComponent.createStringSymbol("SPI_CHARSIZE_BITS_16_BIT_MASK", None)
    spiSym_CHSIZE_16BIT.setDefaultValue("0x00000400")
    spiSym_CHSIZE_16BIT.setVisible(False)

    #SPI 32-bit Character size Mask
    spiSym_CHSIZE_32BIT = spiComponent.createStringSymbol("SPI_CHARSIZE_BITS_32_BIT_MASK", None)
    spiSym_CHSIZE_32BIT.setDefaultValue("0x00000800")
    spiSym_CHSIZE_32BIT.setVisible(False)

    #SPI Clock Phase Leading Edge Mask
    spiSym_CPHA_LE_Mask = spiComponent.createStringSymbol("SPI_CLOCK_PHASE_LEADING_MASK", None)
    spiSym_CPHA_LE_Mask.setDefaultValue("0x00000100")
    spiSym_CPHA_LE_Mask.setVisible(False)

    #SPI Clock Phase Trailing Edge Mask
    spiSym_CPHA_TE_Mask = spiComponent.createStringSymbol("SPI_CLOCK_PHASE_TRAILING_MASK", None)
    spiSym_CPHA_TE_Mask.setDefaultValue("0x00000000")
    spiSym_CPHA_TE_Mask.setVisible(False)

    #SPI Clock Polarity Idle Low Mask
    spiSym_CPOL_IL_Mask = spiComponent.createStringSymbol("SPI_CLOCK_POLARITY_LOW_MASK", None)
    spiSym_CPOL_IL_Mask.setDefaultValue("0x00000000")
    spiSym_CPOL_IL_Mask.setVisible(False)

    #SPI Clock Polarity Idle High Mask
    spiSym_CPOL_IH_Mask = spiComponent.createStringSymbol("SPI_CLOCK_POLARITY_HIGH_MASK", None)
    spiSym_CPOL_IH_Mask.setDefaultValue("0x00000040")
    spiSym_CPOL_IH_Mask.setVisible(False)

    #SPI API Prefix
    spiSym_API_Prefix = spiComponent.createStringSymbol("SPI_PLIB_API_PREFIX", None)
    spiSym_API_Prefix.setDefaultValue(spiInstanceName.getValue())
    spiSym_API_Prefix.setVisible(False)

    #SPI Transmit data register
    transmitRegister = spiComponent.createStringSymbol("TRANSMIT_DATA_REGISTER", None)
    transmitRegister.setDefaultValue("&("+spiInstanceName.getValue()+"BUF)")
    transmitRegister.setVisible(False)

    #SPI Receive data register
    receiveRegister = spiComponent.createStringSymbol("RECEIVE_DATA_REGISTER", None)
    receiveRegister.setDefaultValue("&("+spiInstanceName.getValue()+"BUF)")
    receiveRegister.setVisible(False)

    ############################################################################
    #### Code Generation ####
    ############################################################################

    configName = Variables.get("__CONFIGURATION_NAME")

    spiHeaderFile = spiComponent.createFileSymbol("SPI_COMMON_HEADER", None)
    spiHeaderFile.setSourcePath("../peripheral/spi_01329/templates/plib_spi_common.h")
    spiHeaderFile.setOutputName("plib_spi_common.h")
    spiHeaderFile.setDestPath("peripheral/spi/")
    spiHeaderFile.setProjectPath("config/" + configName + "/peripheral/spi/")
    spiHeaderFile.setType("HEADER")
    spiHeaderFile.setMarkup(False)
    spiHeaderFile.setOverwrite(True)

    spiHeader1File = spiComponent.createFileSymbol("SPI_HEADER", None)
    spiHeader1File.setSourcePath("../peripheral/spi_01329/templates/plib_spi.h.ftl")
    spiHeader1File.setOutputName("plib_" + spiInstanceName.getValue().lower() + ".h")
    spiHeader1File.setDestPath("/peripheral/spi/")
    spiHeader1File.setProjectPath("config/" + configName +"/peripheral/spi/")
    spiHeader1File.setType("HEADER")
    spiHeader1File.setMarkup(True)

    spiSource1File = spiComponent.createFileSymbol("SPI_SOURCE", None)
    spiSource1File.setSourcePath("../peripheral/spi_01329/templates/plib_spi.c.ftl")
    spiSource1File.setOutputName("plib_" + spiInstanceName.getValue().lower() + ".c")
    spiSource1File.setDestPath("/peripheral/spi/")
    spiSource1File.setProjectPath("config/" + configName +"/peripheral/spi/")
    spiSource1File.setType("SOURCE")
    spiSource1File.setMarkup(True)

    spiSystemInitFile = spiComponent.createFileSymbol("SPI_INIT", None)
    spiSystemInitFile.setType("STRING")
    spiSystemInitFile.setOutputName("core.LIST_SYSTEM_INIT_C_SYS_INITIALIZE_PERIPHERALS")
    spiSystemInitFile.setSourcePath("../peripheral/spi_01329/templates/system/initialization.c.ftl")
    spiSystemInitFile.setMarkup(True)

    spiSystemDefFile = spiComponent.createFileSymbol("SPI_DEF", None)
    spiSystemDefFile.setType("STRING")
    spiSystemDefFile.setOutputName("core.LIST_SYSTEM_DEFINITIONS_H_INCLUDES")
    spiSystemDefFile.setSourcePath("../peripheral/spi_01329/templates/system/definitions.h.ftl")
    spiSystemDefFile.setMarkup(True)
