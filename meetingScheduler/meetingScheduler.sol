pragma solidity ^0.8.7;
import "./IMeetingScheduler.sol";
contract MeetingScheduler is IMeetingScheduler {
    
    mapping(uint256 => ScheduledMeeting) private meetings;

    function getStateById(uint256 meetingId)
        external
        view
        returns (MeetingStatus)
    {
        return meetings[meetingId].status;
    }

    function scheduleMeeting(
        uint256 meetingId,
        uint256 startTime,
        uint256 endTime
    ) external {
        require(
            meetings[meetingId].status == MeetingStatus.UNINITIALIZED,
            "meeting has been scheduled"
        );
        require(
            startTime > block.timestamp,
            "invalid start time, meeting has to be scheduled in the future"
        );
        require(endTime > startTime, "meeting has to end after it starts");
        meetings[meetingId] = ScheduledMeeting({
            meetingId: meetingId,
            startTime: startTime,
            endTime: endTime,
            numOfParticipents: 0,
            status: MeetingStatus.PENDING
        });
    }

    function startMeeting(uint256 meetingId) external {
        ScheduledMeeting memory scheduledMeeting = meetings[meetingId];
        require(
            scheduledMeeting.status == MeetingStatus.PENDING,
            "can't start a meeting if isn't pending"
        );
        require(
            block.timestamp >= scheduledMeeting.startTime,
            "meeting can't start in the past"
        );
        require(
            block.timestamp < scheduledMeeting.endTime,
            "can't start a meeting that has already ended"
        );
        meetings[meetingId].status = MeetingStatus.STARTED;
    }

    function cancelMeeting(uint256 meetingId) external {
        ScheduledMeeting memory scheduledMeeting = meetings[meetingId];
        require(
            scheduledMeeting.status == MeetingStatus.PENDING,
            "only if a meeting is pending, you can cancel it"
        );
        meetings[meetingId].status = MeetingStatus.CANCELLED;
    }

    function endMeeting(uint256 meetingId) external {
        ScheduledMeeting memory scheduledMeeting = meetings[meetingId];
        require(
            scheduledMeeting.status == MeetingStatus.STARTED,
            "can't end a meeting if not started"
        );
        require(
            block.timestamp >= scheduledMeeting.endTime,
            "meeting can't end in the future"
        );

        meetings[meetingId].status = MeetingStatus.ENDED;
    }

    function joinMeeting(uint256 meetingId) external {
        ScheduledMeeting memory meeting = meetings[meetingId];
        require(
            meeting.status == MeetingStatus.STARTED,
            "can only join to an existing meeting"
        );
        meetings[meetingId].numOfParticipents++;
    }

    // function buggyCancelMeeting(uint256 meetingId) external{
    //     require(meetings[meetingId].status == MeetingStatus.STARTED,"BUG");
    //     meetings[meetingId].status = MeetingStatus.UNINITIALIZED;
    // }
}
