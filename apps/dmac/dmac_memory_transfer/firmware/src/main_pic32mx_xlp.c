/*******************************************************************************
  Main Source File

  Company:
    Microchip Technology Inc.

  File Name:
    main.c

  Summary:
    This file contains the "main" function for a project.

  Description:
    This file contains the "main" function for a project.  The
    "main" function calls the "SYS_Initialize" function to initialize the state
    machines of all modules in the system
 *******************************************************************************/

// DOM-IGNORE-BEGIN
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
// DOM-IGNORE-END

// *****************************************************************************
// *****************************************************************************
// Section: Included Files
// *****************************************************************************
// *****************************************************************************

#include <stddef.h>                     // Defines NULL
#include <stdbool.h>                    // Defines true
#include <stdlib.h>                     // Defines EXIT_FAILURE
#include <string.h>                     // Defines strncmp
#include <stdio.h>
#include "definitions.h"                // SYS function prototypes

/* Macro definitions */
#define LED_On()                        RED_LED_Clear()
#define LED_Off()                       RED_LED_Set()

#define TRANSFER_SIZE 1024

char __attribute__((coherent)) srcBuffer[TRANSFER_SIZE] = {};
char __attribute__((coherent)) dstBuffer1[TRANSFER_SIZE] = {};
volatile bool completeStatus = false;
volatile bool errorStatus = false;

void APP_Callback(DMAC_TRANSFER_EVENT status, uintptr_t context)
{
    if(status == DMAC_TRANSFER_EVENT_COMPLETE)
    {
        completeStatus = true;
    }
    else
    {
        errorStatus = true;
    }
}

// *****************************************************************************
// *****************************************************************************
// Section: Main Entry Point
// *****************************************************************************
// *****************************************************************************

int main ( void )
{
    uint32_t i = 0;

    /* Initialize all modules */
    SYS_Initialize ( NULL );
    LED_Off();

    /* Build the srcBuffer */
    while(i < TRANSFER_SIZE)
    {
        srcBuffer[i] = (uint8_t)i;
        i++;
    }
    printf("\n\r-------------------------------------------------------------");
    printf("\n\r\t\t DMAC Memory Transfer DEMO\t\t");
    printf("\n\r-------------------------------------------------------------");
    
    /* Register a callback with DMAC PLIB to get transfer complete and erro
     * events. */
    DMAC_ChannelCallbackRegister(DMAC_CHANNEL_0, APP_Callback, 0);

    /* Performing first transfer from srcBuffer to dstBuffer1 with configured
     * burst size of 1 data */
    DMAC_ChannelTransfer(DMAC_CHANNEL_0, &srcBuffer, TRANSFER_SIZE, &dstBuffer1, TRANSFER_SIZE, TRANSFER_SIZE);

    while (1)
    {
        if(completeStatus == true)
        {
            completeStatus = false;

            if(strncmp(srcBuffer, dstBuffer1, TRANSFER_SIZE) == 0)
            {
                /* Successfully transferred the data using DMAC */
                printf("\n\r DMAC Memory Transfer Successful with Data Match\n\r");                    
                LED_On();
            }
            else
            {
                /* Data transfers done, but data mismatch occurred */
                printf("\n\r DMAC Memory Transfer Successful with Data Mismatch !!!\n\r");                    
                LED_Off();
            }
        }
        else if(errorStatus == true)
        {
            /* Error occurred during the transfers */
            errorStatus = false;
            LED_Off();
        }
        else
        {
            /* Nothing to do, loop */
            ;
        }
    }

    /* Execution should not come here during normal operation */

    return ( EXIT_FAILURE );
}


/*******************************************************************************
 End of File
*/

