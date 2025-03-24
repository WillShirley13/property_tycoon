import pygame
from typing import List, Tuple, Dict, Optional, Any


# Split text into multiple lines that fit within a maximum width
def wrap_text(text: str, font: pygame.font.Font, max_width: int) -> List[str]:
    """Wrap text to fit within a certain width."""
    words = text.split(" ")
    lines = []
    current_line = []
    current_width = 0

    for word in words:
        word_width = font.size(word)[0]
        if current_width + word_width <= max_width:
            current_line.append(word)
            current_width += word_width + font.size(" ")[0]
        else:
            if current_line:  # Only add if there's something to add
                lines.append(" ".join(current_line))
            current_line = [word]
            current_width = word_width

    # Add the last line if there's anything left
    if current_line:
        lines.append(" ".join(current_line))

    # If no lines were created (e.g., single very long word), force-split the text
    if not lines:
        lines = [text]

    return lines


# Render text for a board space with appropriate orientation based on space position
def render_text_for_space(
    screen, space, text, font_size, space_type, space_width, is_corner=False
):
    # Reduce font size
    font_size_small = max(int(font_size * 0.52), 8)  # Smaller font for most text

    # Setup fonts
    try:
        bold_font = pygame.font.SysFont("Arial", font_size_small, bold=True)
        regular_font = pygame.font.SysFont("Arial", font_size_small)
    except:
        bold_font = pygame.font.SysFont(None, font_size_small, bold=True)
        regular_font = pygame.font.SysFont(None, font_size_small)

    # Parse the text for property information (name, color, price)
    property_name = text
    property_color = None
    property_price = None

    if "|" in text:
        parts = text.split("|")
        if len(parts) >= 1:
            property_name = parts[0].strip()
        if len(parts) >= 2:
            property_price = parts[1].strip()

    # Set a padding size
    padding = 5

    # Handle different space orientations
    if space_type == "corner":
        # For corner spaces, center the text
        center_x = space.centerx
        center_y = space.centery

        # Wrap long text to fit
        max_text_width = space.width - padding * 2
        name_lines = wrap_text(property_name, bold_font, max_text_width)

        # Calculate total height of wrapped text
        total_name_height = sum(bold_font.size(line)[1] for line in name_lines)

        # Start position for text
        text_y = center_y - total_name_height // 2

        # Render each line of the property name
        for line in name_lines:
            text_surface = bold_font.render(line, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(center_x, text_y))
            screen.blit(text_surface, text_rect)
            text_y += bold_font.size(line)[1]

    elif space_type == "top":
        # For top row spaces
        max_text_width = space.width - padding * 2
        name_lines = wrap_text(property_name, bold_font, max_text_width)

        # Position for vertical text orientation (bottom to top)
        x_offset = space.centerx

        # Calculate vertical positions
        total_name_height = (
            sum(bold_font.size(line)[1] for line in name_lines)
            + (len(name_lines) - 1) * 2
        )

        # Start from center for name
        y_start = space.centery - total_name_height // 2

        # Render property name (bold)
        for line in name_lines:
            text_surface = bold_font.render(line, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(x_offset, y_start))
            screen.blit(text_surface, text_rect)
            y_start += bold_font.size(line)[1] + 2

        # Render price at the bottom if it exists
        if property_price:
            price_surface = regular_font.render(property_price, True, (0, 0, 0))
            price_rect = price_surface.get_rect(
                center=(
                    space.centerx,
                    space.bottom - padding - price_surface.get_height() // 2,
                )
            )
            screen.blit(price_surface, price_rect)

    elif space_type == "right":
        # For right column spaces
        max_text_width = space.height - padding * 2  # Since text is rotated, use height
        name_lines = wrap_text(property_name, bold_font, max_text_width)

        # Position for rotated text
        y_offset = space.centery

        # Calculate horizontal positions for rotated text
        total_name_height = (
            sum(bold_font.size(line)[1] for line in name_lines)
            + (len(name_lines) - 1) * 2
        )

        # Start from center for name
        x_start = space.centerx - total_name_height // 2

        # Create a temporary surface for rotating
        for line in name_lines:
            text_surface = bold_font.render(line, True, (0, 0, 0))
            # Rotate text 90 degrees
            rotated_surface = pygame.transform.rotate(text_surface, 90)
            # Position rotated text
            rotated_rect = rotated_surface.get_rect(center=(x_start, y_offset))
            screen.blit(rotated_surface, rotated_rect)
            x_start += rotated_surface.get_width() + 2

        # Render price at the left if it exists
        if property_price:
            price_surface = regular_font.render(property_price, True, (0, 0, 0))
            rotated_price = pygame.transform.rotate(price_surface, 90)
            price_rect = rotated_price.get_rect(
                center=(
                    space.left + padding + rotated_price.get_width() // 2,
                    space.centery,
                )
            )
            screen.blit(rotated_price, price_rect)

    elif space_type == "bottom":
        # For bottom row spaces
        max_text_width = space.width - padding * 2
        name_lines = wrap_text(property_name, bold_font, max_text_width)

        # Position for normal text orientation
        y_offset = space.centery + font_size_small // 2

        # Calculate vertical positions
        total_name_height = (
            sum(bold_font.size(line)[1] for line in name_lines)
            + (len(name_lines) - 1) * 2
        )

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
            price_rect = price_surface.get_rect(
                center=(
                    space.centerx,
                    space.bottom - padding - price_surface.get_height() // 2,
                )
            )
            screen.blit(price_surface, price_rect)

    elif space_type == "left":
        # For left column spaces
        max_text_width = space.height - padding * 2  # Since text is rotated, use height
        name_lines = wrap_text(property_name, bold_font, max_text_width)

        # Position for rotated text
        y_offset = space.centery

        # Calculate horizontal positions for rotated text
        total_name_height = (
            sum(bold_font.size(line)[1] for line in name_lines)
            + (len(name_lines) - 1) * 2
        )

        # Start from center for name
        x_start = space.centerx + total_name_height // 2

        # Create a temporary surface for rotating
        for line in name_lines:
            text_surface = bold_font.render(line, True, (0, 0, 0))
            # Rotate text -90 degrees (counterclockwise)
            rotated_surface = pygame.transform.rotate(text_surface, -90)
            # Position rotated text
            rotated_rect = rotated_surface.get_rect(center=(x_start, y_offset))
            screen.blit(rotated_surface, rotated_rect)
            x_start -= rotated_surface.get_width() + 2

        # Render price at the right if it exists
        if property_price:
            price_surface = regular_font.render(property_price, True, (0, 0, 0))
            rotated_price = pygame.transform.rotate(price_surface, -90)
            price_rect = rotated_price.get_rect(
                center=(
                    space.right - padding - rotated_price.get_width() // 2,
                    space.centery,
                )
            )
            screen.blit(rotated_price, price_rect)


# Draw text to the screen with various formatting options
def draw_text(
    screen, text, position, color=(0, 0, 0), font_size=20, center=False, bold=False
):
    try:
        font = pygame.font.SysFont("Arial", font_size, bold=bold)
    except:
        font = pygame.font.SysFont(None, font_size, bold=bold)

    text_surface = font.render(text, True, color)

    if center:
        text_rect = text_surface.get_rect(center=position)
    else:
        text_rect = text_surface.get_rect(topleft=position)

    screen.blit(text_surface, text_rect)
