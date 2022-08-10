from dataclasses import dataclass, field

from dataclasses_json import LetterCase, dataclass_json


@dataclass_json()
@dataclass
class S3AgentEvent:
    stream_id: str
    app_name: str
    s3_endpoint: str
    s3_bucket: str
    s3_access_key: str
    s3_secret_key: str
    s3_enable_tls: int


@dataclass_json()
@dataclass
class CustomerWebhookLiveStreamStarted:
    stream_id: str
    action: str
    start_time: str


@dataclass_json()
@dataclass
class CustomerWebhookLiveStreamEnd:
    stream_id: str
    action: str
    start_time: str
    end_time: str


@dataclass_json()
@dataclass
class CustomerWebhookVoD:
    stream_id: str
    action: str
    hls_url: str = None
    s3_url: str = None
    mp4_url: str = None


@dataclass_json()
@dataclass
class AntmediaError:
    description: str
    error: str = None


@dataclass_json()
@dataclass
class StreamAuthResp:
    session_id: str = None
    app_name: str = None
    error: str = None


@dataclass_json()
@dataclass
class TokenStream:
    tokenId: str
    streamId: str
    expireDate: int
    type: str
    roomId: str


@dataclass_json()
@dataclass
class AppSettings:
    appName: str
    # Stream Recording
    mp4MuxingEnabled: bool
    webMMuxingEnabled: bool
    addDateTimeToMp4FileName: bool
    # WebRTC Codec Support
    h264Enabled: bool
    vp8Enabled: bool
    # Adaptive Streaming
    webRTCFrameRate: int
    encoderSettings: list
    # HLS Streaming
    hlsMuxingEnabled: bool
    hlsListSize: str
    hlsTime: str
    # Advanced Settings
    objectDetectionEnabled: bool
    generatePreview: bool
    vodFolder: str
    listenerHookURL: str
    # WebRTC Data Channel
    dataChannelEnabled: bool
    dataChannelPlayerDistribution: str
    # Stream Security
    publishTokenControlEnabled: bool
    playTokenControlEnabled: bool
    timeTokenSubscriberOnly: bool
    enableTimeTokenForPlay: bool
    enableTimeTokenForPublish: bool
    # Accept Undefined Streams
    acceptOnlyStreamsInDataStore: bool
    publishJwtControlEnabled: bool
    playJwtControlEnabled: bool
    jwtStreamSecretKey: str
    # REST API Security
    ipFilterEnabled: bool
    remoteAllowedCIDR: str
    jwtControlEnabled: bool
    jwtSecretKey: str
    # Data store
    s3StreamsFolderPath: str = "streams"
    s3PreviewsFolderPath: str = "previews"

    encoderSettingsString: str = "[]"
    uploadExtensionsToS3: int = 7
    s3StorageClass: str = "STANDARD"
    endpointHealthCheckPeriodMs: int = 2000
    endpointRepublishLimit: int = 3
    dashSegDuration: str = "6"
    dashFragmentDuration: str = "0.5"
    targetLatency: str = "3.5"
    dashWindowSize: str = "5"
    dashExtraWindowSize: str = "5"
    lLDashEnabled: bool = True
    lLHLSEnabled: bool = False
    hlsEnabledViaDash: bool = False
    useTimelineDashMuxing: bool = False
    webRTCEnabled: bool = True
    useOriginalWebRTCEnabled: bool = False
    deleteHLSFilesOnEnded: bool = False  # note here
    deleteDASHFilesOnEnded: bool = True  # note here
    tokenHashSecret: str = ""
    hashControlPublishEnabled: bool = False
    hashControlPlayEnabled: bool = False
    acceptOnlyRoomsInDataStore: bool = False
    timeTokenPeriod: int = 60
    hlsPlayListType: str = ""
    previewOverwrite: bool = False
    stalkerDBServer: str = ""
    stalkerDBUsername: str = ""
    stalkerDBPassword: str = ""
    createPreviewPeriod: int = 5000
    restartStreamFetcherPeriod: int = 0
    startStreamFetcherAutomatically: bool = True
    streamFetcherBufferTime: int = 0
    mySqlClientPath: str = "/usr/local/antmedia/mysql"
    muxerFinishScript: str = ""
    webRTCPortRangeMin: int = 50000
    webRTCPortRangeMax: int = 60000
    stunServerURI: str = "stun:stun1.l.google.com:19302"
    webRTCTcpCandidatesEnabled: bool = False
    webRTCSdpSemantics: str = "unifiedPlan"
    portAllocatorFlags: int = 0
    collectSocialMediaActivity: bool = False
    encoderName: str = None
    encoderPreset: str = None
    encoderProfile: str = None
    encoderLevel: str = None
    encoderRc: str = None
    encoderSpecific: str = None
    encoderThreadCount: int = 0
    encoderThreadType: int = 0
    vp8EncoderSpeed: int = 4
    vp8EncoderDeadline: str = "realtime"
    vp8EncoderThreadCount: int = 1
    previewHeight: int = 480
    writeStatsToDatastore: bool = True
    encoderSelectionPreference: str = "'gpu_and_cpu'"
    allowedPublisherCIDR: str = None
    excessiveBandwidthValue: int = 300000
    excessiveBandwidthCallThreshold: int = 3
    excessiveBandwithTryCountBeforeSwitchback: int = 4
    excessiveBandwidthAlgorithmEnabled: bool = False
    packetLossDiffThresholdForSwitchback: int = 10
    rttMeasurementDiffThresholdForSwitchback: int = 20
    replaceCandidateAddrWithServerAddr: bool = False
    encodingTimeout: int = 5000
    webRTCClientStartTimeoutMs: int = 5000
    defaultDecodersEnabled: bool = False
    updateTime: int = 1650269743407
    httpForwardingExtension: str = "''"
    httpForwardingBaseURL: str = "''"
    maxAnalyzeDurationMS: int = 1500
    disableIPv6Candidates: bool = True
    rtspPullTransportType: str = "tcp"
    rtspTimeoutDurationMs: int = 5000
    maxResolutionAccept: int = 0
    h265Enabled: bool = False
    rtmpIngestBufferTimeMs: int = 0
    h265EncoderPreset: str = None
    h265EncoderProfile: str = None
    h265EncoderRc: str = None
    h265EncoderSpecific: str = None
    h265EncoderLevel: str = None
    heightRtmpForwarding: int = 360
    audioBitrateSFU: int = 96000
    dashMuxingEnabled: bool = False
    aacEncodingEnabled: bool = True
    gopSize: int = 0
    constantRateFactor: str = "23"
    webRTCViewerLimit: int = -1
    toBeDeleted: bool = False
    ingestingStreamLimit: int = -1
    webRTCKeyframeTime: int = 2000
    dashHttpStreaming: bool = True
    dashHttpEndpoint: str = None
    forceDecoding: bool = False
    s3RecordingEnabled: bool = False
    s3AccessKey: str = ""
    s3SecretKey: str = ""
    s3BucketName: str = ""
    s3RegionName: str = ""
    s3Endpoint: str = ""
    s3Permission: str = "public-read"
    hlsEncryptionKeyInfoFile: str = None
    jwksURL: str = None
    forceAspectRatioInTranscoding: bool = False
    webhookAuthenticateURL: str = ""
    hlsFlags: str = '+append_list'
    dataChannelWebHook: str = None


@dataclass_json()
@dataclass
class AppSettingsRequestUpdate:
    appName: str
    # Stream Recording
    mp4MuxingEnabled: bool
    webMMuxingEnabled: bool
    addDateTimeToMp4FileName: bool
    # WebRTC Codec Support
    h264Enabled: bool
    vp8Enabled: bool
    # Adaptive Streaming
    webRTCFrameRate: int
    encoderSettings: list
    # HLS Streaming
    hlsMuxingEnabled: bool
    hlsListSize: str
    hlsTime: str
    # Advanced Settings
    objectDetectionEnabled: bool
    generatePreview: bool
    vodFolder: str
    listenerHookURL: str
    # WebRTC Data Channel
    dataChannelEnabled: bool
    dataChannelPlayerDistribution: str
    # Stream Security
    publishTokenControlEnabled: bool
    playTokenControlEnabled: bool
    timeTokenSubscriberOnly: bool
    enableTimeTokenForPlay: bool
    enableTimeTokenForPublish: bool
    # Accept Undefined Streams
    acceptOnlyStreamsInDataStore: bool
    publishJwtControlEnabled: bool
    playJwtControlEnabled: bool
    jwtStreamSecretKey: str
    # REST API Security
    ipFilterEnabled: bool
    remoteAllowedCIDR: str
    jwtControlEnabled: bool
    jwtSecretKey: str


@dataclass_json()
@dataclass
class Stream:
    # the date when record is created in milliseconds
    date: int
    # the duration of the stream in milliseconds
    duration: int
    # the expire time in milliseconds For instance if this value is 10000 then broadcast should be
    # started in 10 seconds after it is created.If expire duration is 0, then stream will never expire
    expireDurationMS: int
    # the number of HLS viewers of the stream
    hlsViewerCount: int
    # Number of the allowed maximum HLS viewers for the broadcast
    hlsViewerLimit: int
    # the identifier of whether stream is 360 or not
    is360: bool
    # Meta data filed for the custom usage
    metaData: str
    # MP4 muxing whether enabled or not for the stream,
    # 1 means enabled, -1 means disabled, 0 means no settings for the stream
    mp4Enabled: int
    # the name of the stream
    name: str
    # the origin address server broadcasting
    originAdress: str
    # the number of audio and video packets that is being pending to be encoded in the queue
    pendingPacketSize: int
    # the planned end date
    plannedEndDate: int
    # the planned start date
    plannedStartDate: int
    # the list broadcasts of Playlist Items.
    # This list has values when the broadcast type is playlist
    playListItemList: list
    # the identifier of whether stream is public or not
    publicStream: bool
    # it is a video filter for the service, this value is controlled by the user,
    # default value is true in the db
    publish: bool
    # the received bytes until now
    receivedBytes: int
    # the RTMP URL where to publish live stream to
    rtmpURL: str
    # the number of RTMP viewers of the stream
    rtmpViewerCount: int
    # the speed of the incoming stream, for better quality and performance it should be around 1.00
    speed: int
    # the publishing start time of the stream
    startTime: int
    status: str
    streamId: str
    # the stream URL for fetching stream, especially should be defined for IP Cameras or Cloud streams
    streamUrl: str
    # if this broadcast is main track. This variable hold sub track ids.
    subTrackStreamIds: list
    # the type of the stream
    type: str
    userAgent: str
    # WebM muxing whether enabled or not for the stream,
    # 1 means enabled, -1 means disabled, 0 means no settings for the stream
    webMEnabled: int
    # the number of WebRTC viewers of the stream
    webRTCViewerCount: int
    # Number of the allowed maximum WebRTC viewers for the broadcast
    webRTCViewerLimit: int
    # is true, if a broadcast that is not added to data store through rest service
    # or management console It is false by default
    zombi: bool
    # Absolute start time in milliseconds - unix timestamp. It's used for measuring the absolute latency
    absoluteStartTimeMs: int = 0
    # altitude of the broadcasting location
    altitude: str = None
    # the received bytes / duration
    bitrate: int = 0
    # the category of the stream
    category: str = None
    # Current playing index for playlist types
    currentPlayIndex: int = 0
    description: str = None
    # the list of endpoints such as Facebook, Twitter or custom RTMP endpoints
    endPointList: list = None
    # the IP Address of the IP Camera or publisher
    ipAddr: str = None
    # latitude of the broadcasting location
    latitude: str = None
    # the url that will be notified when stream is published, ended and muxing finished
    listenerHookURL: str = None
    # longitude of the broadcasting location
    longitude: str = None
    # If this broadcast is a track of a WebRTC stream. This variable is Id of that stream.
    mainTrackStreamId: str = None
    # the password of the IP Camera
    password: str = None
    # The status of the playlist. It's usable if type is playlist
    playListStatus: str = None
    # the publish type of the stream
    publishType: str = None
    # the quality of the incoming stream during publishing
    quality: str = None
    # Name of the subfolder that will contain stream files
    subFolder: str = None
    # the user name of the IP Camera
    username: str = None


@dataclass_json()
@dataclass
class StreamRequestCreate:
    name: str
    type: str
    streamId: str
    hlsViewerCount: int = 0
    webRTCViewerCount: int = 0
    rtmpViewerCount: int = 0
    mp4Enabled: int = 0
    playListItemList: list = field(default_factory=list)


@dataclass_json()
@dataclass
class EventLiveStream:
    """Ant Media Server calls this hook when a live stream is ended."""
    id: str
    action: str
    # stream name of the broadcast. It can be null.
    streamName: str = None
    # stream category of the broadcast. It can be null.
    category: str = None


@dataclass_json()
@dataclass
class EventVoDReady:
    """Ant Media Server calls this hook when the recording of the live stream is ended."""
    id: str  # stream id of the broadcast
    action: str
    vodName: str  # vod file name
    vodId: str  # vod id in the datastore


@dataclass_json()
@dataclass
class EventEndpointFailed:
    """Ant Media server calls this hook when the RTMP endpoint broadcast went into the failed status."""
    id: str
    action: str
    metadata: str  # RTMP URL of the endpoint.
    # stream name of the broadcast. It can be null.
    streamName: str = None
    # stream category of the broadcast. It can be null.
    category: str = None


@dataclass_json()
@dataclass
class EventPublishTimeoutError:
    """Ant Media server calls this hook when there is a publish time out error, 
    it generally means that the server is not getting any frames."""
    id: str
    action: str
    # stream name of the broadcast. It can be null.
    streamName: str = None
    # stream category of the broadcast. It can be null.
    category: str = None


@dataclass_json()
@dataclass
class EventEncoderNotOpenedError:
    """Ant Media server calls this hook when the encoder can't be opened."""
    id: str
    action: str
    # stream name of the broadcast. It can be null.
    streamName: str = None
    # stream category of the broadcast. It can be null.
    category: str = None
