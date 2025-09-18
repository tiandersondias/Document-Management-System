import reflex as rx
from app.states.file_state import FileState


def get_file_icon(mime_type: rx.Var[str]) -> rx.Component:
    return rx.match(
        mime_type.split("/")[0],
        ("image", rx.icon("image", class_name="w-5 h-5 text-blue-60")),
        (
            "application",
            rx.cond(
                mime_type.contains("pdf"),
                rx.icon("file-text", class_name="w-5 h-5 text-red-60"),
                rx.icon("file-code", class_name="w-5 h-5 text-gray-60"),
            ),
        ),
        ("text", rx.icon("file-type", class_name="w-5 h-5 text-green-60")),
        ("video", rx.icon("video", class_name="w-5 h-5 text-purple-60")),
        ("audio", rx.icon("volume-2", class_name="w-5 h-5 text-orange-60")),
        rx.icon("file", class_name="w-5 h-5 text-gray-50"),
    )


def format_size(size_bytes: rx.Var[int]) -> rx.Var[str]:
    return rx.cond(
        size_bytes < 1024,
        size_bytes.to_string() + " B",
        rx.cond(
            size_bytes < 1024 * 1024,
            (size_bytes / 1024).to_string() + " KB",
            (size_bytes / (1024 * 1024)).to_string() + " MB",
        ),
    )


def file_list() -> rx.Component:
    return rx.el.div(
        rx.el.h2("My Files", class_name="text-lg font-medium text-gray-90 mb-4"),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "File Name",
                            class_name="text-left font-medium text-sm text-gray-60 p-4",
                        ),
                        rx.el.th(
                            "Size",
                            class_name="text-left font-medium text-sm text-gray-60 p-4",
                        ),
                        rx.el.th(
                            "Date Uploaded",
                            class_name="text-left font-medium text-sm text-gray-60 p-4",
                        ),
                        rx.el.th(
                            "Actions",
                            class_name="text-right font-medium text-sm text-gray-60 p-4",
                        ),
                    ),
                    class_name="border-b border-gray-20 bg-gray-10",
                ),
                rx.el.tbody(
                    rx.foreach(
                        FileState.filtered_files,
                        lambda file: rx.el.tr(
                            rx.el.td(
                                rx.el.div(
                                    get_file_icon(file["mime_type"]),
                                    rx.el.span(file["name"], class_name="truncate"),
                                    class_name="flex items-center gap-x-3",
                                ),
                                class_name="p-4 text-sm text-gray-90",
                            ),
                            rx.el.td(
                                format_size(file["size"]),
                                class_name="p-4 text-sm text-gray-70",
                            ),
                            rx.el.td(
                                file["upload_date"],
                                class_name="p-4 text-sm text-gray-70",
                            ),
                            rx.el.td(
                                rx.el.div(
                                    rx.el.button(
                                        rx.icon("eye", class_name="w-4 h-4"),
                                        on_click=lambda: FileState.view_file(
                                            file["name"]
                                        ),
                                        class_name="p-2 text-gray-60 hover:bg-gray-20",
                                    ),
                                    rx.el.button(
                                        rx.icon("download", class_name="w-4 h-4"),
                                        on_click=lambda: FileState.download_file(
                                            file["name"]
                                        ),
                                        class_name="p-2 text-gray-60 hover:bg-gray-20",
                                    ),
                                    rx.el.button(
                                        rx.icon("trash-2", class_name="w-4 h-4"),
                                        on_click=lambda: FileState.delete_file(
                                            file["id"]
                                        ),
                                        class_name="p-2 text-red-60 hover:bg-red-10",
                                        class_name_append=rx.cond(
                                            FileState.is_admin, " flex", " hidden"
                                        ),
                                    ),
                                    class_name="flex items-center justify-end gap-x-2",
                                ),
                                class_name="p-4",
                            ),
                            class_name="border-b border-gray-20 hover:bg-gray-10 transition-colors",
                        ),
                    )
                ),
            ),
            rx.cond(
                FileState.filtered_files.length() == 0,
                rx.el.div(
                    rx.icon("folder-x", class_name="w-12 h-12 text-gray-40"),
                    rx.el.p(
                        rx.cond(
                            FileState.access_token == "" & ~FileState.is_admin,
                            "Please enter an access token to see your files.",
                            "No files found. Upload some to get started!",
                        ),
                        class_name="mt-4 text-gray-60",
                    ),
                    class_name="flex flex-col items-center justify-center p-16 text-center bg-white",
                ),
                rx.fragment(),
            ),
            class_name="border border-gray-20 overflow-hidden",
        ),
        class_name="bg-white",
    )