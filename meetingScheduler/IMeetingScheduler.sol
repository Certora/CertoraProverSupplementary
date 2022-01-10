interface IMeetingScheduler {
    enum MeetingStatus {
        UNINITIALIZED,
        PENDING,
        STARTED,
        ENDED,
        CANCELLED
    }
    struct ScheduledMeeting {
        uint256 meetingId;
        uint256 startTime;
        uint256 endTime;
        uint256 numOfParticipents;
        MeetingStatus status;
    }

    function getStateById(uint256) external view returns (MeetingStatus);

    function scheduleMeeting(uint256 meetingId, uint256 startTime, uint256 endTime) external;
    function startMeeting(uint256 meetingId) external;
    function cancelMeeting(uint256 meetingId) external;
    function endMeeting(uint256 meetingId) external;
    function joinMeeting(uint256 meetingId) external;
}