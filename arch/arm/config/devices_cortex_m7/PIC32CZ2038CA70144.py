print("Loading System Services for " + Variables.get("__PROCESSOR"))

# load device specific clock manager information
execfile(Variables.get("__CORE_DIR") + "/../peripheral/clk_sam_e70/config/clk.py")

# load dma manager information
execfile(Variables.get("__CORE_DIR") + "/../peripheral/xdmac_11161/config/xdmac.py")

# load device specific nvic manager information
execfile(Variables.get("__CORE_DIR") + "/../peripheral/nvic_m7/config/nvic.py")

# load device specific pin manager information
execfile(Variables.get("__CORE_DIR") + "/../peripheral/pio_11004/config/pio.py")

# load rswdt
execfile(Variables.get("__CORE_DIR") + "/../peripheral/rswdt_11110/config/rswdt.py")

# load wdt
execfile(Variables.get("__CORE_DIR") + "/../peripheral/wdt_6080/config/wdt.py")

# load device specific configurations (fuses) 
devCfgComment = coreComponent.createCommentSymbol("CoreCfgComment1", devCfgMenu)
devCfgComment.setLabel("Note: Set Device Configuration Bits via Programming Tool")

# load family specific configuration
execfile(Variables.get("__ARCH_DIR") + "/PIC32CZ_CA70.py")

