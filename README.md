# Hugging Face German Handwriting Dataset → Paperless-NGX Uploader

This Python script downloads the [fhswf German handwriting dataset](https://huggingface.co/datasets/fhswf/german_handwriting) from Hugging Face and uploads each handwritten document sample to a running Paperless-NGX instance via the REST API.

## Features

- ✅ **Batch Processing**: Upload documents in configurable batches with progress tracking
- ✅ **Error Handling**: Robust error handling with detailed logging and retry mechanisms  
- ✅ **Connection Testing**: Validate Paperless-NGX connectivity before starting uploads
- ✅ **Flexible Configuration**: Command-line arguments for all major settings
- ✅ **Image Processing**: Automatic conversion to JPEG format with quality optimization
- ✅ **Metadata Extraction**: Uses handwriting text content as document titles
- ✅ **API Integration**: Proper multipart/form-data requests with authentication
- ✅ **Dry Run Mode**: Test without actually uploading documents

## Dataset Information

The **fhswf German handwriting dataset** contains approximately 10,000 handwriting samples from 15 different people, created as part of a handwriting recognition project at FH-SWF (Fachhochschule Südwestfalen). Each sample includes:

- **Image**: Handwritten text sample (various formats)
- **Text**: Ground truth transcription of the handwriting
- **Source**: Academic transcripts from school and university materials

## Requirements

### Python Dependencies
```bash
pip install datasets pillow requests
```

### System Requirements
- Python 3.7+
- Internet connection (for Hugging Face dataset download)
- Running Paperless-NGX instance with API access

### Paperless-NGX Setup
1. **API Token**: Generate an API token in your Paperless-NGX web interface:
   - Click your username (top right) → "My Profile"
   - Click the circular arrow icon to generate/regenerate token
   - Copy the token for use with this script

2. **Optional**: Create relevant tags, document types, and correspondents in Paperless-NGX for better organization

## Installation

1. **Clone or download** the script:
   ```bash
   wget https://example.com/upload_german_handwriting_to_paperless.py
   # or copy the script content to a local file
   ```

2. **Install dependencies**:
   ```bash
   pip install datasets pillow requests
   ```

3. **Make executable** (optional):
   ```bash
   chmod +x upload_german_handwriting_to_paperless.py
   ```

## Usage

### Basic Usage
```bash
python upload_german_handwriting_to_paperless.py \
    --url http://localhost:8000 \
    --token YOUR_API_TOKEN_HERE
```

### Advanced Usage
```bash
python upload_german_handwriting_to_paperless.py \
    --url https://paperless.yourdomain.com \
    --token abc123def456 \
    --max 100 \
    --start 50 \
    --batch-size 20 \
    --document-type 5 \
    --correspondent 3
```

### Command-Line Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--url` | ✅ | - | Paperless-NGX base URL (e.g., `http://localhost:8000`) |
| `--token` | ✅ | - | Paperless-NGX API authentication token |
| `--max` | ❌ | 50 | Maximum number of documents to upload |
| `--start` | ❌ | 0 | Starting index in the dataset (for resuming uploads) |
| `--batch-size` | ❌ | 10 | Number of documents to process per batch |
| `--document-type` | ❌ | - | Document type ID to assign to uploads |
| `--correspondent` | ❌ | - | Correspondent ID to assign to uploads |
| `--dry-run` | ❌ | False | Test connection without uploading documents |

### Examples

**Test connection:**
```bash
python upload_german_handwriting_to_paperless.py \
    --url http://localhost:8000 \
    --token your_token \
    --dry-run
```

**Upload first 25 documents:**
```bash
python upload_german_handwriting_to_paperless.py \
    --url http://localhost:8000 \
    --token your_token \
    --max 25
```

**Resume upload from document 100:**
```bash
python upload_german_handwriting_to_paperless.py \
    --url http://localhost:8000 \
    --token your_token \
    --start 100 \
    --max 50
```

## How It Works

1. **Connection Test**: Validates API connectivity to Paperless-NGX
2. **Dataset Loading**: Downloads the fhswf German handwriting dataset from Hugging Face
3. **Image Processing**: Converts images to JPEG format with quality optimization
4. **Document Upload**: Posts each image to Paperless-NGX with metadata:
   - **Title**: Derived from handwriting text content (first ~10 words)
   - **Created Date**: Current date
   - **Optional**: Document type, correspondent, tags
5. **Progress Tracking**: Real-time progress updates and batch processing
6. **Error Handling**: Continues processing even if individual uploads fail

## Expected Output

```
fhswf German Handwriting Dataset → Paperless-NGX Uploader
============================================================
Paperless-NGX URL: http://localhost:8000
API Token: ********abc123
Documents to process: 50
Starting index: 0
Batch size: 10

✓ Successfully connected to Paperless-NGX
Loading fhswf German handwriting dataset...
Dataset loaded successfully!
Total samples in dataset: 10854

Processing batch 1: documents 1 to 10
✓ Uploaded: German Handwriting: Terminvorschlag bis... (Task: uuid-here)
✓ Uploaded: German Handwriting: Module an Michael... (Task: uuid-here)
...

============================================================
UPLOAD COMPLETED
============================================================
Total documents processed: 50
Successful uploads: 48
Failed uploads: 2
Success rate: 96.0%
```

## Troubleshooting

### Common Issues

1. **Authentication Failed**
   - Verify your API token is correct and not expired
   - Check that the token has sufficient permissions

2. **Connection Refused**
   - Ensure Paperless-NGX is running and accessible
   - Verify the URL format (include `http://` or `https://`)
   - Check firewall settings

3. **Upload Failures**
   - Check Paperless-NGX logs for detailed error messages
   - Verify disk space on Paperless-NGX server
   - Confirm file format support in Paperless-NGX

4. **Dataset Download Issues**
   - Ensure stable internet connection
   - Check Hugging Face service status
   - Verify sufficient local disk space (~2GB for dataset)

### Performance Tips

- **Batch Size**: Reduce `--batch-size` if experiencing timeouts
- **Network**: Use wired connection for large uploads
- **Resources**: Ensure adequate RAM (>4GB recommended)
- **Concurrent**: Avoid running multiple instances simultaneously

## Security Considerations

- **API Token**: Never commit tokens to version control
- **Network**: Use HTTPS for production Paperless-NGX instances
- **Access**: Limit API token permissions to minimum required
- **Backup**: Consider backing up Paperless-NGX before bulk uploads

## Integration with Digital Health Workflows

This script is particularly useful for digital health and medical research applications:

- **Medical Handwriting Recognition**: Training datasets for medical prescription analysis
- **Clinical Notes Digitization**: Converting handwritten clinical notes to searchable documents
- **Research Data Management**: Organizing handwriting samples for neuroscience research
- **Document Workflow Automation**: Part of larger medical document processing pipelines

## License

This script is provided as-is for educational and research purposes. Please respect the licensing terms of:
- The fhswf German handwriting dataset
- Paperless-NGX software
- Required Python libraries

## Contributing

Improvements and bug fixes are welcome! Areas for enhancement:
- Add support for custom field mapping
- Implement resume functionality with state persistence
- Add support for additional Hugging Face datasets
- Enhance error recovery mechanisms

## Related Resources

- [Paperless-NGX Documentation](https://docs.paperless-ngx.com/)
- [Paperless-NGX API Reference](https://docs.paperless-ngx.com/api/)
- [fhswf German Handwriting Dataset](https://huggingface.co/datasets/fhswf/german_handwriting)
- [Hugging Face Datasets Library](https://huggingface.co/docs/datasets/)

---

*Script developed for neuroscience consulting workflows - optimized for digital health applications.*
