/*******************************************************************************
  DACC Peripheral Library

  Company:
    Microchip Technology Inc.

  File Name:
    plib_dacc${INDEX?string}.c

  Summary:
    DACC Source File

  Description:
    None

*******************************************************************************/

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

#include "plib_dacc${INDEX?string}.h"

<#--Implementation-->
// *****************************************************************************
// *****************************************************************************
// Section: DACC Implementation
// *****************************************************************************
// *****************************************************************************

void DACC${INDEX?string}_Initialize (void)
{
	<#if (DACC_CHER_CH0 || DACC_CHER_CH1)>
	
    /* Reset DACC Peripheral */
    _DACC_REGS->DACC_CR.w = DACC_CR_SWRST_Msk;

    _DACC_REGS->DACC_MR.w = DACC_MR_PRESCALER(${DACC_MR_PRESCALER}) ${DACC_MR_MAXS0?then('| DACC_MR_MAXS0_Msk', '')}${DACC_MR_MAXS1?then('| DACC_MR_MAXS1_Msk', '')}<#if DACC_MR_DIFF == "DIFFERENTIAL">| DACC_MR_DIFF_Msk </#if>;
    
	<#if (DACC_TRIGR_TRGEN0 && (!DACC_TRIGR_TRGEN1))>
    /* Configure Trigger Source and Over sample ratio for interpolation filter */
    _DACC_REGS->DACC_TRIGR.w = DACC_TRIGR_TRGEN0_Msk | DACC_TRIGR_TRGSEL0(DACC_TRIGR_TRGSEL0_${DACC_TRIGR_TRGSEL0}_Val) | DACC_TRIGR_OSR0(DACC_TRIGR_OSR0_${DACC_TRIGR_OSR0}_Val);
    
	<#elseif ((!DACC_TRIGR_TRGEN0) && DACC_TRIGR_TRGEN1)>
    /* Configure Trigger Source and Over sample ratio for interpolation filter */
    _DACC_REGS->DACC_TRIGR.w = DACC_TRIGR_TRGEN1_Msk | DACC_TRIGR_TRGSEL1(DACC_TRIGR_TRGSEL1_${DACC_TRIGR_TRGSEL1}_Val) | DACC_TRIGR_OSR1(DACC_TRIGR_OSR1_${DACC_TRIGR_OSR1}_Val);
    
    <#elseif (DACC_TRIGR_TRGEN0 && DACC_TRIGR_TRGEN1)>
    /* Configure Trigger Source and Over sample ratio for interpolation filter */
    _DACC_REGS->DACC_TRIGR.w = (DACC_TRIGR_TRGEN0_Msk | DACC_TRIGR_TRGSEL0(DACC_TRIGR_TRGSEL0_${DACC_TRIGR_TRGSEL0}_Val) | DACC_TRIGR_OSR0(DACC_TRIGR_OSR0_${DACC_TRIGR_OSR0}_Val)) |\
                               (DACC_TRIGR_TRGEN1_Msk | DACC_TRIGR_TRGSEL1(DACC_TRIGR_TRGSEL1_${DACC_TRIGR_TRGSEL1}_Val) | DACC_TRIGR_OSR1(DACC_TRIGR_OSR1_${DACC_TRIGR_OSR1}_Val)); 
                               
    </#if>
    /* Configure DACC Bias Current */
	_DACC_REGS->DACC_ACR.w =  ${(DACC_CHER_CH0 && !DACC_CHER_CH1)?then('DACC_ACR_IBCTLCH0(${DACC_ACR_IBCTLCH0})', '')}${(!DACC_CHER_CH0 && DACC_CHER_CH1)?then('DACC_ACR_IBCTLCH1(${DACC_ACR_IBCTLCH1})', '')}${(DACC_CHER_CH0 && DACC_CHER_CH1)?then('DACC_ACR_IBCTLCH0(${DACC_ACR_IBCTLCH0}) | DACC_ACR_IBCTLCH1(${DACC_ACR_IBCTLCH1})', '')};
		
	/* Enable DAC Channel */
	_DACC_REGS->DACC_CHER.w = ${(DACC_CHER_CH0 && !DACC_CHER_CH1)?then('DACC_CHER_CH0_Msk', '')}${(!DACC_CHER_CH0 && DACC_CHER_CH1)?then('DACC_CHER_CH1_Msk', '')}${(DACC_CHER_CH0 && DACC_CHER_CH1)?then('DACC_CHER_CH0_Msk | DACC_CHER_CH1_Msk', '')};

	<#if (DACC_CHER_CH0 && (!DACC_CHER_CH1))>
    /* Wait until DAC Channel 0 is ready*/
    while(!(_DACC_REGS->DACC_CHSR.w & DACC_CHSR_DACRDY0_Msk));
    <#elseif ((!DACC_CHER_CH0) && DACC_CHER_CH1)>
    /* Wait until DAC Channel 1 is ready*/
    while(!(_DACC_REGS->DACC_CHSR.w & DACC_CHSR_DACRDY1_Msk));
    <#elseif (DACC_CHER_CH0 && DACC_CHER_CH1)>
    /* Wait until DAC Channel 0 and Channel 1 is ready*/
    while(!(_DACC_REGS->DACC_CHSR.w & (DACC_CHSR_DACRDY0_Msk | DACC_CHSR_DACRDY1_Msk)));
	</#if>
    </#if>
}

bool DACC${INDEX?string}_StatusGet (DACC${INDEX?string}_CHANNEL_NUM chId)
{
    return ((_DACC_REGS->DACC_ISR.w >> chId) & 0x1U);
}

void DACC${INDEX?string}_DataWrite (DACC${INDEX?string}_CHANNEL_NUM chId, uint32_t data)
{
    _DACC_REGS->DACC_CDR[chId].w = data;  
}