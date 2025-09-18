import reflex as rx
from app.states.file_state import FileState


def token_modal() -> rx.Component:
    return rx.el.dialog(
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "Generate Access Token",
                    class_name="text-xl font-medium text-gray-90",
                ),
                rx.el.button(
                    rx.icon("x", class_name="w-6 h-6"),
                    on_click=FileState.toggle_token_modal,
                    class_name="p-1 rounded-full hover:bg-gray-20",
                ),
                class_name="flex justify-between items-center pb-4 border-b border-gray-20",
            ),
            rx.el.p(
                "Generate a new unique token for users to upload and access files. Share this token with authorized users.",
                class_name="py-4 text-sm text-gray-70",
            ),
            rx.el.div(
                rx.el.button(
                    "Cancel",
                    on_click=FileState.toggle_token_modal,
                    class_name="w-full h-10 px-4 bg-gray-20 text-gray-90 font-medium hover:bg-gray-30",
                ),
                rx.el.button(
                    "Generate and Copy",
                    on_click=FileState.generate_token,
                    class_name="w-full h-10 px-4 bg-blue-60 text-white font-medium hover:bg-blue-70",
                ),
                class_name="grid grid-cols-2 gap-x-4 pt-4",
            ),
            class_name="bg-white p-4 w-[448px]",
        ),
        open=FileState.show_token_modal,
        class_name="fixed inset-0 bg-black/60 open:flex items-center justify-center z-50",
    )


def view_file_modal() -> rx.Component:
    return rx.el.dialog(
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    FileState.view_file_url.split("/")[-1],
                    class_name="text-xl font-medium text-gray-90",
                ),
                rx.el.button(
                    rx.icon("x", class_name="w-6 h-6"),
                    on_click=FileState.toggle_view_modal,
                    class_name="p-1 rounded-full hover:bg-gray-20",
                ),
                class_name="flex justify-between items-center p-4 border-b border-gray-20",
            ),
            rx.el.div(
                rx.match(
                    FileState.view_file_url.split(".")[-1].lower(),
                    (
                        "png",
                        rx.image(
                            src=FileState.view_file_url,
                            class_name="max-w-full max-h-full object-contain",
                        ),
                    ),
                    (
                        "jpg",
                        rx.image(
                            src=FileState.view_file_url,
                            class_name="max-w-full max-h-full object-contain",
                        ),
                    ),
                    (
                        "jpeg",
                        rx.image(
                            src=FileState.view_file_url,
                            class_name="max-w-full max-h-full object-contain",
                        ),
                    ),
                    (
                        "gif",
                        rx.image(
                            src=FileState.view_file_url,
                            class_name="max-w-full max-h-full object-contain",
                        ),
                    ),
                    (
                        "svg",
                        rx.image(
                            src=FileState.view_file_url,
                            class_name="max-w-full max-h-full object-contain",
                        ),
                    ),
                    (
                        "pdf",
                        rx.el.iframe(
                            src=FileState.view_file_url, class_name="w-full h-full"
                        ),
                    ),
                    (
                        "txt",
                        rx.el.iframe(
                            src=FileState.view_file_url, class_name="w-full h-full"
                        ),
                    ),
                    rx.el.div(
                        rx.icon(
                            "flag_triangle_right", class_name="w-16 h-16 text-yellow-50"
                        ),
                        rx.el.p(
                            "Preview not available for this file type.",
                            class_name="mt-4 text-lg text-gray-70",
                        ),
                        rx.el.p(
                            "Please download the file to view it.",
                            class_name="text-sm text-gray-60",
                        ),
                        class_name="flex flex-col items-center justify-center h-full",
                    ),
                ),
                class_name="p-4 flex-grow h-[calc(100%-65px)] flex items-center justify-center",
            ),
            class_name="bg-gray-10 w-[80vw] h-[80vh] flex flex-col",
        ),
        open=FileState.show_view_modal,
        class_name="fixed inset-0 bg-black/60 open:flex items-center justify-center z-50",
    )