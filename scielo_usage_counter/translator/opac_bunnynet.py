from .opac import URLTranslatorOPACSite


class BunnynetOPACBridge(URLTranslatorOPACSite):
    
    def __init__(self, jrnl_data, artcl_data):
        super().__init__(jrnl_data, artcl_data)
