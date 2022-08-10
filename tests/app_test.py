from antmedia_client.base import AntmediaClient
from antmedia_client.domain import AppSettings
antmedia_client = AntmediaClient(
    antmedia_uri="http://103.171.92.145:5080",
    antmedia_user="evglive",
    antmedia_password="a3692eb7a85cf072d85309370f1c2f6c"
)

settings = {'appName': '9276d1a2eeab4444b9c1c53d123a1681',
            'mp4MuxingEnabled': 1, 'webMMuxingEnabled': False,
            'addDateTimeToMp4FileName': True, 'h264Enabled': True,
            'vp8Enabled': True, 'webRTCFrameRate': 30, 'webRTCEnabled': 1,
            'encoderSettings': [{'height': 1080, 'videoBitrate': 2000000, 'audioBitrate': 256000,
                                 'forceEncode': True}, {'height': 720, 'videoBitrate': 1500000, 'audioBitrate': 128000, 'forceEncode': True}],
            'hlsMuxingEnabled': True, 'hlsListSize': '6', 'hlsTime': '2', 'objectDetectionEnabled': False,
            'generatePreview': True, 'vodFolder': '', 'listenerHookURL': '', 'dataChannelEnabled': True,
            'dataChannelPlayerDistribution': 'all', 'publishTokenControlEnabled': False,
            'playTokenControlEnabled': False, 'timeTokenSubscriberOnly': False, 'enableTimeTokenForPlay': False,
            'enableTimeTokenForPublish': False, 'acceptOnlyStreamsInDataStore': True,
            'publishJwtControlEnabled': False, 'playJwtControlEnabled': False,
            'jwtStreamSecretKey': '', 'ipFilterEnabled': False, 'remoteAllowedCIDR': '',
            'jwtControlEnabled': False, 'jwtSecretKey': ''}

app_settings = {'appName': '4c5639806cb04f6dbbbac89fb3a38b6d', 'mp4MuxingEnabled': True, 'webMMuxingEnabled': False,
 'addDateTimeToMp4FileName': False, 'h264Enabled': True, 'vp8Enabled': False, 'webRTCFrameRate': 30,
 'encoderSettings': [{'height': 1080, 'videoBitrate': 2000000, 'audioBitrate': 256000, 'forceEncode': True},
                     {'height': 720, 'videoBitrate': 1500000, 'audioBitrate': 128000, 'forceEncode': True}],
 'hlsMuxingEnabled': True, 'hlsListSize': '5', 'hlsTime': '2', 'objectDetectionEnabled': False,
 'generatePreview': False, 'vodFolder': '', 'listenerHookURL': '', 'dataChannelEnabled': False,
 'dataChannelPlayerDistribution': 'all', 'publishTokenControlEnabled': False, 'playTokenControlEnabled': False,
 'timeTokenSubscriberOnly': False, 'enableTimeTokenForPlay': False, 'enableTimeTokenForPublish': False,
 'acceptOnlyStreamsInDataStore': False, 'publishJwtControlEnabled': False, 'playJwtControlEnabled': False,
 'jwtStreamSecretKey': None, 'ipFilterEnabled': True, 'remoteAllowedCIDR': '127.0.0.1', 'jwtControlEnabled': False,
 'jwtSecretKey': None, 's3StreamsFolderPath': 'streams', 's3PreviewsFolderPath': 'previews',
 'encoderSettingsString': '[]', 'uploadExtensionsToS3': 7, 's3StorageClass': 'STANDARD',
 'endpointHealthCheckPeriodMs': 2000, 'endpointRepublishLimit': 3, 'dashSegDuration': '6',
 'dashFragmentDuration': '0.5', 'targetLatency': '3.5', 'dashWindowSize': '5', 'dashExtraWindowSize': '5',
 'lLDashEnabled': True, 'lLHLSEnabled': False, 'hlsEnabledViaDash': False, 'useTimelineDashMuxing': False,
 'webRTCEnabled': True, 'useOriginalWebRTCEnabled': False, 'deleteHLSFilesOnEnded': True,
 'deleteDASHFilesOnEnded': True, 'tokenHashSecret': '', 'hashControlPublishEnabled': False,
 'hashControlPlayEnabled': False, 'acceptOnlyRoomsInDataStore': False, 'timeTokenPeriod': 60, 'hlsPlayListType': '',
 'previewOverwrite': False, 'stalkerDBServer': '', 'stalkerDBUsername': '', 'stalkerDBPassword': '',
 'createPreviewPeriod': 5000, 'restartStreamFetcherPeriod': 0, 'startStreamFetcherAutomatically': True,
 'streamFetcherBufferTime': 0, 'mySqlClientPath': '/usr/local/antmedia/mysql', 'muxerFinishScript': '',
 'webRTCPortRangeMin': 50000, 'webRTCPortRangeMax': 60000, 'stunServerURI': 'stun:stun1.l.google.com:19302',
 'webRTCTcpCandidatesEnabled': False, 'webRTCSdpSemantics': 'unifiedPlan', 'portAllocatorFlags': 0,
 'collectSocialMediaActivity': False, 'encoderName': None, 'encoderPreset': None, 'encoderProfile': None,
 'encoderLevel': None, 'encoderRc': None, 'encoderSpecific': None, 'encoderThreadCount': 0, 'encoderThreadType': 0,
 'vp8EncoderSpeed': 4, 'vp8EncoderDeadline': 'realtime', 'vp8EncoderThreadCount': 1, 'previewHeight': 480,
 'writeStatsToDatastore': True, 'encoderSelectionPreference': "'gpu_and_cpu'", 'allowedPublisherCIDR': None,
 'excessiveBandwidthValue': 300000, 'excessiveBandwidthCallThreshold': 3,
 'excessiveBandwithTryCountBeforeSwitchback': 4, 'excessiveBandwidthAlgorithmEnabled': False,
 'packetLossDiffThresholdForSwitchback': 10, 'rttMeasurementDiffThresholdForSwitchback': 20,
 'replaceCandidateAddrWithServerAddr': False, 'encodingTimeout': 5000, 'webRTCClientStartTimeoutMs': 5000,
 'defaultDecodersEnabled': False, 'updateTime': 1650269743407, 'httpForwardingExtension': "''",
 'httpForwardingBaseURL': "''", 'maxAnalyzeDurationMS': 1500, 'disableIPv6Candidates': True,
 'rtspPullTransportType': 'tcp', 'rtspTimeoutDurationMs': 5000, 'maxResolutionAccept': 0, 'h265Enabled': False,
 'rtmpIngestBufferTimeMs': 0, 'h265EncoderPreset': None, 'h265EncoderProfile': None, 'h265EncoderRc': None,
 'h265EncoderSpecific': None, 'h265EncoderLevel': None, 'heightRtmpForwarding': 360, 'audioBitrateSFU': 96000,
 'dashMuxingEnabled': False, 'aacEncodingEnabled': True, 'gopSize': 0, 'constantRateFactor': '23',
 'webRTCViewerLimit': -1, 'toBeDeleted': False, 'ingestingStreamLimit': -1, 'webRTCKeyframeTime': 2000,
 'dashHttpStreaming': True, 'dashHttpEndpoint': None, 'forceDecoding': False, 's3RecordingEnabled': False,
 's3AccessKey': '', 's3SecretKey': '', 's3BucketName': '', 's3RegionName': '', 's3Endpoint': '',
 's3Permission': 'public-read', 'hlsEncryptionKeyInfoFile': None,
 'jwksURL': None, 'forceAspectRatioInTranscoding': False, 'webhookAuthenticateURL': '', 'hlsFlags': None,
 'dataChannelWebHook': None}


r = antmedia_client.app.update_app_settings(app_name="4c5639806cb04f6dbbbac89fb3a38b6d", settings=AppSettings(**app_settings))
print(r)