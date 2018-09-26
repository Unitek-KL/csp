/*******************************************************************************
  Real Time Counter (${RTC_INSTANCE_NAME}) PLIB

  Company:
    Microchip Technology Inc.

  File Name:
    plib_${RTC_INSTANCE_NAME?lower_case}.h

  Summary:
    ${RTC_INSTANCE_NAME} PLIB Header file

  Description:
    This file defines the interface to the RTC peripheral library. This
    library provides access to and control of the associated peripheral
    instance.

*******************************************************************************/
// DOM-IGNORE-BEGIN
/*******************************************************************************
Copyright (c) 2017 released Microchip Technology Inc.  All rights reserved.

Microchip licenses to you the right to use, modify, copy and distribute
Software only when embedded on a Microchip microcontroller or digital signal
controller that is integrated into your product or third party product
(pursuant to the sublicense terms in the accompanying license agreement).

You should refer to the license agreement accompanying this Software for
additional information regarding your rights and obligations.

SOFTWARE AND DOCUMENTATION ARE PROVIDED AS IS  WITHOUT  WARRANTY  OF  ANY  KIND,
EITHER EXPRESS  OR  IMPLIED,  INCLUDING  WITHOUT  LIMITATION,  ANY  WARRANTY  OF
MERCHANTABILITY, TITLE, NON-INFRINGEMENT AND FITNESS FOR A  PARTICULAR  PURPOSE.
IN NO EVENT SHALL MICROCHIP OR  ITS  LICENSORS  BE  LIABLE  OR  OBLIGATED  UNDER
CONTRACT, NEGLIGENCE, STRICT LIABILITY, CONTRIBUTION,  BREACH  OF  WARRANTY,  OR
OTHER LEGAL  EQUITABLE  THEORY  ANY  DIRECT  OR  INDIRECT  DAMAGES  OR  EXPENSES
INCLUDING BUT NOT LIMITED TO ANY  INCIDENTAL,  SPECIAL,  INDIRECT,  PUNITIVE  OR
CONSEQUENTIAL DAMAGES, LOST  PROFITS  OR  LOST  DATA,  COST  OF  PROCUREMENT  OF
SUBSTITUTE  GOODS,  TECHNOLOGY,  SERVICES,  OR  ANY  CLAIMS  BY  THIRD   PARTIES
(INCLUDING BUT NOT LIMITED TO ANY DEFENSE  THEREOF),  OR  OTHER  SIMILAR  COSTS.
*******************************************************************************/
// DOM-IGNORE-END

#ifndef PLIB_${RTC_INSTANCE_NAME}_H
#define PLIB_${RTC_INSTANCE_NAME}_H

#include <stddef.h>
#include <stdbool.h>
#include <stdint.h>
<#if RTC_MODULE_SELECTION ="MODE2">
#include <time.h>
</#if>

// DOM-IGNORE-BEGIN
#ifdef __cplusplus // Provide C++ Compatibility
extern "C" {
#endif
// DOM-IGNORE-END

<#if RTC_MODULE_SELECTION = "MODE0">
    <#lt>/* Frequency of Counter Clock for RTC */
    <#if RTC_MODE0_PRESCALER = "0x0">
        <#lt>#define RTC_COUNTER_CLOCK_FREQUENCY         0
    <#else>
        <#lt>#define RTC_COUNTER_CLOCK_FREQUENCY        (${core.RTC_CLOCK_FREQUENCY} / (1 << (${RTC_MODE0_PRESCALER} - 1)))
    </#if>
<#elseif RTC_MODULE_SELECTION = "MODE1">
    <#lt>/* Frequency of Counter Clock for RTC */
    <#if RTC_MODE1_PRESCALER = "0x0">
        <#lt>#define RTC_COUNTER_CLOCK_FREQUENCY         0
    <#else>
        <#lt>#define RTC_COUNTER_CLOCK_FREQUENCY        (${core.RTC_CLOCK_FREQUENCY} / (1 << (${RTC_MODE1_PRESCALER} - 1)))
    </#if>
</#if>

<#if RTC_MODE2_INTERRUPT = true && RTC_MODULE_SELECTION = "MODE2" ||
     RTC_MODE1_INTERRUPT = true && RTC_MODULE_SELECTION = "MODE1" ||
     RTC_MODE0_INTERRUPT = true && RTC_MODULE_SELECTION = "MODE0" >
    <#if RTC_MODULE_SELECTION = "MODE2">
        <#lt>typedef enum
        <#lt>{
        <#lt>    RTC_ALARM_MASK_SS = 0x1,    //Alarm every minute
        <#lt>    RTC_ALARM_MASK_MMSS,        //Alarm every Hour
        <#lt>    RTC_ALARM_MASK_HHMMSS,      //Alarm Every Day
        <#lt>    RTC_ALARM_MASK_DDHHMMSS,    //Alarm Every Month
        <#lt>    RTC_ALARM_MASK_MMDDHHMMSS,  //Alarm Every year
        <#lt>    RTC_ALARM_MASK_YYMMDDHHMMSS //Alarm Once
        <#lt>} RTC_ALARM_MASK;

        <#lt>typedef enum
        <#lt>{
        <#lt>    RTC_CLOCK_INT_MASK_ALARM = 0x0100,
        <#lt>    RTC_CLOCK_INT_MASK_YEAR_OVERFLOW = 0x8000,
        <#lt>    RTC_CLOCK_INT_MASK_PER0 = 0x0001,
        <#lt>    RTC_CLOCK_INT_MASK_PER1 = 0x0002,
        <#lt>    RTC_CLOCK_INT_MASK_PER2 = 0x0004,
        <#lt>    RTC_CLOCK_INT_MASK_PER3 = 0x0008,
        <#lt>    RTC_CLOCK_INT_MASK_PER4 = 0x0010,
        <#lt>    RTC_CLOCK_INT_MASK_PER5 = 0x0020,
        <#lt>    RTC_CLOCK_INT_MASK_PER6 = 0x0040,
        <#lt>    RTC_CLOCK_INT_MASK_PER7 = 0x0080
        <#lt>} RTC_CLOCK_INT_MASK;
        
    <#elseif RTC_MODULE_SELECTION = "MODE0">
        <#lt>typedef enum
        <#lt>{
        <#lt>    RTC_TIMER32_INT_MASK_COMPARE_MATCH = 0x0100, 
        <#lt>    RTC_TIMER32_INT_MASK_COUNTER_OVERFLOW = 0x8000,
        <#lt>    RTC_TIMER32_INT_MASK_PER0 = 0x0001,
        <#lt>    RTC_TIMER32_INT_MASK_PER1 = 0x0002,
        <#lt>    RTC_TIMER32_INT_MASK_PER2 = 0x0004,
        <#lt>    RTC_TIMER32_INT_MASK_PER3 = 0x0008,
        <#lt>    RTC_TIMER32_INT_MASK_PER4 = 0x0010,
        <#lt>    RTC_TIMER32_INT_MASK_PER5 = 0x0020,
        <#lt>    RTC_TIMER32_INT_MASK_PER6 = 0x0040,
        <#lt>    RTC_TIMER32_INT_MASK_PER7 = 0x0080
        <#lt>} RTC_TIMER32_INT_MASK;
    <#else>
        <#lt>typedef enum
        <#lt>{
        <#lt>    RTC_TIMER16_INT_MASK_COMPARE0_MATCH = 0x0100,
        <#lt>    RTC_TIMER16_INT_MASK_COMPARE1_MATCH = 0x0200,
        <#lt>    RTC_TIMER16_INT_MASK_PERIOD_MATCH = 0x8000,
        <#lt>    RTC_TIMER16_INT_MASK_PER0 = 0x0001,
        <#lt>    RTC_TIMER16_INT_MASK_PER1 = 0x0002,
        <#lt>    RTC_TIMER16_INT_MASK_PER2 = 0x0004,
        <#lt>    RTC_TIMER16_INT_MASK_PER3 = 0x0008,
        <#lt>    RTC_TIMER16_INT_MASK_PER4 = 0x0010,
        <#lt>    RTC_TIMER16_INT_MASK_PER5 = 0x0020,
        <#lt>    RTC_TIMER16_INT_MASK_PER6 = 0x0040,
        <#lt>    RTC_TIMER16_INT_MASK_PER7 = 0x0080
        <#lt>} RTC_TIMER16_INT_MASK;
    </#if>    
    <#else>
        <#lt>typedef enum
        <#lt>{
        <#lt>    RTC_PER0_MASK = 0x0001,
        <#lt>    RTC_PER1_MASK = 0x0002,
        <#lt>    RTC_PER2_MASK = 0x0004,
        <#lt>    RTC_PER3_MASK = 0x0008,
        <#lt>    RTC_PER4_MASK = 0x0010,
        <#lt>    RTC_PER5_MASK = 0x0020,
        <#lt>    RTC_PER6_MASK = 0x0040,
        <#lt>    RTC_PER7_MASK = 0x0080
        <#lt>} RTC_PERIODIC_INT_MASK;        
</#if>



<#if RTC_MODE2_INTERRUPT = true && RTC_MODULE_SELECTION = "MODE2" ||
     RTC_MODE1_INTERRUPT = true && RTC_MODULE_SELECTION = "MODE1" ||
     RTC_MODE0_INTERRUPT = true && RTC_MODULE_SELECTION = "MODE0" >
    <#if RTC_MODULE_SELECTION = "MODE0" >
        <#lt>typedef void (*RTC_TIMER32_CALLBACK)( RTC_TIMER32_INT_MASK intCause, uintptr_t context );
    <#elseif RTC_MODULE_SELECTION = "MODE2">
        <#lt>typedef void (*RTC_CALLBACK)( RTC_CLOCK_INT_MASK intCause, uintptr_t context );
    <#else>
        <#lt>typedef void (*RTC_TIMER16_CALLBACK)( RTC_TIMER16_INT_MASK intCause, uintptr_t context );
    </#if>
</#if>

<#if ( RTC_MODE0_INTERRUPT = true && RTC_MODULE_SELECTION = "MODE0" ) ||
     ( RTC_MODE1_INTERRUPT = true && RTC_MODULE_SELECTION = "MODE1" ) ||
     ( RTC_MODE2_INTERRUPT = true && RTC_MODULE_SELECTION = "MODE2" )>

typedef struct
{
<#if RTC_MODULE_SELECTION = "MODE0" >
    /* Timer 32Bit */
    RTC_TIMER32_CALLBACK timer32BitCallback;
    RTC_TIMER32_INT_MASK timer32intCause;
<#elseif RTC_MODULE_SELECTION = "MODE1">
    /* Timer 16Bit */
    RTC_TIMER16_CALLBACK timer16BitCallback;
    RTC_TIMER16_INT_MASK timer16intCause;
<#else>
    /* RTC Clock*/
    RTC_CLOCK_INT_MASK intCause;
    RTC_CALLBACK alarmCallback;
</#if>
    uintptr_t context;
} RTC_OBJECT;
</#if>

void ${RTC_INSTANCE_NAME}_Initialize(void);
<#if RTC_FREQCORR>
    <#lt>void ${RTC_INSTANCE_NAME}_FrequencyCorrect (int8_t correction);
</#if>
<#if RTC_MODE0_INTERRUPT = false && RTC_MODULE_SELECTION = "MODE0" ||
     RTC_MODE1_INTERRUPT = false && RTC_MODULE_SELECTION = "MODE1" >
    <#lt>bool ${RTC_INSTANCE_NAME}_PeriodicIntervalHasCompleted (RTC_PERIODIC_INT_MASK period);
</#if>
<#if RTC_MODULE_SELECTION = "MODE0">
    <#if RTC_MODE0_INTERRUPT = false>
        <#lt>bool ${RTC_INSTANCE_NAME}_Timer32CounterHasOverflowed ( void );
        <#lt>bool ${RTC_INSTANCE_NAME}_Timer32CompareHasMatched(void);
    </#if>
    <#lt>void ${RTC_INSTANCE_NAME}_Timer32Start ( void );
    <#lt>void ${RTC_INSTANCE_NAME}_Timer32Stop ( void );
    <#lt>void ${RTC_INSTANCE_NAME}_Timer32CounterSet ( uint32_t count );
    <#lt>uint32_t ${RTC_INSTANCE_NAME}_Timer32CounterGet ( void );
    <#lt>uint32_t ${RTC_INSTANCE_NAME}_Timer32FrequencyGet ( void );
    <#lt>void ${RTC_INSTANCE_NAME}_Timer32CompareSet ( uint32_t compareValue );
    <#lt>uint32_t ${RTC_INSTANCE_NAME}_Timer32PeriodGet ( void );
    <#if RTC_MODE0_INTERRUPT = true>
        <#lt>void ${RTC_INSTANCE_NAME}_Timer32InterruptEnable(RTC_TIMER32_INT_MASK interrupt);
        <#lt>void ${RTC_INSTANCE_NAME}_Timer32InterruptDisable(RTC_TIMER32_INT_MASK interrupt);
    </#if>
<#elseif RTC_MODULE_SELECTION = "MODE1">
    <#if RTC_MODE1_INTERRUPT = false>
        <#lt>bool ${RTC_INSTANCE_NAME}_Timer16PeriodHasExpired ( void );
        <#lt>bool ${RTC_INSTANCE_NAME}_Timer16CounterHasOverflowed ( void );
        <#lt>bool ${RTC_INSTANCE_NAME}_Timer16Compare0HasMatched(void);
        <#lt>bool ${RTC_INSTANCE_NAME}_Timer16Compare1HasMatched(void);
    </#if>
    <#lt>void ${RTC_INSTANCE_NAME}_Timer16Start ( void );
    <#lt>void ${RTC_INSTANCE_NAME}_Timer16Stop ( void );
    <#lt>void ${RTC_INSTANCE_NAME}_Timer16CounterSet ( uint16_t count );
    <#lt>void ${RTC_INSTANCE_NAME}_Timer16PeriodSet ( uint16_t period );
    <#lt>uint16_t ${RTC_INSTANCE_NAME}_Timer16PeriodGet ( void );
    <#lt>uint16_t ${RTC_INSTANCE_NAME}_Timer16CounterGet ( void );
    <#lt>uint32_t ${RTC_INSTANCE_NAME}_Timer16FrequencyGet ( void );
    <#lt>void ${RTC_INSTANCE_NAME}_Timer16Compare0Set ( uint16_t comparisionValue );
    <#lt>void ${RTC_INSTANCE_NAME}_Timer16Compare1Set ( uint16_t comparisionValue );
    <#if RTC_MODE1_INTERRUPT = true>
        <#lt>void ${RTC_INSTANCE_NAME}_Timer16InterruptEnable(RTC_TIMER16_INT_MASK interrupt);
        <#lt>void ${RTC_INSTANCE_NAME}_Timer16InterruptDisable(RTC_TIMER16_INT_MASK interrupt);
    </#if>
<#else>
    <#lt>void ${RTC_INSTANCE_NAME}_RTCCTimeSet (struct tm * initialTime );
    <#lt>void ${RTC_INSTANCE_NAME}_RTCCTimeGet ( struct tm * currentTime );
    <#if RTC_MODE2_INTERRUPT = true>
        <#lt>void ${RTC_INSTANCE_NAME}_RTCCAlarmSet (struct tm * alarmTime, RTC_ALARM_MASK mask);
    </#if>
</#if>

<#if (RTC_MODULE_SELECTION = "MODE0" && RTC_MODE0_INTERRUPT = true) ||
     (RTC_MODULE_SELECTION = "MODE1" && RTC_MODE1_INTERRUPT = true) ||
     (RTC_MODULE_SELECTION = "MODE2" && RTC_MODE2_INTERRUPT = true) >
    <#if RTC_MODULE_SELECTION = "MODE2">
        <#lt>void ${RTC_INSTANCE_NAME}_RTCCCallbackRegister ( RTC_CALLBACK callback, uintptr_t context);
    <#elseif RTC_MODULE_SELECTION = "MODE0">
        <#lt>void ${RTC_INSTANCE_NAME}_Timer32CallbackRegister ( RTC_TIMER32_CALLBACK callback, uintptr_t context );
    <#else>
        <#lt>void ${RTC_INSTANCE_NAME}_Timer16CallbackRegister ( RTC_TIMER16_CALLBACK callback, uintptr_t context );
    </#if>
</#if>

// DOM-IGNORE-BEGIN
#ifdef __cplusplus  // Provide C++ Compatibility
}
#endif
// DOM-IGNORE-END

#endif /* PLIB_${RTC_INSTANCE_NAME}_H */
