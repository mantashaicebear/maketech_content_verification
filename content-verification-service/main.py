from api.verify_content import verify_content_api

if __name__ == "__main__":
    result = verify_content_api(
        business_id="B001",
        text="Buy premium engine oil for Hyundai vehicles",
        image_path=None
    )

    print(result)
