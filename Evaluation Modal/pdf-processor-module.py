def _extract_tables(self, page) -> List[Dict]:
        """Extract tables from the page"""
        tables = []
        
        # Basic table detection - look for grid-like structures
        # In a full implementation, this would use a more sophisticated algorithm
        # like table structure recognition models
        
        # Get horizontal and vertical lines
        drawings = page.get_drawings()
        h_lines = []
        v_lines = []
        
        for drawing in drawings:
            for item in drawing["items"]:
                if item[0] == "l":  # Line
                    x0, y0, x1, y1 = item[1]
                    # Check if horizontal or vertical
                    if abs(y1 - y0) < 2:  # Horizontal line
                        h_lines.append((min(x0, x1), y0, max(x0, x1), y1))
                    elif abs(x1 - x0) < 2:  # Vertical line
                        v_lines.append((x0, min(y0, y1), x1, max(y0, y1)))
        
        # Simple table detection: Find intersections of horizontal and vertical lines
        if len(h_lines) > 2 and len(v_lines) > 2:
            # Find grid cells
            intersections = self._find_line_intersections(h_lines, v_lines)
            
            if len(intersections) > 4:  # At least a 2x2 grid
                # Extract table structure
                table = {
                    "bbox": self._calculate_table_bbox(h_lines, v_lines),
                    "rows": len(set(y for _, y in intersections)),
                    "columns": len(set(x for x, _ in intersections)),
                    "cells": self._extract_table_cells(page, intersections)
                }
                tables.append(table)
        
        return tables
    
    def _find_line_intersections(self, h_lines, v_lines):
        """Find intersections between horizontal and vertical lines"""
        intersections = []
        
        for h_x0, h_y0, h_x1, h_y1 in h_lines:
            for v_x0, v_y0, v_x1, v_y1 in v_lines:
                # Check if lines intersect
                if h_x0 <= v_x0 <= h_x1 and v_y0 <= h_y0 <= v_y1:
                    intersections.append((v_x0, h_y0))
        
        return intersections
    
    def _calculate_table_bbox(self, h_lines, v_lines):
        """Calculate the bounding box of the table"""
        h_x0 = min(line[0] for line in h_lines)
        h_x1 = max(line[2] for line in h_lines)
        v_y0 = min(line[1] for line in v_lines)
        v_y1 = max(line[3] for line in v_lines)
        
        return [h_x0, v_y0, h_x1, v_y1]
    
    def _extract_table_cells(self, page, intersections):
        """Extract cell content from a table structure"""
        # Sort intersections by row then column
        intersections.sort(key=lambda p: (p[1], p[0]))
        
        # Get unique x and y coordinates (column and row boundaries)
        x_coords = sorted(set(x for x, _ in intersections))
        y_coords = sorted(set(y for _, y in intersections))
        
        # Extract cell content
        cells = []
        
        for i in range(len(y_coords) - 1):
            row = []
            for j in range(len(x_coords) - 1):
                # Cell boundaries
                cell_x0, cell_y0 = x_coords[j], y_coords[i]
                cell_x1, cell_y1 = x_coords[j+1], y_coords[i+1]
                
                # Extract text within cell boundaries
                cell_text = page.get_text("text", clip=[cell_x0, cell_y0, cell_x1, cell_y1])
                
                row.append({
                    "text": cell_text.strip(),
                    "bbox": [cell_x0, cell_y0, cell_x1, cell_y1]
                })
            
            cells.append(row)
        
        return cells
    
    def _extract_forms(self, page) -> List[Dict]:
        """Extract form fields from the page"""
        forms = []
        
        # Get forms from the page
        widgets = page.widgets()
        if widgets:
            for widget in widgets:
                form_field = {
                    "type": widget.field_type_string,
                    "name": widget.field_name,
                    "value": widget.field_value,
                    "bbox": widget.rect
                }
                forms.append(form_field)
        
        return forms
    
    def _extract_figures(self, page) -> List[Dict]:
        """Extract images and figures from the page"""
        figures = []
        
        # Extract images
        image_list = page.get_images(full=True)
        
        for img_index, img in enumerate(image_list):
            xref = img[0]
            
            try:
                # Get image properties
                base_image = page.parent.extract_image(xref)
                if base_image:
                    # Get position data from page
                    for img_bbox in page.get_image_bbox(xref):
                        figure = {
                            "image_index": img_index,
                            "bbox": list(img_bbox),
                            "width": base_image["width"],
                            "height": base_image["height"],
                            "format": base_image["ext"]
                        }
                        figures.append(figure)
            except Exception as e:
                logger.warning(f"Could not extract image {xref}: {str(e)}")
        
        return figures
