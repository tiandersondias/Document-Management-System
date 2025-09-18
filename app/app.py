import reflex as rx
from app.states.file_state import FileState
from app.components.header import header
from app.components.upload_component import upload_component
from app.components.file_list import file_list
from app.components.modals import token_modal, view_file_modal


def index() -> rx.Component:
    return rx.el.div(
        header(),
        rx.el.main(
            rx.el.div(
                rx.el.div(
                    upload_component(), class_name="w-full lg:w-[384px] flex-shrink-0"
                ),
                rx.el.div(file_list(), class_name="flex-grow"),
                class_name="flex flex-col lg:flex-row gap-8 p-8",
            ),
            class_name="max-w-[1536px] mx-auto w-full",
        ),
        token_modal(),
        view_file_modal(),
        class_name="min-h-screen bg-white font-['IBM_Plex_Sans']",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, title="Gremac DocuManager")