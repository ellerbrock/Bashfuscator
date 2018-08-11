from bashfuscator.common.obfuscator import choosePrefObfuscator


class ObfuscationHandler(object):
    """
    Manages command and script obfuscation. Obfuscates based off of 
    the user's set options
    """
    def __init__(self, tokObfuscators, cmdObfuscators, args):
        self.tokObfuscators = tokObfuscators
        self.cmdObfuscators = cmdObfuscators
        self.userLayers = args.manual_layer_ordering
        self.layers = args.layers
        self.sizePref = args.payload_size
        self.timePref = args.execution_time
        self.binaryPref = args.binaryPref

        if args.command:
            self.originalCmd = args.command
        else:
            self.originalCmd = args.file.read()

    def generatePayload(self):
        payload = self.originalCmd
        
        for i in range(self.layers):
            if self.userLayers is not None:
                for userOb in self.userLayers:
                    payload = self.genObfuscationLayer(payload, userOb)
            
            else:
                payload = self.genObfuscationLayer(payload)

        return payload

    def genObfuscationLayer(self, payload, userOb=None):
        tokObfuscator = cmdObfuscator = None

        if userOb is not None:
            if userOb.split("/")[0] == "command":
                cmdObfuscator = choosePrefObfuscator(self.cmdObfuscators, self.sizePref, self.timePref, 
                    self.binaryPref, cmdObfuscator, userOb)
                payload = cmdObfuscator.obfuscate(self.sizePref, self.timePref, self.binaryPref, payload)
            elif userOb.split("/")[0] == "token":
                tokObfuscator = choosePrefObfuscator(self.tokObfuscators, self.sizePref, userOb=userOb)
                payload = tokObfuscator.obfuscate(self.sizePref, payload)

        else:
            cmdObfuscator = choosePrefObfuscator(self.cmdObfuscators, self.sizePref, self.timePref, 
                    self.binaryPref, userOb, cmdObfuscator)
            tokObfuscator = choosePrefObfuscator(self.tokObfuscators, self.sizePref, userOb=userOb)
           
            payload = cmdObfuscator.obfuscate(self.sizePref, self.timePref, self.binaryPref, payload)
            #payload = tokObfuscator.obfuscate(self.sizePref, payload)

        return payload
