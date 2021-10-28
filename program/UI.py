import cv2

def writeText(media, text, pos, scale, align):
    # Make new attributes for background of the text
    fontFace, fontScale, fontColor, thickness = cv2.FONT_HERSHEY_DUPLEX, scale, (0, 0, 0), 2
    pos = [int(pos[0]), int(pos[1])]

    if align == 'center':
        textSize = cv2.getTextSize(text, fontFace, scale, thickness)
        pos = (pos[0] - int(textSize[0][0] / 2), pos[1])
    else:
        pos = (pos[0], pos[1])

    # Write the background of the text on frame
    cv2.putText(media, text, pos, fontFace, fontScale, fontColor, thickness, cv2.LINE_AA)
    # Change attributes to front view of text
    fontColor, thickness = (255, 255, 255), 1
    # Write front view of text on frame
    cv2.putText(media, text, pos, fontFace, fontScale, fontColor, thickness, cv2.LINE_AA)

# Draw the threshold line with label
def drawLine(text, x, y, color, media):
    h, w, _ = media.shape  # Get the height and width of the frame

    cv2.line(media, (0, y), (w, y), color)  # Draw the line

    pos = (10, y - 10)  # Set the position of the text
    face, scale, thickness = cv2.FONT_HERSHEY_DUPLEX, 0.5, 1  # Set other attributes
    cv2.putText(media, text, pos, face, scale, color, thickness, cv2.LINE_AA)  # Write text on frame

# Draw the threshold lines on the frame
def drawData(media, data):

    # Loop all blob datas
    for n, blob in enumerate(data):
        label = blob  # Set blob label, which is the name of the blob
        blobData = data[blob]  # Set blob data

        min = blobData['min']
        max = blobData['max']
        offset = blobData['offset']

        """
        # Draw raw lines
        color = (0, 0, 255)
        drawLine(label + ': min', 0, min, color, media) # Min. line
        drawLine(label + ': max', 0, max, color, media) # Max. line
        """

        # Draw offset lines
        color = (0, 255, 0)
        drawLine(label + ': min', 0, min + offset, color, media)  # Min. line with offset
        drawLine(label + ': max', 0, max - offset, color, media)  # Max. line with threshold

    return media  # Return the frame