import reflex as rx
from app.states.file_state import FileState


def upload_component() -> rx.Component:
    return rx.el.div(
        rx.el.h2("Upload Files", class_name="text-lg font-medium text-gray-90 mb-4"),
        rx.upload.root(
            rx.el.div(
                rx.icon("cloud_upload", class_name="w-8 h-8 text-gray-50"),
                rx.el.p(
                    "Drag & drop files here, or click to select",
                    class_name="text-sm text-gray-60 mt-2",
                ),
                class_name="flex flex-col items-center justify-center p-8 border-2 border-dashed border-gray-30 bg-white hover:bg-gray-10 transition-colors",
            ),
            id="upload_area",
            multiple=True,
            class_name="w-full cursor-pointer",
        ),
        rx.el.div(
            rx.foreach(
                rx.selected_files("upload_area"),
                lambda file: rx.el.div(
                    rx.icon("file", class_name="w-4 h-4 text-gray-60"),
                    rx.el.span(file, class_name="text-sm text-gray-80"),
                    class_name="flex items-center gap-x-2 p-2 bg-gray-10 border border-gray-20",
                ),
            ),
            class_name="mt-4 space-y-2",
        ),
        rx.el.div(
            rx.el.button(
                "Clear",
                on_click=rx.clear_selected_files("upload_area"),
                class_name="h-10 w-full px-4 bg-gray-20 text-gray-90 font-medium hover:bg-gray-30",
            ),
            rx.el.button(
                "Upload",
                on_click=lambda: FileState.handle_upload(
                    rx.upload_files(upload_id="upload_area")
                ),
                class_name="h-10 w-full px-4 bg-blue-60 text-white font-medium hover:bg-blue-70",
            ),
            class_name="grid grid-cols-2 gap-x-4 mt-4",
        ),
        class_name="bg-gray-10 p-4 border border-gray-20",
    )