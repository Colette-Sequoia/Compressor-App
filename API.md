# File Compressor API Documentation

## Base URL
```
http://localhost:5000
```

## Endpoints

### 1. Compress File

Compress a PDF or image file.

**Endpoint:** `/api/compress`  
**Method:** `POST`  
**Content-Type:** `multipart/form-data`

#### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| file | File | Yes | The file to compress |
| target_size | Float | No | Target file size in MB |
| quality | Integer | No | Quality level (30-100), default: 85 |

#### Example Request

**Using cURL:**
```bash
curl -X POST http://localhost:5000/api/compress \
  -F "file=@document.pdf" \
  -F "target_size=4" \
  -F "quality=85" \
  -o compressed.pdf
```

**Using Python:**
```python
import requests

url = 'http://localhost:5000/api/compress'
files = {'file': open('document.pdf', 'rb')}
data = {
    'target_size': 4,
    'quality': 85
}

response = requests.post(url, files=files, data=data)

with open('compressed.pdf', 'wb') as f:
    f.write(response.content)
```

**Using JavaScript:**
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('target_size', 4);
formData.append('quality', 85);

fetch('http://localhost:5000/api/compress', {
    method: 'POST',
    body: formData
})
.then(response => response.blob())
.then(blob => {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'compressed.pdf';
    a.click();
});
```

#### Response

**Success (200 OK):**
Returns the compressed file as a binary download.

**Headers:**
```
Content-Type: application/pdf (for PDFs) or image/jpeg (for images)
Content-Disposition: attachment; filename="compressed_file.pdf"
```

**Error (400 Bad Request):**
```json
{
    "error": "No file provided"
}
```

**Error (500 Internal Server Error):**
```json
{
    "error": "Error message description"
}
```

## Supported File Types

- **PDF:** `.pdf`
- **Images:** `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.tiff`, `.webp`

## File Size Limits

- Maximum upload size: 50 MB
- Output file can be smaller than input
- Target size is a guide, not a guarantee

## Compression Parameters

### Quality Levels

| Quality | Description | Use Case |
|---------|-------------|----------|
| 30-50 | Low quality | Maximum compression, web thumbnails |
| 51-70 | Medium quality | General web use, email attachments |
| 71-85 | Good quality | Balance of size and quality (recommended) |
| 86-95 | High quality | Professional documents, printing |
| 96-100 | Maximum quality | Minimal compression, archival |

### Target Size Behavior

- If specified, the compressor will attempt to reach the target size
- It will reduce quality and DPI iteratively to meet the target
- If target cannot be reached, it returns the best possible result
- Leave empty for automatic optimal compression

## Rate Limiting

Currently, there are no rate limits, but consider implementing them for production:

- Suggested: 100 requests per hour per IP
- Large files may take longer to process
- Consider implementing queue system for production

## Error Codes

| Code | Description |
|------|-------------|
| 400 | Bad Request - Invalid parameters or file type |
| 413 | Payload Too Large - File exceeds 50MB |
| 500 | Internal Server Error - Processing failed |

## Best Practices

1. **Always specify target_size OR quality, not both**
   - If both are provided, target_size takes priority
   
2. **Use appropriate quality levels**
   - Start with 85 and adjust based on results
   
3. **Handle timeouts**
   - Large files may take 30+ seconds
   - Implement timeout handling in your client
   
4. **Validate files client-side**
   - Check file type before uploading
   - Verify file size is under 50MB
   
5. **Implement retry logic**
   - Network issues may occur
   - Retry failed requests with exponential backoff

## Examples by Use Case

### Web Thumbnail Generation
```bash
curl -X POST http://localhost:5000/api/compress \
  -F "file=@image.jpg" \
  -F "quality=50" \
  -o thumbnail.jpg
```

### Email Attachment Optimization
```bash
curl -X POST http://localhost:5000/api/compress \
  -F "file=@document.pdf" \
  -F "target_size=3" \
  -o email_attachment.pdf
```

### Archival with Minimal Loss
```bash
curl -X POST http://localhost:5000/api/compress \
  -F "file=@important.pdf" \
  -F "quality=95" \
  -o archived.pdf
```

## Security Considerations

1. **File Validation**
   - Only allowed file types are processed
   - Filename sanitization is applied
   
2. **Temporary Files**
   - All files are deleted after processing
   - No files are stored permanently
   
3. **Size Limits**
   - 50MB maximum prevents abuse
   - Consider lowering for production
   
4. **HTTPS**
   - Use HTTPS in production
   - Never send sensitive files over HTTP

## Future API Enhancements

Planned features for future versions:

- Batch processing endpoint
- WebSocket support for progress updates
- Webhook callbacks for async processing
- API key authentication
- Usage analytics endpoint
- Comparison preview endpoint

## Support

For issues or questions about the API:
- Open an issue on GitHub
- Check existing documentation
- Review example code in the repository

---

Last updated: 2026
