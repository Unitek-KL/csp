from os.path import join
Log.writeInfoMessage( "Loading Interrupt Manager for " + Variables.get( "__PROCESSOR" ) )

################################################################################
#### Public Globals -- variables used in this module and accessible from other files
################################################################################
global getInterruptName

global interruptNamespace
global interruptSymbolEnable
global interruptSymbolHandler
global interruptSymbolHandlerLock

global interruptLastNameEnable 
global interruptLastNameHandler 
global interruptLastNameLock 

interruptNamespace =        "core"
interruptLastNameEnable =   "_INTERRUPT_ENABLE"
interruptLastNameHandler =  "_INTERRUPT_HANDLER"
interruptLastNameLock =     "_INTERRUPT_HANDLER_LOCK"

################################################################################
global numSharedVectors
global sharedVectors
global subVectorToSharedVector

numSharedVectors = 0
sharedVectors = {}
subVectorToSharedVector = {}

################################################################################
#### Static Globals -- variables intended to be used inside this file only
################################################################################
# not currently public
global interruptsChildren
global interruptLastNameMapType
global interruptLastNameVector
global interruptLastNameSrcType
global interruptLastNamePriority
global aicPriorityChoices
global aicSrcTypes
global aicMinPriorityName
global aicMaxPriorityName

interruptLastNameMapType =  "_INTERRUPT_MAP_TYPE"
interruptLastNameVector =   "_INTERRUPT_VECTOR"
interruptLastNameSrcType =  "_INTERRUPT_SRC_TYPE"
interruptLastNamePriority = "_INTERRUPT_PRIORITY"

interruptsChildren = ATDF.getNode( "/avr-tools-device-file/devices/device/interrupts" ).getChildren()

aicCodeGenerationDependencies = []
aicPriorityChoices =        []
aicSrcTypes =               []
aicMinPriorityName =        ""
aicMaxPriorityName =        ""
neverSecureList =           [ '49', '62' ]
alwaysSecureList =          [  '0', '14', '15', '16', '18', '51', '61', '68', '69', '70' ]
programmedSecureList =      []                                                                      # Todo create map interface to populate this list
internalList =              [  '0',  '2', '49', '56', '57', '64', '65', '66', '67', '71', '72' ]

################################################################################
#### Global Methods
################################################################################
def getInterruptName( interruptNode ):
    if "header:alternate-name" in interruptNode.getAttributeList():
        retval = interruptNode.getAttribute( "header:alternate-name" )
    else:
        retval = interruptNode.getAttribute( "name" )
    return( str( retval ) )

################################################################################
#### Local Methods
################################################################################
def getInterruptDescription( interruptNode ):
    if "header:alternate-caption" in interruptNode.getAttributeList():
        retval = interruptNode.getAttribute( "header:alternate-caption" )
    else:
        retval = interruptNode.getAttribute( "caption" )
    return( str( retval ) )


def getNameValueCaptionTuple( aGroupName, aTupleArray ):
    choiceNode = ATDF.getNode("/avr-tools-device-file/modules/module@[name=\"AIC\"]/value-group@[name=\"" + aGroupName + "\"]")
    if not choiceNode:
        choiceValues = []
    else:
        choiceValues = choiceNode.getChildren()
    for ii in range( 0, len( choiceValues ) ):
        aTupleArray.append( ( choiceValues[ ii ].getAttribute("name"), 
                             choiceValues[ ii ].getAttribute("value"),
                             choiceValues[ ii ].getAttribute("caption")
                             ) )

        
def getTupleNameContaining( aTupleArray, aString ):
    tupleName = aTupleArray[ 0 ][ 0 ]
    aString = aString.upper()
    for tuple in aTupleArray:
        if( aString in tuple[ 0 ].upper() ):
            tupleName = tuple[ 0 ]
            break
    return tupleName

       
def aicMapTypeRedirectionCallback( aicMapType, eventDictionary ):
    if( True == eventDictionary[ "value" ] ):
        # Mapping Secure to NonSecure
        if(     ("AlwaysSecure" == aicMapType.getDefaultValue())
            or  ("Secure" == aicMapType.getDefaultValue())
        ):
            aicMapType.setValue( "RedirectedToNonSecure", 1 )   # make change evident for user
    else:
        if(     ("AlwaysSecure" == aicMapType.getDefaultValue())
            or  ("Secure" == aicMapType.getDefaultValue())
        ):
            aicMapType.clearValue()                             # restore the default value


def priorityMapTypeCallback( aicVectorPriority, eventDictionary ):
    global aicMaxPriorityName
    if(     ("AlwaysSecure" == eventDictionary[ "value" ]) 
        or  ("Secure" == eventDictionary[ "value" ]) 
    ):
        aicVectorPriority.setSelectedKey( aicMaxPriorityName, 0 )
        aicVectorPriority.setVisible( False )
    else:
        aicVectorPriority.setVisible( True )
    

def aicCodeGenerationCallback( aicCodeGeneration, eventDictionary ):
    global interruptLastNameEnable 
    # Interrupt enables and map type determine the code generation to be done later
    secureCount = 0
    nonSecureCount = 0
    for interrupt in interruptsChildren:
        interruptName = getInterruptName( interrupt )
        component = aicCodeGeneration.getComponent()
        enableSymbol = component.getSymbolByID( interruptName + interruptLastNameEnable )
        if( enableSymbol.getValue() ):
            mapTypeSymbol = component.getSymbolByID( interruptName + interruptLastNameMapType )
            if(     ("NeverSecure" == mapTypeSymbol.value) 
                or  ("NonSecure" == mapTypeSymbol.value) 
                or  ("RedirectedToNonSecure" == mapTypeSymbol.value)
            ):
                nonSecureCount = nonSecureCount + 1
            else:
                secureCount = secureCount + 1
    if secureCount and nonSecureCount:
        aicCodeGeneration.setValue( "AICandSAIC", 0xFF )
    elif nonSecureCount:
        aicCodeGeneration.setValue( "AIC", 0xFF )
    elif secureCount:
        aicCodeGeneration.setValue( "SAIC", 0xFF )
    else:
        aicCodeGeneration.setValue( "NONE", 0xFF )


global aicVectorEnableCallback
def aicVectorEnableCallback( aicVectorEnable, eventDictionary ):
    global sharedVectors

    desiredValue = eventDictionary[ "value" ]
    interrupt = eventDictionary[ "id" ].replace( interruptLastNameLock, "" ).replace( interruptLastNameEnable, "" )
    aicVectorEnable.setReadOnly( True )
    if aicVectorEnable.getDefaultValue() == desiredValue:
        aicVectorEnable.clearValue()
    else:
        aicVectorEnable.setValue( desiredValue, 1 )
    aicVectorEnable.setReadOnly( False )

    sharedInterrupt = subVectorToSharedVector.get( interrupt )
    if( sharedInterrupt ):
            # check if any sibling is enabled
            component = aicVectorEnable.getComponent()
            desiredValue = False
            for elem in sharedVectors[ sharedInterrupt ]:
                vectorEnable = component.getSymbolByID( elem + interruptLastNameEnable )
                if vectorEnable and vectorEnable.getValue():
                    desiredValue = True

            aicVectorEnable = component.getSymbolByID( sharedInterrupt + interruptLastNameEnable )
            aicVectorEnable.setValue( desiredValue, 1 )


def setupEnableAndHandler( component, anInterrupt, aicVectorEnable, aicVectorHandler ):
    global sharedVectors

    enableDependencies = []
    interruptName = getInterruptName( anInterrupt )
    moduleInstance = anInterrupt.getAttribute( "module-instance" ).split()
    sharedVectorMaxShares = len( moduleInstance )
    if 1 < sharedVectorMaxShares:
        aicVectorHandler.setReadOnly( True )
        aicVectorHandler.setValue( interruptName + "_SharedHandler", 0 )
        aicVectorHandler.setReadOnly( False )
        sharedVectors[ interruptName ] = moduleInstance
        aicVectorHandler.setVisible( False )

        for elem in moduleInstance:
            subVectorToSharedVector[ elem ] = interruptName
            subVectorEnable = component.createBooleanSymbol( elem + interruptLastNameEnable, aicVectorEnable )
            subVectorEnable.setLabel( "Enable " + elem )
            subVectorEnable.setDefaultValue( False )
            subVectorEnable.setDependencies( aicVectorEnableCallback, [elem + interruptLastNameLock] )
            enableDependencies.append( elem + interruptLastNameEnable )     # Parent enable depends on children

            subVectorHandlerLock = component.createBooleanSymbol( elem + interruptLastNameLock, subVectorEnable )
            subVectorHandlerLock.setDefaultValue( False )
            subVectorHandlerLock.setVisible( False )
            
            subVectorHandler = component.createStringSymbol( elem + interruptLastNameHandler, subVectorEnable )
            subVectorHandler.setLabel( elem + " Handler" )
            subVectorHandler.setDefaultValue( elem + "_Handler" )

    enableDependencies.append( interruptName + interruptLastNameLock )
    aicVectorEnable.setDependencies( aicVectorEnableCallback, enableDependencies )


def setupSharedVectorFtlSymbols( component, anInterrupt, aicVectorEnable ):
    global numSharedVectors

    interruptName = getInterruptName( anInterrupt )
    moduleInstance = anInterrupt.getAttribute( "module-instance" ).split()
    numShares = len( moduleInstance )
    if 1 < numShares:
        numSharedVectors = numSharedVectors + 1
        # SHARED_VECTOR_N = "name", e.g. SHARED_VECTOR_1 = "SYSC"
        # Create a generic shared handler symbol with a value indicating the HANDLER 
        Database.clearSymbolValue( "core", interruptName + "SHARED_VECTOR_" + str( numSharedVectors - 1 ) )
        sharedVector = component.createStringSymbol( "SHARED_VECTOR_" + str( numSharedVectors - 1 ), aicVectorEnable )
        sharedVector.setDefaultValue( interruptName )
        sharedVector.setVisible( False )
        
        Database.clearSymbolValue( "core", interruptName + "_NUM_SHARES" )
        sharedVectorNumShares = component.createIntegerSymbol( interruptName + "_NUM_SHARES", sharedVector )
        sharedVectorNumShares.setValue( numShares, 0 )
        sharedVectorNumShares.setVisible( False )
        # Create symbols for the shared handler names 
        # {SHARED_VECTOR_#}_HANDLER_#, e.g.
        #    SYSC_HANDLER_0 = "PMC"    ==> PMC_InterruptHandler
        #    SYSC_HANDLER_1 = "RSTC"   ==> RSTC_InterruptHandler
        #    SYSC_HANDLER_2 = "RTC"    ==> RTC_InterruptHandler
        ii = 0
        for elem in moduleInstance:
            shareName = component.createStringSymbol( interruptName + "_SHARE_" + str( ii ), aicVectorEnable )
            shareName.setDefaultValue( elem )
            shareName.setVisible( False )
            ii = ii + 1


################################################################################
#### Component
################################################################################
getNameValueCaptionTuple( "AIC_SMR__PRIORITY", aicPriorityChoices )
getNameValueCaptionTuple( "AIC_SMR__SRCTYPE", aicSrcTypes )

aicMinPriorityName = getTupleNameContaining( aicPriorityChoices, "min" )
aicMaxPriorityName = getTupleNameContaining( aicPriorityChoices, "max" )

aicMenu = coreComponent.createMenuSymbol( "AIC_MENU", cortexMenu )
aicMenu.setLabel( "Interrupts (AIC/SAIC)" )
aicMenu.setDescription( "Configuration for AIC Initialization" )

### Symbol for interrupt redirection decision
aicRedirection = coreComponent.createBooleanSymbol( "SECURE_TO_NONSECURE_REDIRECTION", aicMenu )
aicRedirection.setLabel( "Secure to NonSecure Redirection" )
aicRedirection.setDefaultValue( True )

aicVectorMax = coreComponent.createIntegerSymbol( "AIC_VECTOR_MAX", aicMenu )
aicVectorMax.setDefaultValue( Interrupt.getMaxInterruptID() )
aicVectorMax.setVisible( False )

aicVectorMax = coreComponent.createIntegerSymbol( "AIC_VECTOR_MIN", aicMenu )
aicVectorMax.setDefaultValue( Interrupt.getMinInterruptID() )
aicVectorMax.setVisible( False )

for interrupt in interruptsChildren:
    interruptName = getInterruptName( interrupt )
    aicNumber = str( interrupt.getAttribute( "index" ) )

    if aicNumber in neverSecureList:            # secure to nonSecure redirection will have no effect
        mapTypeDefault = "NeverSecure"
    elif aicNumber in alwaysSecureList:         # secure to nonSecure redirection will disable and hide these
        mapTypeDefault = "AlwaysSecure"
    elif aicNumber in programmedSecureList:     # secure to nonSecure redirection will change mapType to 'RedirectedToNonSecure' and set highest priority
        mapTypeDefault = "Secure"
    else: # programmed nonSecure                # secure to nonSecure redirection will have no effect
        mapTypeDefault = "NonSecure"
    # only for use by the aic ftl code
    aicInterruptFirstName = coreComponent.createStringSymbol( "AIC_FIRST_NAME_KEY" + aicNumber, None )
    aicInterruptFirstName.setDefaultValue( interruptName )
    aicInterruptFirstName.setVisible( False )
    ###
    aicVectorEnable = coreComponent.createBooleanSymbol( interruptName + interruptLastNameEnable, aicMenu )
    aicVectorEnable.setLabel( "Enable " + aicNumber + " -- " + getInterruptDescription( interrupt ) )
    aicVectorEnable.setDefaultValue( False )
    ###
    aicVectorSourceGUILabel = coreComponent.createCommentSymbol( interruptName + "_INTERRUPT_VECTOR_LABEL", aicVectorEnable )
    aicVectorSourceGUILabel.setLabel( "Vector: " + interruptName + "_IRQn" )
    #This is the same as aicVectorSourceGUILabel but creates a .var assignment accessible in plib_aic.c.ftl
    aicVectorSource = coreComponent.createStringSymbol( interruptName + interruptLastNameVector, aicVectorEnable )
    aicVectorSource.setDefaultValue( interruptName + "_IRQn" )
    aicVectorSource.setVisible( False )
    ###
    aicVectorLock = coreComponent.createBooleanSymbol( interruptName + interruptLastNameLock, aicVectorEnable )
    aicVectorLock.setDefaultValue( False )
    aicVectorLock.setVisible( False )

    aicVectorHandler = coreComponent.createStringSymbol( interruptName + interruptLastNameHandler, aicVectorEnable )
    aicVectorHandler.setLabel( "Handler" )
    aicVectorHandler.setDefaultValue( interruptName + "_Handler" )
    ###
    setupEnableAndHandler( coreComponent, interrupt, aicVectorEnable, aicVectorHandler )
    setupSharedVectorFtlSymbols( coreComponent, interrupt, aicVectorEnable )
    #
    aicMapType = coreComponent.createStringSymbol( interruptName + interruptLastNameMapType, aicVectorEnable )
    aicMapType.setLabel( "Map Type" )
    aicMapType.setDefaultValue( mapTypeDefault )
    aicMapType.clearValue()
    aicMapType.setReadOnly( True )
    aicMapType.setDependencies( aicMapTypeRedirectionCallback, [ "SECURE_TO_NONSECURE_REDIRECTION" ] )
    
    aicVectorSourceType = coreComponent.createKeyValueSetSymbol( interruptName + interruptLastNameSrcType, aicVectorEnable )
    aicVectorSourceType.setLabel( "Source Type" )
    for tupleElem in aicSrcTypes:
        if (aicNumber in internalList) and ("internal" not in tupleElem[ 2 ]):
            continue
        aicVectorSourceType.addKey( tupleElem[ 0 ], tupleElem[ 1 ], tupleElem[ 2 ] )
    aicVectorSourceType.setOutputMode( "Key" )
    aicVectorSourceType.setDisplayMode( "Description" )
    aicVectorSourceType.setDefaultValue( 0 )
    aicVectorSourceType.setSelectedKey( str( aicSrcTypes[ 0 ][ 0 ] ), 0 )

    aicVectorPriority = coreComponent.createKeyValueSetSymbol( interruptName + interruptLastNamePriority, aicVectorEnable )
    aicVectorPriority.setLabel( "Priority" )
    for tupleElem in aicPriorityChoices:
        aicVectorPriority.addKey( tupleElem[ 0 ], tupleElem[ 1 ], tupleElem[ 2 ] )
    aicVectorPriority.setOutputMode( "Key" )
    aicVectorPriority.setDisplayMode( "Description" )
    aicVectorPriority.setDefaultValue( 0 )
    if( ("AlwaysSecure" == aicMapType.value) or ("Secure" == aicMapType.value) ):
        aicVectorPriority.setSelectedKey( aicMaxPriorityName, 0 )
        aicVectorPriority.setVisible( False )   # fiq interrupts do not have a priority, but if the get forced nonSecure we want a reasonable value
    else: 
        aicVectorPriority.setSelectedKey( aicMinPriorityName, 0 )
    aicVectorPriority.setDependencies( priorityMapTypeCallback, [ interruptName + interruptLastNameMapType ] )

    aicCodeGenerationDependencies.append( interruptName + interruptLastNameEnable )   # add to dependency list for code generation symbol
    aicCodeGenerationDependencies.append( interruptName + interruptLastNameMapType )  # add to dependency list for code generation symbol

###
Database.clearSymbolValue( "core", "NUM_SHARED_VECTORS" )
aicNumSharedVectors = coreComponent.createIntegerSymbol( "NUM_SHARED_VECTORS", aicMenu )
aicNumSharedVectors.setValue( numSharedVectors, 1 )
aicNumSharedVectors.setVisible( False )
### Symbol for code generation decisions
aicCodeGeneration = coreComponent.createComboSymbol( "AIC_CODE_GENERATION", aicMenu, [ "NONE", "AIC", "SAIC", "AICandSAIC" ] )
aicCodeGeneration.setDefaultValue( "NONE" )
aicCodeGeneration.setDependencies( aicCodeGenerationCallback, aicCodeGenerationDependencies )
aicCodeGeneration.setVisible( False )
###
aicRedirection.setValue( True, 0 )  # stimulate a aicMapTypeRedirectionCallback() by setting the aicRedirection value
aicRedirection.setReadOnly( True )

############################################################################
#### Code Generation
############################################################################
configName = Variables.get( "__CONFIGURATION_NAME" )

aicSystemDefFile = coreComponent.createFileSymbol( "SYSTEM_AIC_DEFINITIONS", None )
aicSystemDefFile.setType( "STRING" )
aicSystemDefFile.setSourcePath( "../peripheral/aic_11145/templates/system/system_definitions.h.ftl" )
aicSystemDefFile.setOutputName( "core.LIST_SYSTEM_DEFINITIONS_H_INCLUDES" )
aicSystemDefFile.setMarkup( True )

aicSystemInitFile = coreComponent.createFileSymbol( "SYS_AIC_INITIALIZE", None )
aicSystemInitFile.setType( "STRING" )
aicSystemInitFile.setSourcePath( "../peripheral/aic_11145/templates/system/system_initialize.c.ftl" )
aicSystemInitFile.setOutputName( "core.LIST_SYSTEM_INIT_C_SYS_INITIALIZE_PERIPHERALS" )
aicSystemInitFile.setMarkup( True )

aicSystemIntWeakHandleFile = coreComponent.createFileSymbol( "AIC_WEAK_HANDLERS", None )
aicSystemIntWeakHandleFile.setType( "STRING" )
aicSystemIntWeakHandleFile.setSourcePath( "../peripheral/aic_11145/templates/system/system_interrupt_weak_handlers.h.ftl" )
aicSystemIntWeakHandleFile.setOutputName( "core.LIST_SYSTEM_INTERRUPT_WEAK_HANDLERS" )
aicSystemIntWeakHandleFile.setMarkup( True )

aicSharedHandlerFile = coreComponent.createFileSymbol( "AIC_SHARED_HANDLERS", None )
aicSharedHandlerFile.setType( "STRING" )
aicSharedHandlerFile.setSourcePath( "../peripheral/aic_11145/templates/system/system_interrupt_shared_handlers.h.ftl" )
aicSharedHandlerFile.setOutputName( "core.LIST_SYSTEM_INTERRUPT_SHARED_HANDLERS" )
aicSharedHandlerFile.setMarkup( True )

aicSourceFile = coreComponent.createFileSymbol( "AIC_SOURCE", None )
aicSourceFile.setType( "SOURCE" )
aicSourceFile.setProjectPath( "config/" + configName + "/peripheral/aic/" )
aicSourceFile.setSourcePath( "../peripheral/aic_11145/templates/plib_aic.c.ftl" )
aicSourceFile.setDestPath( "/peripheral/aic/" )
aicSourceFile.setOutputName( "plib_aic.c" )
aicSourceFile.setMarkup( True )
aicSourceFile.setOverwrite( True )
aicSourceFile.setEnabled( True )

aicHeaderFile = coreComponent.createFileSymbol( "AIC_HEADER", None )
aicHeaderFile.setType( "HEADER" )
aicHeaderFile.setProjectPath( "config/" + configName + "/peripheral/aic/" )
aicHeaderFile.setSourcePath( "../peripheral/aic_11145/templates/plib_aic.h.ftl" )
aicHeaderFile.setDestPath( "/peripheral/aic/" )
aicHeaderFile.setOutputName( "plib_aic.h" )
aicHeaderFile.setMarkup( True )
aicHeaderFile.setOverwrite( True )
aicHeaderFile.setEnabled( True )
