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
        uint256 meetingId;
        uint256 startTime;
        uint256 endTime;
        uint256 numOfParticipents;
        MeetingStatus status;
    }
    mapping(uint256 => ScheduledMeeting) private meetings;

    function getState(ScheduledMeeting memory meeting) public pure returns (MeetingStatus){
        return meeting.status;
    }
    function getStateById(uint256 meetingId) external returns (MeetingStatus){
        return getState(getScheduledMeetingInfo(meetingId));
    }
    function getScheduledMeetingInfo(uint256 meetingId) public view returns (ScheduledMeeting memory) {
        return meetings[meetingId];
    }

    function scheduleMetting(uint256 meetingId, uint256 startTime, uint256 endTime) public {
        require(meetings[meetingId].status == MeetingStatus.UNINITIALIZED, "meeting has been scheduled");
        require(startTime > block.timestamp, "invalid start time, meeting has to be scheduled in the future");
        require(endTime > startTime,"meeting has to end after it starts");
        meetings[meetingId] = ScheduledMeeting({
            meetingId: meetingId,
            startTime: startTime,
            endTime: endTime,
            numOfParticipents: 0,
            status: MeetingStatus.PENDING
        });
    }

    function startMeetings(uint256 meetingId) public {
        ScheduledMeeting memory scheduledMeeting = meetings[meetingId];
        require(scheduledMeeting.status == MeetingStatus.PENDING, "can't start a meeting if isn't pending");
        require(block.timestamp >= scheduledMeeting.startTime, "meeting can't start in the past");
        require(block.timestamp < scheduledMeeting.endTime, "can't start a meeting that has already ended");
        meetings[meetingId].status = MeetingStatus.STARTED;
        
    }

    function cancelMeeting(uint256 meetingId) public{
        ScheduledMeeting memory scheduledMeeting = meetings[meetingId];
        require(scheduledMeeting.status!=MeetingStatus.UNINITIALIZED,"meeting hasn't scheduled");
        require(scheduledMeeting.status!=MeetingStatus.STARTED,"meeting has started");
        require(scheduledMeeting.status!=MeetingStatus.ENDED,"meeting has ended");
        require(scheduledMeeting.status!=MeetingStatus.CANCELLED, "can't cancel twice");
        meetings[meetingId].status = MeetingStatus.CANCELLED;
    }
    function endMeetings(uint256 meetingId) public {
        ScheduledMeeting memory scheduledMeeting = meetings[meetingId];
        require(scheduledMeeting.status == MeetingStatus.STARTED, "can't end a meeting if not started");
        require(block.timestamp >= scheduledMeeting.endTime, "meeting can't start in the past");
            
        meetings[meetingId].status = MeetingStatus.ENDED;
        
    }

    function joinMeeting(uint256 meetingId) public{
        ScheduledMeeting memory meeting = meetings[meetingId];
        require(meeting.status == MeetingStatus.STARTED, "can only join to an existing meeting");
        meetings[meetingId].numOfParticipents++;
    }
}
