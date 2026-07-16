from __future__ import annotations

import tkinter as tk
from tkinter import messagebox

from app.services.capture_service import CaptureService
from app.services.storage_service import StoredRecord


class MainWindow:
    def __init__(self, root: tk.Tk, capture_service: CaptureService) -> None:
        self.root = root
        self.capture_service = capture_service
        self.recent_records: list[StoredRecord] = []

        self.root.title("LifeOS")
        self.root.geometry("980x640")

        self._build_layout()
        self.refresh_recent_records()

    def _build_layout(self) -> None:
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        input_frame = tk.Frame(main_frame)
        input_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        list_frame = tk.Frame(main_frame)
        list_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(12, 0))

        input_label = tk.Label(input_frame, text="Capture")
        input_label.pack(anchor=tk.W)

        self.input_text = tk.Text(input_frame, wrap=tk.WORD, height=20)
        self.input_text.pack(fill=tk.BOTH, expand=True, pady=(4, 8))

        save_button = tk.Button(input_frame, text="Save", command=self.handle_save)
        save_button.pack(anchor=tk.E)

        records_label = tk.Label(list_frame, text="Recent Records")
        records_label.pack(anchor=tk.W)

        self.records_listbox = tk.Listbox(list_frame, height=14)
        self.records_listbox.pack(fill=tk.BOTH, expand=False, pady=(4, 8))
        self.records_listbox.bind("<<ListboxSelect>>", self.handle_record_selection)

        preview_label = tk.Label(list_frame, text="Preview")
        preview_label.pack(anchor=tk.W)

        self.preview_text = tk.Text(list_frame, wrap=tk.WORD, height=18)
        self.preview_text.pack(fill=tk.BOTH, expand=True, pady=(4, 0))
        self.preview_text.configure(state=tk.DISABLED)

    def handle_save(self) -> None:
        content = self.input_text.get("1.0", tk.END).rstrip("\n")
        try:
            saved_record = self.capture_service.save_content(content)
        except ValueError as exc:
            messagebox.showwarning("LifeOS", str(exc))
            return

        self.input_text.delete("1.0", tk.END)
        self.refresh_recent_records()
        self._select_record_by_path(saved_record.path)

    def refresh_recent_records(self) -> None:
        self.recent_records = self.capture_service.list_recent_records()
        self.records_listbox.delete(0, tk.END)
        for record in self.recent_records:
            self.records_listbox.insert(tk.END, record.path.name)
        if self.recent_records:
            self.records_listbox.selection_set(0)
            self._show_preview(self.recent_records[0].content)
        else:
            self._show_preview("")

    def handle_record_selection(self, _event: tk.Event) -> None:
        selection = self.records_listbox.curselection()
        if not selection:
            return
        index = selection[0]
        if 0 <= index < len(self.recent_records):
            self._show_preview(self.recent_records[index].content)

    def _select_record_by_path(self, path) -> None:
        for index, record in enumerate(self.recent_records):
            if record.path == path:
                self.records_listbox.selection_clear(0, tk.END)
                self.records_listbox.selection_set(index)
                self.records_listbox.activate(index)
                self._show_preview(record.content)
                return

    def _show_preview(self, content: str) -> None:
        self.preview_text.configure(state=tk.NORMAL)
        self.preview_text.delete("1.0", tk.END)
        self.preview_text.insert("1.0", content)
        self.preview_text.configure(state=tk.DISABLED)
