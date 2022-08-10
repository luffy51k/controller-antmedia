# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present EVGCorp.NET
"""

from cerberus import Validator

from .domain import (EventLiveStream, EventVoDReady, EventEndpointFailed,
                     EventPublishTimeoutError, EventEncoderNotOpenedError)

event_action_allowed = [
    # Ant Media server calls this hook when a new live stream is started.
    'liveStreamStarted',
    # Ant Media Server calls this hook when a live stream is ended.
    'liveStreamEnded',
    # Ant Media Server calls this hook when the recording of the live stream is ended.
    'vodReady',
    # Ant Media server calls this hook when the RTMP endpoint broadcast went into the failed status.
    'endpointFailed',
    # Ant Media server calls this hook when there is a publish time out error, it generally
    # means that the server is not getting any frames.
    'publishTimeoutError',
    # Ant Media server calls this hook when the encoder can't be opened.
    'encoderNotOpenedError',
]


def validate_stream_authenticate_req(data):
    """{'name': '900075289847431794ca4d99a76d74ed', 'mode': 'live', 'queryParams': '{token=Wp8LJkWNh3}'}"""
    schema = {
        "name": {"required": True, "type": "string"},
        "mode": {"required": True, "type": "string"},
        "queryParams": {"required": True, "type": "string"},
    }
    v = Validator(schema)
    if v.validate(data):
        return True, data
    else:
        return False, v.errors


def validate_event_req(data):
    if "action" not in data:
        return False, "bad request"

    action = data["action"]
    if action not in event_action_allowed:
        return False, "bad request"

    event = None

    if action in ["liveStreamStarted", "liveStreamEnded"]:
        event = EventLiveStream(
            id=data["id"],
            action=data["action"],
            streamName=data["streamName"] if "streamName" in data else None,
            category=data["category"] if "category" in data else None,
        )

    if action == "vodReady":
        event = EventVoDReady(
            id=data["id"],
            action=data["action"],
            vodName=data["vodName"],
            vodId=data["vodId"]
        )

    if action == "endpointFailed":
        event = EventEndpointFailed(
            id=data["id"],
            action=data["action"],
            streamName=data["streamName"] if "streamName" in data else None,
            category=data["category"] if "category" in data else None,
            metadata=data["metadata"]
        )

    if action == "publishTimeoutError":
        event = EventPublishTimeoutError(
            id=data["id"],
            action=data["action"],
            streamName=data["streamName"] if "streamName" in data else None,
            category=data["category"] if "category" in data else None,
        )

    if action == "encoderNotOpenedError":
        event = EventEncoderNotOpenedError(
            id=data["id"],
            action=data["action"],
            streamName=data["streamName"] if "streamName" in data else None,
            category=data["category"] if "category" in data else None,
        )

    if event is None:
        return False, "bad request"

    return True, event


def validate_stream_req(data):
    schema = {
        "hlsViewerCount": {"required": True, "type": "number"},
        "webRTCViewerCount": {"required": True, "type": "number"},
        "rtmpViewerCount": {"required": True, "type": "number"},
        "mp4Enabled": {"required": True, "type": "number"},
        "playListItemList": {"required": True, "type": "list"},
        "name": {"required": True, "type": "string"},
        "streamId": {"required": True, "type": "string"},
        "type": {
            "required": True,
            "type": "string",
            "allowed": ["liveStream", "ipCamera", "streamSource", "VoD", "playlist"],
        },
    }

    v = Validator(schema)
    if v.validate(data):
        return True, data
    else:
        return False, v.errors


def validate_stream_bulk_req(data):
    schema = {"streams": {"required": True, "type": "list"}}
    v = Validator(schema)
    if v.validate(data):
        return True, data
    else:
        return False, v.errors


def validate_create_app_req(data):
    schema = {"name": {"required": True, "type": "string"}}
    v = Validator(schema)
    if v.validate(data):
        return True, data
    else:
        return False, v.errors


def validate_stream_history_completed_req(data):
    schema = {
        "stream_id": {"required": True, "type": "string"},
        "completed": {"required": True, "type": "number"}
    }
    v = Validator(schema)
    if v.validate(data):
        return True, data
    else:
        return False, v.errors


def validate_stream_params(data):
    """Validate stream object

    Args:
        data (dict): _description_

    Returns:
        _type_: _description_
    """
    schema = {
        "streamId": {"required": True, "type": "string"},
        "status": {
            "required": True,
            "type": "string",
            "allowed": ["finished", "broadcasting", "created"],
        },
        # The status of the playlist. It's usable if type is playlist
        "playListStatus": {
            "required": True,
            "type": "string",
            "allowed": ["finished", "broadcasting", "created"],
        },
        # the type of the stream
        "type": {
            "required": True,
            "type": "string",
            "allowed": ["liveStream", "ipCamera", "streamSource", "VoD", "playlist"],
        },
        # the publish type of the stream
        "publishType": {
            "required": True,
            "type": "string",
            "allowed": ["WebRTC", "RTMP", "Pull"],
        },
        # the name of the stream
        "name": {"required": True, "type": "string"},
        # the description of the stream
        "description": {"required": True, "type": "string"},
        # it is a video filter for the service, this value is controlled by the user,
        # default value is true in the db
        "publish": {"required": True, "type": "boolean"},
        # the date when record is created in milliseconds
        "date": {"required": True, "type": "number"},
        # the planned start date
        "plannedStartDate": {"required": True, "type": "number"},
        # the planned end date
        "plannedEndDate": {"required": True, "type": "number"},
        # the duration of the stream in milliseconds
        "duration": {"required": True, "type": "number"},
        # the list of endpoints such as Facebook, Twitter or custom RTMP endpoints
        "endPointList": {
            "required": True,
            "type": "list",
            "default": [],
            "schema": {
                "type": "dict",
                "schema": {
                    "status": {"required": False, "type": "string"},
                    "type": {"required": False, "type": "string"},
                    "broadcastId": {"required": False, "type": "string"},
                    "streamId": {"required": False, "type": "string"},
                    "rtmpUrl": {"required": False, "type": "string"},
                    "name": {"required": False, "type": "string"},
                    "endpointServiceId": {"required": False, "type": "string"},
                    "serverStreamId": {"required": False, "type": "string"},
                },
            },
        },
        # the list broadcasts of Playlist Items. This list has values when the broadcast type is playlist
        "playListItemList": {
            "required": True,
            "type": "list",
            "default": [],
            "schema": {
                "type": "dict",
                "schema": {
                    "streamUrl": {"required": False, "type": "string"},
                    "type": {"required": False, "type": "string"},
                },
            },
        },
        # the identifier of whether stream is public or not
        "publicStream": {"required": True, "type": "boolean"},
        # the identifier of whether stream is 360 or not
        "is360": {"required": True, "type": "boolean"},
        # the url that will be notified when stream is published, ended and muxing finished
        "listenerHookURL": {"required": True, "type": "string"},
        # the category of the stream
        "category": {"required": True, "type": "string"},
        # the IP Address of the IP Camera or publisher
        "ipAddr": {"required": True, "type": "string"},
        # the user name of the IP Camera
        "username": {"required": True, "type": "string"},
        # the password of the IP Camera
        "password": {"required": True, "type": "string"},
        # the quality of the incoming stream during publishing
        "quality": {"required": True, "type": "string"},
        # the speed of the incoming stream, for better quality and performance it should be around 1.00
        "speed": {"required": True, "type": "number"},
        # the stream URL for fetching stream, especially should be defined for IP Cameras or Cloud streams
        "streamUrl": {"required": True, "type": "string"},
        # the origin address server broadcasting
        "originAdress": {"required": True, "type": "string"},
        # MP4 muxing whether enabled or not for the stream,
        # 1 means enabled, -1 means disabled, 0 means no settings for the stream
        "mp4Enabled": {"required": True, "type": "number"},
        # WebM muxing whether enabled or not for the stream,
        # 1 means enabled, -1 means disabled, 0 means no settings for the stream
        "webMEnabled": {"required": True, "type": "number"},
        # the expire time in milliseconds For instance if this value is 10000 then broadcast should be
        # started in 10 seconds after it is created.If expire duration is 0, then stream will never expire
        "expireDurationMS": {"required": True, "type": "number"},
        # the RTMP URL where to publish live stream to
        "rtmpURL": {"required": True, "type": "string"},
        # is true, if a broadcast that is not added to data store through rest service
        # or management console It is false by default
        "zombi": {"required": True, "type": "boolean"},
        # the number of audio and video packets that is being pending to be encoded in the queue
        "pendingPacketSize": {"required": True, "type": "number"},
        # the number of HLS viewers of the stream
        "hlsViewerCount": {"required": True, "type": "number"},
        # the number of WebRTC viewers of the stream
        "webRTCViewerCount": {"required": True, "type": "number", "default": 0},
        # the number of RTMP viewers of the stream
        "rtmpViewerCount": {"required": True, "type": "number", "default": 0},
        # the publishing start time of the stream
        "startTime": {"required": True, "type": "number", "default": 0},
        # the received bytes until now
        "receivedBytes": {"required": True, "type": "number", "default": 0},
        # the received bytes / duration
        "bitrate": {"required": True, "type": "number", "default": 0},
        "userAgent": {"required": True, "type": "string", "default": ""},
        # latitude of the broadcasting location
        "latitude": {"required": True, "type": "string", "default": ""},
        # longitude of the broadcasting location
        "longitude": {"required": True, "type": "string", "default": ""},
        # altitude of the broadcasting location
        "altitude": {"required": True, "type": "string", "default": ""},
        # If this broadcast is a track of a WebRTC stream. This variable is Id of that stream.
        "mainTrackStreamId": {"required": True, "type": "string", "default": ""},
        # if this broadcast is main track. This variable hold sub track ids.
        "subTrackStreamIds": {
            "required": False,
            "type": "list",
            "schema": {"type": "string"},
            "default": [],
        },
        # Absolute start time in milliseconds - unix timestamp. It's used for measuring the absolute latency
        "absoluteStartTimeMs": {"required": True, "type": "number", "default": 0},
        # Number of the allowed maximum WebRTC viewers for the broadcast
        "webRTCViewerLimit": {"required": True, "type": "number", "default": 0},
        # Number of the allowed maximum HLS viewers for the broadcast
        "hlsViewerLimit": {"required": True, "type": "number", "default": 0},
        # Name of the subfolder that will contain stream files
        "subFolder": {"required": True, "type": "string", "default": ""},
        # Current playing index for playlist types
        "currentPlayIndex": {"required": True, "type": "number", "default": 0},
        # Meta data filed for the custom usage
        "metaData": {"required": True, "type": "string", "default": ""},
    }

    v = Validator(schema)
    if v.validate(data):
        return True, data
    else:
        return False, v.errors


def validate_app_settings_params(data):
    schema = {
        "encoderSettingsString": {"required": False, "type": "string", "default": "[]"},
        "uploadExtensionsToS3": {"required": False, "type": "number", "default": 7},
        "s3StorageClass": {"required": False, "type": "string", "default": "STANDARD"},
        "endpointHealthCheckPeriodMs": {
            "required": False,
            "type": "number",
            "default": 2000,
        },
        "endpointRepublishLimit": {"required": False, "type": "number", "default": 3},
        "dashSegDuration": {"required": False, "type": "string", "default": "6"},
        "dashFragmentDuration": {"required": False, "type": "string", "default": "0.5"},
        "targetLatency": {"required": False, "type": "string", "default": "3.5"},
        "dashWindowSize": {"required": False, "type": "string", "default": "5"},
        "dashExtraWindowSize": {"required": False, "type": "string", "default": "5"},
        "lLDashEnabled": {"required": False, "type": "boolean", "default": True},
        "lLHLSEnabled": {"required": False, "type": "boolean", "default": False},
        "hlsEnabledViaDash": {"required": False, "type": "boolean", "default": False},
        "useTimelineDashMuxing": {
            "required": False,
            "type": "boolean",
            "default": False,
        },
        "webRTCEnabled": {"required": False, "type": "boolean", "default": True},
        "useOriginalWebRTCEnabled": {
            "required": False,
            "type": "boolean",
            "default": False,
        },
        "deleteHLSFilesOnEnded": {
            "required": False,
            "type": "boolean",
            "default": True,
        },
        "deleteDASHFilesOnEnded": {
            "required": False,
            "type": "boolean",
            "default": True,
        },
        "tokenHashSecret": {"required": False, "type": "string", "default": ""},
        "hashControlPublishEnabled": {
            "required": False,
            "type": "boolean",
            "default": False,
        },
        "hashControlPlayEnabled": {
            "required": False,
            "type": "boolean",
            "default": False,
        },
        "acceptOnlyRoomsInDataStore": {
            "required": False,
            "type": "boolean",
            "default": False,
        },
        "timeTokenPeriod": {"required": False, "type": "number", "default": 60},
        "hlsPlayListType": {"required": False, "type": "string", "default": ""},
        "previewOverwrite": {"required": False, "type": "boolean", "default": False},
        "stalkerDBServer": {"required": False, "type": "string", "default": ""},
        "stalkerDBUsername": {"required": False, "type": "string", "default": ""},
        "stalkerDBPassword": {"required": False, "type": "string", "default": ""},
        "createPreviewPeriod": {"required": False, "type": "number", "default": 5000},
        "restartStreamFetcherPeriod": {
            "required": False,
            "type": "number",
            "default": 0,
        },
        "startStreamFetcherAutomatically": {
            "required": False,
            "type": "boolean",
            "default": True,
        },
        "streamFetcherBufferTime": {"required": False, "type": "number", "default": 0},
        "mySqlClientPath": {
            "required": False,
            "type": "string",
            "default": "/usr/local/antmedia/mysql",
        },
        "muxerFinishScript": {"required": False, "type": "string", "default": ""},
        "webRTCPortRangeMin": {"required": False, "type": "number", "default": 50000},
        "webRTCPortRangeMax": {"required": False, "type": "number", "default": 60000},
        "stunServerURI": {
            "required": False,
            "type": "string",
            "default": "stun:stun1.l.google.com:19302",
        },
        "webRTCTcpCandidatesEnabled": {
            "required": False,
            "type": "boolean",
            "default": False,
        },
        "webRTCSdpSemantics": {
            "required": False,
            "type": "string",
            "default": "unifiedPlan",
        },
        "portAllocatorFlags": {"required": False, "type": "number", "default": 0},
        "collectSocialMediaActivity": {
            "required": False,
            "type": "boolean",
            "default": False,
        },
        "encoderName": {"required": False, "type": "string", "nullable": True},
        "encoderPreset": {"required": False, "type": "string", "nullable": True},
        "encoderProfile": {"required": False, "type": "string", "nullable": True},
        "encoderLevel": {"required": False, "type": "string", "nullable": True},
        "encoderRc": {"required": False, "type": "string", "nullable": True},
        "encoderSpecific": {"required": False, "type": "string", "nullable": True},
        "encoderThreadCount": {"required": False, "type": "number", "default": 0},
        "encoderThreadType": {"required": False, "type": "number", "default": 0},
        "vp8EncoderSpeed": {"required": False, "type": "number", "default": 4},
        "vp8EncoderDeadline": {
            "required": False,
            "type": "string",
            "default": "realtime",
        },
        "vp8EncoderThreadCount": {"required": False, "type": "number", "default": 1},
        "previewHeight": {"required": False, "type": "number", "default": 480},
        "writeStatsToDatastore": {
            "required": False,
            "type": "boolean",
            "default": True,
        },
        "encoderSelectionPreference": {
            "required": False,
            "type": "string",
            "default": "'gpu_and_cpu'",
        },
        "allowedPublisherCIDR": {"required": False, "type": "string", "nullable": True},
        "excessiveBandwidthValue": {
            "required": False,
            "type": "number",
            "default": 300000,
        },
        "excessiveBandwidthCallThreshold": {
            "required": False,
            "type": "number",
            "default": 3,
        },
        "excessiveBandwithTryCountBeforeSwitchback": {
            "required": False,
            "type": "number",
            "default": 4,
        },
        "excessiveBandwidthAlgorithmEnabled": {
            "required": False,
            "type": "boolean",
            "default": False,
        },
        "packetLossDiffThresholdForSwitchback": {
            "required": False,
            "type": "number",
            "default": 10,
        },
        "rttMeasurementDiffThresholdForSwitchback": {
            "required": False,
            "type": "number",
            "default": 20,
        },
        "replaceCandidateAddrWithServerAddr": {
            "required": False,
            "type": "boolean",
            "default": False,
        },
        "encodingTimeout": {"required": False, "type": "number", "default": 5000},
        "webRTCClientStartTimeoutMs": {
            "required": False,
            "type": "number",
            "default": 5000,
        },
        "defaultDecodersEnabled": {
            "required": False,
            "type": "boolean",
            "default": False,
        },
        "updateTime": {"required": False, "type": "number", "default": 1650269743407},
        "httpForwardingExtension": {
            "required": False,
            "type": "string",
            "default": "''",
        },
        "httpForwardingBaseURL": {"required": False, "type": "string", "default": "''"},
        "maxAnalyzeDurationMS": {"required": False, "type": "number", "default": 1500},
        "disableIPv6Candidates": {
            "required": False,
            "type": "boolean",
            "default": True,
        },
        "rtspPullTransportType": {
            "required": False,
            "type": "string",
            "default": "tcp",
        },
        "rtspTimeoutDurationMs": {"required": False, "type": "number", "default": 5000},
        "maxResolutionAccept": {"required": False, "type": "number", "default": 0},
        "h265Enabled": {"required": False, "type": "boolean", "default": False},
        "rtmpIngestBufferTimeMs": {"required": False, "type": "number", "default": 0},
        "h265EncoderPreset": {"required": False, "type": "string", "nullable": True},
        "h265EncoderProfile": {"required": False, "type": "string", "nullable": True},
        "h265EncoderRc": {"required": False, "type": "string", "nullable": True},
        "h265EncoderSpecific": {"required": False, "type": "string", "nullable": True},
        "h265EncoderLevel": {"required": False, "type": "string", "nullable": True},
        "heightRtmpForwarding": {"required": False, "type": "number", "default": 360},
        "audioBitrateSFU": {"required": False, "type": "number", "default": 96000},
        "dashMuxingEnabled": {"required": False, "type": "boolean", "default": False},
        "aacEncodingEnabled": {"required": False, "type": "boolean", "default": True},
        "gopSize": {"required": False, "type": "number", "default": 0},
        "constantRateFactor": {"required": False, "type": "string", "default": "23"},
        "webRTCViewerLimit": {"required": False, "type": "number", "default": -1},
        "toBeDeleted": {"required": False, "type": "boolean", "default": False},
        "ingestingStreamLimit": {"required": False, "type": "number", "default": -1},
        "webRTCKeyframeTime": {"required": False, "type": "number", "default": 2000},
        "dashHttpStreaming": {"required": False, "type": "boolean", "default": True},
        "dashHttpEndpoint": {"required": False, "type": "string", "nullable": True},
        "forceDecoding": {"required": False, "type": "boolean", "default": False},
        "s3RecordingEnabled": {"required": False, "type": "boolean", "default": False},
        "s3AccessKey": {"required": False, "type": "string", "default": ""},
        "s3SecretKey": {"required": False, "type": "string", "default": ""},
        "s3BucketName": {"required": False, "type": "string", "default": ""},
        "s3RegionName": {"required": False, "type": "string", "default": ""},
        "s3Endpoint": {"required": False, "type": "string", "default": ""},
        "s3Permission": {"required": False, "type": "string", "default": "public-read"},
        "hlsEncryptionKeyInfoFile": {
            "required": False,
            "type": "string",
            "nullable": True,
        },
        "jwksURL": {"required": False, "type": "string", "nullable": True},
        "forceAspectRatioInTranscoding": {
            "required": False,
            "type": "boolean",
            "default": False,
        },
        "webhookAuthenticateURL": {"required": False, "type": "string", "default": ""},
        "hlsFlags": {"required": False, "type": "string", "nullable": True},
        "dataChannelWebHook": {"required": False, "type": "string", "nullable": True},
        # App name
        "appName": {"required": True, "type": "string"},
        # Stream Recording
        "mp4MuxingEnabled": {"required": True, "type": "boolean"},
        "webMMuxingEnabled": {"required": True, "type": "boolean"},
        "addDateTimeToMp4FileName": {"required": True, "type": "boolean"},
        # WebRTC Codec Support
        "h264Enabled": {"required": True, "type": "boolean"},
        "vp8Enabled": {"required": True, "type": "boolean"},
        # Adaptive Streaming
        "webRTCFrameRate": {"required": True, "type": "number"},
        "encoderSettings": {
            "required": True,
            "type": "list",
            "default": [],
            "schema": {
                "type": "dict",
                "schema": {
                    "height": {"required": True, "type": "number"},
                    "videoBitrate": {"required": True, "type": "number"},
                    "audioBitrate": {"required": True, "type": "number"},
                    "forceEncode": {"required": True, "type": "boolean"}
                },
            },
        },
        # HLS Streaming
        "hlsMuxingEnabled": {"required": True, "type": "boolean"},
        "hlsListSize": {"required": True, "type": "string"},
        "hlsTime": {"required": True, "type": "string"},
        # Advanced Settings
        "objectDetectionEnabled": {"required": True, "type": "boolean"},
        "generatePreview": {"required": True, "type": "boolean"},
        "vodFolder": {"required": True, "type": "string"},
        "listenerHookURL": {"required": True, "type": "string"},
        # WebRTC Data Channel
        "dataChannelEnabled": {"required": True, "type": "boolean"},
        "dataChannelPlayerDistribution": {
            "required": True,
            "type": "string",
            "allowed": ["none", "publisher", "all"],
        },
        # Stream Security
        "publishTokenControlEnabled": {"required": True, "type": "boolean"},
        "playTokenControlEnabled": {"required": True, "type": "boolean"},
        "timeTokenSubscriberOnly": {"required": True, "type": "boolean"},
        "enableTimeTokenForPlay": {"required": True, "type": "boolean"},
        "enableTimeTokenForPublish": {"required": True, "type": "boolean"},
        # Accept Undefined Streams
        "acceptOnlyStreamsInDataStore": {"required": True, "type": "boolean"},
        "publishJwtControlEnabled": {"required": True, "type": "boolean"},
        "playJwtControlEnabled": {"required": True, "type": "boolean"},
        "jwtStreamSecretKey": {"required": True, "type": "string", "nullable": True},
        # REST API Security
        "ipFilterEnabled": {"required": True, "type": "boolean"},
        "remoteAllowedCIDR": {"required": True, "type": "string"},
        "jwtControlEnabled": {"required": True, "type": "boolean"},
        "jwtSecretKey": {"required": True, "type": "string", "nullable": True},
        # Data store
        "s3StreamsFolderPath": {
            "required": False,
            "type": "string",
            "default": "streams",
        },
        "s3PreviewsFolderPath": {
            "required": False,
            "type": "string",
            "default": "previews",
        },
    }

    v = Validator(schema)
    if v.validate(data):
        return True, data
    else:
        return False, v.errors
