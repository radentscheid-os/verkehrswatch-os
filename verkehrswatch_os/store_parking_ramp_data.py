import os
import traceback
from urllib.parse import urljoin

from base import mail
from base.config import BASE_URL, UTILIZATION_URL, EMAIL_ERROR_MESSAGE
from parking.parking_ramps import get_ramps_overview, get_ramps_utilization
from parking.database import write_ramp_utilization_to_db, write_ramps_details_to_db


def main():
    try:
        ramps_details = get_ramps_overview(BASE_URL, onlyOsna=False)
        write_ramps_details_to_db(ramps_details)
        ramp_utilization = get_ramps_utilization(urljoin(BASE_URL, UTILIZATION_URL))
        write_ramp_utilization_to_db(ramp_utilization, ramps_details)
    except Exception as e:
        print(traceback.format_exc())
        mail.send_email(EMAIL_ERROR_MESSAGE.format(
            script=os.path.basename(__file__),
            error=e,
            traceback=traceback.format_exc()
            )
        )

if __name__ == "__main__":
    main()
