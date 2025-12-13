# DSCI 551 Final Project - Darren Parry

class SimpleJSONParser:
    # A simple JSON parser that handles strings, numbers (int/float), booleans, and null values within a JSON object.
    def __init__(self):
            self.json_string = None
            self.index = 0

    def parse(self, json_string):
        # Method to start parsing
        self.json_string = json_string.strip()
        self.index = 0
        return self._parse_value()

    def _get_current_char(self):
        # Gets the character at the current index 
        if self.index < len(self.json_string):
            return self.json_string[self.index]
        return None

    def _skip_whitespace(self):
        # Skips over any whitespace characters
        while self._get_current_char() and self._get_current_char().isspace():
            self.index += 1

    def _parse_string(self)
        # Parses a string value from the current position
        self._skip_whitespace()
        assert self._get_current_char() == '"'
        self.index += 1
        start_pos = self.index
        while self._get_current_char() != '"':
            self.index += 1
            if self._get_current_char() is None:
                raise ValueError("Unterminated string")
        
        mystr = self.json_string[start_pos:self.index]
        self.index += 1
        return mystr

    def _parse_number(self):
        # Parses a number (integer or float) from the current position
        self._skip_whitespace()
        start_pos = self.index
        is_float = False
        while self._get_current_char() and self._get_current_char() in '0123456789.-':
            if self._get_current_char() == '.':
                is_float = True
            self.index += 1
        
        num_str = self.json_string[start_pos:self.index]
        return float(num_str) if is_float else int(num_str)

    def _parse_object(self):
        # Parses a JSON object into a Python dictionary
        assert self._get_current_char() == '{'
        self.index += 1  
        obj = {}

        while True:
            self._skip_whitespace()
            char = self._get_current_char()

            if char == '}':
                self.index += 1  
                return obj
            elif char == ',':
                self.index += 1
                self._skip_whitespace()
                continue

            key = self._parse_string()
            self._skip_whitespace()

            if self._get_current_char() == ':':
                self.index += 1
            else:
                raise ValueError("Expected ':' after key in JSON object")

            value = self._parse_value()
            obj[key] = value

    def _parse_array(self):
            # Parses a JSON array into a Python list
            self._skip_whitespace()
            assert self._get_current_char() == '['
            self.index += 1
            arr = []

            while True:
                self._skip_whitespace()
                char = self._get_current_char()

                if char == ']': 
                    self.index += 1
                    return arr
                elif char == ',':
                    self.index += 1
                    self._skip_whitespace()
                    continue
            
                value = self._parse_value()
                arr.append(value)

    def _parse_value(self):
        # Determines the type of the value at the current position and calls the appropriate parsing function
        self._skip_whitespace()
        char = self._get_current_char()

        if char == '"':
            return self._parse_string()
        elif char and (char.isdigit() or char == '-'): 
            return self._parse_number()
        elif self.json_string.startswith('true', self.index):
            self.index += 4
            return True
        elif self.json_string.startswith('false', self.index):
            self.index += 5
            return False
        elif self.json_string.startswith('null', self.index):
            self.index += 4
            return None
        elif char == '{': 
            return self._parse_object()
        elif char == '[':
            return self._parse_array()
        else:
            raise ValueError(f"Unexpected character: {char}")