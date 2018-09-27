/*******************************************************************************
  TWIHS Peripheral Library Source File

  Company
    Microchip Technology Inc.

  File Name
    plib_twihs0.c

  Summary
    TWIHS peripheral library interface.

  Description

  Remarks:

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

// *****************************************************************************
// *****************************************************************************
// Included Files
// *****************************************************************************
// *****************************************************************************

#include "device.h"
#include "plib_twihs0.h"

// *****************************************************************************
// *****************************************************************************
// Local Data Type Definitions
// *****************************************************************************
// *****************************************************************************

#define TWIHS_MASTER_MAX_BAUDRATE        (400000U)
#define TWIHS_LOW_LEVEL_TIME_LIMIT       (384000U)
#define TWIHS_CLK_DIVIDER                     (2U)
#define TWIHS_CLK_CALC_ARGU                   (3U)
#define TWIHS_CLK_DIV_MAX                  (0xFFU)
#define TWIHS_CLK_DIV_MIN                     (7U)

// *****************************************************************************
// *****************************************************************************
// Global Data
// *****************************************************************************
// *****************************************************************************

static TWIHS_OBJ twihs0Obj;
static twihs_registers_t *TWIHS0_Module = TWIHS0_REGS;

// *****************************************************************************
// *****************************************************************************
// TWIHS0 PLib Interface Routines
// *****************************************************************************
// *****************************************************************************

// *****************************************************************************
/* Function:
    void TWIHS0_Initialize(void)

   Summary:
    Initializes given instance of the TWIHS peripheral.

   Precondition:
    None.

   Parameters:
    None.

   Returns:
    None
*/

void TWIHS0_Initialize(void)
{
    // Reset the i2c Module
    TWIHS0_Module->TWIHS_CR = TWIHS_CR_SWRST_Msk;

    // Disable the I2C Master/Slave Mode
    TWIHS0_Module->TWIHS_CR = TWIHS_CR_MSDIS_Msk |
                                          TWIHS_CR_SVDIS_Msk;

    // Set Baud rate
    TWIHS0_Module->TWIHS_CWGR = ( TWIHS_CWGR_HOLD_Msk & TWIHS0_Module->TWIHS_CWGR) |
                                            ( TWIHS_CWGR_CLDIV(192) |
                                              TWIHS_CWGR_CHDIV(177) |
                                              TWIHS_CWGR_CKDIV(0) );

    // Starts the transfer by clearing the transmit hold register
    TWIHS0_Module->TWIHS_CR = TWIHS_CR_THRCLR_Msk;

    // Enables interrupt on nack and arbitration lost
    TWIHS0_Module->TWIHS_IER = TWIHS_IER_NACK_Msk |
                                           TWIHS_IER_ARBLST_Msk;

    // Enable Master Mode
    TWIHS0_Module->TWIHS_CR = TWIHS_CR_MSEN_Msk;

    // Initialize the twihs PLib Object
    twihs0Obj.error   = TWIHS_ERROR_NONE;
    twihs0Obj.state   = TWIHS_STATE_IDLE;
}


/******************************************************************************
Local Functions
******************************************************************************/

static void TWIHS0_InitiateRead(void)
{

    twihs0Obj.state = TWIHS_STATE_TRANSFER_READ;

    TWIHS0_Module->TWIHS_MMR |= TWIHS_MMR_MREAD_Msk;

    /* When a single data byte read is performed,
    the START and STOP bits must be set at the same time */
    if(twihs0Obj.readSize == 1)
    {
        TWIHS0_Module->TWIHS_CR = TWIHS_CR_START_Msk | TWIHS_CR_STOP_Msk;
    }
    else
    {
        TWIHS0_Module->TWIHS_CR = TWIHS_CR_START_Msk;
    }

    __enable_irq();
    TWIHS0_Module->TWIHS_IER = TWIHS_IER_RXRDY_Msk | TWIHS_IER_TXCOMP_Msk;
}




static void TWIHS0_InitiateTransfer(uint16_t address, bool type)
{
    // 10-bit Slave Address
    if( address > 0x007F )
    {
        TWIHS0_Module->TWIHS_MMR = TWIHS_MMR_DADR((address & 0x00007F00) >> 8) |
                                               TWIHS_MMR_IADRSZ(1);

        // Set internal address
        TWIHS0_Module->TWIHS_IADR = TWIHS_IADR_IADR(address & 0x000000FF );
    }
    // 7-bit Slave Address
    else
    {
        TWIHS0_Module->TWIHS_MMR = TWIHS_MMR_DADR(address) | TWIHS_MMR_IADRSZ(0);
    }

    twihs0Obj.writeCount= 0;
    twihs0Obj.readCount= 0;

    // Write transfer
    if(type == false)
    {
        // Single Byte Write
        if( twihs0Obj.writeSize == 1 )
        {
            // Single Byte write only
            if(  twihs0Obj.readSize ==0  )
            {
                // Load last byte in transmit register, issue stop condition
                // Generate TXCOMP interrupt after STOP condition has been sent
                twihs0Obj.state = TWIHS_STATE_WAIT_FOR_TXCOMP;

                TWIHS0_Module->TWIHS_THR = TWIHS_THR_TXDATA(twihs0Obj.writeBuffer[twihs0Obj.writeCount++]);
                TWIHS0_Module->TWIHS_CR =  TWIHS_CR_STOP_Msk;
                TWIHS0_Module->TWIHS_IER = TWIHS_IER_TXCOMP_Msk;
            }
            // Single Byte write and than read transfer
            else
            {
                // START bit must be set before the byte is shifted out. Hence disabled interrupt
                __disable_irq();
                TWIHS0_Module->TWIHS_THR = TWIHS_THR_TXDATA(twihs0Obj.writeBuffer[twihs0Obj.writeCount++]);
                type=true;
            }
        }
        // Multi-Byte Write
        else
        {
            twihs0Obj.state = TWIHS_STATE_TRANSFER_WRITE;

            TWIHS0_Module->TWIHS_THR = TWIHS_THR_TXDATA(twihs0Obj.writeBuffer[twihs0Obj.writeCount++]);
            TWIHS0_Module->TWIHS_IER = TWIHS_IDR_TXRDY_Msk | TWIHS_IER_TXCOMP_Msk;
        }
    }
    // Read transfer
    if(type)
    {
        TWIHS0_InitiateRead();
    }
}


// *****************************************************************************
/* Function:
    void TWIHS0_CallbackRegister(TWIHS_CALLBACK callback, uintptr_t contextHandle)

   Summary:
    Sets the pointer to the function (and it's context) to be called when the
    given TWIHS's transfer events occur.

   Precondition:
    TWIHSx_Initialize must have been called for the associated TWIHS instance.

   Parameters:
    callback - A pointer to a function with a calling signature defined
    by the TWIHS_CALLBACK data type.

    context - A value (usually a pointer) passed (unused) into the function
    identified by the callback parameter.

   Returns:
    None.
*/

void TWIHS0_CallbackRegister(TWIHS_CALLBACK callback, uintptr_t contextHandle)
{
    if (callback == NULL)
    {
        return;
    }

    twihs0Obj.callback = callback;
    twihs0Obj.context = contextHandle;
}

// *****************************************************************************
/* Function:
    void TWIHS0_TransferSetup(TWIHS_TRANSFER_SETUP setup, uint32_t srcClkFreq)

   Summary:
    Dynamic setup of TWIHS Peripheral.

   Precondition:
    None.

   Parameters:
    None.

   Returns:
    None
*/

bool TWIHS0_TransferSetup( TWIHS_TRANSFER_SETUP * setup, uint32_t srcClkFreq )
{
    uint32_t clockSrcFreq;
    uint32_t twihsClkSpeed;
    uint32_t ckdiv = 0;
    uint32_t cldiv = 0;
    uint32_t chdiv = 0;
    uint32_t c_lh_div = 0;

    // Check for ongoing transfer
    if( twihs0Obj.state != TWIHS_STATE_IDLE )
    {
        return false;
    }

    if( srcClkFreq )
    {
        clockSrcFreq = srcClkFreq;
    }
    else
    {
        clockSrcFreq = 150000000;
    }

    twihsClkSpeed = setup->clkSpeed;

    /* Set Clock */
    if( TWIHS_MASTER_MAX_BAUDRATE < twihsClkSpeed  )
    {
        return (false);
    }

    /* Low level time not less than 1.3us of I2C Fast Mode. */
    if ( twihsClkSpeed > TWIHS_LOW_LEVEL_TIME_LIMIT )
    {
        /* Low level of time fixed for 1.3us. */
        cldiv = clockSrcFreq / ( TWIHS_LOW_LEVEL_TIME_LIMIT *
                                    TWIHS_CLK_DIVIDER ) -
                                    TWIHS_CLK_CALC_ARGU;

        chdiv = clockSrcFreq / (( twihsClkSpeed +
                            ( twihsClkSpeed - TWIHS_LOW_LEVEL_TIME_LIMIT)) *
                              TWIHS_CLK_DIVIDER ) -
                              TWIHS_CLK_CALC_ARGU;

        /* cldiv must fit in 8 bits, ckdiv must fit in 3 bits */
        while (( cldiv > TWIHS_CLK_DIV_MAX ) &&
               ( ckdiv < TWIHS_CLK_DIV_MIN ))
        {
            /* Increase clock divider */
            ckdiv++;

            /* Divide cldiv value */
            cldiv /= TWIHS_CLK_DIVIDER;
        }

        /* chdiv must fit in 8 bits, ckdiv must fit in 3 bits */
        while (( chdiv > TWIHS_CLK_DIV_MAX ) &&
               ( ckdiv < TWIHS_CLK_DIV_MIN ))
        {
            /* Increase clock divider */
            ckdiv++;

            /* Divide cldiv value */
            chdiv /= TWIHS_CLK_DIVIDER;
        }

        /* set clock waveform generator register */
        TWIHS0_Module->TWIHS_CWGR = ( TWIHS_CWGR_HOLD_Msk & TWIHS0_Module->TWIHS_CWGR) |
                                  ( TWIHS_CWGR_CLDIV(cldiv) |
                                    TWIHS_CWGR_CHDIV(chdiv) |
                                    TWIHS_CWGR_CKDIV(ckdiv) );
    }
    else
    {
        c_lh_div = clockSrcFreq / ( twihsClkSpeed * TWIHS_CLK_DIVIDER ) -
                   TWIHS_CLK_CALC_ARGU;

        /* cldiv must fit in 8 bits, ckdiv must fit in 3 bits */
        while (( c_lh_div > TWIHS_CLK_DIV_MAX ) &&
               ( ckdiv < TWIHS_CLK_DIV_MIN ))
        {
            /* Increase clock divider */
            ckdiv++;

            /* Divide cldiv value */
            c_lh_div /= TWIHS_CLK_DIVIDER;
        }

        /* set clock waveform generator register */
        TWIHS0_Module->TWIHS_CWGR = ( TWIHS_CWGR_HOLD_Msk & TWIHS0_Module->TWIHS_CWGR) |
                                  ( TWIHS_CWGR_CLDIV(c_lh_div) |
                                    TWIHS_CWGR_CHDIV(c_lh_div) |
                                    TWIHS_CWGR_CKDIV(ckdiv) )  ;
    }

    return (true);

}

// *****************************************************************************
/* Function:
    bool TWIHS0_IsBusy(void)

   Summary:
    Returns the Peripheral busy status.

   Precondition:
    TWIHSx_Initialize must have been called for the associated TWIHS instance.

   Parameters:
    None.

   Returns:
    true - Busy.
    false - Not busy.
*/

bool TWIHS0_IsBusy(void)
{
    if( twihs0Obj.state == TWIHS_STATE_IDLE )
    {
        return false;
    }
    else
    {
        return true;
    }
}

// *****************************************************************************
/* Function:
    bool TWIHS0_Read(uint16_t address, uint8_t *pdata, size_t length)

   Summary:
    Reads data from the slave.

   Precondition:
    TWIHSx_Initialize must have been called for the associated TWIHS instance.

   Parameters:
    address - 7-bit / 10-bit slave address.
    pdata   - pointer to destination data buffer
    length  - length of data buffer in number of bytes.

   Returns:
    Request status.
    True - Request was successful.
    False - Request has failed.
*/

bool TWIHS0_Read(uint16_t address, uint8_t *pdata, size_t length)
{
    // Check for ongoing transfer
    if( twihs0Obj.state != TWIHS_STATE_IDLE )
    {
        return false;
    }

    twihs0Obj.address=address;
    twihs0Obj.readBuffer=pdata;
    twihs0Obj.readSize=length;
    twihs0Obj.writeBuffer=NULL;
    twihs0Obj.writeSize=0;
    twihs0Obj.error = TWIHS_ERROR_NONE;

    TWIHS0_InitiateTransfer(address, true);

    return true;
}

// *****************************************************************************
/* Function:
    bool TWIHS0_Write(uint16_t address, uint8_t *pdata, size_t length)

   Summary:
    Writes data onto the slave.

   Precondition:
    TWIHSx_Initialize must have been called for the associated TWIHS instance.

   Parameters:
    address - 7-bit / 10-bit slave address.
    pdata   - pointer to source data buffer
    length  - length of data buffer in number of bytes.

   Returns:
    Request status.
    True - Request was successful.
    False - Request has failed.
*/

bool TWIHS0_Write(uint16_t address, uint8_t *pdata, size_t length)
{
    // Check for ongoing transfer
    if( twihs0Obj.state != TWIHS_STATE_IDLE )
    {
        return false;
    }

    twihs0Obj.address=address;
    twihs0Obj.readBuffer=NULL;
    twihs0Obj.readSize=0;
    twihs0Obj.writeBuffer=pdata;
    twihs0Obj.writeSize=length;
    twihs0Obj.error = TWIHS_ERROR_NONE;

    TWIHS0_InitiateTransfer(address, false);

    return true;
}

// *****************************************************************************
/* Function:
    bool TWIHS0_WriteRead(uint16_t address, uint8_t *wdata, size_t wlength, uint8_t *rdata, size_t rlength)

   Summary:
    Write and Read data from Slave.

   Precondition:
    TWIHSx_Initialize must have been called for the associated TWIHS instance.

   Parameters:
    address - 7-bit / 10-bit slave address.
    wdata   - pointer to write data buffer
    wlength - write data length in bytes.
    rdata   - pointer to read data buffer.
    rlength - read data length in bytes.

   Returns:
    Request status.
    True - Request was successful.
    False - Request has failed.
*/

bool TWIHS0_WriteRead(uint16_t address, uint8_t *wdata, size_t wlength, uint8_t *rdata, size_t rlength)
{

    // Check for ongoing transfer
    if( twihs0Obj.state != TWIHS_STATE_IDLE )
    {
        return false;
    }

    twihs0Obj.address=address;
    twihs0Obj.readBuffer=rdata;
    twihs0Obj.readSize=rlength;
    twihs0Obj.writeBuffer=wdata;
    twihs0Obj.writeSize=wlength;
    twihs0Obj.error = TWIHS_ERROR_NONE;

    TWIHS0_InitiateTransfer(address, false);

    return true;
}

// *****************************************************************************
/* Function:
    TWIHS_ERROR TWIHS0_ErrorGet(void)

   Summary:
    Returns the error during transfer.

   Precondition:
    TWIHSx_Initialize must have been called for the associated TWIHS instance.

   Parameters:
    None.

   Returns:
    Error during transfer.
*/

TWIHS_ERROR TWIHS0_ErrorGet(void)
{
    TWIHS_ERROR error;

    error = twihs0Obj.error;
    twihs0Obj.error = TWIHS_ERROR_NONE;

    return error;
}

// *****************************************************************************
/* Function:
    void TWIHS0_InterruptHandler(void)

   Summary:
    TWIHS0 Peripheral Interrupt Handler.

   Description:
    This function is TWIHS0 Peripheral Interrupt Handler and will
    called on every TWIHS0 interrupt.

   Precondition:
    None.

   Parameters:
    None.

   Returns:
    None.

   Remarks:
    The function is called as peripheral instance's interrupt handler if the
    instance interrupt is enabled. If peripheral instance's interrupt is not
    enabled user need to call it from the main while loop of the application.
*/

void TWIHS0_InterruptHandler(void)
{
    uint32_t status;

    // Read the peripheral status
    status = TWIHS0_Module->TWIHS_SR;

    /* checks if Slave has Nacked */
    if( status & TWIHS_SR_NACK_Msk )
    {
        twihs0Obj.state = TWIHS_STATE_ERROR;
        twihs0Obj.error = TWIHS_ERROR_NACK;
    }

    /* checks if the arbitration is lost in multi-master scenario */
    if( status & TWIHS_SR_ARBLST_Msk )
    {
        /* Re-initiate the transfer if arbitration is lost in
         * between of the transfer
         */
        twihs0Obj.state = TWIHS_STATE_ADDR_SEND;
    }

    switch( twihs0Obj.state )
    {
        case TWIHS_STATE_ADDR_SEND:
        {
            if (twihs0Obj.writeSize != 0 )
            {
                // Initiate Write transfer
                TWIHS0_InitiateTransfer(twihs0Obj.address, false);
            }
            else
            {
                // Initiate Read transfer
                TWIHS0_InitiateTransfer(twihs0Obj.address, true);
            }
        }
        break;

        case TWIHS_STATE_TRANSFER_WRITE:
        {
            /* checks if master is ready to transmit */
            if( status & TWIHS_SR_TXRDY_Msk )
            {
                // Write Last Byte and then initiate read transfer
                if( ( twihs0Obj.writeCount == (twihs0Obj.writeSize -1) ) && ( twihs0Obj.readSize != 0 ))
                {
                    // START bit must be set before the last byte is shifted out to generate repeat start. Hence disabled interrupt
                    __disable_irq();
                    TWIHS0_Module->TWIHS_IDR = TWIHS_IDR_TXRDY_Msk;
                    TWIHS0_Module->TWIHS_THR = TWIHS_THR_TXDATA(twihs0Obj.writeBuffer[twihs0Obj.writeCount++]);
                    TWIHS0_InitiateRead();
                }
                // Write Last byte and then issue STOP condition
                else if ( twihs0Obj.writeCount == (twihs0Obj.writeSize -1))
                {
                    // Load last byte in transmit register, issue stop condition
                    // Generate TXCOMP interrupt after STOP condition has been sent
                    TWIHS0_Module->TWIHS_THR = TWIHS_THR_TXDATA(twihs0Obj.writeBuffer[twihs0Obj.writeCount++]);
                    TWIHS0_Module->TWIHS_CR = TWIHS_CR_STOP_Msk;
                    TWIHS0_Module->TWIHS_IDR = TWIHS_IDR_TXRDY_Msk;

                    /* Check TXCOMP to confirm if STOP condition has been sent, otherwise wait for TXCOMP interrupt */
                    status = TWIHS0_Module->TWIHS_SR;
                    if( status & TWIHS_SR_TXCOMP_Msk )
                    {
                        twihs0Obj.state = TWIHS_STATE_TRANSFER_DONE;
                    }
                    else
                    {
                        twihs0Obj.state = TWIHS_STATE_WAIT_FOR_TXCOMP;
                    }
                }
                // Write next byte
                else
                {
                    TWIHS0_Module->TWIHS_THR = TWIHS_THR_TXDATA(twihs0Obj.writeBuffer[twihs0Obj.writeCount++]);
                }

                // Dummy read to ensure that TXRDY bit is cleared
                status = TWIHS0_Module->TWIHS_SR;
            }

            break;
        }

        case TWIHS_STATE_TRANSFER_READ:
        {
            /* checks if master has received the data */
            if( status & TWIHS_SR_RXRDY_Msk )
            {
                // Set the STOP (or START) bit before reading the TWIHS_RHR on the next-to-last access
                if(  twihs0Obj.readCount == (twihs0Obj.readSize - 2) )
                {
                    TWIHS0_Module->TWIHS_CR = TWIHS_CR_STOP_Msk;
                }

                /* read the received data */
                twihs0Obj.readBuffer[twihs0Obj.readCount++] = (uint8_t)(TWIHS0_Module->TWIHS_RHR & TWIHS_RHR_RXDATA_Msk);

                /* checks if transmission has reached at the end */
                if( twihs0Obj.readCount == twihs0Obj.readSize )
                {
                    /* Disable the RXRDY interrupt*/
                    TWIHS0_Module->TWIHS_IDR = TWIHS_IDR_RXRDY_Msk;

                    /* Check TXCOMP to confirm if STOP condition has been sent, otherwise wait for TXCOMP interrupt */
                    status = TWIHS0_Module->TWIHS_SR;
                    if( status & TWIHS_SR_TXCOMP_Msk )
                    {
                        twihs0Obj.state = TWIHS_STATE_TRANSFER_DONE;
                    }
                    else
                    {
                        twihs0Obj.state = TWIHS_STATE_WAIT_FOR_TXCOMP;
                    }
                }
            }
            break;
        }

        case TWIHS_STATE_WAIT_FOR_TXCOMP:
        {
            if( status & TWIHS_SR_TXCOMP_Msk )
            {
                twihs0Obj.state = TWIHS_STATE_TRANSFER_DONE;
            }
            break;
        }

        default:
        {
            break;
        }
    }

    /* Check for error during transmission */
    if( twihs0Obj.state == TWIHS_STATE_ERROR )
    {
        twihs0Obj.state = TWIHS_STATE_IDLE;
        TWIHS0_Module->TWIHS_IDR = TWIHS_IDR_TXCOMP_Msk |
                                 TWIHS_IDR_TXRDY_Msk  |
                                 TWIHS_IDR_RXRDY_Msk;

        if ( twihs0Obj.callback != NULL )
        {
            twihs0Obj.callback( twihs0Obj.context );
        }
    }

    // check for completion of transfer
    if( twihs0Obj.state == TWIHS_STATE_TRANSFER_DONE )
    {

        twihs0Obj.error = TWIHS_ERROR_NONE;

        // Reset the PLib objects and Interrupts
        twihs0Obj.state = TWIHS_STATE_IDLE;
        TWIHS0_Module->TWIHS_IDR = TWIHS_IDR_TXCOMP_Msk |
                                 TWIHS_IDR_TXRDY_Msk  |
                                 TWIHS_IDR_RXRDY_Msk;

        if ( twihs0Obj.callback != NULL )
        {
            twihs0Obj.callback( twihs0Obj.context );
        }
    }

    return;
}

/*******************************************************************************
 End of File
*/
