package pdef.rest;

import java.net.HttpURLConnection;

/** Simple REST response, which decouples the REST client/server from the transport.
 * The latter can be servlets, Netty, etc.
 *
 * The response contains an HTTP status code, a decoded content string, and a content type.
 */
public class RestResponse {
	private int status;
	private String content;
	private String contentType;

	public RestResponse() {}

	public int getStatus() {
		return status;
	}

	public RestResponse setStatus(final int status) {
		this.status = status;
		return this;
	}

	public RestResponse setOkStatus() {
		this.status = HttpURLConnection.HTTP_OK;
		return this;
	}

	public boolean hasOkStatus() {
		return status == HttpURLConnection.HTTP_OK;
	}

	public String getContent() {
		return content;
	}

	public RestResponse setContent(final String content) {
		this.content = content;
		return this;
	}

	public String getContentType() {
		return contentType;
	}

	public RestResponse setContentType(final String contentType) {
		this.contentType = contentType;
		return this;
	}

	public RestResponse setTextContentType() {
		this.contentType = Rest.TEXT_CONTENT_TYPE;
		return this;
	}

	public RestResponse setJsonContentType() {
		this.contentType = Rest.JSON_CONTENT_TYPE;
		return this;
	}

	public boolean hasJsonContentType() {
		return contentType != null && contentType.toLowerCase()
				.startsWith(Rest.JSON_MIME_TYPE);
	}

	@Override
	public boolean equals(final Object o) {
		if (this == o) return true;
		if (o == null || getClass() != o.getClass()) return false;

		final RestResponse response = (RestResponse) o;

		if (status != response.status) return false;
		if (content != null ? !content.equals(response.content) : response.content != null)
			return false;
		if (contentType != null ? !contentType.equals(response.contentType)
		                        : response.contentType != null) return false;

		return true;
	}

	@Override
	public int hashCode() {
		int result = status;
		result = 31 * result + (content != null ? content.hashCode() : 0);
		result = 31 * result + (contentType != null ? contentType.hashCode() : 0);
		return result;
	}
}
