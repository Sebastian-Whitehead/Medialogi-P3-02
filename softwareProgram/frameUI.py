import cv2


# UI which is being shown on top of the video feedback

# "Space" to calculate-text in center of screen
def pressSpaceToStart(media):
    pos = (int(media.shape[1] / 2), int(media.shape[0] / 2))  # Position center of screen
    writeText(media, '"Space" to calculate', pos, 1, 'center', (255, 255, 255))  # Write on screen
    return media  # Return the updated frame


# Write text on frame in specific position and alginment
def writeText(media, text: str, pos: tuple, scale: int, align: str, color: tuple):
    # Make new attributes for background of the text
    fontFace, fontScale, fontColor = cv2.FONT_HERSHEY_DUPLEX, scale, (0, 0, 0)
    pos = [int(pos[0]), int(pos[1])]  # Convert position to an array

    # Align text in center or left side
    if align == 'center':  # Align text in center
        textSize = cv2.getTextSize(text, fontFace, scale, 2)  # Get the size of text in pixels
        pos = (pos[0] - int(textSize[0][0] / 2), pos[1])  # Change x-pos of text
    else:
        pos = (pos[0], pos[1])  # Keep text aligned left

    # Write the background of the text on frame as black
    cv2.putText(media, text, pos, fontFace, fontScale, fontColor, 2, cv2.LINE_AA)
    # Write front view of text on frame
    fontColor = color  # Change color to chosen color
    cv2.putText(media, text, pos, fontFace, fontScale, fontColor, 1, cv2.LINE_AA)


# Draw a red tracking line above each tracking point
def drawTrackingLine(media, x, y, w):
    pos1 = (int(x + (w / 4)), y)  # Set left-pos of line (1/4)
    pos2 = (int(x + (w / 4) * 3), y)  # Set right-pos of line (3/4)
    cv2.line(media, pos1, pos2, (0, 0, 255), 2)  # Draw the line


# Draw the threshold line with label
def drawLine(media, text, x, y, color, weight):
    h, w, _ = media.shape  # Get the height and width of the frame
    cv2.line(media, (0, y), (w, y), color, weight)  # Draw the line

    pos = (10, y - 10)  # Set the position of the text left side above line
    face, scale, thickness = cv2.FONT_HERSHEY_DUPLEX, 0.5, 1  # Set other attributes
    cv2.putText(media, text, pos, face, scale, color, thickness, cv2.LINE_AA)  # Write text on frame


# Draw the threshold lines for each labeled blob on the frame
def drawData(media, data, direction):
    for n, blob in enumerate(data):  # Loop all blob datas
        label = blob  # Set blob label, which is the name of the blob
        blobData = data[blob]  # Set blob data

        # Shorten variable names
        min, max, offset = blobData['min'], blobData['max'], blobData['offset']

        """
        # Draw raw lines
        color = (0, 0, 255) # Set color to red
        drawLine(label + ': min', 0, min, color, media) # Min. line
        drawLine(label + ': max', 0, max, color, media) # Max. line
        """

        # Change line weight depending on direction
        upper = lower = 1  # Initilize width of both lines
        if not direction:  # Direction is false (down)
            upper = 3  # Set upper line width to 3
        else:  # Direction is true (up)
            lower = 3  # Set lower line width to 3

        # Draw offset lines
        color = (255, 0, 0)  # Set color to blue
        drawLine(media, 'Upper', 0, min + offset, color, upper)  # Min. line with offset
        drawLine(media, 'Lower', 0, max - offset, color, lower)  # Max. line with threshold

    return media  # Return the frame
