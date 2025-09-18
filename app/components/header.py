import reflex as rx
from app.states.file_state import FileState


def header() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.div(
                rx.icon("file-text", class_name="w-8 h-8 text-blue-60"),
                rx.el.h1(
                    "DocuManager", class_name="text-xl font-semibold text-gray-90"
                ),
                class_name="flex items-center gap-x-4",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.input(
                        placeholder="Enter Access Token...",
                        on_change=FileState.set_access_token.debounce(300),
                        class_name="h-10 w-[320px] px-4 bg-white border border-gray-30 text-gray-90 focus:outline-none focus:ring-2 focus:ring-blue-60",
                    ),
                    class_name=rx.cond(FileState.is_admin, "hidden", "block"),
                ),
                rx.el.button(
                    "Generate Token",
                    on_click=FileState.toggle_token_modal,
                    class_name="h-10 px-4 bg-blue-60 text-white font-medium hover:bg-blue-70",
                    class_name_append=rx.cond(FileState.is_admin, " block", " hidden"),
                ),
                class_name="flex items-center",
            ),
            class_name="h-16 flex items-center justify-between px-8",
        ),
        class_name="bg-gray-10 border-b border-gray-20 w-full",
    )