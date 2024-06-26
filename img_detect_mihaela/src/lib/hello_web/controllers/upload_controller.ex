defmodule HelloWeb.UploadController do
  use HelloWeb, :controller

  alias Hello.Uploads
  alias Hello.Uploads.Upload

  def index(conn, _params) do
    uploads = Uploads.list_uploads()
     render(conn, "index.html", uploads: uploads)
  end

  def new(conn, _params) do
    changeset = Uploads.change_upload(%Upload{})
    render(conn, "new.html", changeset: changeset)
  end

  def create(conn, %{"upload" => upload_params}) do
    File.cp(upload_params["docfile"].path, Path.absname("saveimage/#{upload_params["docfile"].filename}"))
    case Uploads.create_upload_from_plug_upload(upload_params["docfile"]) do
      {:ok, upload} ->
            conn
            |> put_flash(:info, "Upload created successfully.")
            |> redirect(to: Routes.upload_path(conn, :show, upload))
      {:error, %Ecto.Changeset{} = changeset} ->
            render(conn, "new.html", changeset: changeset)
    end
  end

  def show(conn, %{"id" => id}) do
    upload = Uploads.get_upload!(id)
    render(conn, "show.html", upload: upload)
  end

  def edit(conn, %{"id" => id}) do
    upload = Uploads.get_upload!(id)
    changeset = Uploads.change_upload(upload)
    render(conn, "edit.html", upload: upload, changeset: changeset)
  end

  def update(conn, %{"id" => id, "upload" => upload_params}) do
    upload = Uploads.get_upload!(id)

    case Uploads.update_upload(upload, upload_params) do
      {:ok, upload} ->
        conn
        |> put_flash(:info, "Upload updated successfully.")
        |> redirect(to: Routes.upload_path(conn, :show, upload))

      {:error, %Ecto.Changeset{} = changeset} ->
        render(conn, "edit.html", upload: upload, changeset: changeset)
    end
  end

  def delete(conn, %{"id" => id}) do
    upload = Uploads.get_upload!(id)
    {:ok, _upload} = Uploads.delete_upload(upload)

    conn
    |> put_flash(:info, "Upload deleted successfully.")
    |> redirect(to: Routes.upload_path(conn, :index))
  end
end
