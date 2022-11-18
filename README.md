# Bosch IoT Data Forwarder

this Azure function acts as a pre-processor to cleanup empty JSON elements and prepares the data in a format the IoT Central Device Bridge can consume.

Bosch IoT Data Forwarder (this here) --> IoT Central Device Bridge --> IOT Central

So, the data we receive from Brunat looks like the following JSON. 

```json
{
    "messageType": "TRACKING_INFO",
    "sendTimestamp": 1535374030719,
    "assets": [
        {
            "assetType": "4ec1e020-a9ba-11e8-a3cf-eeee0affa32e",
            "assetId": "ta_25262",
            "trackingDeviceId": "800440547311010000000025262",
            "measurements": [
                {
                    "timestamp": 1539946020,
                    "geoLocation": {
                        "longitude": 9.911,
                        "latitude": 52.322403,
                        "altitude": 2,
                        "gpsPrecision": 4
                    },
                    "temperature": {
                        "value": 27.9
                    }
                }
            ]
        }
    ]
}
```
First step is to remove empty JSON elements and convert the payload in the generel form 
```json
{
    "device": {
        "deviceId": "800440547311010000000025262",
        "modelId": "dtmi:iotDemo02:AssetTrackingTelemetryData_5yj;1"
    },
    "measurements": {
        "Tracking": {
            "lon": 9.911,
            "lat": 52.322403,
            "alt": 2
        },
        "ITemp": 27.9
    }
}
```
After the transformation the data will be forwarded to the IoT Central Device Bridge.
