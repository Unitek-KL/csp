/*******************************************************************************
  Interface definition of EVSYS PLIB.

  Company:
    Microchip Technology Inc.

  File Name:
    plib_${EVSYS_INSTANCE_NAME?lower_case}.h

  Summary:
    Interface definition of the Event System Plib (EVSYS).

  Description:
    This file defines the interface for the EVSYS Plib.
    It allows user to setup event generators and users.
*******************************************************************************/

/*******************************************************************************
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
*******************************************************************************/

#ifndef ${EVSYS_INSTANCE_NAME}_H    // Guards against multiple inclusion
#define ${EVSYS_INSTANCE_NAME}_H

#include "device.h"
#include <stdint.h>
#include <stddef.h>

#ifdef __cplusplus // Provide C++ Compatibility
 extern "C" {
#endif


// *****************************************************************************
// *****************************************************************************
// Section: Interface
// *****************************************************************************
// *****************************************************************************

<#if EVSYS_INTERRUPT_MODE == true>
	<#lt>typedef void (*EVSYS_CALLBACK)(uintptr_t context, uint32_t int_cause);
</#if>

<#if EVSYS_INTERRUPT_MODE == true>
	<#lt>typedef enum
	<#lt>{
	<#lt>	EVSYS_INT_OVERRUN0 = EVSYS_INTENSET_OVR0_Msk,
	<#lt>	EVSYS_INT_OVERRUN1 = EVSYS_INTENSET_OVR1_Msk,
	<#lt>	EVSYS_INT_OVERRUN2 = EVSYS_INTENSET_OVR2_Msk,
	<#lt>	EVSYS_INT_OVERRUN3 = EVSYS_INTENSET_OVR3_Msk,
	<#lt>	EVSYS_INT_OVERRUN4 = EVSYS_INTENSET_OVR4_Msk,
	<#lt>	EVSYS_INT_OVERRUN5 = EVSYS_INTENSET_OVR5_Msk,
	<#lt>	EVSYS_INT_OVERRUN6 = EVSYS_INTENSET_OVR6_Msk,
	<#lt>	EVSYS_INT_OVERRUN7 = EVSYS_INTENSET_OVR7_Msk,
	<#lt>	EVSYS_INT_OVERRUN8 = EVSYS_INTENSET_OVR8_Msk,
	<#lt>	EVSYS_INT_OVERRUN9 = EVSYS_INTENSET_OVR9_Msk,
	<#lt>	EVSYS_INT_OVERRUN10 = EVSYS_INTENSET_OVR10_Msk,
	<#lt>	EVSYS_INT_OVERRUN11 = EVSYS_INTENSET_OVR11_Msk,
	<#lt>	EVSYS_INT_EVENT0 = EVSYS_INTENSET_EVD0_Msk,
	<#lt>	EVSYS_INT_EVENT1 = EVSYS_INTENSET_EVD1_Msk,
	<#lt>	EVSYS_INT_EVENT2 = EVSYS_INTENSET_EVD2_Msk,
	<#lt>	EVSYS_INT_EVENT3 = EVSYS_INTENSET_EVD3_Msk,
	<#lt>	EVSYS_INT_EVENT4 = EVSYS_INTENSET_EVD4_Msk,
	<#lt>	EVSYS_INT_EVENT5 = EVSYS_INTENSET_EVD5_Msk,
	<#lt>	EVSYS_INT_EVENT6 = EVSYS_INTENSET_EVD6_Msk,
	<#lt>	EVSYS_INT_EVENT7 = EVSYS_INTENSET_EVD7_Msk,
	<#lt>	EVSYS_INT_EVENT8 = EVSYS_INTENSET_EVD8_Msk,
	<#lt>	EVSYS_INT_EVENT9 = EVSYS_INTENSET_EVD9_Msk,
	<#lt>	EVSYS_INT_EVENT10 = EVSYS_INTENSET_EVD10_Msk,
	<#lt>	EVSYS_INT_EVENT11 = EVSYS_INTENSET_EVD11_Msk
	<#lt>} EVSYS_INT_MASK;

	<#lt>typedef struct
	<#lt>{
	<#lt>	EVSYS_CALLBACK          callback;
	<#lt>	uintptr_t               context;
	<#lt>} EVSYS_OBJECT ;
</#if>
/***************************** EVSYS API *******************************/
void ${EVSYS_INSTANCE_NAME}_Initialize( void );
<#if EVSYS_INTERRUPT_MODE == true>
	<#lt>void ${EVSYS_INSTANCE_NAME}_CallbackRegister( EVSYS_CALLBACK callback, uintptr_t context );
	<#lt>void ${EVSYS_INSTANCE_NAME}_InterruptDisable(EVSYS_INT_MASK interrupt);
	<#lt>void ${EVSYS_INSTANCE_NAME}_InterruptEnable(EVSYS_INT_MASK interrupt);
</#if>

#ifdef __cplusplus // Provide C++ Compatibility
 }
#endif

#endif
