import pygame

def wrap_text(text, font, max_width):
    """
    Wrap text to fit within a given width.
    Returns a list of lines.
    
    Args:
        text (str): The text to wrap
        font (pygame.font.Font): The font to use for measuring text width
        max_width (int): The maximum width in pixels
        
    Returns:
        list: A list of text lines
    """
    words = text.split(' ')
    lines = []
    current_line = []
    
    for word in words:
        # Try adding the word to the current line
        test_line = ' '.join(current_line + [word])
        width, _ = font.size(test_line)
        
        if width <= max_width:
            current_line.append(word)
        else:
            # Start a new line
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    
    # Add the last line
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines

def render_text_for_space(screen, space, text, font_size, space_type, space_width, is_corner=False):
    """
    Render text for a board space with appropriate orientation.
    """
    # Reduce font size
    font_size_small = max(int(font_size * 0.6), 10)  # Smaller font for most text
    font_size_title = max(int(font_size * 0.7), 12)  # Slightly larger for property names
    
    try:
        # Try to use a nicer font if available
        regular_font = pygame.font.SysFont('Arial', font_size_small)
        bold_font = pygame.font.SysFont('Arial', font_size_title, bold=True)
    except:
        # Fall back to default font if Arial is not available
        regular_font = pygame.font.SysFont(None, font_size_small)
        bold_font = pygame.font.SysFont(None, font_size_title, bold=True)
    
    # Separate property name and price if applicable
    text_parts = text.split('$')
    property_name = text_parts[0].strip()
    property_price = f"${text_parts[1].strip()}" if len(text_parts) > 1 else ""
    
    # Adjust padding
    padding = 6
    
    if space_type == 'left':
        # For left side spaces
        max_text_width = space.height - padding * 2
        name_lines = wrap_text(property_name, bold_font, max_text_width)
        
        # Position for rotated text (90 degrees)
        x_offset = space.centerx - font_size_small // 2
        
        # Calculate vertical positions for name (will be rotated)
        total_name_height = sum(bold_font.size(line)[1] for line in name_lines) + (len(name_lines) - 1) * 2
        
        # Start from center for name
        x_start = x_offset - total_name_height // 2
        
        # Render property name (bold)
        for line in name_lines:
            text_surface = bold_font.render(line, True, (0, 0, 0))
            rotated_surface = pygame.transform.rotate(text_surface, 270)
            text_rect = rotated_surface.get_rect(center=(x_start, space.centery))
            screen.blit(rotated_surface, text_rect)
            x_start += bold_font.size(line)[1] + 2
        
        # Render price at the right edge if it exists
        if property_price:
            price_surface = regular_font.render(property_price, True, (0, 0, 0))
            rotated_price = pygame.transform.rotate(price_surface, 270)
            price_rect = rotated_price.get_rect(center=(space.right - padding - rotated_price.get_width()//2, space.centery))
            screen.blit(rotated_price, price_rect)
        
    elif space_type == 'right':
        # For right side spaces
        max_text_width = space.height - padding * 2
        name_lines = wrap_text(property_name, bold_font, max_text_width)
        
        # Position for rotated text (270 degrees)
        x_offset = space.centerx + font_size_small // 2
        
        # Calculate vertical positions for name (will be rotated)
        total_name_height = sum(bold_font.size(line)[1] for line in name_lines) + (len(name_lines) - 1) * 2
        
        # Start from center for name
        x_start = x_offset + total_name_height // 2
        
        # Render property name (bold)
        for line in name_lines:
            text_surface = bold_font.render(line, True, (0, 0, 0))
            rotated_surface = pygame.transform.rotate(text_surface, 90)
            text_rect = rotated_surface.get_rect(center=(x_start, space.centery))
            screen.blit(rotated_surface, text_rect)
            x_start -= bold_font.size(line)[1] + 2
        
        # Render price at the left edge if it exists
        if property_price:
            price_surface = regular_font.render(property_price, True, (0, 0, 0))
            rotated_price = pygame.transform.rotate(price_surface, 90)
            price_rect = rotated_price.get_rect(center=(space.left + padding + rotated_price.get_width()//2, space.centery))
            screen.blit(rotated_price, price_rect)
            
    elif space_type == 'top':
        # For top row spaces
        max_text_width = space.width - padding * 2
        name_lines = wrap_text(property_name, bold_font, max_text_width)
        
        # Position for upside-down text (rotated 180 degrees)
        y_offset = space.centery - font_size_small // 2
        
        # Calculate vertical positions for name (will be rotated)
        total_name_height = sum(bold_font.size(line)[1] for line in name_lines) + (len(name_lines) - 1) * 2
        
        # Start from center for name
        y_start = y_offset - total_name_height // 2
        
        # Render property name (bold)
        for line in name_lines:
            text_surface = bold_font.render(line, True, (0, 0, 0))
            rotated_surface = pygame.transform.rotate(text_surface, 180)
            text_rect = rotated_surface.get_rect(center=(space.centerx, y_start))
            screen.blit(rotated_surface, text_rect)
            y_start += bold_font.size(line)[1] + 2
        
        # Render price at the top if it exists
        if property_price:
            price_surface = regular_font.render(property_price, True, (0, 0, 0))
            rotated_price = pygame.transform.rotate(price_surface, 180)
            price_rect = rotated_price.get_rect(center=(space.centerx, space.top + padding + rotated_price.get_height()//2))
            screen.blit(rotated_price, price_rect)
            
    elif space_type == 'bottom':
        # For bottom row spaces
        max_text_width = space.width - padding * 2
        name_lines = wrap_text(property_name, bold_font, max_text_width)
        
        # Position for normal text orientation
        y_offset = space.centery + font_size_small // 2
        
        # Calculate vertical positions
        total_name_height = sum(bold_font.size(line)[1] for line in name_lines) + (len(name_lines) - 1) * 2
        
        # Start from center for name
        y_start = y_offset - total_name_height // 2
        
        # Render property name (bold)
        for line in name_lines:
            text_surface = bold_font.render(line, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(space.centerx, y_start))
            screen.blit(text_surface, text_rect)
            y_start += bold_font.size(line)[1] + 2
        
        # Render price at the bottom if it exists
        if property_price:
            price_surface = regular_font.render(property_price, True, (0, 0, 0))
            price_rect = price_surface.get_rect(center=(space.centerx, space.bottom - padding - price_surface.get_height()//2))
            screen.blit(price_surface, price_rect)
            
    elif space_type == 'corner':
        # For corner spaces, center text with smaller font
        corner_font_size = max(int(font_size * 0.65), 12)  # Larger than regular text but still smaller than original
        corner_font = pygame.font.SysFont('Arial', corner_font_size, bold=True)
        
        max_text_width = min(space.width, space.height) - padding * 3
        text_lines = wrap_text(text, corner_font, max_text_width)
        
        # Position text in the center of the space
        total_height = sum(corner_font.size(line)[1] for line in text_lines) + (len(text_lines) - 1) * 2
        y_start = space.centery - total_height // 2
        
        for line in text_lines:
            text_surface = corner_font.render(line, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(space.centerx, y_start))
            screen.blit(text_surface, text_rect)
            y_start += text_surface.get_height() + 2

def draw_text(screen, text, position, color=(0, 0, 0), font_size=20, center=False, bold=False):
    """
    Draw text on the screen.
    
    Args:
        screen (pygame.Surface): The surface to draw on
        text (str): The text to draw
        position (tuple): The (x, y) position to draw at
        color (tuple): The RGB color of the text
        font_size (int): The font size
        center (bool): Whether to center the text at the position
        bold (bool): Whether to make the text bold
    """
    try:
        font = pygame.font.SysFont('Arial', font_size, bold=bold)
    except:
        font = pygame.font.SysFont(None, font_size, bold=bold)
    
    text_surface = font.render(text, True, color)
    
    if center:
        text_rect = text_surface.get_rect(center=position)
    else:
        text_rect = text_surface.get_rect(topleft=position)
    
    screen.blit(text_surface, text_rect) 