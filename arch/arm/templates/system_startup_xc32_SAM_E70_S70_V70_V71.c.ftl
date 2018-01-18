/*
 *  Constants used for setting the GPNVM bits for TCM Size.
 */
#define GPNVM_TCM_SIZE_Pos        7u
#define GPNVM_TCM_SIZE_Msk        (0x3u << GPNVM_TCM_SIZE_Pos)
#define GPNVM_TCM_SIZE_0K_Val     (0x0u << GPNVM_TCM_SIZE_Pos)
#define GPNVM_TCM_SIZE_32K_Val    (0x1u << GPNVM_TCM_SIZE_Pos)
#define GPNVM_TCM_SIZE_64K_Val    (0x2u << GPNVM_TCM_SIZE_Pos)
#define GPNVM_TCM_SIZE_128K_Val   (0x3u << GPNVM_TCM_SIZE_Pos)

/** \brief  TCM memory configure size

 The function configures size of TCM memory based on __XC32_ITCM_LENGTH macro
 */
__STATIC_INLINE void __attribute__((optimize("-O1"))) TCM_ConfigureSize(void)
{
/*  Define the __XC32_SKIP_STARTUP_GPNVM preprocessor macro when you do not
 *  want this code to modify the GPNVM bits at runtime.
 *  Define the __XC32_SKIP_STARTUP_GPNVM_WAIT preprocessor macro when you do
 *  not want the code to poll the FRDY bit before continuing.
 */
#if !defined(__XC32_SKIP_STARTUP_GPNVM)
#if defined(__XC32_ITCM_LENGTH)

    static uint32_t gpnvm_value;
    _EFC_REGS->EEFC_FCR.w = (EEFC_FCR_FKEY_PASSWD | EEFC_FCR_FCMD_GGPB);
#if !defined(__XC32_SKIP_STARTUP_GPNVM_WAIT)
    while (!(_EFC_REGS->EEFC_FSR.w & EEFC_FSR_FRDY_Msk));
#endif
    gpnvm_value=_EFC_REGS->EEFC_FRR.w;

# if (__XC32_ITCM_LENGTH == 0x8000)
    /* 32K default size of ITCM and DTCM */
    /* GPNVM bits[8:7] == b'01 */
    if ((gpnvm_value & GPNVM_TCM_SIZE_Msk) != GPNVM_TCM_SIZE_32K_Val)
    {
        _EFC_REGS->EEFC_FCR.w = (EEFC_FCR_FKEY_PASSWD | EEFC_FCR_FCMD_CGPB | EEFC_FCR_FARG(8));
#if !defined(__XC32_SKIP_STARTUP_GPNVM_WAIT)
        while (!(_EFC_REGS->EEFC_FSR.w & EEFC_FSR_FRDY_Msk));
#endif
        _EFC_REGS->EEFC_FCR.w = (EEFC_FCR_FKEY_PASSWD | EEFC_FCR_FCMD_SGPB | EEFC_FCR_FARG(7));
#if !defined(__XC32_SKIP_STARTUP_GPNVM_WAIT)
        while (!(_EFC_REGS->EEFC_FSR.w & EEFC_FSR_FRDY_Msk));
        _RSTC_REGS->RSTC_CR.w = RSTC_CR_KEY_PASSWD | RSTC_CR_PROCRST_Msk;
#endif
    }
# elif (__XC32_ITCM_LENGTH == 0x10000)
    /* 64K */
    /* GPNVM bits[8:7] == b'10 */
    if ((gpnvm_value & GPNVM_TCM_SIZE_Msk) != GPNVM_TCM_SIZE_64K_Val)
    {
        _EFC_REGS->EEFC_FCR.w = (EEFC_FCR_FKEY_PASSWD | EEFC_FCR_FCMD_SGPB | EEFC_FCR_FARG(8));
#if !defined(__XC32_SKIP_STARTUP_GPNVM_WAIT)
      while (!(_EFC_REGS->EEFC_FSR.w & EEFC_FSR_FRDY_Msk));
#endif
        _EFC_REGS->EEFC_FCR.w = (EEFC_FCR_FKEY_PASSWD | EEFC_FCR_FCMD_CGPB | EEFC_FCR_FARG(7));
#if !defined(__XC32_SKIP_STARTUP_GPNVM_WAIT)
        while (!(_EFC_REGS->EEFC_FSR.w & EEFC_FSR_FRDY_Msk));
        _RSTC_REGS->RSTC_CR.w = RSTC_CR_KEY_PASSWD | RSTC_CR_PROCRST_Msk;
#endif
    }
# elif (__XC32_ITCM_LENGTH == 0x20000)
    /* 128K */
    /* GPNVM bits[8:7] == b'11 */
    if ((gpnvm_value & GPNVM_TCM_SIZE_Msk) != GPNVM_TCM_SIZE_128K_Val)
    {
        _EFC_REGS->EEFC_FCR.w = (EEFC_FCR_FKEY_PASSWD | EEFC_FCR_FCMD_SGPB
                              | EEFC_FCR_FARG(8));
#if !defined(__XC32_SKIP_STARTUP_GPNVM_WAIT)
        while (!(_EFC_REGS->EEFC_FSR.w & EEFC_FSR_FRDY_Msk));
#endif
        _EFC_REGS->EEFC_FCR.w = (EEFC_FCR_FKEY_PASSWD | EEFC_FCR_FCMD_SGPB
                              | EEFC_FCR_FARG(7));
#if !defined(__XC32_SKIP_STARTUP_GPNVM_WAIT)
        while (!(_EFC_REGS->EEFC_FSR.w & EEFC_FSR_FRDY_Msk));
        _RSTC_REGS->RSTC_CR.w = RSTC_CR_KEY_PASSWD | RSTC_CR_PROCRST_Msk;
#endif
    }
# endif /* __XC32_ITCM_LENGTH == value */
#endif /* defined(__XC32_ITCM_LENGTH) */
#endif /* !defined(__XC32_SKIP_STARTUP_GPNVM) */
}

__STATIC_INLINE void __attribute__((optimize("-O1"))) TCM_ConfigureNoSize(void)
{
    static uint32_t gpnvm_value;
    _EFC_REGS->EEFC_FCR.w = (EEFC_FCR_FKEY_PASSWD | EEFC_FCR_FCMD_GGPB);
#if !defined(__XC32_SKIP_STARTUP_GPNVM_WAIT)
    while (!(_EFC_REGS->EEFC_FSR.w & EEFC_FSR_FRDY_Msk));
#endif
    gpnvm_value=_EFC_REGS->EEFC_FRR.w;

    /* 0K size of ITCM and DTCM */
    /* GPNVM bits[8:7] == b'00 */
    if ((gpnvm_value & GPNVM_TCM_SIZE_Msk) != GPNVM_TCM_SIZE_0K_Val)
    {
        _EFC_REGS->EEFC_FCR.w = (EEFC_FCR_FKEY_PASSWD | EEFC_FCR_FCMD_CGPB | EEFC_FCR_FARG(8));
#if !defined(__XC32_SKIP_STARTUP_GPNVM_WAIT)
        while (!(_EFC_REGS->EEFC_FSR.w & EEFC_FSR_FRDY_Msk));
#endif
        _EFC_REGS->EEFC_FCR.w = (EEFC_FCR_FKEY_PASSWD | EEFC_FCR_FCMD_CGPB | EEFC_FCR_FARG(7));
#if !defined(__XC32_SKIP_STARTUP_GPNVM_WAIT)
        while (!(_EFC_REGS->EEFC_FSR.w & EEFC_FSR_FRDY_Msk));
        _RSTC_REGS->RSTC_CR.w = RSTC_CR_KEY_PASSWD | RSTC_CR_PROCRST_Msk;
#endif
    }
}
