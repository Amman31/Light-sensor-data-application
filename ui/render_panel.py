"""
Description: This is the visual display panel that shows the current background image
depending on the light intensity, time of day and situations.
Author: Mohammad Amman, Modified by: Thet Htar Zin
Reviewed by: Salek MD PEASH BEEN, Thet Htar Zin
Date: 26 May 2025
Last Updated: 27 May 2025

"""
# import necessary modules for UI components
from PyQt6.QtWidgets import QFrame, QLabel, QGraphicsOpacityEffect, QSizePolicy
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QPixmap


class RenderPanel(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("renderPanel")
        self.setFrameStyle(QFrame.Shape.StyledPanel)
        self.image_description = "banner"
        self.LCU_light_intensity = 1

        # Prevent this widget from changing layout size hints
        self.setMinimumSize(1, 1)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Background label
        self.background_label = QLabel(self)
        self.background_label.setObjectName("backgroundLabel")
        self.background_label.setScaledContents(True)
        self.background_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.background_label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)

        # Fade-in overlay label
        self.fade_label = QLabel(self)
        self.fade_label.setScaledContents(True)
        self.fade_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.fade_label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.fade_label.setVisible(False)

        # Initial background image
        self.set_background_image(f"assets/images/{self.image_description}_{self.LCU_light_intensity}.jpg")

    # This method is called when the widget is resized to ensure the labels cover the entire panel.
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.background_label.setGeometry(self.rect())
        self.fade_label.setGeometry(self.rect())

    # Method to set the background image without animation
    def set_background_image(self, image_path):
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            print(f"Warning: Could not load image at {image_path}")
            pixmap = QPixmap("assets/images/default_background.jpg") #Fallback image incase of error

        self.background_label.setPixmap(pixmap.scaled(
            self.size(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        ))

    # Method to update the image with a fade-in effect
    def update_image(self, image_description, lcu_light_intensity):
        self.image_description = image_description
        self.LCU_light_intensity = lcu_light_intensity
        image_path = f"assets/images/{self.image_description}_{self.LCU_light_intensity}.jpg"

        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            print(f"Warning: Could not load image at {image_path}")
            pixmap = QPixmap("assets/images/default_background.jpg")

        # Prepare fade label
        self.fade_label.setPixmap(pixmap.scaled(
            self.size(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        ))
        self.fade_label.setVisible(True)
        self.fade_label.raise_()

        # Apply fade-in effect
        opacity_effect = QGraphicsOpacityEffect(self.fade_label)
        self.fade_label.setGraphicsEffect(opacity_effect)

        animation = QPropertyAnimation(opacity_effect, b"opacity", self)
        animation.setDuration(1000) # 1 second duration for fade-in, can change as needed
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

        # After animation completes, update background and hide overlay
        def on_animation_finished():
            self.set_background_image(image_path)
            self.fade_label.setVisible(False)
            self.fade_label.setGraphicsEffect(None)

        animation.finished.connect(on_animation_finished)
        animation.start()
        self._animation = animation  # Keep a reference
