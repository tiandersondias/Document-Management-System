import reflex as rx
from typing import TypedDict
import datetime
import uuid
import mimetypes
import os
import logging

UPLOAD_DIR = rx.get_upload_dir()


class File(TypedDict):
    id: str
    name: str
    upload_date: str
    size: int
    mime_type: str
    token: str


class FileState(rx.State):
    files: list[File] = []
    access_token: str = ""
    is_admin: bool = False
    view_file_url: str = ""
    show_view_modal: bool = False
    show_token_modal: bool = False

    @rx.var
    def filtered_files(self) -> list[File]:
        if self.is_admin:
            return self.files
        if not self.access_token:
            return []
        return [f for f in self.files if f["token"] == self.access_token]

    @rx.event
    async def handle_upload(self, uploaded_files: list[rx.UploadFile]):
        if not uploaded_files:
            yield rx.toast.error("No files selected for upload.")
            return
        if not self.access_token and (not self.is_admin):
            yield rx.toast.error("You need an access token to upload files.")
            return
        token_to_assign = self.access_token if not self.is_admin else "admin"
        for uploaded_file in uploaded_files:
            data = await uploaded_file.read()
            file_path = UPLOAD_DIR / uploaded_file.name
            with file_path.open("wb") as f:
                f.write(data)
            file_size = os.path.getsize(file_path)
            mime_type, _ = mimetypes.guess_type(uploaded_file.name)
            if mime_type is None:
                mime_type = "application/octet-stream"
            new_file: File = {
                "id": str(uuid.uuid4()),
                "name": uploaded_file.name,
                "upload_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                "size": file_size,
                "mime_type": mime_type,
                "token": token_to_assign,
            }
            self.files.append(new_file)
        yield rx.toast.success(f"Successfully uploaded {len(uploaded_files)} file(s).")
        yield rx.clear_selected_files("upload_area")

    @rx.event
    def generate_token(self):
        if self.is_admin:
            new_token = str(uuid.uuid4())
            self.access_token = new_token
            yield rx.set_clipboard(new_token)
            yield rx.toast.success("New token generated and copied to clipboard.")
            self.show_token_modal = False

    @rx.event
    def delete_file(self, file_id: str):
        if not self.is_admin:
            yield rx.toast.error("You do not have permission to delete files.")
            return
        file_to_delete = next((f for f in self.files if f["id"] == file_id), None)
        if file_to_delete:
            try:
                file_path = UPLOAD_DIR / file_to_delete["name"]
                if file_path.exists():
                    file_path.unlink()
                self.files = [f for f in self.files if f["id"] != file_id]
                yield rx.toast.success(f"File '{file_to_delete['name']}' deleted.")
            except Exception as e:
                logging.exception(f"Error deleting file: {e}")
                yield rx.toast.error(f"Error deleting file: {e}")

    @rx.event
    def download_file(self, filename: str):
        return rx.download(url=f"/_upload/{filename}", filename=filename)

    @rx.event
    def view_file(self, filename: str):
        self.view_file_url = f"/_upload/{filename}"
        self.show_view_modal = True

    @rx.event
    def toggle_view_modal(self):
        self.show_view_modal = not self.show_view_modal
        self.view_file_url = ""

    @rx.event
    def toggle_token_modal(self):
        self.show_token_modal = not self.show_token_modal

    @rx.event
    def set_access_token(self, token: str):
        self.access_token = token
        if token == "admin_override":
            self.is_admin = True
            self.access_token = ""
            yield rx.toast.success("Admin mode activated.")
        else:
            self.is_admin = False