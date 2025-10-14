#!/usr/bin/env python3
"""
Hugging Face fhswf German Handwriting Dataset to Paperless-NGX Uploader

This script downloads the fhswf German handwriting dataset from Hugging Face
and uploads each handwriting sample as a document to a running Paperless-NGX instance.

Requirements:
- pip install datasets pillow requests
- A running Paperless-NGX instance
- Valid API token for Paperless-NGX

Author: Generated for neuroscience consultant workflow
"""

import os
import sys
import requests
from datasets import load_dataset
from PIL import Image
import tempfile
import uuid
import time
import json
from typing import Optional, Dict, Any
import argparse
from datetime import datetime

class PaperlessNGXUploader:
    """Handle uploads to Paperless-NGX via REST API"""

    def __init__(self, paperless_url: str, token: str):
        """
        Initialize the Paperless-NGX uploader

        Args:
            paperless_url: Base URL of your Paperless-NGX instance
            token: API token for authentication
        """
        self.paperless_url = paperless_url.rstrip('/')
        self.token = token
        self.headers = {
            'Authorization': f'Token {token}'
        }
        self.upload_endpoint = f"{self.paperless_url}/api/documents/post_document/"
        self.tasks_endpoint = f"{self.paperless_url}/api/tasks/"

    def test_connection(self) -> bool:
        """Test the connection to Paperless-NGX"""
        try:
            response = requests.get(f"{self.paperless_url}/api/", headers=self.headers)
            if response.status_code == 200:
                print("✓ Successfully connected to Paperless-NGX")
                return True
            else:
                print(f"✗ Failed to connect to Paperless-NGX: {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ Connection error: {str(e)}")
            return False

    def upload_document(self, file_path: str, title: str, text_content: str = None, 
                       tags: list = None, document_type: int = None, 
                       correspondent: int = None) -> Optional[Dict[str, Any]]:
        """
        Upload a document to Paperless-NGX

        Args:
            file_path: Path to the document file
            title: Title for the document
            text_content: Optional text content description
            tags: Optional list of tag IDs
            document_type: Optional document type ID
            correspondent: Optional correspondent ID

        Returns:
            Response data if successful, None otherwise
        """
        try:
            # Prepare the file for upload
            with open(file_path, 'rb') as file:
                # Determine content type based on file extension
                content_type = 'image/jpeg'
                if file_path.lower().endswith('.png'):
                    content_type = 'image/png'
                elif file_path.lower().endswith('.pdf'):
                    content_type = 'application/pdf'

                files = {
                    'document': (os.path.basename(file_path), file, content_type)
                }

                # Prepare form data
                data = {
                    'title': title,
                    'created': datetime.now().strftime('%Y-%m-%d')
                }

                # Add optional fields
                if document_type:
                    data['document_type'] = str(document_type)
                if correspondent:
                    data['correspondent'] = str(correspondent)
                if tags:
                    # Tags can be specified multiple times
                    for tag in tags:
                        data['tags'] = str(tag)

                # Make the upload request
                response = requests.post(
                    self.upload_endpoint,
                    headers=self.headers,
                    files=files,
                    data=data,
                    timeout=30
                )

                if response.status_code == 200:
                    result = response.json()
                    return result
                else:
                    print(f"Upload failed: {response.status_code} - {response.text}")
                    return None

        except Exception as e:
            print(f"Error uploading document: {str(e)}")
            return None

    def check_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Check the status of a consumption task"""
        try:
            response = requests.get(
                f"{self.tasks_endpoint}?task_id={task_id}",
                headers=self.headers
            )
            if response.status_code == 200:
                data = response.json()
                if data.get('results'):
                    return data['results'][0]
            return None
        except Exception as e:
            print(f"Error checking task status: {str(e)}")
            return None

def create_tags_for_dataset(uploader: PaperlessNGXUploader) -> Dict[str, int]:
    """Create relevant tags for the German handwriting dataset"""
    tags_to_create = [
        "German Handwriting",
        "FHSWF Dataset", 
        "Machine Learning",
        "Training Data",
        "Handwriting Recognition"
    ]

    created_tags = {}

    # In a real implementation, you'd call the tags API to create these
    # For now, we'll return empty dict and let users create tags manually
    print("Note: You may want to create the following tags in Paperless-NGX:")
    for tag in tags_to_create:
        print(f"  - {tag}")

    return created_tags

def process_handwriting_dataset(paperless_url: str, token: str, max_documents: int = 100,
                              start_index: int = 0, document_type: int = None,
                              correspondent: int = None, batch_size: int = 10):
    """
    Process the fhswf German handwriting dataset and upload to Paperless-NGX

    Args:
        paperless_url: Base URL of your Paperless-NGX instance
        token: API token for authentication
        max_documents: Maximum number of documents to upload
        start_index: Starting index in the dataset
        document_type: Document type ID to assign
        correspondent: Correspondent ID to assign
        batch_size: Number of documents to process in each batch
    """
    # Initialize the uploader
    uploader = PaperlessNGXUploader(paperless_url, token)

    # Test connection first
    if not uploader.test_connection():
        print("Cannot proceed without a valid connection to Paperless-NGX")
        return False

    print("Loading fhswf German handwriting dataset...")
    try:
        # Load the dataset
        dataset = load_dataset('fhswf/german_handwriting', split='train')

        print(f"Dataset loaded successfully!")
        print(f"Total samples in dataset: {len(dataset)}")
        print(f"Will process {max_documents} documents starting from index {start_index}")

        # Create suggested tags
        create_tags_for_dataset(uploader)

        # Create a temporary directory for images
        with tempfile.TemporaryDirectory() as temp_dir:
            successful_uploads = 0
            failed_uploads = 0

            # Process dataset in batches
            end_index = min(start_index + max_documents, len(dataset))

            for i in range(start_index, end_index, batch_size):
                batch_end = min(i + batch_size, end_index)
                print(f"\nProcessing batch {i//batch_size + 1}: documents {i+1} to {batch_end}")

                for j in range(i, batch_end):
                    try:
                        sample = dataset[j]

                        # Get the image and text
                        image = sample['image']  # PIL Image
                        text = sample.get('text', '').strip()

                        # Create a meaningful filename and title
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"german_handwriting_{j+1:05d}_{timestamp}.jpg"
                        temp_image_path = os.path.join(temp_dir, filename)

                        # Save image as JPEG
                        if image.mode in ('RGBA', 'LA'):
                            # Convert RGBA/LA to RGB
                            background = Image.new('RGB', image.size, (255, 255, 255))
                            if image.mode == 'RGBA':
                                background.paste(image, mask=image.split()[-1])
                            else:
                                background.paste(image)
                            image = background

                        image.save(temp_image_path, 'JPEG', quality=95)

                        # Create a meaningful title
                        if text and len(text) > 0:
                            # Use first few words as title, max 100 chars
                            words = text.split()[:10]
                            title = f"German Handwriting: {' '.join(words)}"
                            if len(title) > 100:
                                title = title[:97] + "..."
                        else:
                            title = f"German Handwriting Sample {j+1:05d}"

                        # Upload to Paperless-NGX
                        result = uploader.upload_document(
                            file_path=temp_image_path,
                            title=title,
                            text_content=text,
                            document_type=document_type,
                            correspondent=correspondent
                        )

                        if result:
                            successful_uploads += 1
                            task_id = result
                            print(f"✓ Uploaded: {title[:50]}... (Task: {task_id})")
                        else:
                            failed_uploads += 1
                            print(f"✗ Failed: {title[:50]}...")

                        # Small delay to avoid overwhelming the server
                        time.sleep(0.1)

                    except Exception as e:
                        print(f"✗ Error processing sample {j+1}: {str(e)}")
                        failed_uploads += 1
                        continue

                # Progress update after each batch
                total_processed = successful_uploads + failed_uploads
                print(f"Batch completed. Progress: {total_processed}/{max_documents} "
                      f"(Success: {successful_uploads}, Failed: {failed_uploads})")

                # Brief pause between batches
                if batch_end < end_index:
                    time.sleep(1)

            # Final summary
            print(f"\n{'='*60}")
            print(f"UPLOAD COMPLETED")
            print(f"{'='*60}")
            print(f"Total documents processed: {successful_uploads + failed_uploads}")
            print(f"Successful uploads: {successful_uploads}")
            print(f"Failed uploads: {failed_uploads}")
            print(f"Success rate: {(successful_uploads/(successful_uploads + failed_uploads)*100):.1f}%")

            if successful_uploads > 0:
                print(f"\nDocuments should appear in your Paperless-NGX instance shortly.")
                print(f"Check the Tasks page in Paperless-NGX for consumption status.")

            return successful_uploads > 0

    except Exception as e:
        print(f"Error loading or processing dataset: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Upload fhswf German handwriting dataset to Paperless-NGX",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python %(prog)s --url http://localhost:8000 --token your_token_here
  python %(prog)s --url https://paperless.example.com --token abc123 --max 25
  python %(prog)s --url http://localhost:8000 --token abc123 --start 100 --max 50
        """
    )

    parser.add_argument('--url', required=True,
                       help='Paperless-NGX base URL (e.g., http://localhost:8000)')
    parser.add_argument('--token', required=True,
                       help='Paperless-NGX API token')
    parser.add_argument('--max', type=int, default=50,
                       help='Maximum number of documents to upload (default: 50)')
    parser.add_argument('--start', type=int, default=0,
                       help='Starting index in dataset (default: 0)')
    parser.add_argument('--document-type', type=int,
                       help='Document type ID to assign to uploaded documents')
    parser.add_argument('--correspondent', type=int,
                       help='Correspondent ID to assign to uploaded documents')
    parser.add_argument('--batch-size', type=int, default=10,
                       help='Batch size for processing (default: 10)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Test connection and show what would be uploaded without uploading')

    args = parser.parse_args()

    # Validate arguments
    if not args.url.startswith(('http://', 'https://')):
        print("Error: URL must start with http:// or https://")
        sys.exit(1)

    if args.max <= 0:
        print("Error: --max must be a positive number")
        sys.exit(1)

    if args.start < 0:
        print("Error: --start must be non-negative")
        sys.exit(1)

    # Display configuration
    print("fhswf German Handwriting Dataset → Paperless-NGX Uploader")
    print("=" * 60)
    print(f"Paperless-NGX URL: {args.url}")
    print(f"API Token: {'*' * (len(args.token) - 8) + args.token[-8:] if len(args.token) > 8 else '*' * len(args.token)}")
    print(f"Documents to process: {args.max}")
    print(f"Starting index: {args.start}")
    print(f"Batch size: {args.batch_size}")
    if args.document_type:
        print(f"Document type ID: {args.document_type}")
    if args.correspondent:
        print(f"Correspondent ID: {args.correspondent}")
    print(f"Dry run: {'Yes' if args.dry_run else 'No'}")
    print()

    if args.dry_run:
        print("DRY RUN MODE: Testing connection only...")
        uploader = PaperlessNGXUploader(args.url, args.token)
        if uploader.test_connection():
            print("✓ Connection test successful!")
            print("✓ Ready to upload documents (remove --dry-run to proceed)")
        else:
            print("✗ Connection test failed!")
            sys.exit(1)
        return

    # Confirm before proceeding
    print("This script will:")
    print("1. Download the fhswf German handwriting dataset from Hugging Face")
    print("2. Convert handwriting images to JPEG format")
    print("3. Upload each image as a document to your Paperless-NGX instance")
    print("4. Use handwriting text content as document titles")
    print()

    response = input("Do you want to continue? (y/N): ")
    if response.lower() != 'y':
        print("Operation cancelled.")
        sys.exit(0)

    # Start the upload process
    success = process_handwriting_dataset(
        paperless_url=args.url,
        token=args.token,
        max_documents=args.max,
        start_index=args.start,
        document_type=args.document_type,
        correspondent=args.correspondent,
        batch_size=args.batch_size
    )

    if success:
        print("\nUpload process completed successfully!")
        sys.exit(0)
    else:
        print("\nUpload process encountered errors.")
        sys.exit(1)

if __name__ == "__main__":
    main()
