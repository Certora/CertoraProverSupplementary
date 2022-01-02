pragma solidity ^0.8.7;
contract MeetingScheduler{
    enum MeetingStatus {
        UNINITIALIZED,
        PENDING,
        STARTED,
        ENDED,
        CANCELLED
    }
    struct ScheduledMeeting{
        bytes32 meetingId;
        uint256 startTime;
        uint256 endTime;
        uint256 numOfParticipents;
        MeetingStatus status;
    }
    mapping(bytes32 => ScheduledMeeting) private meetings;

    function getScheduleId(bytes32 meetingId, uint256 startTime, uint256 endTime) public pure returns (bytes32){
        return keccak256(abi.encodePacked(meetingId, startTime, endTime));
    }
    function getState(ScheduledMeeting memory meeting) external pure returns (MeetingStatus){
        return meeting.status;
    }
    function getScheduledMeetingInfo(bytes32 scheduleId) external view returns (ScheduledMeeting memory) {
        return meetings[scheduleId];
    }

    function scheduleMetting(bytes32 meetingId, uint256 startTime, uint256 endTime) external returns (bytes32 scheduleId){
        scheduleId = getScheduleId(meetingId, startTime, endTime);
        require(meetings[scheduleId].status == MeetingStatus.UNINITIALIZED, "meeting has been scheduled");
        require(startTime > block.timestamp, "invalid start time, meeting has to be scheduled in the future");
        require(endTime > startTime,"meeting has to end after it starts");
        meetings[scheduleId] = ScheduledMeeting({
            meetingId: meetingId,
            startTime: startTime,
            endTime: endTime,
            numOfParticipents: 0,
            status: MeetingStatus.PENDING
        });
    }

    function startMeetings(bytes32 scheduleId) external {
        ScheduledMeeting memory scheduledMeeting = meetings[scheduleId];
        require(scheduledMeeting.status == MeetingStatus.PENDING, "can't start a meeting if isn't pending");
        require(block.timestamp >= scheduledMeeting.startTime, "meeting can't start in the past");
        require(block.timestamp < scheduledMeeting.endTime, "can't start a meeting that has already ended");
        meetings[scheduleId].status = MeetingStatus.STARTED;
        
    }

    function cancelMeeting(bytes32 meetingId) external{
        ScheduledMeeting memory scheduledMeeting = meetings[meetingId];
        require(scheduledMeeting.status!=MeetingStatus.UNINITIALIZED,"meeting hasn't scheduled");
        require(scheduledMeeting.status!=MeetingStatus.STARTED,"meeting has started");
        require(scheduledMeeting.status!=MeetingStatus.ENDED,"meeting has ended");
        require(scheduledMeeting.status!=MeetingStatus.CANCELLED, "can't cancel twice");
        meetings[meetingId].status = MeetingStatus.CANCELLED;
    }
    function endMeetings(bytes32 scheduleId) external {
        
            ScheduledMeeting memory scheduledMeeting = meetings[scheduleId];
            require(scheduledMeeting.status == MeetingStatus.STARTED, "can't end a meeting if not started");
            require(block.timestamp >= scheduledMeeting.endTime, "meeting can't start in the past");
            
            meetings[scheduleId].status = MeetingStatus.ENDED;
        
    }

    function joinMeeting(bytes32 meetingId) external{
        ScheduledMeeting memory meeting = meetings[meetingId];
        require(meeting.status == MeetingStatus.STARTED, "can only join to an existing meeting");
        meetings[meetingId].numOfParticipents ++;
    }
}
