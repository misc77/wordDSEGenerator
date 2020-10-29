class Filter:
    def __init__ (self):
        self.removeElements = {'andere Daten:', 'Sonstiges:', 'Sonstige:'}

    def applyTextFilter(self, text):
        for e in self.removeElements:
            
            if text.lstrip().startswith(e):
                text.replace(e, '')
        return text
