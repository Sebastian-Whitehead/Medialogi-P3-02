import cv2


def writeText(media, text: str, pos: tuple, scale: int, align: str, color: tuple):
    # Make new attributes for background of the text
    fontFace, fontScale, fontColor = cv2.FONT_HERSHEY_DUPLEX, scale, (0, 0, 0)
    pos = [int(pos[0]), int(pos[1])]  # Set position to array

    if align == 'center':
        textSize = cv2.getTextSize(text, fontFace, scale, 2)
        pos = (pos[0] - int(textSize[0][0] / 2), pos[1])
    else:
        pos = (pos[0], pos[1])

    # Write the background of the text on frame
    cv2.putText(media, text, pos, fontFace, fontScale, fontColor, 2, cv2.LINE_AA)

    fontColor = color  # Change attributes to front view of text
    # Write front view of text on frame
    cv2.putText(media, text, pos, fontFace, fontScale, fontColor, 1, cv2.LINE_AA)


# Draw the threshold line with label
def drawLine(text, x, y, color, media, weight):
    h, w, _ = media.shape  # Get the height and width of the frame

    cv2.line(media, (0, y), (w, y), color, weight)  # Draw the line

    pos = (10, y - 10)  # Set the position of the text
    face, scale, thickness = cv2.FONT_HERSHEY_DUPLEX, 0.5, 1  # Set other attributes
    cv2.putText(media, text, pos, face, scale, color, thickness, cv2.LINE_AA)  # Write text on frame


# Draw the threshold lines on the frame
def drawData(media, data, direction):
    # Loop all blob datas
    for n, blob in enumerate(data):
        label = blob  # Set blob label, which is the name of the blob
        blobData = data[blob]  # Set blob data

        # Shorten variable names
        min, max = blobData['min'], blobData['max']
        offset = blobData['offset']

        """
        # Draw raw lines
        color = (0, 0, 255)
        drawLine(label + ': min', 0, min, color, media) # Min. line
        drawLine(label + ': max', 0, max, color, media) # Max. line
        """

        # Change line weight depending on direction
        upper = lower = 1
        if direction:
            upper = 3
        else:
            lower = 3

        # Draw offset lines
        color = (0, 255, 0)
        drawLine('Upper', 0, min + offset, color, media, upper)  # Min. line with offset
        drawLine('Lower', 0, max - offset, color, media, lower)  # Max. line with threshold

    return media  # Return the frame
