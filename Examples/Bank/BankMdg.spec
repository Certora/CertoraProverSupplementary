pragma specify 0.1

methods {
    deposit(uint256)
        /* [dep_success] deposit by a of amt succeeds if
            - message value is at least amt
            - sender's funds + amt does not overflow
            - amt + this.balance does not overflow
            */
        /* successful deposit by a of amt has the following effects:
            - [dep_increase] a's funds increase
            - [dep_correct]  a's funds increase by amt
            */

    withdraw()
        returns bool
        /* [withdraw_success] withdraw by a always succeeds */
        /* successful withdraw by a has the following effects:
            - [withdraw_pays] a message with value (a's funds) is sent to a
            - [withdraw_zero] (a's funds are set to 0) */
        /* [withdraw_return] withdraw returns ...? (same as a.send) */

    transfer(address,uint256)
        /* [transfer_success] transfer by a to b of amt succeeds if
            - a's funds are at least amt
            - b's funds + amt does not overflow
            */
        /* successful transfer has the following effects:
            - [transfer_increase] b's funds are increased by at least amt
            - [transfer_decrease] a's funds are decreased by no more than amt
            */

    getFunds(address account)
        /* [getFunds_success] always succeeds */
        returns (uint256)
        /* [getFunds_return]  returns funds(a) */
        envfree

    getTotalFunds() returns(uint256)
        /* [total_success] always succeeds */
        /* [total_correct] returns the sum over a of funds(a) */
        envfree
}

ghost funds(address) returns mathint {
    init_state axiom forall address a.funds(a) == 0;
}
    /*
     * [funds_monotonic] funds(a) can only be decreased by withdrawals or transfers initiated by a
     * [funds_positive]  funds(a) is always positive
     * [funds_stable]    *funds(a) can only be increased by deposit by a or transfer to a
     * [funds_balance]   *balance is >= sum over a of funds(a)
     */

// funds ///////////////////////////////////////////////////////////////////////

rule funds_monotonic(method f) {
    env e;
    calldataarg args;
    address a;

    mathint funds_before = funds(a);
    f(e,args);
    mathint funds_after  = funds(a);

    require funds_after < funds_before;

    assert f.selector != withdraw().selector
        || f.selector != transfer(address,uint256).selector,
        "unauthorized method reduced funds";

    assert e.msg.sender == a,
        "unauthorized sender reduced funds";
}

invariant funds_positive(address a)
    funds(a) >= 0

rule funds_stable(method f) {
    env e;
    calldataarg args;
    address a;

    mathint funds_before = funds(a);
    f(e,args);
    mathint funds_after  = funds(a);

    require funds_after > funds_before;

    assert f.selector == deposit(uint256).selector
        || f.selector == transfer(address,uint256).selector,
        "unauthorized method increased funds";

    assert f.selector == deposit(uint256).selector
        => a == e.msg.sender;

    assert f.selector == transfer(address,uint256).selector
        => false,
        "TODO: check that first argument is a. Can I destructure calldataargs?";
}

rule funds_balance() {
    assert false, "TODO: how to refer to the bank's balance?";
}

// deposit /////////////////////////////////////////////////////////////////////

rule dep_success() {
    assert false, "TODO: rule not implemented";
}

rule dep_increase() {
    assert false, "TODO: rule not implemented";
}

rule dep_correct() {
    assert false, "TODO: rule not implemented";
}

// withdraw ////////////////////////////////////////////////////////////////////

rule withdraw_success() {
    assert false, "TODO: rule not implemented";
}

rule withdraw_pays() {
    assert false, "TODO: rule not implemented";
}

rule withdraw_zero() {
    assert false, "TODO: rule not implemented";
}

rule withdraw_return() {
    assert false, "TODO: rule not implemented";
}

// transfer ////////////////////////////////////////////////////////////////////

rule transfer_todo() {
    assert false, "TODO: transfer rules not yet encoded";
}

// getFunds ////////////////////////////////////////////////////////////////////

rule getFunds_todo() {
    assert false, "TODO: getFunds rules not yet encoded";
}

// getTotalFunds ///////////////////////////////////////////////////////////////

rule getTotalFunds_todo() {
    assert false, "TODO: getTotalFunds rules not yet encoded";
}
