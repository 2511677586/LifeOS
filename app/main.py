from __future__ import annotations

import tkinter as tk

from app.services.capture_service import CaptureService
from app.services.metadata_service import MetadataService
from app.services.storage_service import StorageService
from app.ui.main_window import MainWindow


def create_application() -> tuple[tk.Tk, MainWindow]:
    root = tk.Tk()
    storage_service = StorageService()
    metadata_service = MetadataService()
    capture_service = CaptureService(metadata_service=metadata_service, storage_service=storage_service)
    window = MainWindow(root=root, capture_service=capture_service)
    return root, window


def main() -> None:
    root, _window = create_application()
    root.mainloop()


if __name__ == "__main__":
    main()
