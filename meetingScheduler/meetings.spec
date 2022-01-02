methods{
    getStateById(uint256);
    scheduleMeeting(uint256, uint256, uint256);
    startMeeting(uint256);
    cancelMeeting(uint256);
    joinMeeting(uint256);
    endMeeting(uint256);
}

rule checkUnintializedToPending(method f, uint256 meetingId){
    env e;
    calldataarg args;
    uint stateBefore = getStateById(e, meetingId);
    f(e, args);
    uint stateAfter = getStateById(e, meetingId);

    assert (stateBefore == 0 => (stateAfter == 1||stateAfter == 0));

}

rule checkPendingToCancelledOrStarted(method f, uint256 meetingId){
    env e;
    calldataarg args;
    uint stateBefore = getStateById(e, meetingId);
    f(e, args);
    uint stateAfter = getStateById(e, meetingId);

    assert (stateBefore == 1 => (stateAfter == 1||stateAfter == 2||stateAfter==4));

}

rule checkStartedToEnded(method f, uint256 meetingId){
    env e;
    calldataarg args;
    uint stateBefore = getStateById(e, meetingId);
    f(e, args);
    uint stateAfter = getStateById(e, meetingId);

    assert (stateBefore == 2 => (stateAfter == 2 || stateAfter == 3));
    assert ((stateBefore == 2 && stateAfter == 3) => f.selector == endMeeting(uint256).selector);
}
