/*******************************************************************************
  SPI PLIB

  Company:
    Microchip Technology Inc.

  File Name:
    plib_spi.h

  Summary:
    SPI PLIB Common Header File

  Description:
    This file has prototype of all the interfaces which are common for all the
    SPI peripherals.

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

#ifndef PLIB_SPI_H
#define PLIB_SPI_H

#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>
#include "${__PROCESSOR?lower_case}.h"

/* Provide C++ Compatibility */
#ifdef __cplusplus  

    extern "C" {

#endif

/****************************** SPI${SPI_INDEX?string} Interface *********************************/

typedef enum
{
    DATA_VALID_ON_CLOCK_TRAILING_EDGE = 0 << SPI_CSR_NCPHA_Pos,
    DATA_VALID_ON_CLOCK_LEADING_EDGE = 1 << SPI_CSR_NCPHA_Pos
    
}SPI_CLOCK_PHASE;

typedef enum
{
    SPI_CLOCK_POLARITY_IDLE_LOW = 0 << SPI_CSR_CPOL_Pos,
    SPI_CLOCK_POLARITY_IDLE_HIGH = 1 << SPI_CSR_CPOL_Pos
    
}SPI_CLOCK_POLARITY;

typedef enum
{
    SPI_DATA_BITS_8 = SPI_CSR_BITS_8_BIT_Val,
    SPI_DATA_BITS_9 = SPI_CSR_BITS_9_BIT_Val,
    SPI_DATA_BITS_10 = SPI_CSR_BITS_10_BIT_Val,
    SPI_DATA_BITS_11 = SPI_CSR_BITS_11_BIT_Val,
    SPI_DATA_BITS_12 = SPI_CSR_BITS_12_BIT_Val,
    SPI_DATA_BITS_13 = SPI_CSR_BITS_13_BIT_Val,
    SPI_DATA_BITS_14 = SPI_CSR_BITS_14_BIT_Val,
    SPI_DATA_BITS_15 = SPI_CSR_BITS_15_BIT_Val,
    SPI_DATA_BITS_16 = SPI_CSR_BITS_16_BIT_Val

}SPI_DATA_BITS;

typedef enum
{
    SPI_CHIP_SELECT_NPCS0 = SPI_TDR_PCS_NPCS0 | 0x00,
    SPI_CHIP_SELECT_NPCS1 = SPI_TDR_PCS_NPCS1 | 0x01,
    SPI_CHIP_SELECT_NPCS2 = SPI_TDR_PCS_NPCS2 | 0x02,
    SPI_CHIP_SELECT_NPCS3 = SPI_TDR_PCS_NPCS3 | 0x03,
    
}SPI_CHIP_SELECT;

typedef struct
{     
    uint32_t    clockFrequency;
    SPI_CLOCK_PHASE clockPhase;
    SPI_CLOCK_POLARITY clockPolarity;
    SPI_DATA_BITS   dataBits;
    SPI_CHIP_SELECT chipSelect;

}SPI_SLAVE_SETUP;

typedef enum 
{
    SPI_ERROR_NONE = 0,
    SPI_OVERRUN_ERROR = 1 << SPI_SR_OVRES_Pos

}SPI_ERROR;

typedef  void (*SPI_EVENT_HANDLER) (void* context);

// *****************************************************************************
// *****************************************************************************
// Section: Local: **** Do Not Use ****
// *****************************************************************************
// *****************************************************************************

typedef struct
{
    void*                   txBuffer;    
    void*                   rxBuffer;
    size_t                  exchangeSize;
    size_t                  rxCount;
    size_t                  txCount;
    bool                    exchangeIsBusy;
    SPI_EVENT_HANDLER       callback; 
    void*                   context;
    SPI_CHIP_SELECT         chipSelect;
} SPI_OBJECT ;

/* Provide C++ Compatibility */
#ifdef __cplusplus

    }
    
#endif

#endif // PLIB_SPI_H

/*******************************************************************************
 End of File
*/