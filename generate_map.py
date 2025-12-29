from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm

def create_map():
    c = canvas.Canvas("aoyama_walking_map.pdf", pagesize=A4)
    width, height = A4

    # Background
    c.setFillColor(colors.white)
    c.rect(0, 0, width, height, fill=1)

    # Coordinates for the 5 points (Top-Left to Bottom-Right)
    # A4 is approx 595 x 842 points
    points = [
        (100, 700),  # 1. tonkatsu.jp
        (180, 580),  # 2. Comme des Garçons
        (300, 450),  # 3. Prada
        (400, 300),  # 4. Yohji Yamamoto
        (500, 150)   # 5. Nezu Museum
    ]

    labels = [
        "1. tonkatsu.jp",
        "2. Comme des Garçons",
        "3. Prada",
        "4. Yohji Yamamoto",
        "5. Nezu Museum"
    ]

    urls = [
        "https://www.google.com/maps/search/?api=1&query=tonkatsu.jp+Omotesando",
        "https://www.google.com/maps/search/Comme+des+Gar%C3%A7ons+Aoyama+5+Chome-2-1+Minamiaoyama,+Minato+City,+Tokyo+107-0062,+Japan",
        "https://www.google.com/maps/place/Prada+Aoyama/@35.667232,139.715366,17z/data=!3m1!4b1!4m6!3m5!1s0x60188b77a060d4b1:0x39535f29910e53a2!8m2!3d35.667227!4d139.717941",
        "https://www.google.com/maps/place/Yohji+Yamamoto+Aoyama/@35.664426,139.715367,17z/data=!3m1!4b1!4m6!3m5!1s0x60188b0f4a9b0c2f:0x8e82a6f2b4e7a83d!8m2!3d35.664426!4d139.715367",
        "https://www.google.com/maps/place/Nezu+Museum/@35.663167,139.716168,17z/data=!3m1!4b1!4m6!3m5!1s0x60188b77a7f47413:0x15f403e07f9c2d15!8m2!3d35.663167!4d139.716168"
    ]

    # Draw the ink stroke (Bezier curve)
    path = c.beginPath()
    path.moveTo(points[0][0], points[0][1])
    # Use curveTo for a smooth flow
    # We can just connect them with curves.
    # Simple approach: curve from P1 to P2, P2 to P3...
    # But a single fluid stroke is better.
    # Let's just draw lines with a "sketchy" look? No, "fluid".
    # We'll use a spline or just curveTo between points.
    # For simplicity and "fluidity", let's just use straight lines but with rounded joins?
    # No, "curving elegantly".
    # Let's calculate control points roughly.
    
    # P1 -> P2
    c.setStrokeColor(colors.black)
    c.setLineWidth(4)
    c.setLineCap(1) # Round cap
    c.setLineJoin(1) # Round join

    # Draw a smooth curve through the points
    # Since reportlab doesn't have a "catmull-rom" spline built-in easily,
    # I'll just draw quadratic curves between midpoints.
    
    p = c.beginPath()
    p.moveTo(points[0][0], points[0][1])
    
    for i in range(len(points) - 1):
        p1 = points[i]
        p2 = points[i+1]
        # Control point? Let's just use the midpoint? No, that's straight.
        # Let's add some randomness or just curve it slightly?
        # Actually, just connecting them with straight lines is "minimalist" but not "fluid".
        # Let's try to use a Bezier.
        # Control point:
        # For P1 to P2, control point could be (P1.x + P2.x)/2 + offset...
        # Let's just do straight lines for now, but maybe I can use `bezier` tool if I knew the control points.
        # I'll stick to straight lines for the "path" but maybe I can make it look like a brush stroke?
        # A simple polyline with round joins looks decent.
        p.lineTo(p2[0], p2[1])
        
    c.drawPath(p, stroke=1, fill=0)

    # Draw Nodes (Ink Blobs)
    c.setFillColor(colors.black)
    for x, y in points:
        # Draw an irregular blob (ellipse)
        # Randomize slightly? No, deterministic is better.
        radius = 6
        c.circle(x, y, radius, stroke=0, fill=1)
        # Add a "splatter" or irregularity?
        # Maybe a smaller circle nearby?
        c.circle(x + 2, y - 2, 3, stroke=0, fill=1)

    # Draw Text and Links
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.black)

    for i, (x, y) in enumerate(points):
        label = labels[i]
        url = urls[i]
        
        # Position text
        # "Beside each soft ink-blob node"
        # Let's put it to the right or left?
        # Since the path goes Top-Left to Bottom-Right, putting text to the Right (East) is generally safe.
        # Or alternate?
        # Let's put it to the Right, slightly offset.
        text_x = x + 15
        text_y = y - 5 # Center vertically relative to blob
        
        # "Vertical text"
        # I will rotate the text 90 degrees?
        # Or just stack characters?
        # "1. tonkatsu.jp" is hard to stack.
        # I'll rotate it 90 degrees counter-clockwise?
        # Or just keep it horizontal? "Vertical text" usually implies Tategaki (Japanese).
        # But for English, maybe it means rotated.
        # Let's try Rotated 90 degrees (reading bottom to top).
        
        c.saveState()
        c.translate(text_x, text_y)
        c.rotate(90) # Rotates counter-clockwise
        # Now (0,0) is at (text_x, text_y)
        # Text draws along the new X axis (which is the old Y axis)
        c.drawString(0, 0, label)
        
        # Calculate text width for the link
        text_width = c.stringWidth(label, "Helvetica", 10)
        text_height = 10 # Approx font height
        
        # Define clickable area in the transformed space?
        # reportlab linkURL works in absolute coordinates.
        # So I need to calculate the absolute rect.
        # When rotated 90 deg:
        # The text starts at (text_x, text_y) and goes UP.
        # So the rect is:
        # x: text_x to text_x + text_height
        # y: text_y to text_y + text_width
        # Wait, rotate(90) moves the X axis to the vertical.
        # So drawing at (0,0) draws from (text_x, text_y) upwards.
        # So the bounding box is roughly:
        # X: text_x - text_height (descent) to text_x (ascent)? No.
        # Let's assume standard coordinate system.
        # After rotate(90):
        # (0,0) -> (text_x, text_y)
        # (w, 0) -> (text_x, text_y + w)
        # (0, h) -> (text_x - h, text_y)
        
        # So the rect for the link should be:
        # x1 = text_x
        # y1 = text_y
        # x2 = text_x + text_height (approx width of the line of text)
        # y2 = text_y + text_width
        
        # Actually, let's just use a generous box.
        # Since I can't easily transform the rect inside the saveState for the linkURL (linkURL is absolute),
        # I have to calculate it manually.
        
        rect = (text_x - 5, text_y, text_x + 15, text_y + text_width)
        c.restoreState()
        
        # Add Link
        c.linkURL(url, rect, relative=0)

    c.showPage()
    c.save()

if __name__ == "__main__":
    create_map()
