"""*****************************************************************************
* Copyright (C) 2019 Microchip Technology Inc. and its subsidiaries.
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

print ("Loading System Services for " + Variables.get("__PROCESSOR"))

deviceFamily = coreComponent.createStringSymbol("DeviceFamily", devCfgMenu)
deviceFamily.setLabel("Device Family")
deviceFamily.setDefaultValue("SAM9X60")
deviceFamily.setReadOnly(True)
deviceFamily.setVisible(False)

cortexMenu = coreComponent.createMenuSymbol("CORTEX_MENU", None)
cortexMenu.setLabel("ARM 926 Configuration")
cortexMenu.setDescription("Configuration for ARM 926")

freeRTOSVectors = coreComponent.createBooleanSymbol("USE_FREERTOS_VECTORS", None)
freeRTOSVectors.setVisible(False)
freeRTOSVectors.setReadOnly(True)
freeRTOSVectors.setDefaultValue(False)

# load MMU
execfile(Variables.get("__CORE_DIR") + "/../peripheral/mmu_sam_9x60/config/mmu.py")

# load clock manager information
execfile(Variables.get("__CORE_DIR") + "/../peripheral/clk_sam_9x60/config/clk.py")

# load device specific pin manager information
execfile(Variables.get("__CORE_DIR") + "/../peripheral/pio_11004/config/pio.py")
coreComponent.addPlugin("../peripheral/pio_11004/plugin/pio_11004.jar")

# load AIC

# load dma manager information

# load wdt

armSysStartSourceFile = coreComponent.createFileSymbol(None, None)
armSysStartSourceFile.setSourcePath("arm/templates/iar/arm_926/SAM9X60/cstartup.s.ftl")
armSysStartSourceFile.setOutputName("cstartup.s")
armSysStartSourceFile.setMarkup(True)
armSysStartSourceFile.setOverwrite(True)
armSysStartSourceFile.setDestPath("")
armSysStartSourceFile.setProjectPath("config/" + configName + "/")
armSysStartSourceFile.setType("SOURCE")

#default exception handlers.
faultSourceFile = coreComponent.createFileSymbol(None, None)
faultSourceFile.setSourcePath("arm/templates/iar/arm_926/SAM9X60/vectortrap.s")
faultSourceFile.setOutputName("vectortrap.s")
faultSourceFile.setMarkup(False)
faultSourceFile.setOverwrite(True)
faultSourceFile.setDestPath("")
faultSourceFile.setProjectPath("config/" + configName + "/")
faultSourceFile.setType("SOURCE")

#linker file
linkerFile = coreComponent.createFileSymbol(None, None)
linkerFile.setSourcePath("arm/templates/iar/arm_926/SAM9X60/ddram.icf.ftl")
linkerFile.setOutputName("ddram.icf")
linkerFile.setMarkup(True)
linkerFile.setOverwrite(True)
linkerFile.setDestPath("")
linkerFile.setProjectPath("config/" + configName + "/")
linkerFile.setType("LINKER")
