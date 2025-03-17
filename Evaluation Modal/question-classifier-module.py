def _extract_matching_features(self, question: Dict) -> Dict:
        """Extract features specific to matching questions"""
        text = question["text"]
        
        # Try to extract columns to match
        left_column = []
        right_column = []
        
        # Look for common patterns in matching questions
        lines = text.split('\n')
        column_pattern = r'([A-Z])\.\s*(.*?)\s*(\d+)\.\s*(.*)'
        
        # Extract matching items
        matches = []
        for line in lines:
            match = re.search(column_pattern, line)
            if match:
                left_item = {"id": match.group(1), "text": match.group(2).strip()}
                right_item = {"id": match.group(3), "text": match.group(4).strip()}
                
                left_column.append(left_item)
                right_column.append(right_item)
                
                matches.append((left_item["id"], right_item["id"]))
        
        if left_column and right_column:
            question["left_column"] = left_column
            question["right_column"] = right_column
            question["matches"] = matches
        
        return question
    
    def _extract_mathematical_features(self, question: Dict) -> Dict:
        """Extract features specific to mathematical questions"""
        text = question["text"]
        
        # Identify mathematical expressions
        math_expressions = re.findall(r'\$(.+?)\$', text)
        if math_expressions:
            question["math_expressions"] = math_expressions
        
        # Identify units if present
        units_pattern = r'in\s+(\w+)$|express\s+in\s+(\w+)'
        units_match = re.search(units_pattern, text.lower())
        if units_match:
            units = units_match.group(1) or units_match.group(2)
            question["required_units"] = units
        
        return question
