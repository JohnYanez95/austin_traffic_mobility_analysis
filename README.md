# Data Sources
- Camera Traffic Counts
    - https://data.austintexas.gov/Transportation-and-Mobility/Camera-Traffic-Counts/sh59-i6y9/about_data
- Traffic Detectors
    - https://data.austintexas.gov/Transportation-and-Mobility/Traffic-Detectors/qpuw-8eeb/about_data
- Radar Traffic Counts
    - https://data.austintexas.gov/Transportation-and-Mobility/Radar-Traffic-Counts/i626-g7ub/about_data
- Bluetooth Travel Sensors - Individual Address Files (IAFs) 
    - https://data.austintexas.gov/Transportation-and-Mobility/Bluetooth-Travel-Sensors-Individual-Address-Files-/qnpj-zrb9/data
- Bluetooth Travel Sensors - Individual Traffic Match Files (ITMF) 
    - https://data.austintexas.gov/Transportation-and-Mobility/Bluetooth-Travel-Sensors-Individual-Traffic-Match-/x44q-icha/data
- Bluetooth Travel Sensors - Traffic Match Summary Records (TMSR)
    - https://data.austintexas.gov/Transportation-and-Mobility/Bluetooth-Travel-Sensors-Traffic-Match-Summary-Rec/v7zg-5jg9/about_data

## Bluetooth Travel Sensors - Individual Address Files (IAFs)
Each row in this dataset represents a Bluetooth device that was detected by one of the sensors. Each record contains a detected device’s anonymized Media Access Control (MAC) address along with the time and location the device was detected. These records alone are not traffic data but can be post-processed to measure the movement of detected devices through the roadway network

### Column Descriptions

        record_id: 
            The unique record identifer generated as an MD5 hash of the row contents
        host_read_time:
            The timestamp on the host server when the device address was received. By default, this is the timestamp used in travel time estimation.
        field_device_read_time:
            The timestamp of the field device when the address was received. By default, this is not used in travel time estimation.
        reader_identifier:
            The unique identifier of the sensor that the Bluetooth device address record originated from.
        device_address:
            The unique address of the device that was read by the sensor. For security, the source MAC address is discarded and replaced with a random address.

## Bluetooth Travel Sensors - Individual Traffic Match Files (ITMF) 
Each row in this dataset represents one Bluetooth enabled device that was detected at two locations in the roadway network. Each record contains a detected device’s anonymized Media Access Control (MAC) address along with information about origin and destination points at which the device was detected, as well the time, date, and distance traveled.

### Column Descriptions

        record_id:
            The unique record identifer generated as an MD5 hash of the row contents
        device_address:
            The unique address of the device that was read by the field software. For security, the source MAC address is discarded and replaced with a random address.
        origin_reader_identifier:
            The unique identifier assigned to origin sensor that recorded a device address match.
        destination_reader_identifier:
            The unique identifier assigned to destination sensor that recorded a device address match.
        start_time:
            The time the device address was recorded at the origin sensor.
        end_time:
            The time the device address was recorded at the destination sensor.
        day_of_week:
            The name of the day of the week at the time the device address was recorded at the origin sensor.
        travel_time_seconds:
            The travel time in seconds from the origin to the destination sensor.
        speed_miles_per_hour:
            The speed in miles per hour between the origin and the destination sensors.
        match_validity:
            Indicates whether the sensor server classified the traffic data sample as being valid or invalid based on the filtering algorithm and minimum/maximum allowable speeds applied to the roadway segment. Values are valid or invalid.
        filter_identifier:
            The numeric code of the filtering algorithm used in the outlier filter for the roadway segment. See the host documentation section titled “Algorithm Configuration” for more information.