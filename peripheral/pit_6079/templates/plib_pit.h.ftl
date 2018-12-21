/*******************************************************************************
  Periodic Interval Timer (${PIT_INSTANCE_NAME}) 

  Company:
    Microchip Technology Inc.

  File Name:
    plib_${PIT_INSTANCE_NAME?lower_case}.h

  Summary:
    Periodic Interval Timer (${PIT_INSTANCE_NAME}) PLIB.

  Description:
    This file declares the interface for the Periodic Interval Timer (${PIT_INSTANCE_NAME}).
*******************************************************************************/

// DOM-IGNORE-BEGIN
/*******************************************************************************
Copyright (c) 2018 released Microchip Technology Inc.  All rights reserved.

Microchip licenses to you the right to use, modify, copy and distribute
Software only when embedded on a Microchip microcontroller or digital signal
controller that is integrated into your product or third party product
(pursuant to the sublicense terms in the accompanying license agreement).

You should refer to the license agreement accompanying this Software for
additional information regarding your rights and obligations.

SOFTWARE AND DOCUMENTATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND,
EITHER EXPRESS OR IMPLIED, INCLUDING WITHOUT LIMITATION, ANY WARRANTY OF
MERCHANTABILITY, TITLE, NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.
IN NO EVENT SHALL MICROCHIP OR ITS LICENSORS BE LIABLE OR OBLIGATED UNDER
CONTRACT, NEGLIGENCE, STRICT LIABILITY, CONTRIBUTION, BREACH OF WARRANTY, OR
OTHER LEGAL EQUITABLE THEORY ANY DIRECT OR INDIRECT DAMAGES OR EXPENSES
INCLUDING BUT NOT LIMITED TO ANY INCIDENTAL, SPECIAL, INDIRECT, PUNITIVE OR
CONSEQUENTIAL DAMAGES, LOST PROFITS OR LOST DATA, COST OF PROCUREMENT OF
SUBSTITUTE GOODS, TECHNOLOGY, SERVICES, OR ANY CLAIMS BY THIRD PARTIES
(INCLUDING BUT NOT LIMITED TO ANY DEFENSE THEREOF), OR OTHER SIMILAR COSTS.
*******************************************************************************/
// DOM-IGNORE-END

#ifndef _PLIB_${PIT_INSTANCE_NAME}_H
#define _PLIB_${PIT_INSTANCE_NAME}_H


// *****************************************************************************
// *****************************************************************************
// Section: Included Files
// *****************************************************************************
// *****************************************************************************
#include <stdbool.h>
#include <stdint.h>

#ifdef __cplusplus  // Provide C++ Compatibility

    extern "C" {

#endif

// *****************************************************************************
// *****************************************************************************
// Section: Data Types
// *****************************************************************************

<#if ENABLE_INTERRUPT == true>
// *****************************************************************************
/* ${PIT_INSTANCE_NAME} Interrupt Callback Function definition.

  Summary:
    ${PIT_INSTANCE_NAME} Interrupt Callback Function definition.

  Description:
    Defines the function signature for the ${PIT_INSTANCE_NAME} interrupt callback.

*/

typedef void (*${PIT_INSTANCE_NAME}_CALLBACK)(uintptr_t context);
</#if>

// *****************************************************************************
// *****************************************************************************
// Section: Interface Routines
// *****************************************************************************
// *****************************************************************************

// *****************************************************************************
/* Function:
   void ${PIT_INSTANCE_NAME}_TimerInitialize(void);

  Summary:
    Initialize ${PIT_INSTANCE_NAME} registers per user config.

  Description:
    Initalize the period and, if configured, enable the counter and interrupt.

  Precondition:
    None.

  Parameters:
    None.
  
  Returns:
    None.
*/
void ${PIT_INSTANCE_NAME}_TimerInitialize(void);

// *****************************************************************************
/* Function:
    void ${PIT_INSTANCE_NAME}_TimerRestart(void);

  Summary:
   Restart the ${PIT_INSTANCE_NAME} counter.

  Description:
    Signal the ${PIT_INSTANCE_NAME} counter to stop, wait for it to stop, then restart the counter.

  Precondition:
    None.

  Parameters:
    None.
  
  Returns:
    None.
*/
void ${PIT_INSTANCE_NAME}_TimerRestart(void);

// *****************************************************************************
/* Function:
    void ${PIT_INSTANCE_NAME}_TimerStart(void);

  Summary:
   Start the ${PIT_INSTANCE_NAME} counter.

  Description:
    Start the ${PIT_INSTANCE_NAME} counter.  If interrupts are enabled an interrupt will occur
    every time the PIV value is reached.

  Precondition:
    None.

  Parameters:
    None.
  
  Returns:
    None.
*/
void ${PIT_INSTANCE_NAME}_TimerStart(void);

// *****************************************************************************
/* Function:
    void ${PIT_INSTANCE_NAME}_TimerStop(void);

  Summary:
   Stop the ${PIT_INSTANCE_NAME} counter.

  Description:
    Stop the ${PIT_INSTANCE_NAME} counter.

  Precondition:
    None.

  Parameters:
    None.
  
  Returns:
    None.
*/
void ${PIT_INSTANCE_NAME}_TimerStop(void);

// *****************************************************************************
/* Function:
   void ${PIT_INSTANCE_NAME}_TimerPeriodSet(uint32_t period);

  Summary:
   Set the timer period value.

  Description:
    Set the timer period value by programming the PIV field in the MR register.

  Precondition:
    None.

  Parameters:
   period       - The period (PIV) value of the ${PIT_INSTANCE_NAME}. 
  
  Returns:
    None.
*/
void ${PIT_INSTANCE_NAME}_TimerPeriodSet(uint32_t period);

// *****************************************************************************
/* Function:
    uint32_t ${PIT_INSTANCE_NAME}_TimerPeriodGet(void);

  Summary:
   Get the timer period value.

  Description:
    Return the current PIV value of the ${PIT_INSTANCE_NAME}.

  Precondition:
    None.

  Parameters:
    None.
  
  Returns:
    None.
*/
uint32_t ${PIT_INSTANCE_NAME}_TimerPeriodGet(void);

// *****************************************************************************
/* Function:
    uint32_t ${PIT_INSTANCE_NAME}_TimerCounterGet(void);

  Summary:
   Get the timer counter value.

  Description:
    Return the current counter (CPIV) value of the ${PIT_INSTANCE_NAME}.

  Precondition:
    None.

  Parameters:
    None.
  
  Returns:
    None.
*/
uint32_t ${PIT_INSTANCE_NAME}_TimerCounterGet(void);


// *****************************************************************************
/* Function:
    void ${PIT_INSTANCE_NAME}_TimerCompareSet(void);

  Summary:
   Set the timer comparison value.

  Description:
    Provide a future PIT count value for comparison purposes.  When PIT timer
    counter is greater than or equal to the value an event will be created.

  Precondition:
    None.

  Parameters:
    None.
  
  Returns:
    None.
*/
void ${PIT_INSTANCE_NAME}_TimerCompareSet( uint16_t compare );


// *****************************************************************************
/* Function:
    uint32_t ${PIT_INSTANCE_NAME}_TimerFrequencyGet(void);

  Summary:
    Get the timer clock frequency.

  Description:
    Return the clock frequency of the ${PIT_INSTANCE_NAME}.

  Precondition:
    None.

  Parameters:
    None.
  
  Returns:
    None.
*/
uint32_t ${PIT_INSTANCE_NAME}_TimerFrequencyGet(void);

<#if ENABLE_INTERRUPT == false>
// *****************************************************************************
/* Function:
    bool ${PIT_INSTANCE_NAME}_TimerPeriodHasExpired(void);

  Summary:
    Return whether or not the Timer Period has expired.

  Description:
    Check the ${PIT_INSTANCE_NAME} Status register to determine if period has expired.

  Precondition:
    None.

  Parameters:
    None.
  
  Returns:
    True    - Indicates period has expired
    False   - Indicates period has not expired
*/
bool ${PIT_INSTANCE_NAME}_TimerPeriodHasExpired(void);
<#elseif ENABLE_INTERRUPT == true>
// *****************************************************************************
/* Function:
    void ${PIT_INSTANCE_NAME}_DelayMs(uint32_t ms);

  Summary:
    Delays processing for x milliseconds.

  Description:
    Delays execution by using  the ${PIT_INSTANCE_NAME} timer to determine when given number of
    milliseconds has expired.  

  Precondition:
    ${PIT_INSTANCE_NAME} is configured and enabled.  The ${PIT_INSTANCE_NAME} interrupt is also enabled.

  Parameters:
    ms      - number of milliseconds to delay
  
  Returns:
    None.
*/
void ${PIT_INSTANCE_NAME}_DelayMs(uint32_t ms);

// *****************************************************************************
/* Function:
    void ${PIT_INSTANCE_NAME}_TimerCallbackSet(${PIT_INSTANCE_NAME}_CALLBACK callback, uintptr_t context);

  Summary:
    Register callback for ${PIT_INSTANCE_NAME} interrupt.

  Description:
    When the timer interrupt occurs the given callback will called with the
    given context.

  Precondition:
    None.

  Parameters:
    callback    - Callback function
    context     - paramter to callback function
  
  Returns:
    None.
*/
void ${PIT_INSTANCE_NAME}_TimerCallbackSet(${PIT_INSTANCE_NAME}_CALLBACK callback, uintptr_t context);

// *****************************************************************************
/* Function:
    void ${PIT_INSTANCE_NAME}_InterruptHandler(void);

  Summary:
    ${PIT_INSTANCE_NAME} Interrupt Handler.

  Description:
    Internal ${PIT_INSTANCE_NAME} interrupt handler called by interrupt controller.

  Precondition:
    None.

  Parameters:
    None.
  
  Returns:
    None.
*/
void ${PIT_INSTANCE_NAME}_InterruptHandler(void);
</#if>

#ifdef __cplusplus  // Provide C++ Compatibility

    }

#endif

#endif

/*******************************************************************************
 End of File
*/
