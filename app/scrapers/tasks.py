from ..worker import celery_app
from ..dependencies import SessionLocal
from ..models import Address, Record
from .engine import run_scraper
from .configs import SCRAPER_CONFIGS
from sqlalchemy.orm import Session
import datetime

@celery_app.task(name="scrape_address")
def scrape_address_task(address_id: str):
    """
    The main Celery task to orchestrate scraping for a single address.
    This task runs asynchronously in a Celery worker, not in the main API process.
    """
    db: Session = SessionLocal()  # Create a new, independent database session for this task
    try:
        address = db.query(Address).filter(Address.id == address_id).first()
        if not address:
            print(f"Address with ID {address_id} not found.")
            return

        print(f"Starting scraping for: {address.street_address}, {address.city}")

        # The address object needs to be converted to a simple dict for the scraper engine
        address_dict = {
            "street_address": address.street_address,
            "city": address.city,
            "state": address.state,
            "zip_code": address.zip_code,
        }

        # Iterate through all available scrapers defined in the configs
        for source_key, config in SCRAPER_CONFIGS.items():
            print(f"Running scraper for source: {source_key}")

            # Run the scraper engine with the address and the specific config for this source
            scraped_records = run_scraper(address_dict, config)

            if not scraped_records:
                print(f"No records found by scraper for source: {source_key}")
                continue

            # --- Data Normalization and Deduplication ---
            new_records_found = 0
            for record_data in scraped_records:
                # Check if a record with the same title and address already exists to prevent duplicates
                existing_record = (
                    db.query(Record)
                    .filter(
                        Record.address_id == address.id,
                        Record.title == record_data["title"],
                    )
                    .first()
                )

                if not existing_record:
                    # This is a new record, so we save it to the database
                    new_record = Record(
                        address_id=address.id,
                        source=record_data["source"],
                        record_type=record_data["record_type"],
                        title=record_data["title"],
                        summary=record_data["summary"],
                        url=record_data["url"],
                        scraped_at=datetime.datetime.utcnow(),
                    )
                    db.add(new_record)
                    db.commit()
                    db.refresh(new_record)
                    new_records_found += 1

                    # TODO: Trigger a notification task for the newly created record
                    # from app.notifications.tasks import send_notification_task
                    # send_notification_task.delay(str(new_record.id))

            print(f"Saved {new_records_found} new records for source: {source_key}")

    except Exception as e:
        print(f"An error occurred in scrape_address_task: {e}")
        # In a production environment, this error would be logged to a monitoring service
    finally:
        db.close()  # Ensure the database session is always closed to prevent connection leaks
