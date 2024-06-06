defmodule Hello.Uploads do
  @moduledoc """
  The Uploads context.
  """

  import Ecto.Query, warn: false
  alias Hello.Repo

  alias Hello.Uploads.Upload

  @doc """
  Returns the list of uploads.

  ## Examples

      iex> list_uploads()
      [%Upload{}, ...]

  """
  def list_uploads do
    Repo.all(Upload)
  end

  @doc """
  Gets a single upload.

  Raises `Ecto.NoResultsError` if the Upload does not exist.

  ## Examples

      iex> get_upload!(123)
      %Upload{}

      iex> get_upload!(456)
      ** (Ecto.NoResultsError)

  """
  def get_upload!(id), do: Repo.get!(Upload, id)

  @doc """
  Creates a upload.

  ## Examples

      iex> create_upload(%{field: value})
      {:ok, %Upload{}}

      iex> create_upload(%{field: bad_value})
      {:error, %Ecto.Changeset{}}

  """
  def create_upload(attrs \\ %{}) do
    %Upload{}
    |> Upload.changeset(attrs)
    |> Repo.insert()
  end

  def sha256(chunks_enum) do
    chunks_enum
    |> Enum.reduce(
        :crypto.hash_init(:sha256),
        &(:crypto.hash_update(&2, &1))
    )
    |> :crypto.hash_final()
    |> Base.encode16()
    |> String.downcase()
  end

 @upload_directory Application.get_env(:hello, :saveimage)

  # def local_path(id, filename) do
  #   [@upload_directory, "#{id}-#{filename}"]
  #   |> Path.join()
  # end

  def create_upload_from_plug_upload(%Plug.Upload{
    filename: filename,
    path: tmp_path,
    content_type: content_type
  }) do

    hash =
      File.stream!(tmp_path, [], 2048)
      |> sha256()

    with {:ok, %File.Stat{size: size}} <- File.stat(tmp_path),
      {:ok, upload} <-
        %Upload{} |> Upload.changeset(%{
          filename: filename, content_type: content_type,
          hash: hash, size: size })
        |> Repo.insert()

      # :ok <- File.cp(
      #     tmp_path,
      #      local_path(upload.id, filename)
      #  )
       do

        {:ok, upload}

      else

        {:error, reason}=error -> error

      end

  end

  @doc """
  Updates a upload.

  ## Examples

      iex> update_upload(upload, %{field: new_value})
      {:ok, %Upload{}}

      iex> update_upload(upload, %{field: bad_value})
      {:error, %Ecto.Changeset{}}

  """
  def update_upload(%Upload{} = upload, attrs) do
    upload
    |> Upload.changeset(attrs)
    |> Repo.update()
  end

  @doc """
  Deletes a upload.

  ## Examples

      iex> delete_upload(upload)
      {:ok, %Upload{}}

      iex> delete_upload(upload)
      {:error, %Ecto.Changeset{}}

  """
  def delete_upload(%Upload{} = upload) do
    Repo.delete(upload)
  end

  @doc """
  Returns an `%Ecto.Changeset{}` for tracking upload changes.

  ## Examples

      iex> change_upload(upload)
      %Ecto.Changeset{data: %Upload{}}

  """
  def change_upload(%Upload{} = upload, attrs \\ %{}) do
    Upload.changeset(upload, attrs)
  end
end
